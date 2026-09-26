#!/usr/bin/env python3
"""Verify owned C# coverage/host parity, Roslyn organization and semantic formatting."""
from pathlib import Path
import argparse
import json
import os
import re
import subprocess
import sys


def analyzer_receipts(log, expected_projects):
    """Pinned English dotnet-format diagnostic protocol; unknown/skipped phases fail closed."""
    phases = {'Code Style': {}, 'Analyzer Reference': {}}
    phase = None
    for line in log.splitlines():
        line = line.strip()
        if line.startswith('Running ') and line.endswith(' analysis.'):
            phase = line[len('Running '):-len(' analysis.')]
        match = re.fullmatch(r'Running (\d+) analyzers on (.+)\.', line)
        if match and phase in phases:
            count, project = match.groups()
            phases[phase][project] = int(count)
    missing = [f'{project} [{phase}]' for phase, counts in phases.items()
               for project in sorted(expected_projects) if counts.get(project, 0) <= 0]
    if missing:
        raise RuntimeError('Missing analyzer execution: ' + ', '.join(missing))
    return {phase: {project: counts[project] for project in sorted(expected_projects)}
            for phase, counts in phases.items()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument('--artifacts', type=Path, help='Report directory; CI supplies its fresh run directory.')
    parser.add_argument('paths', nargs='*')
    args = parser.parse_args()
    root = args.root.resolve()
    config = json.loads((root / 'tooling/quality/coverage.json').read_text())
    profile = json.loads((root / config['ownedProjects']).read_text())
    artifacts = (root / (args.artifacts or Path('artifacts/quality'))).resolve()
    artifacts.mkdir(parents=True, exist_ok=True)
    report_path = artifacts / 'coverage.json'
    report_path.write_text(json.dumps({'status': 'incomplete'}) + '\n')
    environment = dict(os.environ, DOTNET_CLI_UI_LANGUAGE='en-US')

    def run(command, label):
        result = subprocess.run(command, cwd=root, env=environment, capture_output=True, text=True)
        log_path = artifacts / (label + '.log')
        log_path.write_text(result.stdout + result.stderr)
        if result.returncode:
            raise RuntimeError(f'{label} failed; see {log_path}')
        return result.stdout + result.stderr

    def owned(path):
        relative = path.resolve().relative_to(root).as_posix()
        return (relative.startswith(('Assets/Game/', 'tooling/')) and path.suffix == '.cs'
                and not path.name.endswith(('.g.cs', '.generated.cs'))
                and not set(path.parts) & {'bin', 'obj'})

    names = args.paths
    if not names:
        names = subprocess.check_output(
            ['git', 'ls-files', '-z', '--cached', '--others', '--exclude-standard', '--', 'Assets/Game', 'tooling'],
            cwd=root).decode().split('\0')
    files = sorted({(root / name).resolve() for name in names if name and owned(root / name)})
    if not files or any(not path.is_file() for path in files):
        raise RuntimeError('Expected existing owned source files; refusing empty or missing coverage.')
    selected = set(files)

    def inspect(project, label, namespace=None):
        if not project.is_file():
            raise RuntimeError(f'Missing {project.name}; regenerate Unity projects or complete SDK setup.')
        output = run(['dotnet', 'msbuild', str(project), '-nologo', '-getItem:Compile',
                      '-getProperty:Nullable,LangVersion,RootNamespace,TreatWarningsAsErrors'], label)
        data = json.loads(output)
        properties = data['Properties']
        for key, expected in [('Nullable', profile['nullable']), ('LangVersion', profile['languageVersion']),
                              ('TreatWarningsAsErrors', 'true')]:
            if properties.get(key) != expected:
                raise RuntimeError(f'{project.name}: {key}={properties.get(key)!r}; expected {expected!r}.')
        if namespace is not None and properties.get('RootNamespace') != namespace:
            raise RuntimeError(f'{project.name}: generated namespace profile mismatch.')
        return {Path(item['FullPath']).resolve() for item in data['Items']['Compile']}

    def solution_projects(solution, label):
        if not solution.is_file():
            raise RuntimeError(f'Missing {solution}; regenerate or complete workspace setup.')
        output = run(['dotnet', 'sln', str(solution), 'list'], label)
        projects = {(solution.parent / line.strip().replace('\\', '/')).resolve()
                    for line in output.splitlines() if line.strip().endswith('.csproj')}
        if not projects:
            raise RuntimeError(f'{solution.name} has no C# projects.')
        return projects

    unity_solution = root / config['unitySolution']
    unity_projects = solution_projects(unity_solution, 'unity-projects')
    unity_files = set()
    unity_compile = {}
    names = set()
    for entry in profile['projects']:
        if entry['name'] in names:
            raise RuntimeError('Duplicate owned project in IDE profile.')
        names.add(entry['name'])
        project = root / (entry['name'] + '.csproj')
        if project not in unity_projects:
            raise RuntimeError(f'{project.name} is absent from the selected Unity solution.')
        compiled = inspect(project, 'unity-' + entry['name'], entry['rootNamespace'])
        unity_compile[project.stem] = compiled
        if not args.paths and not compiled & selected:
            raise RuntimeError(f'{project.name}: no selected owned source; qualify the active assembly profile.')
        unity_files |= compiled
    sdk_solution = root / config['sdkSolution']
    projects = sorted(solution_projects(sdk_solution, 'sdk-projects'))
    sdk_files = set()
    sdk_compile = {}
    for index, project in enumerate(projects):
        if project.stem in sdk_compile:
            raise RuntimeError('SDK project names must be unique for analyzer execution receipts.')
        compiled = inspect(project, f'sdk-{index}')
        sdk_compile[project.stem] = compiled
        sdk_files |= compiled
    unity_required = {path for path in files if path.relative_to(root).as_posix().startswith('Assets/Game/')}
    tooling_required = selected - unity_required
    pure_roots = [(root / path).resolve() for path in config['pureSourceRoots']]
    if not pure_roots or any(not path.is_relative_to(root / 'Assets/Game') for path in pure_roots):
        raise RuntimeError('Configure nonempty pureSourceRoots within owned Assets/Game source.')
    pure_required = {path for path in files if any(path.is_relative_to(folder) for folder in pure_roots)}
    missing_unity = unity_required - unity_files
    missing_sdk = (tooling_required | pure_required) - sdk_files
    if missing_unity or missing_sdk:
        gaps = [f'{path.relative_to(root)} [{host}]' for host, missing in
                [('Unity', missing_unity), ('SDK', missing_sdk)] for path in sorted(missing)]
        raise RuntimeError('Missing semantic coverage: ' + ', '.join(gaps))

    report = {
        'status': 'incomplete', 'scope': 'selected' if args.paths else 'all-owned',
        'selected': [str(path.relative_to(root)) for path in files],
        'unityCovered': len(selected & unity_files), 'sdkCovered': len(selected & sdk_files),
        'pureRequiredInBoth': [str(path.relative_to(root)) for path in sorted(pure_required)],
        'syntaxSymbols': config['syntaxSymbols'], 'analyzerExecution': {}}
    report_path.write_text(json.dumps(report, indent=2) + '\n')
    file_list = artifacts / 'organization-files.json'
    file_list.write_text(json.dumps([str(path) for path in files]))
    run(['dotnet', 'run', '--project', str(root / config['organizationProject']), '--configuration', 'Release',
         '--no-restore', '--', str(file_list), *config['syntaxSymbols']], 'organization')

    for label, solution, covered, compile_map in [
            ('unity-format', unity_solution, unity_files, unity_compile),
            ('sdk-format', sdk_solution, sdk_files, sdk_compile)]:
        included = sorted(selected & covered)
        if not included:
            continue
        if not solution.is_file():
            raise RuntimeError(f'Missing {solution}; no whitespace-only fallback.')
        log = run(['dotnet', 'format', str(solution), '--verify-no-changes', '--no-restore',
                   '--verbosity', 'diagnostic', '--include', *[str(path.relative_to(root)) for path in included]], label)
        workspace_failures = ['Warnings were encountered while loading the workspace',
                              'Unable to load project', 'Failed to load project']
        if any(message in log for message in workspace_failures) or re.search(r'\berror (?:CS|MSB|NU)\d+', log):
            raise RuntimeError(f'{label}: workspace/compilation problems; inspect its retained log.')
        expected = {name for name, compiled in compile_map.items() if selected & compiled}
        report['analyzerExecution'][label] = analyzer_receipts(log, expected)
        report_path.write_text(json.dumps(report, indent=2) + '\n')
    report['status'] = 'passed'
    report_path.write_text(json.dumps(report, indent=2) + '\n')
    print(f'Owned C# semantic/style checks passed ({report["scope"]}): {len(files)} files; '
          'compile coverage, analyzer execution and compiler profile checked. '
          'Actual Unity compilation, behavior and visual acceptance are separate.')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError, RuntimeError, subprocess.CalledProcessError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
