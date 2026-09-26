---
name: unity-asset-workflow
description: Generate, prepare or import 3D, texture, sprite, pixel-art, particle-effect or motion-reference assets for this Unity workflow.
---

Resolve references under `docs/standards/references/` in an adopted project, or `references/` at the supplied kit root. Read only the files listed for the current operation. Follow applicable project AGENTS.md and the feature/asset contract. Apply `clarification.md` when intent or consequential constraints are unresolved; inspect/recommend before asking, preserve approved defaults, and continue independent work.

Read `assets.md` and exactly the needed pipeline: `assets-3d.md`, `assets-2d.md`, or `assets-motion.md`. For particle effects read `vfx.md`: prefer VFX Graph, qualify the package/target and document Shuriken exceptions. Use the asset/motion brief and project art direction.

For UI or a new game's visual direction, follow `ui-art-direction.md`. Choose generation/vector/procedural work to match the visual target; tool convenience alone does not justify a simpler appearance.

Use available provider skills/tools within the task's generation budget. Preserve job identity and accepted source/export lineage. For recurring cleanup/export operations use project-owned Blender/import presets rather than repeated ad hoc edits.

Promote a candidate only after technical import checks and in-game inspection from `validation.md`. Video reference does not itself supply a skeleton or animation clip. Update the asset registry and evidence, not a new generic art manual.

Apply `spec-driven-development.md` to changed behavior and acceptance: read the affected spec/active change, preserve requirement IDs and link evidence. Scale records to the change; do not add an approval phase to already authorized work.
