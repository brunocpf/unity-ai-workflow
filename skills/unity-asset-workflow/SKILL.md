---
name: unity-asset-workflow
description: Generate, prepare or import 3D, texture, sprite, pixel-art, particle-effect or motion-reference assets for this Unity workflow.
---

Use project rules and the active OpenSpec change. Reference names below resolve under `docs/standards/references/` (or `references/` in the kit); load only the concern being changed.

Author assets for the current game/visual target; generate only needed content and respect the agreed budget. Read `assets.md` for ownership/provenance, then one applicable pipeline: `assets-2d.md`, `assets-3d.md`, `assets-motion.md` or `vfx.md`.

1. Clarify unresolved appearance, dimensions, animation behavior or paid-generation choices. Use the existing art direction and a compact asset/batch brief; don't create a document per incidental asset.
2. Use the selected image/PixelLab/Tripo/Blender tools and their relevant skills. Request real transparency/alpha explicitly where needed—never a painted checkerboard. Save accepted source outputs and generation metadata; do not depend on expiring URLs or regenerating identical hosted output.
3. Import through the selected Unity profile, preserve GUIDs and authored edits, and verify scale/pivots/alpha/materials/rigs/clips/budgets as applicable. Factories consume editable authored assets.
4. Inspect in-game results under actual lighting, motion, framing and target scale. Iterate against the visual target; technical validity alone is insufficient.
5. Keep machine provenance beside source assets and link it from the current change's checks. Update only the owning brief/registry when decisions change; no duplicate asset completion report.
