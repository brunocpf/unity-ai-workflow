"""Convert one active schema-1 verification map to schema 2; no inferred commands/verdicts."""
import argparse
import importlib.util
import json
from pathlib import Path
import sys


def convert(data, command, target):
    if data.get('schema') == 2:
        return data  # Already adopted; do not refresh verdicts.
    if data.get('schema') != 1 or not isinstance(data.get('requirements'), list):
        raise ValueError('Expected schema-1 verification')
    if not isinstance(command, list) or not command or any(not isinstance(a, str) or not a for a in command) or not target:
        raise ValueError('Supply the reviewed project check command as a JSON argument array and its target')
    checks, rows = {}, []
    for row in data['requirements']:
        names = []
        for kind in row.get('required_kinds', []):
            if kind not in ('automated', 'visual', 'authoring', 'playtest', 'device'):
                raise ValueError(f'Unknown review kind: {kind}')
            key = 'tests' if kind == 'automated' else f'{kind}-{row["id"].lower()}'
            names.append(key)
            if kind == 'automated':
                checks[key] = {'kind': kind, 'command': command, 'target': target}
            else:
                previous = [e for e in row.get('evidence', []) if e.get('kind') == kind]
                procedures = list(dict.fromkeys(e.get('command_or_procedure', '') for e in previous))
                checks[key] = {'kind': kind, 'status': 'pending',
                               'procedure': '; '.join(p for p in procedures if p) or f'Review {row["id"]} {kind}',
                               'target': '; '.join(dict.fromkeys(e.get('target', '') for e in previous)) or target}
        rows.append({'id': row['id'], 'checks': names})
    return {'schema': 2, 'requirements': rows, 'checks': checks}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--change', required=True)
    parser.add_argument('--command-json', required=True)
    parser.add_argument('--target', required=True)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    if args.change.startswith('archive/'):
        raise ValueError('Do not rewrite historical archives; migrate the active delivery')
    root = Path(__file__).resolve().parents[2]
    spec = importlib.util.spec_from_file_location('gate', Path(__file__).with_name('check.py'))
    gate = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gate)
    folder = gate.change_dir(root, args.change)
    path = gate.safe_file(folder, 'verification.json')
    original = path.read_text(encoding='utf-8')
    data = json.loads(original)
    if data.get('schema') == 2:
        gate.load(root, args.change)
        print('Already schema 2; unchanged')
        return
    converted = convert(data, json.loads(args.command_json), args.target)
    output = json.dumps(converted, indent=2) + '\n'
    if args.apply:
        gate.load(root, args.change, supplied=converted)
        if path.read_text(encoding='utf-8') != original:
            raise ValueError('Verification changed while planning; rerun migration')
        gate.write_json_atomic(path, converted)
        print('Converted active mapping; manual checks remain pending. Run actual delivery checks.')
    else:
        print(output, end='')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError) as error:
        print(f'Migration failed: {error}', file=sys.stderr)
        sys.exit(1)
