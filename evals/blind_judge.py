"""Blind file-level grading for `claude plugin eval` runs kept with --keep-temp.

The eval's own llm graders see either the written-file list or an elided trace,
never the full file contents. This judges each kept workspace's files directly,
one rubric item at a time, without telling the judge which arm produced them.

Usage: python3 evals/blind_judge.py <aggregate-result.json> [--votes 3] [-j 4]
Run `chmod 700 <run dir> <run dir>/sealed` on kept runs first (eval prints how).
"""
from pathlib import Path
import argparse
import concurrent.futures
import json
import random
import re
import subprocess
import sys

HERE = Path(__file__).resolve().parent
FIXTURE = HERE / 'fixtures' / 'minimal-project'
TEXT = {'.cs', '.asmdef', '.asmref', '.uxml', '.uss', '.tss', '.json', '.md', '.yml', '.yaml',
        '.rsp', '.txt', '.editorconfig', '.props', '.targets', '.xml', '.gitignore', '.gitattributes'}
# Files copied verbatim by the kit installer, not written for this task.
KIT_COPIES = re.compile(r'^(docs/standards/|\.agents/|\.claude/|\.codex/|\.unity-workflow/|AGENTS\.md$|CLAUDE\.md$)')
MAX_CHARS = 180_000


def rubric(case_dir):
    text = (case_dir / 'case.yaml').read_text(encoding='utf-8')
    block = re.search(r'type: llm\n(?:    .*\n)*?    criteria: \|\n((?:      .*\n?)+)', text).group(1)
    lines = [line[6:] for line in block.splitlines()
             if not line.strip().startswith(('Evidence is the run trace', 'Fail if any'))]
    # Each criterion is scored on its own here, so drop the all-or-nothing framing.
    preamble = [l.replace(' Pass only if ALL of these hold:', '') for l in lines if not re.match(r'\d+\.', l)]
    return [l for l in lines if re.match(r'\d+\.', l)], preamble


def bundle(workspace):
    parts, total = [], 0
    for path in sorted(p for p in workspace.rglob('*') if p.is_file()):
        rel = path.relative_to(workspace).as_posix()
        if KIT_COPIES.match(rel) or (path.suffix or path.name) not in TEXT:
            continue
        original = FIXTURE / rel
        content = path.read_text(encoding='utf-8', errors='replace')
        if original.is_file() and original.read_text(encoding='utf-8') == content:
            continue
        status = 'modified' if original.is_file() else 'new'
        chunk = f'===== {rel} ({status}) =====\n{content}\n'
        if total + len(chunk) > MAX_CHARS:
            parts.append(f'===== {rel} (omitted: size budget reached) =====\n')
            continue
        parts.append(chunk)
        total += len(chunk)
    return ''.join(parts)


def judge(task, criteria, preamble, files):
    numbered = '\n'.join(criteria)
    prompt = f"""You are reviewing one submission for a Unity programming task. Grade only the files below.

TASK GIVEN TO THE DEVELOPER:
{task}

FILES THE DEVELOPER CREATED OR CHANGED (unchanged starter files are omitted):
{files or '(none)'}

{chr(10).join(preamble)}
Decide each numbered criterion independently, PASS or FAIL, based only on what the files show:
{numbered}

Reply with JSON only: {{"criteria": [{{"id": 1, "pass": true, "reason": "<one sentence>"}}, ...]}}"""
    out = subprocess.run(['claude', '-p', '--model', 'sonnet', '--tools', ''], input=prompt,
                         capture_output=True, text=True, timeout=600).stdout
    data = json.loads(re.search(r'\{.*\}', out, re.S).group(0))
    return {int(c['id']): (bool(c['pass']), c.get('reason', '')) for c in data['criteria']}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('aggregate')
    parser.add_argument('--votes', type=int, default=3)
    parser.add_argument('-j', type=int, default=4)
    args = parser.parse_args()
    result = json.loads(Path(args.aggregate).read_text(encoding='utf-8'))

    jobs = []
    for case in result['cases']:
        case_dir = Path(result['suite']['root']) / case['dir']
        if 'focus: trace' not in (case_dir / 'case.yaml').read_text(encoding='utf-8'):  # answer-only cases
            continue
        criteria, preamble = rubric(case_dir)
        for arm, runs in case['arms'].items():
            for index, run in enumerate(runs):
                workspace = Path(run['tracePath']).parents[1] / 'sealed' / 'home' / 'cwd'
                if not workspace.is_dir():
                    print(f'skip {case["name"]} {arm} #{index}: no kept workspace at {workspace}', file=sys.stderr)
                    continue
                files = bundle(workspace)
                for vote in range(args.votes):
                    jobs.append((case['name'], arm, index, vote, case['promptMarkdown'], criteria, preamble, files))
    random.shuffle(jobs)  # interleave arms so ordering can't leak which is which

    verdicts = {}
    with concurrent.futures.ThreadPoolExecutor(args.j) as pool:
        futures = {pool.submit(judge, *job[4:]): job for job in jobs}
        for future in concurrent.futures.as_completed(futures):
            name, arm, index, vote, *_ = futures[future]
            try:
                verdicts.setdefault((name, arm, index), []).append(future.result())
            except Exception as error:  # a failed vote is dropped, not scored as a fail
                print(f'vote failed {name} {arm} #{index}: {error}', file=sys.stderr)

    report = {}
    for (name, arm, index), votes in sorted(verdicts.items()):
        ids = sorted({i for vote in votes for i in vote})
        majority = {i: sum(v.get(i, (False, ''))[0] for v in votes) * 2 > len(votes) for i in ids}
        reasons = {i: [v[i][1] for v in votes if i in v] for i in ids}
        score = sum(majority.values()) / len(ids) if ids else 0.0
        report.setdefault(name, {}).setdefault(arm, []).append(
            {'run': index, 'score': score, 'criteria': majority, 'reasons': reasons, 'votes': len(votes)})

    out = Path(args.aggregate).with_name('blind-judge.json')
    out.write_text(json.dumps(report, indent=1, default=str), encoding='utf-8')
    print(f'{"CASE":22} {"WITH":>6} {"W/OUT":>6} {"Δ":>6}  per-criterion (with | without)')
    for name, arms in report.items():
        mean = {arm: sum(r['score'] for r in runs) / len(runs) for arm, runs in arms.items()}
        crit = {arm: ''.join('✓' if all(r['criteria'].get(i) for r in runs) else
                             ('~' if any(r['criteria'].get(i) for r in runs) else '✗')
                             for i in sorted(runs[0]['criteria'])) for arm, runs in arms.items()}
        w, wo = mean.get('with', 0.0), mean.get('without', 0.0)
        print(f'{name:22} {w:6.2f} {wo:6.2f} {w - wo:+6.2f}  {crit.get("with", "")} | {crit.get("without", "")}')
    print(f'Wrote {out}')


if __name__ == '__main__':
    main()
