#!/usr/bin/env python3
"""Install global entrypoints or project-local workflow instructions; never creates or runs Unity."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile

SOURCE = Path(__file__).resolve().parent
STATE = '.unity-workflow/installation.json'
BEGIN = b'<!-- unity-ai-workflow:begin -->'
END = b'<!-- unity-ai-workflow:end -->'
CLIENTS = {'codex': '.agents/skills', 'claude': '.claude/skills'}
EXCLUDED = {'.git', 'bin', 'obj', '__pycache__', '.DS_Store'}


class InstallError(Exception):
    pass


def digest(data):
    # Git/editor line-ending conversion must not look like a policy edit.
    # Keep binary content byte-exact; normalize only UTF-8 text without NULs.
    try:
        data.decode('utf-8')
        if b'\0' not in data:
            data = data.replace(b'\r\n', b'\n')
    except UnicodeDecodeError:
        pass
    return hashlib.sha256(data).hexdigest()


def safe_path(root, relative):
    parts = PurePosixPath(relative).parts
    if not parts or '\\' in relative or ':' in relative or any(p in ('..', '.') for p in parts) or relative.startswith('/'):
        raise InstallError(f'Invalid managed path: {relative}')
    path = root
    for part in parts:
        path = path / part
        if path.is_symlink():
            raise InstallError(f'Symlink in managed path: {path}')
        if path.exists() and path != root / relative and not path.is_dir():
            raise InstallError(f'Parent is not a directory: {path}')
    if path.exists() and not path.is_file():
        raise InstallError(f'Managed path is not a file: {path}')
    return path


def read(root, relative):
    path = safe_path(root, relative)
    return path.read_bytes() if path.exists() else None


def block(data):
    data = data or b''
    if not data.count(BEGIN) and not data.count(END):
        return None
    if data.count(BEGIN) != 1 or data.count(END) != 1:
        raise InstallError('Malformed or duplicate workflow markers in instruction file')
    start, end = data.index(BEGIN), data.index(END) + len(END)
    if end <= start:
        raise InstallError('Reversed workflow markers in instruction file')
    return data[start:end]


def merge_block(current, desired):
    current = current or b''
    previous = block(current)
    if previous is not None:
        return current.replace(previous, desired, 1)
    separator = b'' if not current or current.endswith(b'\n\n') else b'\n' if current.endswith(b'\n') else b'\n\n'
    return current + separator + desired + b'\n'


def read_state(root):
    raw = read(root, STATE)
    if raw is None:
        return None
    state = json.loads(raw)
    if state.get('schema') != 1 or state.get('kit') != 'unity-ai-workflow':
        raise InstallError('Unsupported installation manifest')
    agents = state.get('agents')
    if not isinstance(agents, list) or not agents or any(a not in CLIENTS for a in agents):
        raise InstallError('Invalid installed clients')
    for category in ('files', 'blocks'):
        if not isinstance(state.get(category), dict):
            raise InstallError(f'Invalid manifest {category}')
        for path, value in state[category].items():
            safe_path(root, path)
            allowed = path in ('AGENTS.md', 'CLAUDE.md') if category == 'blocks' else path.startswith(('docs/standards/', '.agents/skills/unity-', '.claude/skills/unity-'))
            if not allowed or not isinstance(value, str) or not re.fullmatch('[0-9a-f]{64}', value):
                raise InstallError(f'Invalid manifest entry: {path}')
    if 'AGENTS.md' not in state['blocks'] or ('claude' in agents and 'CLAUDE.md' not in state['blocks']):
        raise InstallError('Installation manifest is missing instruction ownership')
    skills = state.get('skills')
    if not isinstance(skills, list) or not skills or any(not isinstance(s, str) or not re.fullmatch('unity-[a-z0-9-]+', s) for s in skills):
        raise InstallError('Invalid installed skill inventory')
    return state


def payload(source, agents):
    metadata = json.loads((source / 'kit.json').read_text())
    if metadata.get('id') != 'unity-ai-workflow' or not re.fullmatch(r'\d+\.\d+\.\d+(?:[-+][a-zA-Z0-9.-]+)?', metadata.get('version', '')):
        raise InstallError('Invalid kit metadata')
    skills = metadata.get('skills', [])
    if not skills or len(set(skills)) != len(skills) or any(not re.fullmatch('unity-[a-z0-9-]+', s) for s in skills):
        raise InstallError('Invalid skill inventory')
    files = {}

    def copy_tree(folder, destination):
        base = source / folder
        if not base.is_dir() or base.is_symlink():
            raise InstallError(f'Missing/linked source directory: {folder}')
        for p in sorted(base.rglob('*')):
            relative = p.relative_to(base)
            if any(part in EXCLUDED for part in relative.parts) or p.suffix == '.pyc':
                continue
            if p.is_symlink():
                raise InstallError(f'Linked source asset: {p}')
            if p.is_file():
                files[f'{destination}/{relative.as_posix()}'] = p.read_bytes()

    for folder in ('references', 'starter', 'examples'):
        copy_tree(folder, f'docs/standards/{folder}')
    for name in skills:
        entry = source / 'skills' / name / 'SKILL.md'
        if not entry.is_file():
            raise InstallError(f'Missing skill: {name}')
        for agent in agents:
            copy_tree(f'skills/{name}', f'{CLIENTS[agent]}/{name}')
    files['docs/standards/PROJECT-RULES.md'] = files['docs/standards/starter/AGENTS.md']
    blocks = {'AGENTS.md': BEGIN + b'\nRead and apply docs/standards/PROJECT-RULES.md for Unity game work.\nInstallation alone does not authorize project creation or gameplay implementation.\n' + END}
    if 'claude' in agents:
        blocks['CLAUDE.md'] = BEGIN + b'\n@AGENTS.md\n@docs/standards/PROJECT-RULES.md\n' + END
    return metadata, files, blocks


def verify(root):
    state = read_state(root)
    if state is None:
        raise InstallError('Workflow is not installed')
    issues = []
    for category in ('files', 'blocks'):
        for path, expected in state[category].items():
            current = read(root, path)
            if category == 'blocks':
                current = block(current)
            if current is None or digest(current) != expected:
                issues.append(path)
    if issues:
        raise InstallError('Missing or modified managed content:\n' + '\n'.join(issues))
    for agent in state['agents']:
        for name in state['skills']:
            path = f'{CLIENTS[agent]}/{name}/SKILL.md'
            if path not in state['files'] or read(root, path) is None:
                raise InstallError(f'Missing registered skill: {path}')
    for path in ('docs/standards/PROJECT-RULES.md', 'docs/standards/references/adoption.md', 'docs/standards/references/INDEX.md'):
        if path not in state['files']:
            raise InstallError(f'Missing shared dependency: {path}')
    return {'status': 'pass', 'version': state['version'], 'agents': state['agents'], 'skills': state['skills'], 'note': 'File integrity and layout only; client discovery and Unity acceptance are separate.'}


def atomic_write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    mode = path.stat().st_mode & 0o777 if path.exists() else 0o644
    fd, temporary = tempfile.mkstemp(prefix='.workflow-', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(data)
        os.chmod(temporary, mode)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def install(source, root, command, agent=None, dry_run=False):
    if root == source or source in root.parents:
        raise InstallError('Install into a game workspace outside the kit checkout')
    old = read_state(root)
    if command == 'update' and old is None:
        raise InstallError('No installation manifest; use install first')
    selected = list(CLIENTS) if agent == 'both' else [agent] if agent else old['agents'] if old else list(CLIENTS)
    agents = sorted(set(selected) | set(old['agents'] if old else []))
    metadata, files, blocks = payload(source, agents)
    snapshots, changes, conflicts = {}, {}, []
    for category, desired in (('files', files), ('blocks', blocks)):
        previous = old[category] if old else {}
        for relative in sorted(set(previous) | set(desired)):
            current = read(root, relative)
            snapshots[relative] = current
            inspected = block(current) if category == 'blocks' else current
            wanted = desired.get(relative)
            if inspected != wanted and inspected is not None and digest(inspected) != previous.get(relative):
                conflicts.append(relative)
                continue
            if inspected is None and relative in previous and wanted is not None:
                conflicts.append(relative)
                continue
            if inspected is not None and wanted is not None and digest(inspected) == digest(wanted):
                output = current
            else:
                output = merge_block(current, wanted) if category == 'blocks' else wanted
            if current != output:
                changes[relative] = output
    if conflicts:
        raise InstallError('Local edits/unmanaged collisions; no files changed. Review and merge or restore these paths before retrying:\n' + '\n'.join(conflicts))
    revision, dirty = None, None
    try:
        git_root = subprocess.check_output(['git', '-C', str(source), 'rev-parse', '--show-toplevel'], stderr=subprocess.DEVNULL, text=True).strip()
        if Path(git_root).resolve() == source.resolve():
            revision = subprocess.check_output(['git', '-C', str(source), 'rev-parse', 'HEAD'], stderr=subprocess.DEVNULL, text=True).strip()
            dirty = bool(subprocess.check_output(['git', '-C', str(source), 'status', '--porcelain'], stderr=subprocess.DEVNULL, text=True).strip())
    except (OSError, subprocess.CalledProcessError):
        pass
    state = {
        'schema': 1, 'kit': metadata['id'], 'version': metadata['version'],
        'source_revision': revision, 'source_dirty': dirty, 'agents': agents, 'skills': metadata['skills'],
        'files': {p: digest(d) for p, d in sorted(files.items())},
        'blocks': {p: digest(d) for p, d in sorted(blocks.items())},
    }
    state['payload_sha256'] = digest(json.dumps({'files': state['files'], 'blocks': state['blocks']}, sort_keys=True).encode())
    state_bytes = (json.dumps(state, indent=2, sort_keys=True) + '\n').encode()
    snapshots[STATE] = read(root, STATE)
    if snapshots[STATE] is None or digest(snapshots[STATE]) != digest(state_bytes):
        changes[STATE] = state_bytes
    result = {'operation': command, 'dry_run': dry_run, 'version': state['version'], 'agents': agents, 'changes': {p: 'remove' if d is None else 'write' for p, d in changes.items()}}
    if dry_run or not changes:
        return result
    apply_changes(root, changes, snapshots, '.unity-workflow/install.lock')
    return result


def apply_changes(root, changes, snapshots, lock_relative):
    lock = safe_path(root, lock_relative)
    lock.parent.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        raise InstallError(f'Another installation is running (or a stale {lock_relative} exists)') from None
    applied = []
    try:
        os.close(fd)
        for relative, original in snapshots.items():
            if read(root, relative) != original:
                raise InstallError(f'File changed during planning: {relative}')
        try:
            for relative, data in changes.items():
                path = safe_path(root, relative)
                if data is None:
                    path.unlink()
                else:
                    atomic_write(path, data)
                applied.append(relative)
        except Exception:
            for relative in reversed(applied):
                path = safe_path(root, relative)
                if snapshots[relative] is None:
                    path.unlink()
                else:
                    atomic_write(path, snapshots[relative])
            raise
    finally:
        lock.unlink()


def assess(source, root):
    """Report candidate differences without claiming semantic applicability or writing files."""
    old = read_state(root)
    if old is None:
        raise InstallError('No project installation manifest to assess')
    metadata, files, blocks = payload(source, old['agents'])
    changes = []
    for category, desired in (('files', files), ('blocks', blocks)):
        for path in sorted(set(old[category]) | set(desired)):
            current = read(root, path)
            if category == 'blocks':
                current = block(current)
            actual = digest(current) if current is not None else None
            incoming = digest(desired[path]) if path in desired else None
            previous = old[category].get(path)
            if previous != incoming or actual != previous:
                changes.append({'path': path, 'installed_hash': previous, 'current_hash': actual,
                                'candidate_hash': incoming, 'local_drift': actual != previous,
                                'candidate_change': 'remove' if incoming is None else 'add' if previous is None else 'unchanged' if incoming == previous else 'modify'})
    return {'operation': 'assess', 'installed_version': old['version'], 'candidate_version': metadata['version'],
            'changes': changes, 'writes': 0,
            'applicability': 'Unreviewed. Inspect changed source, project contracts, Unity/package pins and evidence before deciding. This report does not establish runtime compatibility.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['install', 'update', 'assess', 'check', 'install-global', 'check-global'])
    parser.add_argument('--target', type=Path, help='Game workspace (not the kit checkout)')
    parser.add_argument('--home', type=Path, help='Global install home override (for isolated tests)')
    parser.add_argument('--agent', choices=['codex', 'claude', 'both'], help='Default: both on install, existing clients on update; selections only add clients')
    parser.add_argument('--dry-run', action='store_true', help='Show the plan without writing files')
    args = parser.parse_args()
    try:
        if args.command in ('install-global', 'check-global'):
            if args.target or (args.command == 'check-global' and (args.agent or args.dry_run)):
                parser.error('Global commands do not accept --target; check-global accepts only --home')
            import global_install
            result = global_install.run(SOURCE, (args.home or Path.home()).expanduser().resolve(), args.command, args.agent, args.dry_run, sys.modules[__name__])
            print(json.dumps(result, indent=2))
            return 0
        if args.target is None or args.home:
            parser.error('Project commands require --target and do not accept --home')
        root = args.target.expanduser().resolve()
        if args.command == 'assess':
            if args.agent or args.dry_run:
                parser.error('assess accepts only --target and never writes files')
            result = assess(SOURCE, root)
        elif args.command == 'check':
            if args.agent or args.dry_run:
                parser.error('check does not accept --agent or --dry-run')
            result = verify(root)
        else:
            result = install(SOURCE, root, args.command, args.agent, args.dry_run)
        print(json.dumps(result, indent=2))
        return 0
    except (InstallError, OSError, ValueError, KeyError, TypeError) as error:
        print(f'Error: {error}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
