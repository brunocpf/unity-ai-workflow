#!/usr/bin/env python3
"""Check owned C# for compiler settings, project coverage, code organization and formatting."""
from pathlib import Path
import argparse
import json
import os
import re
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument('paths', nargs='*', help='Owned source files to check; default is all owned source.')
    args = parser.parse_args()
    root = args.root.resolve()
    config = json.loads((root / 'tooling/quality/coverage.json').read_text())
    profile = json.loads((root / config['ownedProjects']).read_text())
    environment = dict(os.environ, DOTNET_CLI_UI_LANGUAGE='en-US')

    def run(command, label):
        result = subprocess.run(command, cwd=root, env=environment, capture_output=True, text=True)
        output = result.stdout + result.stderr
        if result.returncode:
            raise RuntimeError(f'{label} failed:\n{output}')
        return output

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
    missing = [str(path.relative_to(root)) for path in files if not path.is_file()]
    if missing:
        raise RuntimeError('Files not found: ' + ', '.join(missing))
    if not files:
        if args.paths:
            return 0  # The hook passed only non-owned files.
        raise RuntimeError('No owned C# found under Assets/Game or tooling; check the project layout.')
    selected = set(files)

    def compile_items(project, namespace=None):
        if not project.is_file():
            raise RuntimeError(f'Missing {project.name}; regenerate Unity projects or complete SDK setup.')
        output = run(['dotnet', 'msbuild', str(project), '-nologo', '-getItem:Compile',
                      '-getProperty:Nullable,LangVersion,RootNamespace,TreatWarningsAsErrors'], project.name)
        data = json.loads(output)
        properties = data['Properties']
        for key, expected in [('Nullable', profile['nullable']), ('LangVersion', profile['languageVersion']),
                              ('TreatWarningsAsErrors', 'true')]:
            if properties.get(key) != expected:
                raise RuntimeError(f'{project.name}: {key}={properties.get(key)!r}; expected {expected!r}.')
        if namespace is not None and properties.get('RootNamespace') != namespace:
            raise RuntimeError(f'{project.name}: RootNamespace does not match tooling/ide/owned-projects.json.')
        return {Path(item['FullPath']).resolve() for item in data['Items']['Compile']}

    def solution_projects(solution):
        if not solution.is_file():
            raise RuntimeError(f'Missing {solution}; regenerate or complete workspace setup.')
        output = run(['dotnet', 'sln', str(solution), 'list'], solution.name)
        return {(solution.parent / line.strip().replace('\\', '/')).resolve()
                for line in output.splitlines() if line.strip().endswith('.csproj')}

    unity_solution = root / config['unitySolution']
    unity_projects = solution_projects(unity_solution)
    unity_files = set()
    for entry in profile['projects']:
        project = root / (entry['name'] + '.csproj')
        if project not in unity_projects:
            raise RuntimeError(f'{project.name} is missing from {unity_solution.name}.')
        unity_files |= compile_items(project, entry['rootNamespace'])
    sdk_solution = root / config['sdkSolution']
    sdk_files = set()
    for project in sorted(solution_projects(sdk_solution)):
        sdk_files |= compile_items(project)

    # Every owned file must be compiled somewhere, or formatting and analyzers silently skip it.
    unity_required = {path for path in files if path.relative_to(root).as_posix().startswith('Assets/Game/')}
    pure_roots = [(root / path).resolve() for path in config['pureSourceRoots']]
    if not pure_roots or any(not path.is_relative_to(root / 'Assets/Game') for path in pure_roots):
        raise RuntimeError('Set pureSourceRoots in coverage.json to the pure folders under Assets/Game.')
    pure_required = {path for path in files if any(path.is_relative_to(folder) for folder in pure_roots)}
    sdk_required = (selected - unity_required) | pure_required
    gaps = [f'{path.relative_to(root)} [Unity]' for path in sorted(unity_required - unity_files)]
    gaps += [f'{path.relative_to(root)} [SDK]' for path in sorted(sdk_required - sdk_files)]
    if gaps:
        raise RuntimeError('Files not included in any project: ' + ', '.join(gaps))

    file_list = root / 'artifacts/quality/organization-files.json'
    file_list.parent.mkdir(parents=True, exist_ok=True)
    file_list.write_text(json.dumps([str(path) for path in files]))
    run(['dotnet', 'run', '--project', str(root / config['organizationProject']), '--configuration', 'Release',
         '--no-restore', '--', str(file_list), *config['syntaxSymbols']], 'Code organization')

    for solution, covered in [(unity_solution, unity_files), (sdk_solution, sdk_files)]:
        included = sorted(selected & covered)
        if not included:
            continue
        output = run(['dotnet', 'format', str(solution), '--verify-no-changes', '--no-restore', '--verbosity', 'diagnostic',
                      '--include', *[str(path.relative_to(root)) for path in included]], f'dotnet format ({solution.name})')
        # dotnet format can exit 0 when it fails to load the workspace or the code doesn't compile.
        load_failures = ['Warnings were encountered while loading the workspace', 'Unable to load project',
                         'Failed to load project']
        if any(message in output for message in load_failures) or re.search(r'\berror (?:CS|MSB|NU)\d+', output):
            raise RuntimeError(f'dotnet format could not load or compile {solution.name}:\n{output}')
    print(f'Quality check passed: {len(files)} files.')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError, RuntimeError, subprocess.CalledProcessError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
