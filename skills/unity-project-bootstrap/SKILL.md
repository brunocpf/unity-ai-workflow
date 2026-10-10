---
name: unity-project-bootstrap
description: Bootstrap a Unity project foundation, then implement and validate its first playable slice when requested; track the milestones separately.
---

Use project rules and the current request. Reference names below resolve under `docs/standards/references/` (or `references/` in the kit); load only the concern being changed.

Bootstrap is foundation setup; a playable-game request also includes the first slice. Read `adoption.md` for the two completion gates. Ask only unresolved product choices, including platforms and languages; apply established technical defaults.

Use `context-efficiency.md#skill-ownership`: this skill owns project setup; available Unity CLI/package skills own tool mechanics. Do not run a second bootstrap questionnaire.

1. Inspect the workspace and chosen toolchain. Install/verify local rules, then establish source/assembly boundaries and selected dependencies (`architecture.md`, `repository.md`, `composition.md`, `dependencies.md`). Do not install every optional package.
2. Apply the shipped compiler/IDE/quality configuration and reusable tooling (`code-quality.md`, `ide.md`, `code-organization.md`, `developer-tooling.md`). Use real project commands and prove the configured gates reject faults.
3. Create only README.md, docs/project.md and docs/architecture.md by default; use `docs/standards/starter/DOCUMENT-TEMPLATES.md`. Native locks own versions.
4. Save and verify the startup/smoke authoring assets. Record foundation result links/gaps in README.md. Setup-only scope ends here; no gameplay/UI framework or completion handoff.
5. When requested, build the first playable slice with authored prefabs/data, localization and the helpers it consumes. Use the UI/asset skill for those subtasks. Verify integration, visual quality, authoring preservation and clean target-player launch (`validation.md`). Mark the slice accepted separately from foundation.

Load toolchain/profiles/API references only while selecting or qualifying that capability. Resume existing projects instead of repeating bootstrap.
