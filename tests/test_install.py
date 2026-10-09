import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('installer', ROOT / 'install.py')
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='unity kit tests ')
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.source = self.base / 'kit'
        self.source.mkdir()
        shutil.copy2(ROOT / 'kit.json', self.source)
        for folder in ('references', 'starter', 'examples', 'skills'):
            shutil.copytree(ROOT / folder, self.source / folder,
                            ignore=shutil.ignore_patterns('bin', 'obj', '__pycache__', '.DS_Store'))
        self.target = self.base / 'game with spaces'

    def run_install(self, command='install', agent=None, dry_run=False):
        return installer.install(self.source, self.target, command, agent, dry_run)

    def snapshot(self):
        return {p.relative_to(self.target).as_posix(): p.read_bytes()
                for p in self.target.rglob('*') if p.is_file()}

    def test_both_clients_and_dependency_closure(self):
        self.run_install()
        result = installer.verify(self.target)
        self.assertEqual(result['agents'], ['claude', 'codex'])
        for client in installer.CLIENTS.values():
            for skill in result['skills']:
                self.assertTrue((self.target / client / skill / 'SKILL.md').is_file())
        self.assertFalse((self.target / 'docs/standards/examples').exists())
        release_ref = json.loads((self.source / 'kit.json').read_text())['release_ref']
        self.assertIn(f'blob/{release_ref}/examples/', (self.target / 'docs/standards/references/ui-navigation.md').read_text())
        self.assertIn('@AGENTS.md', (self.target / 'CLAUDE.md').read_text())
        self.assertFalse((self.target / 'Assets').exists())
        self.assertFalse((self.target / 'ProjectSettings').exists())
        self.assertFalse((self.target / '.editorconfig').exists())
        self.assertFalse((self.target / 'docs/index.md').exists())

    def test_single_clients(self):
        for agent, other in [('codex', 'claude'), ('claude', 'codex')]:
            with self.subTest(agent=agent):
                self.target = self.base / agent
                self.run_install(agent=agent)
                self.assertEqual(installer.verify(self.target)['agents'], [agent])
                self.assertFalse((self.target / installer.CLIENTS[other]).exists())

    def test_dry_run_does_not_create_target(self):
        self.assertTrue(self.run_install(dry_run=True)['changes'])
        self.assertFalse(self.target.exists())

    def test_idempotent_install(self):
        self.run_install()
        before = self.snapshot()
        self.assertEqual(self.run_install()['changes'], {})
        self.assertEqual(before, self.snapshot())

    def test_existing_instructions_preserved(self):
        self.target.mkdir()
        for name in ('AGENTS.md', 'CLAUDE.md'):
            (self.target / name).write_bytes(b'# Team rules\r\nDo not replace.\r\n')
        self.run_install()
        for name in ('AGENTS.md', 'CLAUDE.md'):
            self.assertTrue((self.target / name).read_bytes().startswith(b'# Team rules\r\nDo not replace.\r\n'))
        (self.target / 'AGENTS.md').write_text((self.target / 'AGENTS.md').read_text() + '\nMy new rule.\n')
        self.run_install('update')
        self.assertTrue((self.target / 'AGENTS.md').read_text().endswith('My new rule.\n'))
        installer.verify(self.target)

    def test_collision_prevents_all_writes(self):
        p = self.target / 'docs/standards/references/adoption.md'
        p.parent.mkdir(parents=True)
        p.write_text('Existing standards')
        before = self.snapshot()
        with self.assertRaises(installer.InstallError):
            self.run_install()
        self.assertEqual(before, self.snapshot())

    def test_git_crlf_checkout_is_not_local_drift(self):
        self.run_install()
        for p in self.target.rglob('*'):
            if p.is_file():
                data = p.read_bytes()
                p.write_bytes(data.replace(b'\r\n', b'\n').replace(b'\n', b'\r\n'))
        before = self.snapshot()
        installer.verify(self.target)
        self.assertEqual(self.run_install('update')['changes'], {})
        self.assertEqual(before, self.snapshot())
        self.assertNotEqual(installer.digest(b'\0\r\n'), installer.digest(b'\0\n'))

    def test_local_modification_prevents_all_update_writes(self):
        self.run_install()
        (self.target / 'docs/standards/references/adoption.md').write_text('Local changes')
        (self.source / 'references/toolchain.md').write_text('Upstream changes')
        before = self.snapshot()
        with self.assertRaises(installer.InstallError):
            self.run_install('update')
        self.assertEqual(before, self.snapshot())
        with self.assertRaises(installer.InstallError):
            installer.verify(self.target)

    def test_update_dry_run_and_apply(self):
        self.run_install()
        (self.source / 'references/toolchain.md').write_text('New toolchain policy')
        before = self.snapshot()
        self.assertIn('docs/standards/references/toolchain.md', self.run_install('update', dry_run=True)['changes'])
        self.assertEqual(before, self.snapshot())
        self.run_install('update')
        self.assertEqual((self.target / 'docs/standards/references/toolchain.md').read_text(), 'New toolchain policy')
        installer.verify(self.target)

    def test_upstream_removal_preserves_unmanaged_neighbors(self):
        installer.install(self.source, self.target, 'install', examples='all')
        (self.source / 'examples/ui-recipes.md').unlink()
        neighbor = self.target / 'docs/standards/examples/my-notes.md'
        neighbor.write_text('Project notes')
        self.run_install('update')
        self.assertFalse((self.target / 'docs/standards/examples/ui-recipes.md').exists())
        self.assertEqual(neighbor.read_text(), 'Project notes')

    def test_removal_of_locally_modified_upstream_file_conflicts(self):
        installer.install(self.source, self.target, 'install', examples='all')
        (self.source / 'examples/ui-recipes.md').unlink()
        (self.target / 'docs/standards/examples/ui-recipes.md').write_text('Edited locally')
        before = self.snapshot()
        with self.assertRaises(installer.InstallError):
            self.run_install('update')
        self.assertEqual(before, self.snapshot())

    def test_add_client_without_removing_existing(self):
        self.run_install(agent='codex')
        self.run_install('update', agent='claude')
        self.assertEqual(installer.verify(self.target)['agents'], ['claude', 'codex'])

    def test_missing_owned_file_requires_review(self):
        self.run_install()
        (self.target / 'docs/standards/references/toolchain.md').unlink()
        with self.assertRaises(installer.InstallError):
            self.run_install('update')

    def test_edited_instruction_block_conflicts(self):
        self.run_install()
        p = self.target / 'AGENTS.md'
        p.write_text(p.read_text().replace('Unity game work', 'unrelated work'))
        with self.assertRaises(installer.InstallError):
            self.run_install('update')

    def test_malformed_markers_rejected(self):
        self.target.mkdir()
        (self.target / 'AGENTS.md').write_bytes(installer.BEGIN)
        with self.assertRaises(installer.InstallError):
            self.run_install()
        self.assertFalse((self.target / 'docs').exists())

    def test_symlink_target_rejected(self):
        outside = self.base / 'outside'
        outside.mkdir()
        self.target.mkdir()
        try:
            (self.target / 'docs').symlink_to(outside, target_is_directory=True)
        except OSError:
            self.skipTest('Symlink creation unavailable on this host')
        with self.assertRaises(installer.InstallError):
            self.run_install()
        self.assertEqual(list(outside.iterdir()), [])

    def test_manifest_path_traversal_rejected(self):
        self.run_install()
        state_path = self.target / installer.STATE
        data = json.loads(state_path.read_text())
        data['files']['../escape'] = '0' * 64
        state_path.write_text(json.dumps(data))
        with self.assertRaises(installer.InstallError):
            self.run_install('update')

    def test_build_products_excluded(self):
        p = self.source / 'examples/Verification/bin/private.txt'
        p.parent.mkdir(parents=True)
        p.write_text('Do not distribute')
        self.run_install()
        self.assertFalse((self.target / 'docs/standards/examples/Verification/bin').exists())

    def test_rollback_on_write_error(self):
        self.run_install()
        for file in ('adoption.md', 'toolchain.md'):
            (self.source / 'references' / file).write_text('New revision')
        before = self.snapshot()
        original = installer.atomic_write
        count = 0

        def failing(path, data):
            nonlocal count
            count += 1
            if count == 2:
                raise OSError('Injected write failure')
            original(path, data)

        with patch.object(installer, 'atomic_write', failing):
            with self.assertRaises(OSError):
                self.run_install('update')
        self.assertEqual(before, self.snapshot())

    def test_lock_prevents_writes(self):
        self.run_install()
        (self.source / 'references/toolchain.md').write_text('New policy')
        (self.target / '.unity-workflow/install.lock').touch()
        before = self.snapshot()
        with self.assertRaises(installer.InstallError):
            self.run_install('update')
        self.assertEqual(before, self.snapshot())

    def test_update_requires_install(self):
        with self.assertRaises(installer.InstallError):
            self.run_install('update')

    def test_optional_examples_add_remove_and_local_edit_protection(self):
        self.run_install()
        installer.install(self.source, self.target, 'update', examples='all')
        file = self.target / 'docs/standards/examples/README.md'
        self.assertTrue(file.is_file())
        self.run_install('update')
        self.assertTrue(file.is_file())
        before = file.read_bytes()
        file.write_bytes(before + b'\ncustom change')
        with self.assertRaises(installer.InstallError):
            installer.install(self.source, self.target, 'update', examples='none')
        file.write_bytes(before)
        plan = installer.assess(self.source, self.target, examples='none')
        self.assertTrue(any(c['candidate_change'] == 'remove' for c in plan['changes']))
        installer.install(self.source, self.target, 'update', examples='none')
        self.assertFalse(file.exists())
        installer.verify(self.target)

    def test_legacy_pack_choice_and_installed_link_closure(self):
        import subprocess
        import sys
        installer.install(self.source, self.target, 'install', examples='all')
        state_path = self.target / installer.STATE
        state = json.loads(state_path.read_text())
        del state['examples']  # 0.3.x manifests installed the full library without a selector.
        state_path.write_text(json.dumps(state))
        self.run_install('update')
        self.assertTrue((self.target / 'docs/standards/examples/README.md').is_file())
        for choice in ('all', 'none'):
            installer.install(self.source, self.target, 'update', examples=choice)
            result = subprocess.run([sys.executable, str(ROOT / 'tools/check_kit.py'), str(self.target)],
                                    capture_output=True, text=True)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            installer.verify(self.target)


if __name__ == '__main__':
    unittest.main()
