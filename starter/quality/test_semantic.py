#!/usr/bin/env python3
"""Exercise the adopted driver/hook in disposable SDK workspaces; no live source mutations.

These fixtures model the two analysis hosts. Actual Unity compiler/IDE acceptance is separate.
"""
from pathlib import Path
import argparse
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import uuid


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--husky", action="store_true", help="Exercise the installed Husky entrypoint in the fixture.")
    parser.add_argument('--artifacts', type=Path, help='Fresh output directory; must not already exist.')
    args = parser.parse_args()
    quality = Path(__file__).resolve().parent
    adopted = quality.parents[1]
    evidence = (args.artifacts or adopted / 'artifacts/semantic-probes' / uuid.uuid4().hex).resolve()
    evidence.mkdir(parents=True)
    results = []
    spec = importlib.util.spec_from_file_location('quality_driver', quality / 'check.py')
    driver = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(driver)
    valid_log = ('Running Code Style analysis.\nRunning 16 analyzers on Game.Probe.\n'
                 'Running Analyzer Reference analysis.\nRunning 20 analyzers on Game.Probe.\n')
    driver.analyzer_receipts(valid_log, {'Game.Probe'})
    for name, log in [('empty log', ''), ('wrong project', valid_log.replace('Game.Probe', 'Vendor')),
                      ('zero analyzers', valid_log.replace('16 analyzers', '0 analyzers')),
                      ('missing phase', valid_log.split('Running Analyzer Reference analysis.')[0])]:
        try:
            driver.analyzer_receipts(log, {'Game.Probe'})
        except RuntimeError:
            results.append(name + ' rejected')
        else:
            raise RuntimeError(name + ' falsely passed')

    with tempfile.TemporaryDirectory(prefix='semantic probes ') as directory:
        root = Path(directory)

        def write(path, text):
            target = root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text)
            return target

        def run(command):
            environment = dict(os.environ, HUSKY="1")
            return subprocess.run(command, cwd=root, env=environment, capture_output=True, text=True)

        def setup(command):
            result = run(command)
            if result.returncode:
                raise RuntimeError(result.stdout + result.stderr)

        for name in ['.editorconfig', 'global.json', 'tooling/dotnet/Directory.Build.props']:
            write(name, (adopted / name).read_text())
        shutil.copytree(quality, root / 'tooling/quality',
                        ignore=shutil.ignore_patterns('bin', 'obj', '__pycache__'))
        write('.gitignore', '**/bin/\n**/obj/\nartifacts/\n')
        config = {
            'unitySolution': 'Game.slnx', 'sdkSolution': 'tooling/dotnet/Game.slnx',
            'ownedProjects': 'tooling/ide/owned-projects.json',
            'organizationProject': 'tooling/quality/CodeOrganization/CodeOrganization.csproj',
            'syntaxSymbols': ['UNITY_EDITOR'], 'pureSourceRoots': ['Assets/Game/Core']}
        write('tooling/quality/coverage.json', json.dumps(config))
        profile = json.loads((adopted / 'tooling/ide/owned-projects.json').read_text())
        profile['projects'] = [{'name': name, 'rootNamespace': name}
                               for name in ['Game.Core', 'Game.Unity.Runtime']]
        write('tooling/ide/owned-projects.json', json.dumps(profile))
        for name, folder in [('Game.Core', 'Core'), ('Game.Unity.Runtime', 'Unity/Runtime')]:
            write(name + '.csproj', f'''<Project Sdk="Microsoft.NET.Sdk">
  <Import Project="tooling/dotnet/Directory.Build.props" />
  <PropertyGroup><TargetFramework>net10.0</TargetFramework><RootNamespace>{name}</RootNamespace>
    <EnableDefaultCompileItems>false</EnableDefaultCompileItems>
    <BaseIntermediateOutputPath>artifacts/{name}/obj/</BaseIntermediateOutputPath>
    <OutputPath>artifacts/{name}/bin/</OutputPath></PropertyGroup>
  <ItemGroup><Compile Include="Assets/Game/{folder}/*.cs" /></ItemGroup>
</Project>''')
        write('tooling/dotnet/Core/Core.csproj', '''<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup><TargetFramework>net10.0</TargetFramework><EnableDefaultCompileItems>false</EnableDefaultCompileItems></PropertyGroup>
  <ItemGroup><Compile Include="../../../Assets/Game/Core/*.cs" /></ItemGroup>
</Project>''')
        write('Game.slnx', '<Solution><Project Path="Game.Core.csproj" /><Project Path="Game.Unity.Runtime.csproj" /></Solution>')
        write('tooling/dotnet/Game.slnx', '<Solution><Project Path="Core/Core.csproj" /><Project Path="../quality/CodeOrganization/CodeOrganization.csproj" /></Solution>')
        clean = 'namespace Game\n{\n    public sealed class Probe\n    {\n    }\n}\n'
        sources = [write('Assets/Game/' + folder + '/Probe.cs', clean) for folder in ['Core', 'Unity/Runtime']]
        setup(['git', 'init', '-q'])
        if args.husky:
            for name in ['.config/dotnet-tools.json', '.husky/pre-commit', '.husky/pre-push',
                         '.husky/task-runner.json', 'tooling/hooks/check_staged.py']:
                write(name, (adopted / name).read_text())
            setup(['dotnet', 'tool', 'restore'])
            setup(['dotnet', 'husky', 'install'])
        setup(['git', 'add', '.'])
        setup(['dotnet', 'restore', 'Game.slnx'])
        setup(['dotnet', 'restore', 'tooling/dotnet/Game.slnx'])

        def check(name, command, diagnostic=None):
            shutil.rmtree(root / 'artifacts/quality', ignore_errors=True)
            result = run(command)
            logs = '\n'.join(p.read_text() for p in (root / 'artifacts/quality').glob('*.log'))
            output = result.stdout + result.stderr + '\n' + logs
            (evidence / (name + '.log')).write_text(output)
            if (result.returncode == 0) != (diagnostic is None) or diagnostic and diagnostic not in output:
                raise RuntimeError(f'{name}: unexpected result; see {evidence}')
            results.append(name)

        gate = [sys.executable, str(root / 'tooling/quality/check.py')]
        hook = ['sh', '.husky/pre-commit'] if args.husky else [sys.executable, str(adopted / 'tooling/hooks/check_staged.py')]
        check('clean-all-owned', gate)
        for source in sources:
            for name, prefix, diagnostic in [('unused-import', 'using System.Text;\n\n', 'IDE0005'),
                                              ('redundant-nullable', '#nullable enable\n', 'IDE0240')]:
                try:
                    source.write_text(prefix + clean)
                    setup(['git', 'add', str(source)])
                    check(source.parent.name + '-' + name + '-hook', hook, diagnostic)
                finally:
                    source.write_text(clean)
                    setup(['git', 'add', str(source)])
        for source in sources:
            source.write_text(clean + '\npublic interface Extra {}\n')
            setup(['git', 'add', str(source)])
            check(source.parent.name + '-organization-hook', hook, 'ORG001')
            source.write_text(clean)
            setup(['git', 'add', str(source)])
        extra = write('Assets/Game/Uncovered.cs', clean.replace('Probe', 'Uncovered'))
        check('missing-compile-coverage', gate, 'Missing semantic coverage')
        extra.unlink()
        check('clean-restored', gate)
    (evidence / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
    print(f'PASS: {len(results)} semantic/hook/receipt probes; evidence: {evidence}. '
          'SDK fixtures only; run the separate actual Unity compiler/IDE acceptance.')


if __name__ == '__main__':
    main()
