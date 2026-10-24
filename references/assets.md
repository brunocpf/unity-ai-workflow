# Asset pipeline

```text
Brief → reference → candidate → technical cleanup → Unity import
      → look at it in the game → approved source + export
```

A generated asset is a candidate until it meets its brief in the game. Keep raw outputs and authoring files under SourceAssets. Move only approved exports into Assets/Game/Content. Keep large binary sources/exports in LFS; preserve Unity .meta files and use stable asset IDs.

Use one brief per meaningful asset or batch. Note the relevant role/style/size/budget/pivot/collider/rig/platform constraints; omit irrelevant fields. Generation/import scripts save their settings (prompt, seed, model, job ID) beside the approved sources, plus any license information the intended distribution needs. Set a generation budget and reroll limit before a batch; resume known provider jobs instead of submitting duplicates after timeouts.

### Tool routing

| Need | Starting tool | Finishing work |
|---|---|---|
| Organic prop, stylized character, complex concept mesh | Tripo from approved images | Blender cleanup and Unity import |
| Exact modular architecture, sockets, mechanical dimensions | Blender procedural modeling | UV/material authoring and export |
| Character skeleton quickly | Tripo rig-check/rig | Weight and deformation review |
| Production animation control | Blender control rig/Rigify or custom rig | Bake to a stable deform skeleton |
| Painting, concept sheets, non-pixel textures/sprites | Image generation | Surface mapping, alpha/seam/import checks |
| Pixel characters, directional animations, terrain tiles | PixelLab | Palette/frame/tile cleanup and Unity import |
| Authored particle effects | VFX Graph | Saved graph/prefab, target rendering, lifetime and budget |
| Motion exploration | Veo through Gemini API | Motion specification, animation authoring or separate mocap |
| UI icons requiring crisp scaling | Vector authoring | UI import and style integration |

For particle effects, use the [VFX Graph setup](vfx.md). Read only the chosen pipeline: [3D](assets-3d.md), [images/pixel art](assets-2d.md), [motion reference](assets-motion.md). See the conditional records in [document templates](../starter/DOCUMENT-TEMPLATES.md#conditional-records).

For game UI and its surrounding art, [art direction](ui-art-direction.md) sets the visual target and tool-selection criteria. Original or licensed assets still need to meet that target at gameplay scale.

## Production content changes

Treat importer presets, catalog schemas, skeleton/socket names and stable asset IDs as versioned contracts; changing them needs compatibility notes for dependent prefabs, clips, saves and content. Editor validators reject missing IDs/GUIDs, unresolved LFS pointers, budget overruns and incompatible skeleton/material mappings. Parallel generators write to separate candidate paths and never silently overwrite an approved asset.

Keep provider outputs locally; hosted URLs expire and regenerating rarely reproduces the same result. A transport timeout doesn't justify submitting a duplicate paid job. CI uses the committed files and pinned export scripts, never fresh generation. [Module contracts](modules.md) and [change discipline](engineering-baseline.md) also apply to content tooling.

Imported/generated media becomes usable authored content where applicable: wire saved prefab/scene/material assets and expose tuning/previews under the [Editor authoring contract](authoring.md).
