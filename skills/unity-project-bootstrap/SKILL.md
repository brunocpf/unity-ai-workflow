---
name: unity-project-bootstrap
description: Set up a Unity project with this kit's architecture and tooling, then build its first playable slice when requested.
---

Use project rules and the current request. Reference names below resolve under `docs/standards/references/` (or `references/` in the kit); load only the concern being changed.

A setup request means project setup; a playable-game request also includes the first slice. Ask only unresolved product choices, including platforms and languages; apply established technical defaults.

Use `context-efficiency.md#skill-ownership`: this skill owns project setup; available Unity CLI/package skills own tool mechanics. Don't run a second bootstrap questionnaire.

1. Work through `setup-checklist.md`. It covers the toolchain check (`install.py doctor`), installing the kit, `install.py scaffold` for the fixed starter files, assemblies, the SDK build, hooks, documents and CI. Open another reference only for the decision the checklist names beside it; don't read the reference directory up front or copy starter files by hand.
2. Follow the doctor guidance for missing tools: when Unity isn't available, write the files, skip Editor verification and list the remaining commands in README.md instead of probing the machine.
3. Setup-only scope ends at the checklist's done criteria; no gameplay/UI framework ahead of need.
4. When requested, build the first playable slice (`adoption.md#first-playable-slice`) with authored prefabs/data, localization and the helpers it uses. Use the UI/asset skill for those subtasks. Test it, build and launch the player, and look at it against the visual target (`testing.md`, `ui-art-direction.md`).

Resume existing projects instead of repeating bootstrap.
