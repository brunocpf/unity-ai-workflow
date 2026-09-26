"""Offline documentation/configuration/skill checks; not Unity or client acceptance."""
from pathlib import Path
import json
import os
import re
import sys
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
errors = []
counts = {'links': 0, 'json': 0, 'xml': 0, 'skills': 0}


def headings(path):
    found, repeats = set(), {}
    content = re.sub(r'^```.*?^```\s*$', '', path.read_text(encoding='utf-8'), flags=re.S | re.M)
    for title in re.findall(r'^#{1,6} (.+)$', content, re.M):
        slug = re.sub(r'[^\w\- ]', '', title.lower().strip().rstrip('#').strip()).replace(' ', '-')
        count = repeats.get(slug, 0)
        repeats[slug] = count + 1
        found.add(slug if count == 0 else f'{slug}-{count}')
    return found


for folder, dirs, names in os.walk(root):
    dirs[:] = [d for d in dirs if d not in {'.git', 'bin', 'obj', '__pycache__', '.venv', 'node_modules'}]
    for name in names:
        path = Path(folder) / name
        try:
            if path.suffix in ('.json', '.asmdef'):
                json.loads(path.read_text(encoding='utf-8'))
                counts['json'] += 1
            if path.suffix in ('.uxml', '.csproj', '.props', '.targets'):
                tree = ET.parse(path)
                counts['xml'] += 1
                if path.suffix == '.uxml':
                    for node in tree.iter():
                        src = node.get('src', '')
                        if node.tag.rsplit('}', 1)[-1] == 'Style' and src and not urlsplit(src).scheme:
                            assert (path.parent / src).exists(), f'Missing stylesheet {src}'
            if path.suffix == '.uss':
                content = re.sub(r'/\*.*?\*/', '', path.read_text(encoding='utf-8'), flags=re.S)
                assert content.count('{') == content.count('}'), 'Unbalanced USS braces'
            if path.suffix == '.py':
                compile(path.read_text(encoding='utf-8'), str(path), 'exec')
            if path.suffix == '.md':
                content = re.sub(r'^```.*?^```\s*$', '', path.read_text(encoding='utf-8'), flags=re.S | re.M)
                for link in re.findall(r'\[[^\]]*\]\((<[^>]+>|[^\s)]+)\)', content):
                    parsed = urlsplit(unquote(link.strip('<>')))
                    if parsed.scheme or parsed.netloc:
                        continue
                    counts['links'] += 1
                    target = path.parent / parsed.path if parsed.path else path
                    assert target.exists(), f'Missing link {link}'
                    if parsed.fragment and target.suffix == '.md':
                        assert parsed.fragment in headings(target), f'Missing anchor {link}'
        except (AssertionError, ValueError, OSError, ET.ParseError, SyntaxError) as error:
            errors.append(f'{path.relative_to(root)}: {error}')

if (root / 'kit.json').exists():
    metadata = json.loads((root / 'kit.json').read_text(encoding='utf-8'))
    for folder, name in [('skills', n) for n in metadata['skills']] + [('global', n) for n in metadata.get('global_skills', [])]:
        skill = root / folder / name / 'SKILL.md'
        text = skill.read_text(encoding='utf-8')
        front = text.split('---', 2)
        if len(front) != 3 or not re.search(r'^name: ' + re.escape(name) + r'$', front[1], re.M) or not re.search(r'^description: .+', front[1], re.M):
            errors.append(f'Invalid skill metadata: {name}')
        counts['skills'] += 1
print(json.dumps({'counts': counts, 'errors': errors}, indent=2))
sys.exit(bool(errors))
