"""Shared cache behavior: pins, links, ownership, restore and migration."""
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile
import unittest
from unittest.mock import patch

import install as core
import shared_install as shared
import cache_restore as cache
import global_install

ROOT = Path(__file__).resolve().parents[1]


class SharedTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='shared kit ')
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.source, self.game, self.home = [self.base / n for n in ['source', 'game', 'home']]
        for name, data in global_install.snapshot(ROOT, core).items():
            p = self.source / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(data)
        (self.source / '.gitignore').write_text('__pycache__/\n')
        subprocess.run(['git', 'init', '-q', str(self.source)], check=True)
        # Disposable repositories must not leave background maintenance racing cleanup.
        subprocess.run(['git', '-C', str(self.source), 'config', 'gc.auto', '0'], check=True)
        subprocess.run(['git', '-C', str(self.source), 'config', 'maintenance.auto', 'false'], check=True)
        self.commit()
        probe = self.base / 'probe'
        try:
            probe.symlink_to(self.source, target_is_directory=True)
            probe.unlink()
        except OSError:
            self.skipTest('Directory symlinks unavailable; use vendored mode')

    def commit(self):
        subprocess.run(['git', '-C', str(self.source), 'add', '.'], check=True)
        subprocess.run(['git', '-C', str(self.source), '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
                        'commit', '-qm', 'fixture'], check=True)

    def run_install(self, command='install', mode=None, dry=False, game=None, source=None):
        return shared.run(source or self.source, game or self.game, self.home, command, 'both' if command=='install' else None,
                          dry, mode, core)

    def test_default_cli_and_shared_snapshot_reuse(self):
        subprocess.run([sys.executable, str(self.source/'install.py'), 'install', '--target', str(self.game),
                        '--home', str(self.home)], check=True, capture_output=True)
        shared.verify(self.game, self.home, core)
        other = self.base / 'other game'
        self.run_install(game=other)
        self.assertEqual((self.game/'docs/standards').resolve(), (other/'docs/standards').resolve())
        self.assertTrue((self.game/'.agents/skills/unity-feature-workflow').is_symlink())
        self.assertEqual({}, self.run_install('update')['changes'])
        pin = (self.game/core.STATE).read_text()
        self.assertNotIn(str(self.home), pin)
        self.assertNotIn(str(self.source), pin)

    def test_dry_run_writes_nothing(self):
        self.run_install(dry=True)
        self.assertFalse(self.home.exists())
        self.assertFalse(self.game.exists())

    def test_missing_cache_and_restore_on_new_machine(self):
        self.run_install()
        clone = self.base/'clone'
        for relative in [core.STATE, shared.HELPER, 'AGENTS.md', 'CLAUDE.md', '.gitignore']:
            p=clone/relative;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(self.game/relative,p)
        pin=json.loads((clone/core.STATE).read_text())
        new_home=self.base/'new-home'
        with self.assertRaisesRegex(ValueError,'missing'):
            cache.ensure_cache(new_home,pin)
        cache.ensure_cache(new_home,pin,source=self.source)
        shared.run(self.source,clone,new_home,'restore',None,False,None,core)
        shared.verify(clone,new_home,core)
        self.assertEqual((self.game/core.STATE).read_bytes(),(clone/core.STATE).read_bytes())

    def test_update_is_pinned_and_rollback_restores_old_links(self):
        self.run_install()
        old={p:(self.game/p).read_bytes() for p in [core.STATE, shared.HELPER, 'AGENTS.md','CLAUDE.md','.gitignore']}
        other=self.base/'other';self.run_install(game=other)
        p=self.source/'README.md';p.write_text(p.read_text()+'\nNew guidance.\n');self.commit()
        self.run_install('update')
        self.assertNotEqual((self.game/'docs/standards').resolve(),(other/'docs/standards').resolve())
        for name,data in old.items():(self.game/name).write_bytes(data)
        self.run_install('restore')
        shared.verify(self.game,self.home,core)
        self.assertEqual((self.game/'docs/standards').resolve(),(other/'docs/standards').resolve())

    def test_vendored_migration_both_directions_and_custom_files(self):
        core.install(self.source,self.game,'install','both')
        (self.game/'AGENTS.md').write_text((self.game/'AGENTS.md').read_text()+'\nMy project choice.\n')
        self.run_install('update',mode='shared')
        shared.verify(self.game,self.home,core)
        self.run_install('update',mode='vendored')
        core.verify(self.game)
        self.assertFalse((self.game/'docs/standards').is_symlink())
        self.assertIn('My project choice.',(self.game/'AGENTS.md').read_text())
        self.assertNotIn('/docs/standards',(self.game/'.gitignore').read_text())
        self.assertFalse((self.game/shared.HELPER).exists())

    def test_extra_and_edited_vendored_files_block_migration(self):
        core.install(self.source,self.game,'install','both')
        extra=self.game/'docs/standards/notes.md';extra.write_text('unique')
        with self.assertRaisesRegex(ValueError,'Unmanaged content'):
            self.run_install('update',mode='shared')
        self.assertEqual('unique',extra.read_text());extra.unlink()
        owned=self.game/'docs/standards/references/ci.md';owned.write_text('customized')
        with self.assertRaises(core.InstallError):self.run_install('update',mode='shared')
        self.assertEqual('customized',owned.read_text())

    def test_cache_tamper_and_link_retarget_rejected(self):
        self.run_install()
        target=(self.game/'docs/standards').resolve()
        p=target/'README.md';old=p.read_bytes();p.write_text('tamper')
        with self.assertRaisesRegex(ValueError,'content changed'):shared.verify(self.game,self.home,core)
        p.write_bytes(old)
        link=self.game/'.agents/skills/unity-feature-workflow';link.unlink();link.symlink_to(self.source/'skills/unity-feature-workflow',target_is_directory=True)
        with self.assertRaisesRegex(ValueError,'retargeted'):self.run_install('update')

    def test_failed_link_creation_rolls_back_vendored_content(self):
        core.install(self.source,self.game,'install','both')
        before={p.relative_to(self.game):p.read_bytes() for p in self.game.rglob('*') if p.is_file()}
        with patch.object(Path,'symlink_to',side_effect=OSError('no symlink privilege')):
            with self.assertRaises(OSError):self.run_install('update',mode='shared')
        after={p.relative_to(self.game):p.read_bytes() for p in self.game.rglob('*') if p.is_file()}
        self.assertEqual(before,after)
        core.verify(self.game)

    def test_exact_download_verified_before_execution(self):
        pin=shared.pin_for(self.source,self.home,['codex'])
        data=io.BytesIO()
        with tarfile.open(fileobj=data,mode='w:gz') as archive:
            for name,content in cache.snapshot(self.source).items():
                entry=tarfile.TarInfo('release/'+name);entry.size=len(content);archive.addfile(entry,io.BytesIO(content))
        with patch('urllib.request.urlopen',return_value=io.BytesIO(data.getvalue())) as download:
            target=cache.ensure_cache(self.home,pin,fetch=True)
        self.assertIn(pin['source_revision'],download.call_args.args[0])
        cache.verify_cache(target,pin)
        pin['cache_sha256']='0'*64
        with patch('urllib.request.urlopen',return_value=io.BytesIO(data.getvalue())):
            with self.assertRaisesRegex(ValueError,'exact project pin'):cache.ensure_cache(self.home,pin,fetch=True)
        self.assertFalse(cache.cache_path(self.home,pin).exists())

    def test_global_and_project_share_same_cache(self):
        global_install.run(self.source,self.home,'install-global','both',False,core)
        state=json.loads((self.home/global_install.STATE).read_text())
        source=self.home/state['cache']
        self.run_install(source=source)
        self.assertEqual(source,(self.game/'docs/standards').resolve())
        global_install.verify(self.home,core)

    def test_modified_helper_and_unsafe_parent_rejected(self):
        self.run_install()
        (self.game/shared.HELPER).write_text('custom')
        with self.assertRaisesRegex(ValueError,'helper'):self.run_install('update')
        other=self.base/'unsafe';other.mkdir();(other/'docs').symlink_to(self.base,target_is_directory=True)
        with self.assertRaisesRegex(ValueError,'parent'):self.run_install(game=other)

    def test_dirty_source_rejected(self):
        (self.source/'README.md').write_text('uncommitted')
        with self.assertRaisesRegex(ValueError,'clean committed'):self.run_install()

    def test_tracked_vendored_files_become_ignored_links(self):
        core.install(self.source,self.game,'install','both')
        subprocess.run(['git','init','-q',str(self.game)],check=True)
        subprocess.run(['git','-C',str(self.game),'add','.'],check=True)
        self.run_install('update',mode='shared')
        subprocess.run(['git','-C',str(self.game),'add','-u'],check=True)
        tracked=subprocess.check_output(['git','-C',str(self.game),'ls-files'],text=True).splitlines()
        self.assertFalse(any(p.startswith(('docs/standards/','.agents/skills/unity-','.claude/skills/unity-')) for p in tracked))
        for name in ['docs/standards','.agents/skills/unity-feature-workflow',shared.LOCAL]:
            self.assertEqual(0,subprocess.run(['git','-C',str(self.game),'check-ignore',name],capture_output=True).returncode)
        self.assertTrue((self.game/'docs/standards').is_symlink())

    def test_unmanaged_helper_or_file_and_concurrent_install_rejected(self):
        self.game.mkdir()
        (self.game/shared.HELPER).parent.mkdir(parents=True)
        (self.game/shared.HELPER).write_text('user helper')
        with self.assertRaisesRegex(ValueError,'collision'):self.run_install()
        (self.game/shared.HELPER).unlink()
        (self.game/'docs').mkdir();(self.game/'docs/standards').write_text('user file')
        with self.assertRaisesRegex(ValueError,'Unmanaged file'):self.run_install()
        (self.game/'docs/standards').unlink()
        (self.game/'.unity-workflow/install.lock').write_text('other installer')
        with self.assertRaises(FileExistsError):self.run_install()
        self.assertTrue((self.game/'.unity-workflow/install.lock').exists())

    def test_malicious_archive_paths_rejected(self):
        pin=shared.pin_for(self.source,self.home,['codex'])
        data=io.BytesIO()
        with tarfile.open(fileobj=data,mode='w:gz') as archive:
            entry=tarfile.TarInfo('release/../escape.py');entry.size=1;archive.addfile(entry,io.BytesIO(b'x'))
        with patch('urllib.request.urlopen',return_value=io.BytesIO(data.getvalue())):
            with self.assertRaisesRegex(ValueError,'Unsafe'):cache.ensure_cache(self.home,pin,fetch=True)
        self.assertFalse(cache.cache_path(self.home,pin).exists())

    def test_cli_restores_from_pinned_cache_without_source_checkout(self):
        self.run_install()
        self.source.rename(self.base/'removed-source')
        result=subprocess.run([sys.executable,str(self.game/shared.HELPER),'--home',str(self.home)],capture_output=True,text=True)
        self.assertEqual(0,result.returncode,result.stderr)
        shared.verify(self.game,self.home,core)
