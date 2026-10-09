"""Shared checks for a delivered OpenSpec change; no whole-tree acceptance fingerprint."""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

ID = re.compile(r'^[A-Z][A-Z0-9]*-[0-9]{3,}$')
KINDS = {'automated', 'visual', 'authoring', 'playtest', 'device'}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def safe_file(root, relative):
    if not isinstance(relative, str) or not relative:
        raise ValueError('Expected a nonempty relative file path')
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
    safe_file(root, f'openspec/changes/{name}/.openspec.yaml')
    return root / 'openspec/changes' / name


def requirement_ids(folder):
    ids = set()
    for file in sorted((folder / 'specs').rglob('*.md')):
        text = safe_file(folder, file.relative_to(folder).as_posix()).read_text(encoding='utf-8')
        if '## RENAMED Requirements' in text:
            raise ValueError('Keep requirement IDs stable; use MODIFIED or explicit remove/add migration')
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


def load(root, name, refreshing=None, supplied=None):
    folder = change_dir(root, name)
    data = supplied if supplied is not None else json.loads(
        safe_file(root, f'openspec/changes/{name}/verification.json').read_text(encoding='utf-8'))
    if data.get('schema') != 2:
        raise ValueError('Expected verification schema 2; migrate active delivery explicitly; leave historical archives unchanged')
    rows, checks = data.get('requirements'), data.get('checks')
    if not isinstance(rows, list) or not rows or not isinstance(checks, dict) or not checks:
        raise ValueError('Requirements and shared checks must be nonempty')
    required, listed, used = requirement_ids(folder), set(), set()
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError('Requirement rows must be objects')
        identifier, names = row.get('id'), row.get('checks')
        if not isinstance(identifier, str) or not ID.fullmatch(identifier) or identifier in listed:
            raise ValueError('Invalid/duplicate requirement mapping')
        if not isinstance(names, list) or not names or any(not isinstance(n, str) for n in names):
            raise ValueError(f'Missing check mapping: {identifier}')
        if len(names) != len(set(names)) or not set(names) <= checks.keys():
            raise ValueError(f'Unknown/duplicate check mapping: {identifier}')
        listed.add(identifier)
        used.update(names)
    if not required <= listed or used != checks.keys():
        raise ValueError('Missing requirement mapping or unused checks')
    for key, item in checks.items():
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', key) or not isinstance(item, dict):
            raise ValueError('Invalid shared check')
        if item.get('kind') not in KINDS or not item.get('target'):
            raise ValueError(f'Invalid kind/target: {key}')
        if item['kind'] == 'automated':
            command = item.get('command')
            if not isinstance(command, list) or not command or any(not isinstance(s, str) or not s for s in command):
                raise ValueError(f'Expected command argument array: {key}')
            if 'status' in item or 'artifacts' in item:
                raise ValueError('Automated outcomes are produced by execution, not declared in verification.json')
            timeout = item.get('timeout_seconds', 600)
            if type(timeout) is not int or not 1 <= timeout <= 7200:
                raise ValueError('timeout_seconds must be 1..7200')
        else:
            if item.get('status') not in ('pending', 'pass', 'fail') or not item.get('procedure'):
                raise ValueError(f'Invalid manual verdict/procedure: {key}')
            artifacts = item.get('artifacts', [])
            if not isinstance(artifacts, list):
                raise ValueError('Manual artifacts must be a list')
            for artifact in ([] if key == refreshing else artifacts):
                path = artifact['path']
                if not path.startswith(('artifacts/', 'docs/evidence/')):
                    raise ValueError('Review artifacts must live in artifacts/ or docs/evidence/')
                content = safe_file(root, path).read_bytes()
                if not content.strip() or sha(content) != artifact.get('sha256'):
                    raise ValueError(f'Empty/modified manual artifact: {path}')
            if item['status'] == 'pass' and (not item.get('reviewer') or not item.get('reviewed_at') or not artifacts):
                raise ValueError('Passing manual review requires reviewer, time and artifacts; use record-review')
    return folder, data


def write_json_atomic(path, data):
    mode = path.stat().st_mode & 0o777
    fd, temporary = tempfile.mkstemp(prefix='.verification-', dir=path.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as output:
            json.dump(data, output, indent=2)
            output.write('\n')
        os.chmod(temporary, mode)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def record_review(root, name, key, status, reviewer, paths):
    folder, data = load(root, name, refreshing=key)
    item = data['checks'].get(key)
    if item is None or item['kind'] == 'automated' or status not in ('pass', 'fail'):
        raise ValueError('Select a declared manual check and actual pass/fail verdict')
    if not reviewer.strip() or not paths:
        raise ValueError('Actual reviewer and inspected artifacts are required')
    artifacts = []
    for path in dict.fromkeys(paths):
        if not path.startswith(('artifacts/', 'docs/evidence/')):
            raise ValueError('Review artifacts must live in artifacts/ or docs/evidence/')
        content = safe_file(root, path).read_bytes()
        if not content.strip():
            raise ValueError('Empty review artifact')
        artifacts.append({'path': path, 'sha256': sha(content)})
    item.update(status=status, reviewer=reviewer, artifacts=artifacts,
                reviewed_at=datetime.now(timezone.utc).isoformat())
    write_json_atomic(folder / 'verification.json', data)
    return {'status': 'recorded', 'check': key, 'verdict': status}


def check(root, name, accept=False):
    folder, data = load(root, name)
    if not accept:
        return {'status': 'pass', 'mode': 'mapping', 'requirements': len(data['requirements'])}
    markers = re.findall(r'^\s*-\s+\[([^]]*)\]', safe_file(folder, 'tasks.md').read_text(encoding='utf-8'), re.M)
    if not markers or any(m.strip().lower() != 'x' for m in markers):
        raise ValueError('Incomplete/empty tasks')
    for key, item in data['checks'].items():
        if item['kind'] != 'automated' and item['status'] != 'pass':
            raise ValueError(f'Unaccepted manual check: {key}')
    output = root / 'artifacts/verification'
    output.mkdir(parents=True, exist_ok=True)
    run = Path(tempfile.mkdtemp(prefix='run-', dir=output))
    try:
        revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, stderr=subprocess.DEVNULL, text=True).strip()
        dirty = bool(subprocess.check_output(['git', 'status', '--porcelain'], cwd=root, stderr=subprocess.DEVNULL, text=True).strip())
    except (OSError, subprocess.CalledProcessError):
        revision, dirty = None, None
    report = {'revision': revision, 'dirty': dirty, 'python': sys.version.split()[0], 'change': name, 'started_at': datetime.now(timezone.utc).isoformat(), 'status': 'running', 'checks': {}}
    # Reuse the bounded-output/full-log runner. No shell, cached pass or author-written command result.
    spec = importlib.util.spec_from_file_location('workflow_output', Path(__file__).with_name('ci.py'))
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    try:
        for key, item in data['checks'].items():
            if item['kind'] != 'automated':
                report['checks'][key] = item
                continue
            command = [sys.executable if arg == '{python}' else arg for arg in item['command']]
            report['checks'][key] = {'command': command, 'target': item['target'], 'status': 'running', 'log': key + '.log'}
            runner.execute(command, root, run / (key + '.log'), key, quiet=True,
                           timeout=item.get('timeout_seconds', 600))
            report['checks'][key]['status'] = 'pass'
        if load(root, name)[1] != data:
            raise ValueError("Verification definition changed during execution")
        report['status'] = 'pass'
    except (ValueError, OSError, subprocess.SubprocessError) as error:
        report['status'] = 'fail'
        report['failure'] = str(error)
        if 'key' in locals():
            report['checks'][key]['status'] = 'fail'
        raise
    finally:
        report['finished_at'] = datetime.now(timezone.utc).isoformat()
        (run / 'results.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    return {'status': 'pass', 'mode': 'delivery', 'requirements': len(data['requirements']),
            'report': str(run / 'results.json'), 'note': 'Current command results; manual verdicts still need semantic freshness review.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=['check', 'record-review'])
    parser.add_argument('--change', required=True)
    parser.add_argument('--accept', action='store_true')
    parser.add_argument('--check-id')
    parser.add_argument('--status', choices=['pass', 'fail'])
    parser.add_argument('--reviewer')
    parser.add_argument('--artifact', action='append', default=[])
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    if args.operation == 'record-review':
        if args.accept or not args.check_id or not args.status or not args.reviewer:
            parser.error('record-review requires --check-id, --status, --reviewer and --artifact')
        result = record_review(root, args.change, args.check_id, args.status, args.reviewer, args.artifact)
    else:
        if args.check_id or args.status or args.reviewer or args.artifact:
            parser.error('Review arguments apply only to record-review')
        result = check(root, args.change, args.accept)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError, subprocess.SubprocessError) as error:
        print(f'Spec gate failed: {error}', file=sys.stderr)
        sys.exit(error.returncode if isinstance(error, subprocess.CalledProcessError) and error.returncode > 0 else 1)
