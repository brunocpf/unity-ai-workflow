---
name: unity-feature-workflow
description: Implement a bounded gameplay or application feature in a project using this kit; route UI and asset work to their focused references.
---

Resolve references under `docs/standards/references/` in an adopted project, or `references/` at the supplied kit root. Read only the files listed for the current operation. Follow applicable project AGENTS.md and the feature/asset contract.

Apply `clarification.md` when behavior, scope or consequential choices are unclear; preserve previous answers and continue independent work. Read `localization.md` when adding/changing player-facing text, language settings or localized content.

Read `architecture.md`; add `modules.md` for public/cross-module changes and `reliability.md` for storage/network/failure contracts; read `reactive.md` when changing state streams or async behavior. Read `authoring.md` when changing scenes, prefab spawning, tuning definitions or generators; runtime factories consume authored assets by default. Read `dependencies.md` only when choosing/changing packages and `utilities.md` when adding shared infrastructure.

Implement the feature's next playable acceptance slice without weakening project standards. Keep existing approved profile exceptions. For UI work use the UI skill and the project's visual target; new/substantial visual work follows `ui-art-direction.md`. For art use the asset skill/reference. Follow `code-organization.md` for owned C# organization and complete quality coverage. Run changed-boundary checks from `validation.md`, record behavior/evidence and update the affected feature contract. Do not turn a local feature into a template/toolchain overhaul.
