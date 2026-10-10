"""Portable shared-kit restore helper. Uses only Python's standard library."""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import urllib.request

REPOSITORY = 'https://github.com/brunocpf/unity-ai-workflow'
BASE = '.local/share/unity-ai-workflow/kits'
FOLDERS = ('references', 'starter', 'examples', 'skills', 'global', 'tools', 'verification', 'tests', '.github')
EXCLUDED = {'.git', 'bin', 'obj', '__pycache__', '.DS_Store', 'node_modules'}


def digest(data):
    try:
        data.decode('utf-8')
        if b'\0' not in data:
            data = data.replace(b'\r\n', b'\n')
    except UnicodeDecodeError:
        pass
    return hashlib.sha256(data).hexdigest()


def snapshot(source):
    paths = list(source.glob('*.md')) + list(source.glob('*.py')) + [source / 'kit.json']
    for folder in FOLDERS:
        paths.extend((source / folder).rglob('*'))
    files = {}
    for path in sorted(set(paths)):
        relative = path.relative_to(source)
        if any(p in EXCLUDED for p in relative.parts) or path.suffix == '.pyc':
            continue
        if path.is_symlink():
            raise ValueError(f'Symlink in cache source: {path}')
        if path.is_file():
            files[relative.as_posix()] = path.read_bytes()
    return files


def tree_hash(files):
    return digest(json.dumps({p: digest(d) for p, d in sorted(files.items())}, sort_keys=True).encode())


def validate_pin(pin):
    if not isinstance(pin, dict):
        raise ValueError('Invalid project pin')
    if pin.get('schema') != 2 or pin.get('mode') != 'shared' or pin.get('kit') != 'unity-ai-workflow':
        raise ValueError('Not a shared installation record')
    if pin.get('repository') != REPOSITORY:
        raise ValueError('Unrecognized kit repository')
    for key, pattern in [('version', r'\d+\.\d+\.\d+'), ('source_revision', r'[0-9a-f]{40}'), ('cache_sha256', r'[0-9a-f]{64}')]:
        if not isinstance(pin.get(key), str) or not re.fullmatch(pattern, pin[key]):
            raise ValueError(f'Invalid pin: {key}')
    if 'blocks' in pin:
        expected = {'AGENTS.md', '.gitignore'} | ({'CLAUDE.md'} if 'claude' in pin.get('agents', []) else set())
        if set(pin['blocks']) != expected or any(not re.fullmatch(r'[0-9a-f]{64}', v) for v in pin['blocks'].values()):
            raise ValueError('Invalid managed block inventory')
        if not re.fullmatch(r'[0-9a-f]{64}', pin.get('helper_sha256', '')):
            raise ValueError('Invalid helper hash')
    if not isinstance(pin.get('agents'), list) or not pin['agents'] or any(a not in ('codex', 'claude') for a in pin['agents']):
        raise ValueError('Invalid clients')
    if not isinstance(pin.get('skills'), list) or not pin['skills'] or any(not isinstance(s, str) or not re.fullmatch(r'unity-[a-z0-9-]+', s) for s in pin['skills']):
        raise ValueError('Invalid skills')


def cache_path(home, pin):
    validate_pin(pin)
    home = home.expanduser().resolve()
    path = home / BASE / (pin['version'] + '-' + pin['cache_sha256'])
    for parent in [path, *path.parents]:
        if parent.is_symlink():
            raise ValueError(f'Symlink in cache location: {parent}')
    return path


def verify_cache(path, pin):
    validate_pin(pin)
    if not path.is_dir() or path.is_symlink():
        raise ValueError('Pinned cache missing; run the project restore helper with --fetch')
    files = snapshot(path)
    # Reject additions outside snapshot folders too; caches are immutable.
    actual = {p.relative_to(path).as_posix() for p in path.rglob('*')
              if p.is_file() and '__pycache__' not in p.parts}
    if actual != set(files) or any(p.is_symlink() for p in path.rglob('*')):
        raise ValueError('Unexpected files/links in pinned cache')
    if tree_hash(files) != pin['cache_sha256']:
        raise ValueError('Pinned cache content changed; preserve edits and restore explicitly')
    meta = json.loads(files['kit.json'])
    if meta['version'] != pin['version'] or meta['skills'] != pin['skills']:
        raise ValueError('Cache metadata disagrees with project pin')
    for name in ['install.py', 'shared_install.py', 'cache_restore.py', 'PROJECT-RULES.md']:
        if name not in files:
            raise ValueError(f'Missing cache entry: {name}')
    return files


def ensure_cache(home, pin, source=None, fetch=False):
    path = cache_path(home, pin)
    if path.exists():
        verify_cache(path, pin)
        return path
    if source is None and not fetch:
        raise ValueError('Pinned cache missing. Run python3 .unity-workflow/restore.py --fetch; no newer version is substituted.')
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.restore-', dir=path.parent) as temp:
        staging = Path(temp) / 'kit'
        staging.mkdir()
        if source is not None:
            files = snapshot(source)
        else:
            url = REPOSITORY + '/archive/' + pin['source_revision'] + '.tar.gz'
            with urllib.request.urlopen(url, timeout=120) as response:
                data = response.read()
            files = {}
            with tarfile.open(fileobj=io.BytesIO(data), mode='r:gz') as archive:
                for member in archive.getmembers():
                    parts = member.name.split('/')[1:]
                    if not parts or member.isdir():
                        continue
                    if not member.isfile() or any(x in ('', '.', '..') or ':' in x for x in parts) or member.name.startswith('/') or '\\' in member.name:
                        raise ValueError('Unsafe release archive member')
                    relative = '/'.join(parts)
                    # Match the kit snapshot, not unrelated repository files.
                    if any(x in EXCLUDED for x in parts) or relative.endswith('.pyc'):
                        continue
                    if not (parts[0] in FOLDERS or (len(parts) == 1 and (relative.endswith(('.md', '.py')) or relative == 'kit.json'))):
                        continue
                    files[relative] = archive.extractfile(member).read()
        if tree_hash(files) != pin['cache_sha256']:
            raise ValueError('Source/download does not match the exact project pin')
        for name, data in files.items():
            dest = staging / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
        verify_cache(staging, pin)
        try:
            os.rename(staging, path)
        except OSError:
            if not path.exists():
                raise
            verify_cache(path, pin)  # Another restore may have completed first.
    return path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument('--home', type=Path, default=Path.home())
    parser.add_argument('--fetch', action='store_true', help='Allow fetching only the locked commit when absent')
    args = parser.parse_args()
    try:
        root = args.target.resolve()
        pin = json.loads((root / '.unity-workflow/installation.json').read_text())
        cache = ensure_cache(args.home.expanduser().resolve(), pin, fetch=args.fetch)
        return subprocess.call([sys.executable, str(cache / 'install.py'), 'restore', '--target', str(root), '--home', str(args.home.expanduser().resolve())])
    except (ValueError, OSError, KeyError, tarfile.TarError) as error:
        print(f'Error: {error}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
