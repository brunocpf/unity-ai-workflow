---
name: unity-project-bootstrap
description: Set up a Unity project with this kit's architecture and tooling, then build its first playable slice when requested.
---

Use project rules and the current request. Reference names below resolve under `docs/standards/references/` (or `references/` in the kit); load only the concern being changed.

A setup request means project setup; a playable-game request also includes the first slice. Read `adoption.md`. Ask only unresolved product choices, including platforms and languages; apply established technical defaults.

Use `context-efficiency.md#skill-ownership`: this skill owns project setup; available Unity CLI/package skills own tool mechanics. Don't run a second bootstrap questionnaire.

1. Inspect the workspace and chosen toolchain. Install the kit, then set up source/assembly boundaries and selected dependencies (`architecture.md`, `repository.md`, `composition.md`, `dependencies.md`). Don't install every optional package.
2. Apply the compiler/IDE/quality configuration, hooks and CI (`code-quality.md`, `ide.md`, `code-organization.md`, `developer-tooling.md`, `ci.md`). Put the real commands in README.md and make sure they run.
3. Create only README.md, docs/project.md and docs/architecture.md by default; use `docs/standards/starter/DOCUMENT-TEMPLATES.md`. Native locks own versions.
4. Save the startup scene and assets the project needs to open and run. Setup-only scope ends here; no gameplay/UI framework ahead of need.
5. When requested, build the first playable slice with authored prefabs/data, localization and the helpers it uses. Use the UI/asset skill for those subtasks. Test it, build and launch the player, and look at it against the visual target (`testing.md`, `ui-art-direction.md`).

Load toolchain/profile/API references only while choosing that capability. Resume existing projects instead of repeating bootstrap.
