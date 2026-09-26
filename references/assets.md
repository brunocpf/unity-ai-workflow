# Asset acceptance contract

```text
Brief → reference → candidate → technical cleanup → Unity import
      → visual/gameplay validation → accepted source + export + provenance
```

A generated asset is a candidate until it meets its brief in the game. Keep raw outputs and authoring files under SourceAssets. Promote only accepted exports into Assets/Game/Content. Keep large binary sources/exports in LFS or a versioned artifact store; preserve Unity .meta files and use stable asset IDs.

Every asset brief specifies role, style references, physical size, camera distance, silhouette, polygon/texture/material budgets, pivot, collider needs, skeleton/animation requirements, target platforms, and acceptance views. Include rights/provenance records needed for the intended distribution. Set a generation budget and reroll limit before a batch; resume known provider jobs instead of submitting duplicates after timeouts.

### Tool routing

| Need | Starting tool | Finishing work |
|---|---|---|
| Organic prop, stylized character, complex concept mesh | Tripo from approved images | Blender cleanup and Unity validation |
| Exact modular architecture, sockets, mechanical dimensions | Blender procedural modeling | UV/material authoring and export |
| Character skeleton quickly | Tripo rig-check/rig | Weight and deformation review |
| Production animation control | Blender control rig/Rigify or custom rig | Bake to a stable deform skeleton |
| Painting, concept sheets, non-pixel textures/sprites | Image generation | Surface mapping, alpha/seam/import validation |
| Pixel characters, directional animations, terrain tiles | PixelLab | Palette/frame/tile cleanup and Unity import |
| Motion exploration | Veo through Gemini API | Motion specification, animation authoring or separate mocap |
| UI icons requiring crisp scaling | Vector authoring | UI import and style integration |

Read only the chosen pipeline: [3D](assets-3d.md), [images/pixel art](assets-2d.md), [motion reference](assets-motion.md). Use the asset/motion forms in [document templates](../starter/DOCUMENT-TEMPLATES.md). [Validation](validation.md) owns inspection and iteration.

For game UI and its surrounding art, [ui-art-direction.md](ui-art-direction.md) establishes the visual target and tool-selection criteria. Original/licensed assets still need to meet that target at gameplay scale; provenance is not a quality verdict.

## Production content changes

Treat importer presets, catalog schemas, skeleton/socket names and stable asset IDs as versioned contracts. Changes include dependent prefab/clip/save/content compatibility and rollback notes. Build validators reject missing IDs/GUIDs, unresolved LFS pointers, budget overruns and incompatible skeleton/material mappings before promotion. One owner publishes accepted revisions; parallel generators write separate candidate paths and never overwrite a live accepted asset silently.

Archive provider outputs independently of hosted availability. Batch generation resumes tracked job IDs and uses bounded retries/budgets; a transport timeout does not authorize duplicate paid jobs. Production CI consumes accepted files and pinned export scripts, not fresh nondeterministic generation. Acceptance captures reference exact source/export/importer hashes so later regressions can be traced. [Module contracts](modules.md) and [release discipline](engineering-baseline.md) also apply to content tooling.

Imported/generated media must become usable authored content where applicable: wire saved prefab/scene/material assets and expose tuning/previews under the [Editor authoring contract](authoring.md). Generation provenance alone does not prove authoring usability.
