"""Structural evidence gate; actual test jobs and human/agent review remain independent gates."""
import argparse
import codecs
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ID = re.compile(r'^[A-Z][A-Z0-9]*-[0-9]{3,}$')
KINDS = {'automated', 'visual', 'authoring', 'playtest', 'device'}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def source_hash(path):
    # Stream large textures/meshes; normalize CRLF only for valid UTF-8 without NULs.
    raw, normalized = hashlib.sha256(), hashlib.sha256()
    decoder = codecs.getincrementaldecoder('utf-8')()
    text, tail = True, b''
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(65536), b''):
            raw.update(chunk)
            if text:
                try:
                    decoder.decode(chunk)
                    text = b'\0' not in chunk
                except UnicodeDecodeError:
                    text = False
            combined = tail + chunk
            tail = b'\r' if combined.endswith(b'\r') else b''
            if tail:
                combined = combined[:-1]
            normalized.update(combined.replace(b'\r\n', b'\n'))
    normalized.update(tail)
    if text:
        try:
            decoder.decode(b'', final=True)
        except UnicodeDecodeError:
            text = False
    return normalized.hexdigest() if text else raw.hexdigest()


def safe_file(root, relative):
    path = Path(relative)
    if path.is_absolute() or '..' in path.parts or '\\' in relative or ':' in relative:
        raise ValueError(f'Unsafe path: {relative}')
    result = root / path
    for part in [result, *result.parents]:
        if part == root:
            break
        if part.is_symlink():
            raise ValueError(f'Symlink: {relative}')
    if not result.is_file():
        raise ValueError(f'Missing file: {relative}')
    return result


def change_dir(root, name):
    if not re.fullmatch(r'(?:archive/)?[a-z0-9]+(?:-[a-z0-9]+)*', name):
        raise ValueError('Use a kebab-case change name or archive/date-name')
    folder = root / 'openspec/changes' / name
    safe_file(root, f'openspec/changes/{name}/.openspec.yaml')
    return folder


def fingerprint(root, name):
    change_dir(root, name)
    # Git ignores govern generated output. Evidence/task bookkeeping is deliberately excluded.
    files = subprocess.check_output(['git', 'ls-files', '-z', '--cached', '--others', '--exclude-standard'], cwd=root)
    entries = {}
    for raw in sorted(set(files.split(b'\0')) - {b''}):
        relative = raw.decode('utf-8')
        p = Path(relative)
        if relative.startswith(('artifacts/', 'docs/evidence/', '.unity-workflow/')):
            continue
        if relative.startswith('openspec/changes/') and p.name in ('verification.json', 'tasks.md'):
            continue
        path = root / relative
        if not path.exists() and not path.is_symlink():
            entries[relative] = 'deleted'
            continue
        entries[relative] = source_hash(safe_file(root, relative))
    return sha(json.dumps(entries, sort_keys=True).encode())


def requirement_ids(folder):
    ids = set()
    for file in sorted((folder / 'specs').rglob('*.md')):
        text = safe_file(folder, file.relative_to(folder).as_posix()).read_text(encoding='utf-8')
        if '## RENAMED Requirements' in text:
            raise ValueError('Unity profile keeps titles/IDs stable; use MODIFIED or an explicit remove/add migration')
        for title in re.findall(r'^### Requirement:\s*(.+)$', text, re.M):
            identifier = title.split(' ', 1)[0]
            if not ID.fullmatch(identifier) or identifier in ids:
                raise ValueError(f'Invalid/duplicate requirement ID: {identifier}')
            ids.add(identifier)
    if not ids:
        metadata = (folder / '.openspec.yaml').read_text(encoding='utf-8')
        if not re.search(r'^skip_specs:\s*true\s*$', metadata, re.M):
            raise ValueError('No requirements; nonbehavioral changes must explicitly set skip_specs: true')
        ids.add('CHANGE-001')
    return ids


def check(root, name, accept=False):
    folder = change_dir(root, name)
    required = requirement_ids(folder)
    data = json.loads(safe_file(root, f'openspec/changes/{name}/verification.json').read_text(encoding='utf-8'))
    if data.get('schema') != 1 or not isinstance(data.get('requirements'), list):
        raise ValueError('Invalid verification schema')
    rows = data['requirements']
    listed = [r['id'] for r in rows]
    if len(listed) != len(set(listed)) or not required.issubset(listed):
        raise ValueError(f'Missing/duplicate acceptance mapping: {sorted(required - set(listed))}')
    for row in rows:
        if not ID.fullmatch(row['id']) or row.get('status') not in ('pending', 'pass', 'fail'):
            raise ValueError('Invalid requirement/status')
        kinds = row.get('required_kinds', [])
        if not kinds or len(kinds) != len(set(kinds)) or not set(kinds) <= KINDS:
            raise ValueError(f'Invalid required check kinds: {row["id"]}')
        evidence = row.get('evidence', [])
        if not isinstance(evidence, list):
            raise ValueError('Evidence must be a list')
        seen = set()
        for item in evidence:
            if item.get('kind') not in KINDS:
                raise ValueError('Unknown evidence kind')
            path = item['path']
            if not path.startswith(('artifacts/', 'docs/evidence/')):
                raise ValueError('Evidence must live in artifacts/ or docs/evidence/')
            contents = safe_file(root, path).read_bytes()
            if not contents.strip() or sha(contents) != item.get('sha256'):
                raise ValueError(f'Empty/modified evidence: {path}')
            if not item.get('command_or_procedure') or not item.get('target') or not item.get('run_id'):
                raise ValueError('Evidence requires procedure/command, target and run ID')
            if item['kind'] != 'automated' and not item.get('reviewer'):
                raise ValueError('Manual evidence requires its actual reviewer; never invent user approval')
            seen.add(item['kind'])
        if accept and (row['status'] != 'pass' or not set(kinds) <= seen):
            raise ValueError(f'Unaccepted or missing required evidence: {row["id"]}')
    if accept:
        tasks = safe_file(root, f'openspec/changes/{name}/tasks.md').read_text(encoding='utf-8')
        markers = re.findall(r'^\s*-\s+\[([^]]*)\]', tasks, re.M)
        if not markers or any(m.strip().lower() != 'x' for m in markers):
            raise ValueError('Incomplete/empty tasks')
        if data.get('fingerprint') != fingerprint(root, name):
            raise ValueError('Stale source/spec fingerprint; rerun affected checks and reconcile evidence')
    return {'status': 'pass', 'mode': 'acceptance-evidence' if accept else 'mapping',
            'requirements': len(rows), 'note': 'Integrity/mapping only. Independent test jobs, semantic review and actual manual verdicts are required.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=['fingerprint', 'check'])
    parser.add_argument('--change', required=True)
    parser.add_argument('--accept', action='store_true')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = {'fingerprint': fingerprint(root, args.change)} if args.operation == 'fingerprint' else check(root, args.change, args.accept)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError, subprocess.CalledProcessError) as error:
        print(f'Spec gate failed: {error}', file=sys.stderr)
        sys.exit(1)
