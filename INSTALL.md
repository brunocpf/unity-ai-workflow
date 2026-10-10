# Install the workflow

Requires Python 3.10+. Shared mode is the default for new projects: one immutable kit snapshot per version/content hash on each machine, a committed project pin and restore helper, and ignored local links. It does not create Unity content or install planning tools. Global entrypoints are optional.

From a clean, committed kit checkout (or the provenance-bearing global cache):

```sh
python3 install.py install --target /path/to/game --agent both --dry-run
python3 install.py install --target /path/to/game --agent both
python3 install.py check --target /path/to/game
```

Select codex, claude or both. Existing projects retain their mode unless `--mode shared` or `--mode vendored` is explicit. Shared installation refuses dirty/unidentified source; commit/review a candidate first. A release archive without provenance can be vendored, or use a clean checkout of the exact commit for shared mode.

## Global entrypoints

```sh
python3 install.py install-global --agent both
python3 install.py check-global
```

Global start/update skills live in ~/.agents/skills and ~/.claude/skills. Shared projects and global entrypoints reuse the same content-hashed snapshot in ~/.local/share/unity-ai-workflow/kits/. Global updates never move project pins. `--home /temporary/home` supports isolated tests for global and shared commands. Do not edit immutable caches or automatically delete old versions; another project/worktree may still reference them.

## What is installed

| Project path | Ownership |
|---|---|
| .unity-workflow/installation.json | Committed portable pin: repository, commit, version, content hash, clients and managed routing hashes |
| .unity-workflow/restore.py | Committed standard-library restore helper |
| AGENTS.md / CLAUDE.md | Committed managed routing blocks; project text outside blocks preserved |
| .gitignore | Committed managed ignore block for generated links/local state |
| .unity-workflow/local.json | Ignored link ownership; contains machine-local paths |
| docs/standards | Ignored link to complete pinned kit |
| .agents/skills/unity-* / .claude/skills/unity-* | Ignored links for the six selected-client task skills |

Only the kit-owned six skill paths are ignored, not unrelated project skills. The pin contains no absolute machine paths. Project-specific decisions, overrides and adopted source/tooling stay outside docs/standards. That path is read-only reference material shared by all projects on the pin. Run engineering checks from project-owned scripts; game CI must not depend on this instruction cache.

## Fresh checkout and worktrees

From the game root, before starting an agent session:

```sh
python3 .unity-workflow/restore.py --fetch
```

An existing valid cache is reused offline. `--fetch` permits downloading only the locked Git commit when missing and verifies its content hash before executing the cached installer. Omit it to require offline restore. A corrupted cache is rejected, not silently repaired or upgraded; preserve edits, remove/quarantine that exact cache and restore intentionally. Never substitute the globally newest kit. Repeat restore for fresh worktrees or another machine; do not commit absolute links/local state. Restricted environments may need cache read access or vendored mode.

## Vendored option

Use `install --mode vendored` for a self-contained project. It copies standards and six skill folders into the same discovery paths, with no cache dependency. Default vendored examples are omitted, with release-pinned links; `--examples all` includes them. Updates preserve that selection. Shared mode always exposes the complete cache and does not accept `--examples`.

Conversion uses a reviewed `update --mode shared|vendored --dry-run`, then update/check. See [migration](references/upgrades/shared-cache-0.6.0.md) for Git index cleanup and conflict handling. On Windows, shared mode requires permission to create directory symlinks; a failure rolls back project changes. Choose vendored mode explicitly when symlinks are unavailable.

## Safe updates

Use a reviewed clean candidate checkout:

```sh
python3 /candidate/install.py assess --target /game
python3 /candidate/install.py update --target /game --dry-run
python3 /candidate/install.py update --target /game
python3 /candidate/install.py check --target /game
```

Assessment compares content, not semantic applicability. Shared update changes only this project's pin/links and routing; previous cache versions remain. New clients are additive. Modified managed blocks/helpers, retargeted links, corrupted caches and unmanaged replacement-directory contents block mutation. Review project-specific exceptions using [workflow updates](references/workflow-updates.md). Installer success is not adoption of changed engineering requirements.

Rollback a shared update by reverting its committed pin/helper/routing changes and running restore again. To roll back shared adoption itself, use the current installer to convert back to vendored before reverting the migration commit; never copy through a shared link. Preserve unrelated working changes.

## Verify discovery separately

`check` verifies integrity and layout, not model behavior or Unity acceptance. Open a new client session after restore/update; confirm the six project skills and that their guidance follows the project pin. Both clients document symlinked skill-folder discovery: [Codex](https://learn.chatgpt.com/docs/build-skills), [Claude](https://code.claude.com/docs/en/skills). Test actual installed client versions; filesystem checks alone are not client certification. Existing same-name personal skills can conflict with project discovery; keep global start/update names distinct from the six project skills.

## Validation

```sh
python3 -m unittest discover -s tests -v
python3 tools/check_kit.py
```

Tests cover vendored behavior, shared cache reuse, exact-pin fetching, migrations, rollback, corruption and collisions. GitHub-hosted CI runs on Linux, macOS and Windows; symlink tests report a skip if the OS disallows links. Live client discovery and game acceptance remain separate.
