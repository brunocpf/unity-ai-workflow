import importlib.util
import json
import os
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
        p = self.source / 'examples/Build/bin/private.txt'
        p.parent.mkdir(parents=True)
        p.write_text('Do not distribute')
        self.run_install()
        self.assertFalse((self.target / 'docs/standards/examples/Build/bin').exists())

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

    def test_failed_first_install_leaves_no_folders(self):
        self.target.mkdir()
        original = installer.atomic_write
        count = 0

        def failing(path, data):
            nonlocal count
            count += 1
            if count == 5:
                raise OSError('Injected write failure')
            original(path, data)

        with patch.object(installer, 'atomic_write', failing):
            with self.assertRaises(OSError):
                self.run_install()
        self.assertEqual([], list(self.target.iterdir()))

    def test_scaffold_places_starter_files_without_overwriting(self):
        self.run_install()
        core = self.target / 'Assets/Game/Core'
        core.mkdir(parents=True)
        (core / 'Game.Core.asmdef').write_text('{}')
        (self.target / '.gitignore').write_text('custom\n')
        result = installer.scaffold(self.target)
        self.assertIn('.gitignore', result['merge'])
        self.assertEqual('custom\n', (self.target / '.gitignore').read_text())
        for path in ('.editorconfig', 'tooling/dotnet/Directory.Build.props', '.husky/pre-commit',
                     'tooling/quality/check.py', 'tooling/quality/CodeOrganization/Program.cs',
                     '.vscode/settings.json', 'tooling/ide/owned-projects.json', 'Assets/Game/Core/csc.rsp'):
            self.assertTrue((self.target / path).is_file(), path)
        if os.name != 'nt':  # Windows has no POSIX execute bit; Git records it separately.
            self.assertTrue((self.target / '.husky/pre-commit').stat().st_mode & 0o100)
        self.assertIn('-langversion:9.0', (self.target / 'Assets/Game/Core/csc.rsp').read_text())
        self.assertIn('namespace Workflow.Tooling\n{',
                      (self.target / 'tooling/quality/CodeOrganization/Program.cs').read_text())
        again = installer.scaffold(self.target)
        self.assertEqual([], again['written'])
        self.assertEqual(['.gitignore'], again['merge'])

    def test_scaffold_language_profile_and_dry_run(self):
        self.run_install()
        (self.target / 'Assets/Game/Core').mkdir(parents=True)
        (self.target / 'Assets/Game/Core/Game.Core.asmdef').write_text('{}')
        before = self.snapshot()
        plan = installer.scaffold(self.target, 'csharp14', dry_run=True)
        self.assertIn('Assets/Game/Core/csc.rsp', plan['written'])
        self.assertEqual(before, self.snapshot())
        installer.scaffold(self.target, 'csharp14')
        self.assertIn('-langversion:14.0', (self.target / 'Assets/Game/Core/csc.rsp').read_text())
        self.assertIn('>14.0</LangVersion>', (self.target / 'tooling/dotnet/Directory.Build.props').read_text())
        self.assertIn('"14.0"', (self.target / 'tooling/ide/owned-projects.json').read_text())
        # The checker itself must pass ORG006/IDE0161 under the file-scoped profile.
        checker = (self.target / 'tooling/quality/CodeOrganization/Program.cs').read_text()
        self.assertIn('namespace Workflow.Tooling;\n\ninternal static class Program\n{\n    //', checker)
        self.assertNotIn('\n        private static int Main', checker)
        self.assertTrue(checker.endswith('}\n'))

    def test_scaffold_reports_unwritable_files_and_continues(self):
        self.run_install()
        original = installer.atomic_write

        def failing(path, data):
            if '.vscode' in path.parts:
                raise PermissionError('Operation not permitted')
            original(path, data)

        with patch.object(installer, 'atomic_write', failing):
            result = installer.scaffold(self.target)
        self.assertEqual({'.vscode/settings.json', '.vscode/extensions.json', '.vscode/tasks.json'}, set(result['failed']))
        self.assertTrue((self.target / 'tooling/quality/check.py').is_file())
        retry = installer.scaffold(self.target)
        self.assertEqual(sorted(result['failed']), sorted(retry['written']))

    def test_scaffold_requires_install(self):
        self.target.mkdir()
        with self.assertRaises(installer.InstallError):
            installer.scaffold(self.target)

    def test_scaffold_rerun_keeps_the_project_profile(self):
        self.run_install()
        (self.target / 'Assets/Game/Core').mkdir(parents=True)
        (self.target / 'Assets/Game/Core/Game.Core.asmdef').write_text('{}')
        installer.scaffold(self.target, 'csharp14')
        (self.target / 'Assets/Game/Application').mkdir()
        (self.target / 'Assets/Game/Application/Game.Application.asmdef').write_text('{}')
        result = installer.scaffold(self.target)
        self.assertEqual('csharp14', result['profile'])
        self.assertEqual(['Assets/Game/Application/csc.rsp'], result['written'])
        self.assertIn('-langversion:14.0', (self.target / 'Assets/Game/Application/csc.rsp').read_text())
        self.assertTrue(any('csharp14.editorconfig' in step for step in result['next_steps']))
        with self.assertRaises(installer.InstallError):
            installer.scaffold(self.target, 'csharp9')

    @unittest.skipIf(os.name == 'nt', 'Windows has no POSIX execute bit')
    def test_scaffold_repairs_hook_executable_bit(self):
        self.run_install()
        installer.scaffold(self.target)
        hook = self.target / '.husky/pre-commit'
        hook.chmod(0o644)
        result = installer.scaffold(self.target)
        self.assertIn('.husky/pre-commit', result['unchanged'])
        self.assertTrue(hook.stat().st_mode & 0o100)

    def test_scaffold_reports_unusable_destination_and_continues(self):
        self.run_install()
        elsewhere = self.base / 'shared-vscode'
        elsewhere.mkdir()
        try:
            (self.target / '.vscode').symlink_to(elsewhere, target_is_directory=True)
        except OSError:
            self.skipTest('Symlinks need extra privileges on this platform')
        result = installer.scaffold(self.target)
        self.assertEqual({'.vscode/settings.json', '.vscode/extensions.json', '.vscode/tasks.json'}, set(result['failed']))
        self.assertEqual([], list(elsewhere.iterdir()))
        self.assertTrue((self.target / 'tooling/quality/check.py').is_file())

    def test_doctor_reports_gaps_without_unity(self):
        with patch.object(installer, 'probe', return_value=None), \
                patch.object(installer, 'reachable', return_value=False), \
                patch.object(installer, 'hub_editor_folders', return_value=[]), \
                patch.dict(installer.os.environ, {'UNITY_EDITOR': ''}):
            result = installer.doctor()
        self.assertIsNone(result['tools']['unity_cli'])
        self.assertEqual([], result['tools']['hub_editors'])
        self.assertTrue(any('No Unity CLI' in g for g in result['guidance']))
        self.assertTrue(any('No dotnet' in g for g in result['guidance']))
        self.assertTrue(any('did not answer' in g for g in result['guidance']))

    def test_doctor_finds_custom_hub_location_and_flags_certificate_errors(self):
        home = self.base / 'home'
        custom = self.base / 'D-drive/Unity'
        (custom / '6000.7.0b3').mkdir(parents=True)
        config = home / '.config/UnityHub'
        config.mkdir(parents=True)
        (config / 'secondaryInstallPath.json').write_text(json.dumps(str(custom)))
        with patch.object(installer, 'probe', return_value=None), \
                patch.object(installer, 'reachable', return_value='certificate-error'), \
                patch.object(installer.Path, 'home', return_value=home), \
                patch.dict(installer.os.environ, {'UNITY_EDITOR': '', 'APPDATA': ''}):
            result = installer.doctor()
        self.assertIn('6000.7.0b3', result['tools']['hub_editors'])
        self.assertFalse(any('No Unity CLI' in g for g in result['guidance']))
        self.assertTrue(any('TLS certificates' in g for g in result['guidance']))
        self.assertFalse(any('did not answer' in g for g in result['guidance']))

    def test_lock_prevents_writes(self):
        self.run_install()
        (self.source / 'references/toolchain.md').write_text('New policy')
        (self.target / '.unity-workflow/install.lock').touch()
        before = self.snapshot()
        with self.assertRaises(installer.InstallError):
            self.run_install('update')
        self.assertEqual(before, self.snapshot())

    def test_upstream_removal_preserves_project_owned_files(self):
        legacy = self.source / 'starter/retired/tooling/ci.py'
        legacy.parent.mkdir(parents=True)
        legacy.write_text('# retired starter script\n')
        self.run_install(agent='both')
        owned = {
            'tooling/specs/ci.py': '# customized game checks\n',
            'docs/design/game.md': 'Useful requirements\n',
            '.agents/skills/team-planning/SKILL.md': 'Project skill\n',
            '.claude/skills/team-planning/SKILL.md': 'Project skill\n',
            '.github/workflows/game.yml': '# existing game CI\n',
        }
        for name, content in owned.items():
            path = self.target / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
        legacy.unlink()
        before = self.snapshot()
        self.run_install('update', dry_run=True)
        self.assertEqual(before, self.snapshot())
        self.run_install('update')
        self.assertFalse((self.target / 'docs/standards/starter/retired/tooling/ci.py').exists())
        for name, content in owned.items():
            self.assertEqual(content, (self.target / name).read_text())
        self.assertEqual({}, self.run_install('update')['changes'])

    def test_linked_layout_manifest_explains_conversion(self):
        state = self.target / '.unity-workflow/installation.json'
        state.parent.mkdir(parents=True)
        state.write_text(json.dumps({'schema': 2, 'mode': 'shared', 'kit': 'unity-ai-workflow'}))
        with self.assertRaisesRegex(installer.InstallError, '--mode vendored'):
            self.run_install('update')

    def test_removed_files_do_not_leave_empty_folders(self):
        retired = self.source / 'references/retired/old.md'
        retired.parent.mkdir(parents=True)
        retired.write_text('Old policy\n')
        self.run_install()
        self.assertTrue((self.target / 'docs/standards/references/retired/old.md').exists())
        retired.unlink()
        retired.parent.rmdir()
        self.run_install('update')
        self.assertFalse((self.target / 'docs/standards/references/retired').exists())
        self.assertTrue((self.target / 'docs/standards/references').is_dir())

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
