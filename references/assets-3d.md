# 3D: Tripo → Blender → Unity

Use approved front/side/back references with consistent proportions and lighting; independent generated views can contradict one another. Inspect those views before paying for mesh generation. For characters, use a neutral riggable pose with visible separated limbs, clear hands, and no unnecessary occlusion.

The installed Tripo skills provide generation, rig-check, rigging, preset retargeting, segmentation, conversion, and LOD workflows. They also note that decimation targets can be exceeded and model/preset selection affects topology. Pin the CLI, inspect its current help/capabilities, record the resolved model and parameters, and measure actual exports. See [Tripo developer portal](https://platform.tripo3d.ai/) for the service; exact local command behavior comes from the installed tripo-3d and tripo-game-asset skills.

Do not treat automatic rigging as production-ready facial animation, garment simulation, or a complete animator controller. Humanoid-compatible naming still needs successful Unity Avatar validation. Use Generic rigs for creatures, vehicles, and non-humanoid skeletons when appropriate.

Blender preparation:

1. Preserve the imported source collection; work on an authoring copy. Inspect linked meshes/materials and make single-user copies before changing shared data.
2. Check dimensions, transforms, handedness/axes, pivot and origin using a known size reference. Avoid late scale changes on an already rigged asset.
3. Remove unintended internal geometry; inspect silhouette, normals, UV seams, material count, and deformation topology. Retopologize when needed; decimation is not deformation-aware retopology.
4. Establish UV density/padding, bake high-to-low normal/AO where appropriate, and inspect the asset under neutral lighting.
5. Build collision proxies and LODs appropriate to gameplay and camera distance. Verify measured triangles and materials after export.
6. For rigs, agree on bone names, hierarchy, rest pose, root motion, and attachment sockets. Reuse the skeleton across a character family rather than rerigging every animation.
7. Validate weights with extreme poses; inspect shoulders, elbows, hips, knees, feet, clothing, and weapon attachment.
8. Export explicit mesh/armature selections using a pinned preset. Bake constraints/control motion onto deform bones. Export only intended clips, with explicit frame ranges and sampling.
9. Reimport the export into a clean Blender scene and Unity. Verify animation, scale, materials, root, and silhouette at both boundaries.

The Blender MCP available here exposes scene summaries, object inspection, documentation search, screenshots, and Python execution. Use inspection and screenshots to make editing reviewable; promote stable repeated operations into version-controlled Blender scripts for headless CI. MCP is an interactive control channel, not a substitute for pinned export scripts.

Rigify generates a control rig from a fitted metarig. Its constraints and controls are authoring machinery; bake the desired result for export. Blender's bundled manual documents FBX action selection and baking, which is why export-all-actions should never be an accidental default. [Blender FBX manual](https://docs.blender.org/manual/en/latest/addons/import_export/scene_fbx.html), [Rigify basic workflow](https://docs.blender.org/manual/en/latest/addons/rigging/rigify/basics.html). These topics were also checked through the connected MCP's bundled documentation.

In Unity, keep imported model files separate from authored prefab variants. Apply deterministic importer presets, construct materials for the selected render pipeline, assign colliders/LOD groups/Avatar, and run the animation test scene. Do not expect FBX to preserve arbitrary Blender shader graphs.
