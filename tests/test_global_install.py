import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / (name + '.py'))
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


core = module('install')
global_install = module('global_install')


class GlobalTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='global kit tests ')
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.source = self.base / 'source'
        for path, data in global_install.snapshot(ROOT, core).items():
            target = self.source / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        self.home = self.base / 'home with spaces'

    def run_install(self, agent='both', dry=False):
        return global_install.run(self.source, self.home, 'install-global', agent, dry, core)

    def test_dry_run_no_writes(self):
        self.run_install(dry=True)
        self.assertFalse(self.home.exists())

    def test_both_clients_complete_offline_snapshot_and_noop(self):
        result = self.run_install()
        cache = Path(result['kit_root'])
        for client, folder in global_install.LOCATIONS.items():
            for name in global_install.NAMES:
                text = (self.home / folder / name / 'SKILL.md').read_text(encoding='utf-8')
                self.assertIn(cache.as_posix(), text)
                self.assertNotIn('{{', text)
        self.assertEqual(0, self.run_install()['changed_files'])
        global_install.verify(self.home, core)
        # Cached installer works independently of the source checkout.
        self.source.rename(self.base / 'hidden-source')
        game = self.base / 'game'
        subprocess.run([sys.executable, str(cache / 'install.py'), 'install', '--target', str(game), '--agent', 'both', '--mode', 'vendored'], check=True, capture_output=True)
        core.verify(game)
        self.assertFalse((game / 'Assets').exists())

    def test_single_client_then_add_other(self):
        self.run_install('codex')
        self.assertFalse((self.home / '.claude').exists())
        self.run_install('claude')
        self.assertEqual(['claude', 'codex'], global_install.verify(self.home, core)['agents'])

    def test_collision_prevents_cache_writes(self):
        path = self.home / '.agents/skills/unity-workflow-start/SKILL.md'
        path.parent.mkdir(parents=True)
        path.write_text('my skill')
        with self.assertRaises(core.InstallError):
            self.run_install()
        self.assertEqual('my skill', path.read_text(encoding='utf-8'))
        self.assertFalse((self.home / global_install.BASE).exists())

    def test_modified_adapter_or_cache_blocks_update(self):
        result = self.run_install()
        path = Path(result['kit_root']) / 'README.md'
        path.write_text('local edit')
        with self.assertRaises(core.InstallError):
            self.run_install()
        with self.assertRaises(core.InstallError):
            global_install.verify(self.home, core)

    def test_new_snapshot_retains_old_and_project_version(self):
        old = self.run_install()
        game = self.base / 'game'
        core.install(self.source, game, 'install')
        manifest = (game / core.STATE).read_bytes()
        p = self.source / 'README.md'
        p.write_text(p.read_text(encoding='utf-8') + '\nA reviewed update.\n', encoding='utf-8')
        new = self.run_install()
        self.assertNotEqual(old['kit_root'], new['kit_root'])
        self.assertTrue(Path(old['kit_root']).exists())
        self.assertEqual(manifest, (game / core.STATE).read_bytes())
        global_install.verify(self.home, core)

    def test_symlink_parent_rejected(self):
        self.home.mkdir()
        elsewhere = self.base / 'elsewhere'
        elsewhere.mkdir()
        try:
            (self.home / '.agents').symlink_to(elsewhere, target_is_directory=True)
        except OSError:
            self.skipTest('Symlinks unavailable')
        with self.assertRaises(core.InstallError):
            self.run_install()
        self.assertFalse(list(elsewhere.iterdir()))

    def test_failed_install_can_retry(self):
        real = core.atomic_write
        count = 0
        def fail(path, data):
            nonlocal count
            count += 1
            if count == 4:
                raise OSError('test failure')
            real(path, data)
        with patch.object(core, 'atomic_write', side_effect=fail):
            with self.assertRaises(OSError):
                self.run_install()
        self.run_install()
        global_install.verify(self.home, core)

    def test_assess_reports_drift_and_changes_without_writes(self):
        game = self.base / 'game'
        core.install(self.source, game, 'install')
        owned = game / 'docs/standards/references/adoption.md'
        owned.write_text(owned.read_text(encoding='utf-8') + '\nLocal exception.\n', encoding='utf-8')
        (self.source / 'references/new-policy.md').write_text('New policy')
        (self.source / 'references/vfx.md').unlink()
        before = {str(p): p.read_bytes() for p in game.rglob('*') if p.is_file()}
        report = core.assess(self.source, game)
        rows = {x['path']: x for x in report['changes']}
        self.assertTrue(rows['docs/standards/references/adoption.md']['local_drift'])
        self.assertEqual('add', rows['docs/standards/references/new-policy.md']['candidate_change'])
        self.assertEqual('remove', rows['docs/standards/references/vfx.md']['candidate_change'])
        self.assertEqual(before, {str(p): p.read_bytes() for p in game.rglob('*') if p.is_file()})
        self.assertEqual(0, report['writes'])

    def test_assess_requires_baseline(self):
        with self.assertRaises(core.InstallError):
            core.assess(self.source, self.base / 'unadopted')
