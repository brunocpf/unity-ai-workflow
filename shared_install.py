"""Project pins, shared cache links and explicit vendored/shared migration."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import cache_restore as cache

LOCAL = '.unity-workflow/local.json'
HELPER = '.unity-workflow/restore.py'
IGNORE_BEGIN = b'# unity-ai-workflow:begin'
IGNORE_END = b'# unity-ai-workflow:end'


def revision(source, home):
    try:
        top = subprocess.check_output(['git', '-C', str(source), 'rev-parse', '--show-toplevel'], stderr=subprocess.DEVNULL, text=True).strip()
        if Path(top).resolve() == source.resolve():
            if subprocess.check_output(['git', '-C', str(source), 'status', '--porcelain'], text=True).strip():
                raise ValueError('Shared installation requires a clean committed kit source')
            return subprocess.check_output(['git', '-C', str(source), 'rev-parse', 'HEAD'], text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        pass
    state_path = home / '.local/share/unity-ai-workflow/global.json'
    if state_path.is_file():
        state = json.loads(state_path.read_text())
        if (home / state['cache']).resolve() == source.resolve() and state.get('source_revision'):
            return state['source_revision']
    raise ValueError('Source commit unavailable. Use a clean pinned Git checkout or a provenance-bearing global cache.')


def pin_for(source, home, agents):
    files = cache.snapshot(source)
    meta = json.loads(files['kit.json'])
    pin = {'schema': 2, 'mode': 'shared', 'kit': meta['id'], 'version': meta['version'],
           'repository': cache.REPOSITORY, 'source_revision': revision(source, home),
           'cache_sha256': cache.tree_hash(files), 'agents': agents, 'skills': meta['skills']}
    cache.validate_pin(pin)
    return pin


def paths(pin):
    return {'docs/standards': '.', **{f'{folder}/{name}': f'skills/{name}'
            for client, folder in [('codex', '.agents/skills'), ('claude', '.claude/skills')]
            if client in pin['agents'] for name in pin['skills']}}


def ign_block(data):
    data = data or b''
    if not data.count(IGNORE_BEGIN) and not data.count(IGNORE_END):
        return None
    if data.count(IGNORE_BEGIN) != 1 or data.count(IGNORE_END) != 1:
        raise ValueError('Malformed workflow .gitignore block')
    a, b = data.index(IGNORE_BEGIN), data.index(IGNORE_END) + len(IGNORE_END)
    if b <= a:
        raise ValueError('Reversed workflow .gitignore block')
    return data[a:b]


def blocks(pin, core):
    values = {'AGENTS.md': core.BEGIN + b'\nRead docs/standards/PROJECT-RULES.md for Unity work. This is a link to the project-pinned kit.\nIf absent, run python3 .unity-workflow/restore.py --fetch before using kit guidance. Never substitute the global latest.\nInstallation alone does not authorize project creation.\n' + core.END}
    if 'claude' in pin['agents']:
        values['CLAUDE.md'] = core.BEGIN + b'\n@AGENTS.md\n@docs/standards/PROJECT-RULES.md\n' + core.END
    ignored = [LOCAL, '.unity-workflow/install.lock', *paths(pin)]
    values['.gitignore'] = IGNORE_BEGIN + b'\n' + '\n'.join('/' + p for p in ignored).encode() + b'\n' + IGNORE_END
    return values


def read_pin(root, core):
    raw = core.read(root, core.STATE)
    return json.loads(raw) if raw else None


def local_state(root, core):
    raw = core.read(root, LOCAL)
    return json.loads(raw) if raw else None


def check_parents(root, relative):
    current = root
    for part in Path(relative).parts[:-1]:
        current = current / part
        if current.is_symlink() or (current.exists() and not current.is_dir()):
            raise ValueError(f'Unsafe link parent: {current}')


def inspect_links(root, pin, local, allow_missing=False):
    expected_paths = paths(pin)
    if local is not None and set(local.get('links', {})) != set(expected_paths):
        raise ValueError('Local link inventory differs; inspect before restoring')
    for relative in expected_paths:
        check_parents(root, relative)
        path = root / relative
        if not path.is_symlink():
            if allow_missing and not path.exists():
                continue
            raise ValueError(f'Missing/non-link managed path: {relative}; run restore or reconcile local files')
        if local is None or os.readlink(path) != local['links'][relative]:
            raise ValueError(f'Unowned/retargeted link: {relative}')


def verify(root, home, core):
    pin = read_pin(root, core)
    cache.validate_pin(pin)
    target = cache.cache_path(home, pin)
    cache.verify_cache(target, pin)
    local = local_state(root, core)
    inspect_links(root, pin, local)
    for relative, suffix in paths(pin).items():
        if (root / relative).resolve() != (target / suffix).resolve():
            raise ValueError('Links do not resolve to the locked kit; run restore')
    for relative, expected in pin['blocks'].items():
        raw = core.read(root, relative)
        value = ign_block(raw) if relative == '.gitignore' else core.block(raw)
        if value is None or core.digest(value) != expected:
            raise ValueError(f'Modified instruction/ignore block: {relative}')
    if core.digest(core.read(root, HELPER) or b'') != pin['helper_sha256']:
        raise ValueError('Missing/modified restore helper')
    return {'status': 'pass', 'mode': 'shared', 'version': pin['version'], 'agents': pin['agents'],
            'kit_root': str(target), 'note': 'Integrity and link layout only; client discovery is separate.'}


def transact(root, directory_changes, file_changes, core):
    """Rename old directories/links to backups and roll back all owned changes on failure."""
    lock = core.safe_path(root, '.unity-workflow/install.lock')
    lock.parent.mkdir(parents=True, exist_ok=True)
    try:
        with tempfile.TemporaryDirectory(prefix='.install-', dir=lock.parent) as temp:
            backup = Path(temp)
            moved, written = [], []
            originals = {p: core.read(root, p) for p in file_changes}
            try:
                for index, (relative, desired) in enumerate(directory_changes.items()):
                    check_parents(root, relative)
                    dest = root / relative
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    saved = backup / str(index)
                    had = dest.exists() or dest.is_symlink()
                    if had:
                        os.replace(dest, saved)
                    moved.append((dest, saved, had))
                    if isinstance(desired, Path):
                        dest.symlink_to(desired, target_is_directory=True)
                    elif desired is not None:
                        dest.mkdir()
                        for name, data in desired.items():
                            core.atomic_write(dest / name, data)
                for relative, data in file_changes.items():
                    dest = core.safe_path(root, relative)
                    if data is None:
                        if dest.exists():
                            dest.unlink()
                    else:
                        core.atomic_write(dest, data)
                    written.append(relative)
            except Exception:
                for relative in reversed(written):
                    dest = core.safe_path(root, relative)
                    if originals[relative] is None:
                        dest.unlink(missing_ok=True)
                    else:
                        core.atomic_write(dest, originals[relative])
                for dest, saved, had in reversed(moved):
                    if dest.is_symlink():
                        dest.unlink()
                    elif dest.exists():
                        shutil.rmtree(dest)
                    if had:
                        os.replace(saved, dest)
                raise
    finally:
        pass


def _run(source, root, home, command, agent, dry_run, mode, core, examples=None):
    if root == source or source in root.parents:
        raise ValueError('Install outside the kit source/cache')
    old = read_pin(root, core)
    if command == 'check':
        return verify(root, home, core)
    if command in ('update', 'assess', 'restore') and old is None:
        raise ValueError('No project pin; use install first')
    is_shared = old and old.get('schema') == 2
    if command == 'restore':
        if not is_shared:
            raise ValueError('Restore applies only to shared projects')
        mode = 'shared'
    mode = mode or ('shared' if not old or is_shared else 'vendored')
    selected = list(core.CLIENTS) if agent == 'both' else [agent] if agent else old['agents'] if old else list(core.CLIENTS)
    agents = sorted(set(selected) | set(old['agents'] if old else []))
    local = local_state(root, core)
    if is_shared:
        cache.validate_pin(old)
        # A reverted lock may differ from the currently materialized links.
        ownership = local.get('pin', old) if local else old
        cache.validate_pin(ownership)
        inspect_links(root, ownership, local, allow_missing=command == 'restore')
        for relative, expected in old['blocks'].items():
            raw = core.read(root, relative)
            observed = ign_block(raw) if relative == '.gitignore' else core.block(raw)
            if observed is None or core.digest(observed) != expected:
                raise ValueError(f'Modified managed block: {relative}')
        if core.digest(core.read(root, HELPER) or b'') != old['helper_sha256']:
            raise ValueError('Modified/missing restore helper; reconcile before update')
        if command != 'restore':
            cache.verify_cache(cache.cache_path(home, old), old)
    elif old:
        core.verify(root)
    if not is_shared:
        for relative in (HELPER, LOCAL):
            if core.read(root, relative) is not None:
                raise ValueError(f'Unmanaged helper/state collision: {relative}')
    previous_dirs = paths(local.get('pin', old) if is_shared and local else old) if old else {}
    if not is_shared:
        for relative in set(previous_dirs) | set(paths({'agents': agents, 'skills': json.loads((source / 'kit.json').read_text())['skills']})):
            check_parents(root, relative)
            path = root / relative
            if path.is_symlink():
                raise ValueError(f'Unmanaged link: {relative}')
            if path.exists() and not path.is_dir():
                raise ValueError(f'Unmanaged file blocks directory replacement: {relative}')
            if path.exists():
                for child in path.rglob('*'):
                    if child.is_symlink() or (child.is_file() and (not old or child.relative_to(root).as_posix() not in old['files'])):
                        raise ValueError(f'Unmanaged content blocks directory replacement: {child}')
    if mode == 'shared':
        pin = old if command == 'restore' else pin_for(source, home, agents)
        cache_target = cache.cache_path(home, pin)
        # Existing cache corruption must be detected even during dry-run.
        if cache_target.exists():
            cache.verify_cache(cache_target, pin)
        wanted_blocks = blocks(pin, core)
        helper = (source / 'cache_restore.py').read_bytes() if command != 'restore' else core.read(root, HELPER)
        if command != 'restore':
            pin['blocks'] = {p: core.digest(d) for p, d in wanted_blocks.items()}
            pin['helper_sha256'] = core.digest(helper)
        directories = {p: cache_target / suffix for p, suffix in paths(pin).items()}
        new_local = {'pin': pin, 'links': {p: str(d) for p, d in directories.items()}}
        files = {HELPER: helper, LOCAL: (json.dumps(new_local, indent=2) + '\n').encode()}
    else:
        if not is_shared:
            return core.install(source, root, command, agent, dry_run, examples)
        meta, payload, wanted_blocks = core.payload(source, agents, examples or 'none')
        with tempfile.TemporaryDirectory() as temp:
            staging = Path(temp) / 'game'
            core.install(source, staging, 'install', 'both' if len(agents) == 2 else agents[0], examples=examples or 'none')
            pin = json.loads((staging / core.STATE).read_text())
        directories = {p: {name[len(p)+1:]: data for name, data in payload.items() if name.startswith(p+'/')}
                       for p in paths({'agents': agents, 'skills': meta['skills']})}
        files = {HELPER: None, LOCAL: None}
        wanted_blocks['.gitignore'] = None
    for relative, wanted in wanted_blocks.items():
        raw = core.read(root, relative) or b''
        previous = ign_block(raw) if relative == '.gitignore' else core.block(raw)
        expected = old.get('blocks', {}).get(relative) if old else None
        if previous is not None and core.digest(previous) != expected and previous != wanted:
            raise ValueError(f'Unowned/edited routing block: {relative}')
        if relative == '.gitignore':
            value = raw.replace(previous, wanted or b'', 1) if previous else raw + (b'\n' if raw else b'') + (wanted or b'') + b'\n'
        else:
            value = core.merge_block(raw, wanted)
        files[relative] = value
    files[core.STATE] = (json.dumps(pin, indent=2, sort_keys=True) + '\n').encode()
    for relative in previous_dirs:
        directories.setdefault(relative, None)
    directories = {p: d for p, d in directories.items() if not (isinstance(d, Path) and (root/p).is_symlink() and os.readlink(root/p) == str(d))}
    files = {p: d for p, d in files.items() if core.read(root, p) != d}
    result = {'operation': command, 'mode': mode, 'version': pin['version'], 'dry_run': dry_run or command == 'assess',
              'changes': {**{p: 'link' if isinstance(d, Path) else 'vendor' for p, d in directories.items()}, **{p: 'remove' if d is None else 'write' for p, d in files.items()}}}
    if command == 'assess':
        result['installed_version'] = old['version']
        if is_shared:
            before = cache.snapshot(cache.cache_path(home, old))
            after = cache.snapshot(source)
            result['source_changes'] = [p for p in sorted(set(before) | set(after)) if before.get(p) != after.get(p)]
        else:
            result['source_changes'] = core.assess(source, root, examples)['changes']
    if dry_run or command == 'assess':
        return result
    if mode == 'shared':
        cache.ensure_cache(home, pin, source=None if command == 'restore' else source)
    if directories or files:
        transact(root, directories, files, core)
    return result


def run(source, root, home, command, agent, dry_run, mode, core, examples=None):
    if dry_run or command in ('assess', 'check'):
        return _run(source, root, home, command, agent, dry_run, mode, core, examples)
    lock = core.safe_path(root, '.unity-workflow/install.lock')
    lock.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    os.close(fd)
    try:
        return _run(source, root, home, command, agent, dry_run, mode, core, examples)
    finally:
        lock.unlink()
