---
name: unity-toolchain-workflow
description: Assess/update the project workflow kit, or choose/upgrade Unity editors, packages, compiler/analyzer configuration and library defaults for this workflow.
---

Use project rules and the current request. Reference names below resolve under `docs/standards/references/` (or `references/` in the kit); load only the concern being changed.

Delegate command/package mechanics to available Unity skills using `context-efficiency.md#skill-ownership`. Inspect existing pins and working setup before changing tools. Use `toolchain.md` for CLI discovery/readiness, `language-profiles.md` for C#/runtime compatibility and `dependencies.md` for package choices. A newer installed Editor does not authorize a game migration.

1. Establish the requested change and compatibility target. Read exact installed help/primary documentation for affected commands/APIs; keep CLI/Editor/package pins project-owned.
2. Make the scoped change with a recovery path. Preserve Unity-authored assets, native locks, custom wrappers and client integrations. Use `code-quality.md`, `ide.md` and `code-organization.md` when compiler/IDE/analyzer behavior changes.
3. Validate actual capabilities and rejection behavior, including local/CI parity where affected. Installation or configuration presence is not runtime compatibility. Use `ci.md` for pipeline changes and report unsupported targets honestly.
4. Native locks and the installation manifest own versions. Record exceptions/rationale in docs/architecture.md and results in the existing project record or final response; no separate toolchain/status ledger.

For workflow upgrades, use `workflow-updates.md` and the current migration guide. Managed standards, project-owned tooling and global entrypoints are separate installations; full adoption may require changes to all three within the authorized scope.
