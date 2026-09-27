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
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True)
        self.folder = self.root / 'openspec/changes/test-feature'
        (self.folder / 'specs/pause').mkdir(parents=True)
        (self.folder / '.openspec.yaml').write_text('schema: unity-game\n', encoding='utf-8')
        self.spec = self.folder / 'specs/pause/spec.md'
        self.spec.write_text('## ADDED Requirements\n### Requirement: PAUSE-001 - Pause\nGame SHALL pause.\n#### Scenario: Pause\n- WHEN paused\n- THEN time stops\n', encoding='utf-8')
        (self.folder / 'tasks.md').write_text('- [x] 1.1 Test pause\n', encoding='utf-8')
        evidence = self.root / 'docs/evidence/pause.txt'
        evidence.parent.mkdir(parents=True)
        evidence.write_bytes(b'Explicit fixture evidence; not a real Unity result.\n')
        self.row = {'id': 'PAUSE-001', 'status': 'pass', 'required_kinds': ['automated'], 'evidence': [
            {'kind': 'automated', 'path': 'docs/evidence/pause.txt', 'sha256': gate.sha(evidence.read_bytes()),
             'command_or_procedure': 'fixture-only', 'target': 'test', 'run_id': 'fixture-1'}]}
        self.data = {'schema': 1, 'fingerprint': gate.fingerprint(self.root, 'test-feature'), 'requirements': [self.row]}
        self.write()

    def write(self):
        (self.folder / 'verification.json').write_text(json.dumps(self.data), encoding='utf-8')

    def check(self, accept=True):
        return gate.check(self.root, 'test-feature', accept)

    def test_valid_fixture(self):
        self.assertEqual('pass', self.check()['status'])

    def test_stream_hash_preserves_binary_and_normalizes_text(self):
        path = self.root / 'sample'
        for data in (b'a' * 65535 + b'\r\nend\r', b'\xc3\xa9\r\n', b'\0\r\n', b'\xff\r\n', b'\xc3'):
            path.write_bytes(data)
            try:
                data.decode('utf-8')
                expected = data if b'\0' in data else data.replace(b'\r\n', b'\n')
            except UnicodeDecodeError:
                expected = data
            self.assertEqual(gate.sha(expected), gate.source_hash(path))

    def test_archive_requires_final_tree_fingerprint(self):
        archive = self.root / 'openspec/changes/archive/2026-09-26-test-feature'
        archive.parent.mkdir(parents=True)
        self.folder.rename(archive)
        name = 'archive/2026-09-26-test-feature'
        with self.assertRaisesRegex(ValueError, 'Stale'):
            gate.check(self.root, name, True)
        self.data['fingerprint'] = gate.fingerprint(self.root, name)
        (archive / 'verification.json').write_text(json.dumps(self.data), encoding='utf-8')
        self.assertEqual('pass', gate.check(self.root, name, True)['status'])

    def test_missing_mapping_rejected(self):
        self.data['requirements'] = []
        self.write()
        with self.assertRaisesRegex(ValueError, 'mapping'):
            self.check()

    def test_deleted_source_invalidates_but_staging_is_stable(self):
        source = self.root / 'source.cs'
        source.write_text('// source', encoding='utf-8')
        subprocess.run(['git', 'add', '.'], cwd=self.root, check=True)
        self.data['fingerprint'] = gate.fingerprint(self.root, 'test-feature')
        self.write()
        source.unlink()
        with self.assertRaisesRegex(ValueError, 'Stale'):
            self.check()
        before = gate.fingerprint(self.root, 'test-feature')
        subprocess.run(['git', 'add', '-u'], cwd=self.root, check=True)
        self.assertEqual(before, gate.fingerprint(self.root, 'test-feature'))

    def test_tracked_archive_acceptance_survives_staging(self):
        subprocess.run(['git', 'add', '.'], cwd=self.root, check=True)
        archive = self.root / 'openspec/changes/archive/2026-09-27-test-feature'
        archive.parent.mkdir(parents=True)
        self.folder.rename(archive)
        name = 'archive/2026-09-27-test-feature'
        with self.assertRaisesRegex(ValueError, 'Stale'):
            gate.check(self.root, name, True)
        self.data['fingerprint'] = gate.fingerprint(self.root, name)
        (archive / 'verification.json').write_text(json.dumps(self.data), encoding='utf-8')
        subprocess.run(['git', 'add', '-A'], cwd=self.root, check=True)
        self.assertEqual('pass', gate.check(self.root, name, True)['status'])
        (self.root / 'later.cs').write_text('// changed source', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Stale'):
            gate.check(self.root, name, True)

    def test_failed_pending_and_missing_kind_rejected(self):
        for status in ('fail', 'pending'):
            self.row['status'] = status
            self.write()
            with self.assertRaises(ValueError):
                self.check()
        self.row['status'] = 'pass'
        self.row['required_kinds'].append('visual')
        self.write()
        with self.assertRaises(ValueError):
            self.check()

    def test_pending_allowed_only_in_mapping_mode(self):
        self.row['status'] = 'pending'
        self.row['evidence'] = []
        self.write()
        self.check(False)
        with self.assertRaises(ValueError):
            self.check()

    def test_stale_spec_and_code_rejected(self):
        self.spec.write_text(self.spec.read_text(encoding='utf-8') + '\nChanged outcome\n', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Stale'):
            self.check()
        self.data['fingerprint'] = gate.fingerprint(self.root, 'test-feature')
        self.write()
        (self.root / 'game.cs').write_text('// new code', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Stale'):
            self.check()

    def test_changed_evidence_rejected(self):
        (self.root / 'docs/evidence/pause.txt').write_text('different evidence', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'evidence'):
            self.check()

    def test_missing_manual_reviewer_rejected(self):
        self.row['required_kinds'] = ['visual']
        self.row['evidence'][0]['kind'] = 'visual'
        self.write()
        with self.assertRaisesRegex(ValueError, 'reviewer'):
            self.check()

    def test_incomplete_tasks_rejected(self):
        (self.folder / 'tasks.md').write_text('- [ ] 1.1 Pending playtest\n', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'tasks'):
            self.check()

    def test_duplicate_ids_rejected(self):
        self.spec.write_text(self.spec.read_text(encoding='utf-8') + '\n### Requirement: PAUSE-001 - duplicate\n', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            self.check()

    def test_removal_requires_mapping(self):
        self.spec.write_text('## REMOVED Requirements\n### Requirement: PAUSE-002 - Old behavior\n', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'mapping'):
            self.check()

    def test_setup_collision_and_dry_run(self):
        dest = Path(self.temp.name) / 'new'
        setup.stage(ROOT / 'starter/openspec', dest, True)
        self.assertFalse(dest.exists())
        (self.root / 'openspec/config.yaml').write_text('my config', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'differs'):
            setup.stage(ROOT / 'starter/openspec', self.root)
        self.assertEqual('my config', (self.root / 'openspec/config.yaml').read_text(encoding='utf-8'))

    def test_symlink_evidence_rejected(self):
        link = self.root / 'docs/evidence/link.txt'
        try:
            link.symlink_to(self.root / 'docs/evidence/pause.txt')
        except OSError:
            self.skipTest('Symlinks unavailable')
        self.row['evidence'][0]['path'] = 'docs/evidence/link.txt'
        self.write()
        with self.assertRaisesRegex(ValueError, 'Symlink'):
            self.check()

    def test_explicit_nonbehavioral_change(self):
        self.spec.unlink()
        with self.assertRaisesRegex(ValueError, 'No requirements'):
            self.check()
        (self.folder / '.openspec.yaml').write_text('schema: unity-game\nskip_specs: true\n', encoding='utf-8')
        self.row['id'] = 'CHANGE-001'
        self.data['fingerprint'] = gate.fingerprint(self.root, 'test-feature')
        self.write()
        self.check()
