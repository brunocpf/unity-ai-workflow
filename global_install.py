"""Global discovery adapter backed by an immutable, complete local kit snapshot."""
import json
import re

BASE = '.local/share/unity-ai-workflow'
STATE = BASE + '/global.json'
NAMES = ('unity-workflow-start', 'unity-workflow-update')
LOCATIONS = {'codex': '.agents/skills', 'claude': '.claude/skills'}
ENTRIES = {f'{folder}/{name}/SKILL.md' for folder in LOCATIONS.values() for name in NAMES}
FOLDERS = ('references', 'starter', 'examples', 'skills', 'global', 'tools', 'verification', 'tests', '.github')


def snapshot(source, core):
    files = {}
    paths = list(source.glob('*.md')) + list(source.glob('*.py')) + [source / 'kit.json']
    for folder in FOLDERS:
        paths.extend((source / folder).rglob('*'))
    for path in sorted(set(paths)):
        relative = path.relative_to(source)
        if any(p in core.EXCLUDED for p in relative.parts) or path.suffix == '.pyc':
            continue
        if path.is_symlink():
            raise core.InstallError(f'Symlink in source snapshot: {path}')
        if path.is_file():
            files[relative.as_posix()] = path.read_bytes()
    for required in ('kit.json', 'install.py', 'global_install.py', *(f'global/{name}/SKILL.md' for name in NAMES)):
        if required not in files:
            raise core.InstallError(f'Incomplete global source: {required}')
    return files


def state_at(home, core):
    data = core.read(home, STATE)
    if data is None:
        return None
    state = json.loads(data)
    if state.get('schema') != 1 or state.get('kit') != 'unity-ai-workflow-global':
        raise core.InstallError('Invalid global installation manifest')
    if not isinstance(state.get('agents'), list) or not state['agents'] or any(a not in LOCATIONS for a in state['agents']):
        raise core.InstallError('Invalid global client inventory')
    cache = state.get('cache', '')
    if not re.fullmatch(re.escape(BASE) + r'/kits/\d+\.\d+\.\d+-[0-9a-f]{64}', cache):
        raise core.InstallError('Invalid global cache path')
    if not isinstance(state.get('files'), dict) or not state['files']:
        raise core.InstallError('Missing global file inventory')
    for path, sha in state['files'].items():
        if not (path.startswith(cache + '/') or path in ENTRIES) or not isinstance(sha, str) or not re.fullmatch('[0-9a-f]{64}', sha):
            raise core.InstallError(f'Invalid global inventory path/hash: {path}')
        core.safe_path(home, path)
    for agent in state['agents']:
        for name in NAMES:
            if f'{LOCATIONS[agent]}/{name}/SKILL.md' not in state['files']:
                raise core.InstallError(f'Missing global adapter: {agent}/{name}')
    for required in ('install.py', 'kit.json', 'references/adoption.md', 'starter/AGENTS.md'):
        if cache + '/' + required not in state['files']:
            raise core.InstallError(f'Missing cached dependency: {required}')
    return state


def verify(home, core, state=None):
    state = state or state_at(home, core)
    if state is None:
        raise core.InstallError('Global entrypoint is not installed')
    for path, sha in state['files'].items():
        data = core.read(home, path)
        if data is None or core.digest(data) != sha:
            raise core.InstallError(f'Missing/modified global content: {path}; preserve edits and restore before updating')
    cache = home / state['cache']
    for path in cache.rglob('*'):
        if '__pycache__' in path.parts:
            continue
        if path.is_symlink() or (path.is_file() and path.relative_to(home).as_posix() not in state['files']):
            raise core.InstallError(f'Unexpected file in pinned cache: {path}')
    return {'status': 'pass', 'version': state['version'], 'agents': state['agents'], 'kit_root': str(cache), 'note': 'Integrity only; restart/open a client session to discover the global entrypoint.'}


def run(source, home, command, agent, dry_run, core):
    old = state_at(home, core)
    if command == 'check-global':
        return verify(home, core, old)
    if old:
        verify(home, core, old)
    selected = list(LOCATIONS) if agent == 'both' else [agent] if agent else old['agents'] if old else list(LOCATIONS)
    agents = sorted(set(selected) | set(old['agents'] if old else []))
    source_files = snapshot(source, core)
    metadata = json.loads(source_files['kit.json'])
    if metadata.get('id') != 'unity-ai-workflow' or metadata.get('global_skills') != list(NAMES):
        raise core.InstallError('Invalid global kit metadata')
    version = metadata['version']
    if not re.fullmatch(r'\d+\.\d+\.\d+', version):
        raise core.InstallError('Global snapshot requires a numeric release version')
    hashes = {p: core.digest(d) for p, d in sorted(source_files.items())}
    tree_hash = core.digest(json.dumps(hashes, sort_keys=True).encode())
    cache = f'{BASE}/kits/{version}-{tree_hash}'
    desired = {f'{cache}/{p}': data for p, data in source_files.items()}
    for name in NAMES:
        template = source_files[f'global/{name}/SKILL.md'].decode('utf-8')
        for client in agents:
            desired[f'{LOCATIONS[client]}/{name}/SKILL.md'] = template.replace('{{KIT_ROOT}}', (home / cache).as_posix()).replace('{{AGENT}}', client).encode('utf-8')
    state = {'schema': 1, 'kit': 'unity-ai-workflow-global', 'version': version, 'cache': cache, 'agents': agents,
             'files': {p: core.digest(d) for p, d in sorted(desired.items())}}
    # A preexisting version directory must be complete and unmodified, not partially overlaid.
    if (home / cache).exists() and any(p.is_file() or p.is_symlink() for p in (home / cache).rglob('*')):
        verify(home, core, {**state, 'agents': [], 'files': {p: sha for p, sha in state['files'].items() if p.startswith(cache + '/')}})
    originals, changes = {}, {}
    for relative, wanted in desired.items():
        current = core.read(home, relative)
        originals[relative] = current
        if current is not None and core.digest(current) == core.digest(wanted):
            continue
        owned = old and relative in old['files'] and current is not None and core.digest(current) == old['files'][relative]
        if current is not None and not owned:
            raise core.InstallError(f'Unmanaged global collision: {relative}; no files changed')
        changes[relative] = wanted
    originals[STATE] = core.read(home, STATE)
    new_state = (json.dumps(state, indent=2, sort_keys=True) + '\n').encode()
    if originals[STATE] is None or core.digest(originals[STATE]) != core.digest(new_state):
        changes[STATE] = new_state
    result = {'operation': command, 'dry_run': dry_run, 'version': version, 'agents': agents,
              'kit_root': str(home / cache), 'changed_files': len(changes), 'existing_projects_modified': False}
    if changes and not dry_run:
        core.apply_changes(home, changes, originals, BASE + '/install.lock')
    return result
