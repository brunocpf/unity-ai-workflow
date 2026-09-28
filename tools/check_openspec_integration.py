"""Disposable real-CLI lifecycle probe. Synthetic evidence; no Unity/model acceptance claim."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def module(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def run():
    setup = module(ROOT / 'starter/openspec/setup.py')
    gate = module(ROOT / 'starter/openspec/tooling/check.py')
    with tempfile.TemporaryDirectory(prefix='unity-openspec-integration-') as temporary:
        game = Path(temporary) / 'game'
        setup.stage(ROOT / 'starter/openspec', game)
        (game / '.gitignore').write_text('**/node_modules/\nartifacts/\n', encoding='utf-8')
        subprocess.run(['git', 'init', '-q', str(game)], check=True)
        env = dict(os.environ, OPENSPEC_TELEMETRY='0', DO_NOT_TRACK='1')
        node = env.get('WORKFLOW_NODE') or shutil.which('node')
        env['PATH'] = str(Path(node).parent) + os.pathsep + env.get('PATH', '')
        npm = shutil.which('npm', path=env['PATH'])
        # npm's executable command name/flags are fixed; no project content enters a shell.
        result = subprocess.run([npm, 'ci', '--ignore-scripts'], cwd=game / 'tooling/specs', env=env,
                                capture_output=True, text=True, timeout=120, shell=os.name == 'nt')
        if result.returncode:
            raise RuntimeError(result.stdout + result.stderr)

        def cli(*args, success=True):
            value = subprocess.run([sys.executable, str(game / 'tooling/specs/run.py'), *args], cwd=game,
                                   env=env, capture_output=True, text=True, timeout=60)
            if (value.returncode == 0) != success:
                raise AssertionError(f'{args}: {value.stdout}\n{value.stderr}')
            return value.stdout

        cli('init', '--tools', 'codex,claude', '--profile', 'core', '--no-animation')
        for folder in ('.agents/skills', '.claude/skills'):
            assert (game / folder / 'openspec-propose/SKILL.md').is_file()
        cli('schema', 'validate', 'unity-game')
        for iteration, operation in [(1, 'ADDED'), (2, 'MODIFIED')]:
            name = f'pause-{iteration}'
            cli('new', 'change', name)
            state = json.loads(cli('status', '--change', name, '--json'))
            assert state['schemaName'] == 'unity-game'
            folder = game / 'openspec/changes' / name
            (folder / 'specs/pause').mkdir(parents=True)
            purpose = '## Purpose\nAllow users to pause and resume a session while preserving the correct simulation state.\n\n' if iteration == 1 else ''
            spec = folder / 'specs/pause/spec.md'
            spec.write_text(purpose + f'## {operation} Requirements\n\n### Requirement: PAUSE-001 - Pause\nThe game SHALL pause simulation at revision {iteration}.\n\n#### Scenario: Pause\n- **WHEN** pause is requested\n- **THEN** simulation pauses\n', encoding='utf-8')
            (folder / 'proposal.md').write_text('## Why\nExercise the workflow with a synthetic pause change.\n## What Changes\nUpdate pause.\n## Capabilities\n### New Capabilities\n- pause: pause simulation.\n## Impact\nNo real game code.\n', encoding='utf-8')
            (folder / 'design.md').write_text('## Approach\nSynthetic CLI validation only.\n', encoding='utf-8')
            (folder / 'tasks.md').write_text('- [x] 1.1 Validate the synthetic pause spec\n', encoding='utf-8')
            cli('instructions', 'verification', '--change', name, '--json')
            cli('validate', name, '--strict', '--no-interactive')
            good = spec.read_text(encoding='utf-8')
            spec.write_text(good.replace('#### Scenario:', '### Scenario:'), encoding='utf-8')
            cli('validate', name, '--strict', '--no-interactive', success=False)
            spec.write_text(good, encoding='utf-8')
            report = game / 'docs/evidence' / f'{name}.txt'
            report.parent.mkdir(parents=True, exist_ok=True)
            report.write_text('Synthetic structural fixture, not a passed game test.\n', encoding='utf-8')
            data = {'schema': 1, 'fingerprint': gate.fingerprint(game, name), 'requirements': [
                {'id': 'PAUSE-001', 'status': 'pending', 'required_kinds': ['automated'], 'evidence': [
                    {'kind': 'automated', 'path': report.relative_to(game).as_posix(), 'sha256': gate.sha(report.read_bytes()),
                     'command_or_procedure': 'synthetic-fixture', 'target': 'CLI only', 'run_id': name}]}]}
            verification = folder / 'verification.json'
            verification.write_text(json.dumps(data), encoding='utf-8')
            try:
                gate.check(game, name, True)
                raise AssertionError('Pending acceptance was not rejected')
            except ValueError:
                pass
            runner_command = [sys.executable, str(game / 'tooling/specs/ci.py'), '--change', name]
            if iteration == 1:
                runner_command.append('--quiet')
            pending = subprocess.run(runner_command, cwd=game, env=env, capture_output=True, text=True, timeout=60)
            assert pending.returncode != 0 and 'Unaccepted' in pending.stdout
            data['requirements'][0]['status'] = 'pass'
            verification.write_text(json.dumps(data), encoding='utf-8')
            gate.check(game, name, True)
            completed = subprocess.run(runner_command, cwd=game, env=env, capture_output=True, text=True, timeout=60)
            assert completed.returncode == 0, completed.stdout + completed.stderr
            cli('archive', name, '--yes')
            baseline = (game / 'openspec/specs/pause/spec.md').read_text(encoding='utf-8')
            assert f'revision {iteration}' in baseline
            archived = next((game / 'openspec/changes/archive').glob('*-' + name))
            archived_name = 'archive/' + archived.name
            try:
                gate.check(game, archived_name, True)
                raise AssertionError('Pre-archive fingerprint was not rejected')
            except ValueError:
                pass
            # Synthetic fixture only: reconcile the changed archive layout, not a gameplay verdict.
            data['fingerprint'] = gate.fingerprint(game, archived_name)
            (archived / 'verification.json').write_text(json.dumps(data), encoding='utf-8')
            gate.check(game, archived_name, True)
        cli('validate', '--all', '--strict', '--no-interactive')
        print(json.dumps({'status': 'pass', 'openspec': '1.13.2', 'node': '24.15.0',
                          'checks': ['both client integrations generated', 'custom schema', 'instructions',
                                     'invalid scenario rejected', 'pending evidence rejected', 'new capability archive',
                                     'quiet/verbose runner and pending rejection', 'follow-up delta archive', 'archived acceptance reconciliation', 'final strict validation'],
                          'unity_or_model_execution': False}, indent=2))


if __name__ == '__main__':
    run()
