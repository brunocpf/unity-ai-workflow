import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


setup = load(ROOT / 'starter/openspec/setup.py')
gate = load(ROOT / 'starter/openspec/tooling/check.py')


class SpecTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='spec fixture ')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'game'
        setup.stage(ROOT / 'starter/openspec', self.root)
        self.folder = self.root / 'openspec/changes/test-feature'
        (self.folder / 'specs/pause').mkdir(parents=True)
        (self.folder / '.openspec.yaml').write_text('schema: unity-game\n', encoding='utf-8')
        self.spec = self.folder / 'specs/pause/spec.md'
        self.spec.write_text('## ADDED Requirements\n### Requirement: PAUSE-001 - Pause\nGame SHALL pause.\n#### Scenario: Pause\n- WHEN paused\n- THEN time stops\n', encoding='utf-8')
        (self.folder / 'tasks.md').write_text('- [x] 1.1 Test pause\n', encoding='utf-8')
        (self.root / 'probe.py').write_text('from pathlib import Path\np=Path("calls.txt")\np.write_text(p.read_text()+"x" if p.exists() else "x")\n', encoding='utf-8')
        self.data = {'schema': 2, 'requirements': [{'id': 'PAUSE-001', 'checks': ['tests']}],
                     'checks': {'tests': {'kind': 'automated', 'command': ['{python}', 'probe.py'], 'target': 'fixture'}}}
        self.write()

    def write(self):
        (self.folder / 'verification.json').write_text(json.dumps(self.data), encoding='utf-8')

    def check(self, accept=True):
        return gate.check(self.root, 'test-feature', accept)

    def manual(self):
        self.data['checks']['visual'] = {'kind': 'visual', 'status': 'pending', 'procedure': 'Inspect fixture', 'target': 'fixture'}
        self.data['requirements'][0]['checks'].append('visual')
        path = self.root / 'docs/evidence/frame.txt'
        path.parent.mkdir(parents=True)
        path.write_text('fixture, not a game capture', encoding='utf-8')
        self.write()
        return path

    def test_shared_command_executes_once_per_delivery(self):
        self.data['requirements'].append({'id': 'PAUSE-002', 'checks': ['tests']})
        self.write()
        self.check()
        self.assertEqual('x', (self.root / 'calls.txt').read_text())
        self.check()
        self.assertEqual('xx', (self.root / 'calls.txt').read_text())

    def test_mapping_is_read_only_and_does_not_execute(self):
        self.manual()
        self.check(False)
        self.assertFalse((self.root / 'calls.txt').exists())
        self.assertFalse((self.root / 'artifacts').exists())

    def test_current_failure_rejects_previous_pass_and_retains_results(self):
        self.check()
        (self.root / 'probe.py').write_text('raise SystemExit(7)', encoding='utf-8')
        with self.assertRaises(subprocess.CalledProcessError) as error:
            self.check()
        self.assertEqual(7, error.exception.returncode)
        reports = [json.loads(p.read_text()) for p in (self.root / 'artifacts/verification').glob('*/results.json')]
        self.assertEqual({'pass', 'fail'}, {r['status'] for r in reports})

    def test_timeout_fails_and_keeps_report(self):
        (self.root / 'probe.py').write_text('import time\nprint("started", flush=True)\ntime.sleep(30)', encoding='utf-8')
        self.data['checks']['tests']['timeout_seconds'] = 1
        self.write()
        with self.assertRaises(subprocess.TimeoutExpired):
            self.check()
        report = next((self.root / 'artifacts/verification').glob('*/results.json'))
        self.assertEqual('fail', json.loads(report.read_text())['status'])
        self.assertIn('started', (report.parent / 'tests.log').read_text())

    def test_pending_failed_review_rejected_before_commands(self):
        self.manual()
        for status in ('pending', 'fail'):
            self.data['checks']['visual']['status'] = status
            self.write()
            with self.assertRaisesRegex(ValueError, 'Unaccepted'):
                self.check()
        self.assertFalse((self.root / 'calls.txt').exists())

    def test_record_review_and_changed_artifact_rejection(self):
        path = self.manual()
        gate.record_review(self.root, 'test-feature', 'visual', 'pass', 'test-agent', ['docs/evidence/frame.txt'])
        self.check()
        path.write_text('replaced', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'modified'):
            self.check()

    def test_missing_reviewer_rejected(self):
        self.manual()
        with self.assertRaisesRegex(ValueError, 'reviewer'):
            gate.record_review(self.root, 'test-feature', 'visual', 'pass', '', ['docs/evidence/frame.txt'])

    def test_symlink_and_traversal_rejected(self):
        path = self.manual()
        with self.assertRaises(ValueError):
            gate.record_review(self.root, 'test-feature', 'visual', 'pass', 'agent', ['../frame.txt'])
        link = path.with_name('link.txt')
        try:
            link.symlink_to(path)
        except OSError:
            return  # Traversal case still ran; platform cannot create symlinks.
        with self.assertRaisesRegex(ValueError, 'Symlink'):
            gate.record_review(self.root, 'test-feature', 'visual', 'pass', 'agent', ['docs/evidence/link.txt'])

    def test_archive_runs_without_resealing_and_ignores_historical_records(self):
        before = (self.folder / 'verification.json').read_bytes()
        archive = self.folder.parent / 'archive/2026-10-08-test-feature'
        archive.parent.mkdir(parents=True)
        self.folder.rename(archive)
        gate.check(self.root, 'archive/2026-10-08-test-feature', True)
        self.assertEqual(before, (archive / 'verification.json').read_bytes())

    def test_schema_one_requires_explicit_migration(self):
        self.data['schema'] = 1
        self.write()
        with self.assertRaisesRegex(ValueError, 'schema 2'):
            self.check()

    def test_missing_duplicate_or_unused_mapping_rejected(self):
        for rows in ([], [{'id': 'PAUSE-002', 'checks': ['tests']}],
                     [{'id': 'PAUSE-001', 'checks': ['missing']}],
                     [{'id': 'PAUSE-001', 'checks': ['tests', 'tests']}]):
            self.data['requirements'] = rows
            self.write()
            with self.assertRaises(ValueError):
                self.check()

    def test_cannot_claim_automated_pass_without_execution(self):
        self.data['checks']['tests']['status'] = 'pass'
        self.write()
        with self.assertRaisesRegex(ValueError, 'execution'):
            self.check()

    def test_incomplete_tasks_rejected(self):
        (self.folder / 'tasks.md').write_text('- [ ] 1.1 Pending\n', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'tasks'):
            self.check()

    def test_duplicate_ids_and_unmapped_removal_rejected(self):
        self.spec.write_text(self.spec.read_text() + '\n### Requirement: PAUSE-001 - duplicate\n', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            self.check()
        self.spec.write_text('## REMOVED Requirements\n### Requirement: PAUSE-002 - Old\n', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'mapping'):
            self.check()

    def test_setup_collision_and_dry_run(self):
        dest = Path(self.temp.name) / 'new'
        setup.stage(ROOT / 'starter/openspec', dest, True)
        self.assertFalse(dest.exists())
        (self.root / 'openspec/config.yaml').write_text('my config', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'differs'):
            setup.stage(ROOT / 'starter/openspec', self.root)

    def test_explicit_nonbehavioral_change(self):
        self.spec.unlink()
        with self.assertRaisesRegex(ValueError, 'No requirements'):
            self.check()
        (self.folder / '.openspec.yaml').write_text('schema: unity-game\nskip_specs: true\n', encoding='utf-8')
        self.data['requirements'][0]['id'] = 'CHANGE-001'
        self.write()
        self.check()

    def test_migration_preview_apply_idempotence_and_archive_rejection(self):
        import sys
        legacy = {'schema': 1, 'fingerprint': 'old', 'requirements': [
            {'id': 'PAUSE-001', 'status': 'pass', 'required_kinds': ['automated', 'visual'], 'evidence': []}]}
        path = self.folder / 'verification.json'
        path.write_text(json.dumps(legacy), encoding='utf-8')
        before = path.read_bytes()
        command = [sys.executable, str(self.root / 'tooling/specs/migrate.py'), '--change', 'test-feature',
                   '--command-json', '["{python}", "probe.py"]', '--target', 'fixture']
        preview = subprocess.run(command, capture_output=True, text=True, check=True)
        self.assertEqual(before, path.read_bytes())
        self.assertEqual(2, json.loads(preview.stdout)['schema'])
        subprocess.run(command + ['--apply'], capture_output=True, check=True)
        mapped = json.loads(path.read_text())
        self.assertEqual('pending', mapped['checks']['visual-pause-001']['status'])
        self.assertEqual(['tests', 'visual-pause-001'], mapped['requirements'][0]['checks'])
        before = path.read_bytes()
        subprocess.run(command + ['--apply'], capture_output=True, check=True)
        self.assertEqual(before, path.read_bytes())
        command[command.index('test-feature')] = 'archive/2026-test-feature'
        self.assertNotEqual(0, subprocess.run(command, capture_output=True).returncode)

    def test_invalid_migration_rolls_back_exact_original(self):
        import sys
        path = self.folder / 'verification.json'
        path.write_bytes(b'{"schema":1,"requirements":[{"id":"BAD","required_kinds":[]}]}')
        before = path.read_bytes()
        result = subprocess.run([sys.executable, str(self.root / 'tooling/specs/migrate.py'), '--change',
            'test-feature', '--command-json', '["{python}","probe.py"]', '--target', 'fixture', '--apply'],
            capture_output=True)
        self.assertNotEqual(0, result.returncode)
        self.assertEqual(before, path.read_bytes())

    def test_rereview_replaced_artifact_records_new_hash(self):
        path = self.manual()
        gate.record_review(self.root, 'test-feature', 'visual', 'pass', 'agent', ['docs/evidence/frame.txt'])
        path.write_text('new inspected capture', encoding='utf-8')
        gate.record_review(self.root, 'test-feature', 'visual', 'pass', 'agent', ['docs/evidence/frame.txt'])
        self.check()

    def test_command_cannot_replace_reviewed_artifact(self):
        self.manual()
        gate.record_review(self.root, 'test-feature', 'visual', 'pass', 'agent', ['docs/evidence/frame.txt'])
        (self.root / 'probe.py').write_text('from pathlib import Path\nPath("docs/evidence/frame.txt").write_text("different")', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'modified'):
            self.check()

    def test_missing_executable_keeps_failed_report(self):
        self.data['checks']['tests']['command'] = ['workflow-nonexistent-executable-374829']
        self.write()
        with self.assertRaises(OSError):
            self.check()
        report = next((self.root / 'artifacts/verification').glob('*/results.json'))
        self.assertEqual('fail', json.loads(report.read_text())['status'])
