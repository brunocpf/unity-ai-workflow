# UI Toolkit capabilities

Reference Editor **6000.7.0b3** (beta). Use PanelRenderer for this modern UI profile; isolate older UIDocument support. Check new features in UI Builder and a player build, not just that the API compiles.

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
| Native localization bindings | Authored translated labels/assets in Builder/UXML | Use the selected 6.7 runtime API; [localization](localization.md) owns tables, fonts and R3 integration |
| Text vertex post-processing | Per-glyph visual effects | Selected generator, localization and repaint checks; [text effects](ui-text-effects.md) |
| Custom material | Geometry/surface effects, progress masks | Shared asset; do not instantiate per row without a reason |
| Filters | Composited visual effects | GPU/intermediate-surface budget and lower-quality fallback |
| Backdrop filter | Screen-space background treatment | Do not rely on it for world-space panels |
| Keyframed animation | Authored UI sequences/cutscenes | One animation owner; interruption and reduced-motion policy |
| World-space UI | Diegetic panels/nameplates | Dedicated host/input/scale/occlusion policy and target-device tests |

Grid, UI Components, and Shader Graph filter authoring are experimental in the researched 6.7 status. Keep them in optional implementation layers so fallback controls retain the same external API. [Unity UI status](https://discussions.unity.com/t/state-of-ui-toolkit-in-unity-6-7/1736756), [UI Components primer](https://discussions.unity.com/t/unity-6-7-alpha-6-ui-toolkit-update-shader-graph-filters/1735679/4).

Use components for reusable visual concerns such as tooltip metadata or a pulse-on-change behavior, not a component that secretly purchases items or loads a singleton inventory.

## Known 6.7 beta issues

Deleting a malformed stylesheet can crash the Editor; Tile Palettes can render grey with domain reload disabled; precompiled plugins using Hash128 can fail to load; `UnloadUnusedAssets` is slow in players. Nested templates, grid sizing, filters and localized text in Play Mode have had fixes across recent betas, so recheck them after each Editor upgrade. Read each release's notes and known issues before upgrading. [6000.7.0b3 notes](https://unity.com/releases/editor/beta/6000.7.0b3).
