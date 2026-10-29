# Install the kit

Requires Python 3.9+. The installer copies the standards and task skills into a game project. It doesn't create Unity content or install planning tools. Global entrypoints are optional.

From a kit checkout (or the global cache):

```sh
python3 install.py install --target /path/to/game --agent both --dry-run
python3 install.py install --target /path/to/game --agent both
python3 install.py check --target /path/to/game
```

Select `codex`, `claude` or `both`. Source examples aren't copied by default; their links point at the matching kit release on GitHub. Add `--examples all` to copy them into the project too. Updates keep that choice.

## Toolchain report and starter tooling

```sh
python3 install.py doctor --target /path/to/game
python3 install.py scaffold --target /path/to/game --dry-run
python3 install.py scaffold --target /path/to/game --profile csharp9
```

`doctor` reports Python, Git, Git LFS, dotnet, the Unity CLI, Hub editors and package-host reachability in one call, with guidance for anything missing. `scaffold` copies the fixed-destination starter files (EditorConfig, Git attributes/ignore, Husky hook, VS Code settings, tooling/dotnet, tooling/ide, tooling/quality) and a `csc.rsp` beside each asmdef under Assets/Game. It never overwrites: files that already exist with different content are listed under `merge`. These copies are project-owned, not installer-managed; rerun `scaffold` after adding asmdefs. Choose `csharp14` only when the pinned Editor supports it ([language profiles](references/language-profiles.md)).

## Global entrypoints

```sh
python3 install.py install-global --agent both
python3 install.py check-global
```

The global start/update skills live in ~/.agents/skills and ~/.claude/skills, backed by a versioned kit copy in ~/.local/share/unity-ai-workflow/kits/. Global updates never change existing projects. `--home /temporary/home` lets you test global commands in isolation. Don't edit the cached copies; another skill may still reference them.

## What is installed

| Project path | Purpose |
|---|---|
| .unity-workflow/installation.json | Installed kit version, clients and file hashes (committed) |
| AGENTS.md / CLAUDE.md | Managed routing block; your text outside the block is preserved |
| docs/standards/ | Kit references, starter files and optional examples |
| .agents/skills/unity-* / .claude/skills/unity-* | The kit's task skills for the selected clients |

Commit all of these. Project-specific decisions, overrides and adopted tooling stay outside docs/standards; treat that folder as read-only reference material managed by the installer. Game CI runs the project's own scripts and doesn't depend on docs/standards.

## Safe updates

Use a candidate kit checkout:

```sh
python3 /candidate/install.py assess --target /game
python3 /candidate/install.py update --target /game --dry-run
python3 /candidate/install.py update --target /game
python3 /candidate/install.py check --target /game
```

`assess` compares file content; it doesn't decide what applies to your project. Locally edited managed files block the update until you merge or restore them, and nothing is written in that case. New clients are added, never removed. See [updating the kit](references/workflow-updates.md) for deciding what applies.

To roll back, revert the update commit.

## Client discovery

`check` confirms the installed files are intact. Open a new client session after installing or updating and confirm the project skills appear. Both clients document project skill folders: [Codex](https://learn.chatgpt.com/docs/build-skills), [Claude](https://code.claude.com/docs/en/skills). An existing personal skill with the same name can shadow a project skill; the global start/update names are deliberately distinct from the project skills.
