---
name: unity-toolchain-workflow
description: Update the project's workflow kit, or choose/upgrade Unity editors, packages, compiler/analyzer configuration and library defaults for this workflow.
---

Use project rules and the current request. Reference names below resolve under `docs/standards/references/` (or `references/` in the kit); load only the concern being changed.

Delegate command/package mechanics to available Unity skills using `context-efficiency.md#skill-ownership`. Inspect existing pins and setup before changing tools. Use `toolchain.md` for the CLI and Editor upgrades, `language-profiles.md` for C# versions and `dependencies.md` for package choices. A newer installed Editor doesn't mean the game should migrate.

1. Establish the requested change and target versions. Read the installed help or official documentation for affected commands/APIs; keep CLI/Editor/package pins in the project.
2. Make the change on a branch. Preserve Unity-authored assets, native locks, custom scripts and client integrations. Use `code-quality.md`, `ide.md` and `code-organization.md` when compiler/IDE/analyzer settings change.
3. Run the quality check, tests and a player build. Use `ci.md` for pipeline changes and say plainly if a target isn't supported.
4. Native locks and the installation manifest own versions. Record exceptions and their rationale in docs/architecture.md.

For kit updates, use `workflow-updates.md`.
