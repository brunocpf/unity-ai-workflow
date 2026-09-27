---
name: unity-toolchain-workflow
description: Assess/update the project workflow kit, or choose/upgrade Unity editors, packages, compiler/analyzer configuration and library defaults for this workflow.
---

References resolve under `docs/standards/references/` (or `references/` at the kit root). Follow project rules, the active change and `context-efficiency.md`; load only sections triggered by this task. Apply `clarification.md` when intent or consequential constraints are unresolved; inspect/recommend before asking, preserve approved defaults, and continue independent work.

For kit updates, start with `workflow-updates.md`; load toolchain/package policies only if the assessed changes affect them. For Editor/CLI/compiler upgrades read `toolchain.md`; read `dependencies.md` when selecting/changing packages. Add `dependencies-optional.md` when selecting an optional library; use `profiles.md` for new target/use-case selection. Changes to repository boundaries also require `architecture.md`/`repository.md`.

Inspect native version authorities and installed CLI help. Resolve a pinned candidate in an isolated project copy/branch, respecting the user's authorized upgrade scope. Run impacted acceptance fixtures from `validation.md`, including player/AOT/render checks where relevant. Use `ci.md` for runner changes and `lifecycle.md` for reload changes.

Review incremental release notes, known issues and archive/content compatibility; load the matching note under `references/upgrades/` (or `docs/standards/references/upgrades/` after adoption). Keep historical evidence labeled by its original version and record checks not rerun. Record resolved versions, compatibility results and migration notes. Upgrade an active project's files only within scope; an installed editor upgrade is not a project migration.

Compiler/analyzer or IDE changes also follow `ide.md` and `code-organization.md`: synchronize the three compiler contexts, regenerate and repeat capability/rejection probes.

For workflow-kit updates, follow `workflow-updates.md` instead of treating the operation as an engine upgrade. Compare the candidate with the installed manifest and project implementation; record applicability and deferred migrations before applying.

Apply `spec-driven-development.md`; use `spec-evidence.md` when defining verification or delivering the increment.
