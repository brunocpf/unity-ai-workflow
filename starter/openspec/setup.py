"""Stage the Unity OpenSpec profile without installing packages or modifying client instructions."""
import argparse
from pathlib import Path
import shutil
import sys


def stage(source, target, dry_run=False):
    target = target.resolve()
    planned = {'openspec/config.yaml': source / 'config.yaml'}
    for folder, destination in [('schema', 'openspec/schemas/unity-game'), ('tooling', 'tooling/specs')]:
        for path in (source / folder).rglob('*'):
            if any(p in ('node_modules', '__pycache__') for p in path.parts) or path.suffix == '.pyc':
                continue
            if path.is_file():
                planned[f'{destination}/{path.relative_to(source / folder).as_posix()}'] = path
    writes = {}
    for relative, src in planned.items():
        dest = target / relative
        for path in (dest, *dest.parents):
            if path == target:
                break
            if path.is_symlink():
                raise ValueError(f'Symlink in destination: {path}')
        if dest.exists():
            if not dest.is_file() or dest.read_bytes() != src.read_bytes():
                raise ValueError(f'Existing profile differs: {relative}; reconcile it explicitly, no files changed')
        else:
            writes[dest] = src
    if not dry_run:
        created = []
        try:
            for dest, src in writes.items():
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(src, dest)
                created.append(dest)
        except Exception:
            for dest in reversed(created):
                dest.unlink()
            raise
    return len(writes)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', required=True, type=Path)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    try:
        count = stage(Path(__file__).resolve().parent, args.target, args.dry_run)
        print(f'{count} profile files {"planned" if args.dry_run else "staged"}; npm/CLI initialization and project integration remain separate.')
    except (OSError, ValueError) as error:
        print(error, file=sys.stderr)
        sys.exit(1)
