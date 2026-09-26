---
name: unity-project-bootstrap
description: Bootstrap a Unity project foundation, then implement and validate its first playable slice when requested; track the milestones separately.
---

Resolve references under `docs/standards/references/` in an adopted project, or `references/` at the supplied kit root. Read only the files listed for the current operation. Follow applicable project AGENTS.md and the feature/asset contract.

A game brief plus the kit entrypoint is sufficient. Apply adoption.md's milestone scope: bootstrap alone means Foundation ready; a playable-game or end-to-end trial request includes First slice accepted unless limited to setup. Complete authorized milestones without an extra approval stop. Apply the bootstrap contract; do not ask the user to restate technical defaults. Apply `clarification.md` to unresolved product choices, including target platforms and the primary acceptance target, before dependent work; record answers and pending decisions. Read `localization.md` for first-slice text, supported-language intake and native UITK localization.

Read `engineering-baseline.md`, `adoption.md`, `architecture.md`, `repository.md`, `toolchain.md`; select packages/profile using `dependencies.md` and `profiles.md`.

Apply `authoring.md`, `composition.md`, `code-quality.md`, `ide.md`, `code-organization.md` and `developer-tooling.md` during setup; record actual baseline evidence/gaps. A small first slice retains the full architectural standard.

Establish the actual project and native version locks. Use the kit installer for the selected client(s), or verify an existing installation; preserve its managed root instruction blocks. Apply the relevant starter configuration and create project docs from adoption.md. Installation alone is not foundation completion. Before ending bootstrap, ensure AGENTS.md, docs/index.md and the local standard/skill routes resolve without the original kit path. Use available Unity CLI/project-creation skills; inspect pinned help rather than assuming commands.

Implement the setup validation entrypoints (`ci.md`, `validation.md`). Run adoption.md's foundation completion checks and record results before claiming Foundation ready. For setup-only scope, stop with a concise handoff and deferred slice checks; do not generate gameplay or polished UI.

When milestone 2 is in scope, implement one playable acceptance slice and the helpers it consumes (`utilities.md`). If it includes UI, apply `ui-art-direction.md` and the rendering/motion defaults in `ui-advanced.md` before expanding screens/levels; the slice includes a representative screen realized against a concrete visual target. Use `ui-construction.md`, `ui-binding.md` and `lifecycle.md` for implementation. Extend those validation entrypoints for gameplay integration and prove clean-checkout build/launch before tagging a template. Report technical and visual acceptance separately. Record unresolved provisioning/runtime gaps; this kit is not already an implemented template.

Apply `spec-driven-development.md` to changed behavior and acceptance: read the affected spec/active change, preserve requirement IDs and link evidence. Scale records to the change; do not add an approval phase to already authorized work.
