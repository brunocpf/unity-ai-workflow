# Install the workflow

Requires Python 3.10+; no pip dependencies. Use `python` instead of `python3` if that is your Windows launcher. Install into a game workspace, not this kit checkout. A Git clone or extracted release archive works. Installation is local and makes no network calls.

```sh
git clone https://github.com/brunocpf/unity-ai-workflow.git
cd unity-ai-workflow
python3 install.py install --target /path/to/game --agent both --dry-run
python3 install.py install --target /path/to/game --agent both
python3 install.py check --target /path/to/game
```

Use `--agent codex`, `--agent claude` or `--agent both`. Both is the initial default. Paths with spaces must be quoted. Commit installed files with the game so other sessions and contributors inherit the same version.

## Global entrypoints

Run `python3 install.py install-global --agent both` from a reviewed kit checkout, then `python3 install.py check-global`. `--dry-run` previews changes. `--home /temporary/home` supports isolated tests; normally omit it.

| User destination | Content |
|---|---|
| `~/.agents/skills/unity-workflow-{start,update}/` | Codex global skills |
| `~/.claude/skills/unity-workflow-{start,update}/` | Claude Code global skills |
| `~/.local/share/unity-ai-workflow/kits/<version>-<hash>/` | Complete pinned kit snapshot |
| `~/.local/share/unity-ai-workflow/global.json` | Global ownership and integrity manifest |

These two entrypoints have different names from the six project skills. Restart/open a session and invoke `unity-workflow-start` in a new workspace, or `unity-workflow-update` in an adopted game. The start skill installs local rules first; continued development uses those local rules. Neither global installation nor an update starts Unity or generates assets.

To update the global kit, fetch a reviewed upstream commit into a separate checkout and rerun `install-global` there. Its content hash selects a new cache; old caches remain, existing projects stay pinned. `check-global` checks file integrity, not upstream freshness or client discovery. Do not edit caches; global local edits/collisions block updates. Review the candidate before running its installer. Network access is the agent's explicit update step, not an installer side effect.

## Optional examples

New project installs omit the full example library. References link to the immutable release tag; core policy and starter tooling stay local. Use `install --target /game --examples all` for complete offline examples, or `update --target /game --examples all` to add them later. Adapt only needed implementations into the game. Updates preserve the installed choice; migrate an older full installation with `assess --target /game --examples none`, then `update --target /game --examples none --dry-run` and update. Locally modified managed examples block removal. Global caches remain complete, so the reviewed kit is also available offline there.

## What is installed

| Destination in the game | Purpose |
|---|---|
| `.agents/skills/unity-*/` | Codex skill discovery, when selected |
| `.claude/skills/unity-*/` | Claude Code skill discovery, when selected |
| `docs/standards/{references,starter}/` | Local policy and reusable configuration/tooling |
| `docs/standards/examples/` | Optional complete offline example pack |
| `docs/standards/PROJECT-RULES.md` | Shared workflow rules |
| `AGENTS.md` | Small managed routing block; existing content retained |
| `CLAUDE.md` | Managed imports of AGENTS.md and shared rules, for Claude |
| `.unity-workflow/installation.json` | Version, source revision when available, clients and installed hashes |

The six skill sources are canonical under this repository's `skills/`; installation copies them into the selected discovery directories without symlinks. Both clients use the same shared standards. A skill folder copied alone is not a complete installation.

The installer does **not** create Unity assets, modify Packages/ProjectSettings, apply the starter EditorConfig to game code, provision hooks/CI credentials, install MCP servers or spend generation credits. Those are foundation or feature tasks. Installing instructions does not authorize running bootstrap. Reference and example files are passive source material under docs, not imported Unity content.

## Use after installation

Start the client in the game workspace. For setup only: “Bootstrap the foundation for [game brief].” For both milestones: “Bootstrap the foundation, then implement and validate the first playable slice for [brief].” Subsequent requests can simply describe changes. See [milestone scope](references/adoption.md#milestones-and-request-scope).

Codex discovers repo skills in `.agents/skills/`; Claude Code uses `.claude/skills/`. The standard `SKILL.md` sources are shared. Other agents may read the standards, but their discovery/install behavior is not certified here. [Codex skills](https://learn.chatgpt.com/docs/build-skills), [Claude skills](https://code.claude.com/docs/en/skills).

Claude's `@` imports make shared rules explicit even when automatic AGENTS.md loading is unavailable or an existing CLAUDE.md takes precedence. Project-specific rules stay outside managed markers and deviations belong in ADRs. [Claude instruction imports](https://code.claude.com/docs/en/memory#share-one-file-with-other-coding-tools).

## Verify discovery separately

`check` verifies installed hashes, expected paths and core dependency presence. UTF-8 text hashes normalize CRLF/LF for cross-platform Git checkouts; binary hashes remain byte-exact. Unchanged content retains its existing line endings. It does not execute a model, test Unity, or prove skill invocation. Restart the client if newly installed skills do not appear.

- **Codex:** confirm all six `unity-*` skills in the skill picker (or app-server `skills/list` for this workspace), then invoke `$unity-project-bootstrap` with a read-only request to explain the two milestones.
- **Claude Code:** confirm all six `/unity-*` commands, use `/context` to inspect the instruction imports, then invoke `/unity-project-bootstrap` with the same read-only request.
- Verify the response uses local standards and does not create a Unity project. Global skills with the same names can shadow or duplicate project skills; remove or rename the conflicting installation after reviewing ownership. Client settings that disable skills/instructions also prevent discovery.

See [client evidence](verification/client-compatibility.md) for what was actually tested. Asset tools and MCP connections remain separate capabilities; the agent must inspect available tools and report missing required providers rather than invent their availability.

## Safe updates

Choose a reviewed kit tag or commit in a separate kit checkout; updating the checkout does not update any game automatically. Version is in kit.json; the installed payload hash identifies exact content, including changes made before a release. Source revision is provenance, not a promise that the source checkout was clean.

```sh
python3 install.py assess --target /path/to/game
python3 install.py update --target /path/to/game --dry-run
python3 install.py update --target /path/to/game
python3 install.py check --target /path/to/game
```

Follow the [applicability review](references/workflow-updates.md) before applying: inspect changed requirements and project code/pins, record apply/defer/not-applicable/migration decisions, then validate affected boundaries. `assess` is read-only; hashes cannot establish semantic compatibility.

Updates retain the existing clients; `--agent both` adds the other client. They do not uninstall adapters. Repeating install/update with identical inputs is a no-op. Review the game's diff before committing the upgrade.

The installer preflights every managed path. Unmanaged collisions, missing owned files, edited shared standards/skills or changed routing blocks stop the entire plan without writing content. Text outside the AGENTS.md/CLAUDE.md blocks and unrelated project files is preserved. Unchanged files removed upstream are removed; modified ones conflict. Symlinked managed paths are rejected.

For a conflict, retain the local work in Git/backup, compare the incoming kit file, and move project-specific deviations into project rules/ADRs or reconcile the managed file explicitly. Restore the previous installed version or use the exact incoming content, then rerun the dry run. There is no force-overwrite switch. Earlier manual installations may need this reconciliation before the installer can adopt ownership.

Writes use atomic file replacement and rollback on ordinary write exceptions, with the manifest written last. This is not a filesystem-wide transaction: after process termination/power loss, inspect the diff, restore the interrupted changes from Git, then retry. Remove a stale `.unity-workflow/install.lock` only after confirming no installer is running. Do not edit managed files concurrently with installation.

## Maintain the kit

```sh
python3 -m unittest discover -s tests -v
python3 tools/check_kit.py
```

Installer regression tests run in disposable workspaces and exercise conflicts, preservation, update/removal, symlinks, dry runs and rollback. CI runs these checks on Linux, macOS and Windows. Client discovery is a separately recorded integration check; a filesystem test is not a client acceptance result.

## OpenSpec process activation (0.3)

Global/project workflow installation still only installs passive instructions. Requested foundation setup or an authorized existing-project workflow migration activates [OpenSpec](references/openspec-setup.md): Node 24.15.0, OpenSpec 1.13.2 with a locked npm graph, the unity-game schema, selected-client integrations and an evidence-mapping gate. Existing projects preserve ongoing work and migrate behavioral authority incrementally. CI must still run real game tests; the structural evidence gate cannot establish correctness or a user's playtest verdict.

Maintainer CLI integration check (requires the pinned Node/npm and network for npm ci): `python3 tools/check_openspec_integration.py`. It uses disposable synthetic fixtures, not a Unity player or a model-generated feature.

Full 0.4 adoption also updates project-owned OpenSpec helpers and consolidates docs; follow the [migration](references/upgrades/lean-0.4.0.md). Installer success alone is not adoption.

For 0.4.1, reconcile project-owned instruction routing using the [skill ownership migration](references/upgrades/skill-ownership-0.4.1.md). Generated OpenSpec integrations and optional Unity plugins remain separately owned; the installer does not rewrite them.
