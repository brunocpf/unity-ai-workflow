"""Run the project-pinned OpenSpec CLI. Does not auto-install or upgrade packages."""
import json
import os
from pathlib import Path
import subprocess
import sys


def main():
    folder = Path(__file__).resolve().parent
    package = folder / 'node_modules/@fission-ai/openspec'
    wanted = json.loads((folder / 'package.json').read_text(encoding='utf-8'))
    actual = json.loads((package / 'package.json').read_text(encoding='utf-8'))
    if actual['version'] != wanted['devDependencies']['@fission-ai/openspec']:
        raise ValueError('OpenSpec version mismatch; run npm ci in tooling/specs')
    node = os.environ.get('WORKFLOW_NODE', 'node')
    version = subprocess.check_output([node, '--version'], text=True).strip().lstrip('v')
    if version != wanted['engines']['node']:
        raise ValueError(f'Node {wanted["engines"]["node"]} required, found {version}; select the pinned runtime')
    env = dict(os.environ, OPENSPEC_TELEMETRY='0', DO_NOT_TRACK='1')
    return subprocess.call([node, str(package / 'bin/openspec.js'), *sys.argv[1:]],
                           cwd=folder.parents[1], env=env)


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError) as error:
        print(f'OpenSpec setup error: {error}', file=sys.stderr)
        sys.exit(2)
