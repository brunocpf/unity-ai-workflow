# UITK capability gates

Evaluation target **6000.7.0b2**: the Editor is beta. Use PanelRenderer for this modern UI profile; isolate older UIDocument support. The [upgrade record](upgrades/unity-6000.7.0b2.md) owns version-specific fixes, known issues and evidence. API compilation does not establish Builder or player compatibility.

## Modern feature routing

| Feature | Where to use it | Constraint |
|---|---|---|
| Grid | Dense bounded inventory/menu layouts | Experimental flag; grid is not virtualization |
| ListView/TreeView | Large/recycled data sets | Bind/unbind/destroy lifecycle; keyed identity |
| gap | Consistent spacing in supported layouts | Choose gap or per-child spacing intentionally |
| z-index | Local overlap within a stacking context | A root overlay layer still owns cross-screen modals/tooltips |
| UI Components | Attach orthogonal visual behavior/data | Experimental; no hidden global business services |
| Manipulators | Pointer/keyboard behavior and capture | Register/unregister symmetrically; handle cancellation |
| Custom drawing / mesh modifiers | Procedural controls or generated-geometry effects | Bounded work and invocation-only mesh access; [advanced UI](ui-advanced.md) |
| Native localization bindings | Authored translated labels/assets in Builder/UXML | Use the selected 6.7 runtime API; [localization](localization.md) owns tables, fonts, R3 integration and player proof |
| Text vertex post-processing | Per-glyph visual effects | Selected generator, localization and repaint checks; [text effects](ui-text-effects.md) |
| Custom material | Geometry/surface effects, progress masks | Shared asset; do not instantiate per row without a reason |
| Filters | Composited visual effects | GPU/intermediate-surface budget and lower-quality fallback |
| Backdrop filter | Screen-space background treatment | Do not rely on it for world-space panels |
| Keyframed animation | Authored UI sequences/cutscenes | One animation owner; interruption and reduced-motion policy |
| World-space UI | Diegetic panels/nameplates | Dedicated host/input/scale/occlusion policy and target-device tests |

Grid, UI Components, and Shader Graph filter authoring are experimental in the researched 6.7 status. Keep them in optional implementation layers so fallback controls retain the same external API. [Unity UI status](https://discussions.unity.com/t/state-of-ui-toolkit-in-unity-6-7/1736756), [UI Components primer](https://discussions.unity.com/t/unity-6-7-alpha-6-ui-toolkit-update-shader-graph-filters/1735679/4).

Use components for reusable visual concerns such as tooltip metadata or a pulse-on-change behavior, not a component that secretly purchases items or loads a singleton inventory.

Retain component-reference, grid-size and content-unload/material regressions from the earlier b1 evaluation. Add the [b2 template, font and teardown cases](upgrades/unity-6000.7.0b2.md#acceptance-after-installation); their release-note fixes are not test results. Use the [UI acceptance matrix](validation.md#ui-acceptance).
