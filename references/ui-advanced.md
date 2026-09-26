# Advanced rendering and motion

Use with [capability gates](ui-capabilities.md), [USS](ui-styling.md) and [text effects](ui-text-effects.md). These are view-layer mechanisms; MVVM and content ownership stay unchanged.

Choose treatments from the [visual target](ui-art-direction.md). “Simplest mechanism” means the simplest implementation that achieves it, not reducing the target to a plain interface. Restrained motion leaves room for rich imagery, custom controls, meaningful depth and satisfying action feedback.

## Expected rendering and motion

For player-facing game UI, **actively implement rich custom rendering and coordinated animation as the default**. Painter2D, gradients, UI materials, filters and LitMotion belong in ordinary screen/control development; do not wait for the user to request them by API name. A finished primary screen should demonstrate designed silhouettes/detail, deliberate surface/depth treatment and meaningful animated interactions. Choose the combination for the art direction and target budget; an explicitly minimal style or a small utility/debug panel can use a simpler treatment.

| Design work | Technical starting point | Example result |
|---|---|---|
| Intricate framing and silhouettes | `generateVisualContent` + Painter2D paths, curves, layered fills/strokes; mesh generation for explicit topology/UVs | Notched frames, ornamental corners, inset tracks, segmented rings, connectors and route contours |
| Color, light and translucent depth | Painter2D gradients, supported USS gradients or authored gradient assets; explicit color/alpha stops | Shaded gauges, translucent selection fields, directional surface light and layered map edges |
| Surface character and dynamic masks | UITK custom materials/UI Shader Graph with owned parameters | Paper grain, water distortion, ink reveal, masked progress or a localized confirmation highlight |
| Composited depth and focus | Bounded shadows/glow/blur and qualified filters | A lifted parcel, recessed inventory well, focused modal layer or selected route halo |
| Choreographed interactions | View-owned LitMotion sequences/handles plus named USS state transitions | Anticipation → move → settle, staggered screen entry, cargo transfer, animated progress and completion stamp |
| Expressive text | Typography plus bounded text post-processing where appropriate | Short title flourish, reward emphasis or shaped-text reveal with a readable static baseline |
| Rich authored detail | Layered illustrations, textures, icons and decorative UXML elements | Material edges, emblems, destination marks and theme-specific controls instead of generic rectangular cards |

Carry detail through focus/hover/press/selection/disabled and state transitions. Compose a few strong treatments into reusable control families; do not scatter one-off effects over otherwise generic screens. Static intricate artwork does not need a repeating clock. A shader may be useful without continuous animation; event-driven effects can be energetic and tactile while idle screens remain calm.

For each signature control, record `visual feature → drawing/material/motion mechanism → assets/parameters → lifetime owner → target-player evidence` in the visual design brief. Implement the selected mechanisms in the early representative screen. Merely listing these APIs, installing LitMotion or delivering a high-fidelity mockup does not satisfy this technical default. Qualify the exact [capabilities](ui-capabilities.md), then use the [rendering and motion fixtures](visual-fixtures.md) to verify the result.

For example, a delivery-game daylight control can combine a Painter2D sun arc/ticks, a translucent cost-preview gradient and a LitMotion transition after travel. A cargo tray can combine inset textured slots, shaped parcel controls, lift/settle feedback and a short ink/stamp reveal on delivery. These are recipes to adapt, not mandatory nautical styling for other games.

Construction still produces a static Builder preview. Mechanical R3 bindings forward small targets to one visual owner; drawing callbacks consume prepared state, and the runtime owner starts/stops effects. Reuse the existing content, MVVM, visibility and disposal patterns while making their appearance substantially richer.

## Select the rendering mechanism

| Requirement | Default |
|---|---|
| Static skin, focus/hover, gradients, ordinary shape | USS and asset-backed styling |
| Radial meters, graphs, procedural borders | `generateVisualContent` + Painter2D; explicit mesh allocation when topology/UV control warrants it |
| Modify already-generated element geometry | `AddMeshModifier` with a paired removal; keep modifiers scoped and ordered |
| Dissolve, hologram, moving highlight, GPU deformation | UITK custom material / UI Shader Graph |
| Blur, silhouette shadow, composite glow/distortion | Built-in filter first; custom filter only for an unmet effect |
| Per-glyph deformation/reveal | Text post-processing, following the [text contract](ui-text-effects.md) |
| Reactive feedback and interrupted transitions | View-owned LitMotion handles |
| Designer-authored cinematic choreography | UITK keyframed animation; one owner per affected property |

Default to the simplest mechanism meeting the art brief, then profile the actual target. `generateVisualContent` supports both Painter2D and mesh generation. Do not use a paint callback as an update loop. [Unity drawing APIs](https://docs.unity3d.com/6000.7/Documentation/Manual/UIE-generate-2d-visual-content.html).

## Custom geometry contract

The [ArcMeter source](../examples/Unity/UI/Elements/ArcMeter/ArcMeter.cs) uses clamped attributes, current resolved color, bounded geometry and repaint only when values change. Register its private [UXML](../examples/Unity/UI/Elements/ArcMeter/ArcMeter.uxml) as `controls/arc-meter`; it owns the USS and drawing surface, so Builder and runtime use the standard catalog pattern. Open the [preview UXML](../examples/Unity/UI/Previews/Effects/EffectsPreview.uxml) after registration. A Label-derived leaf such as WaveLabel needs no structural template; ordinary text renders without extra assets or initialization.

Paint callbacks read layout and already-prepared visual state. No loads, queries, subscriptions, hierarchy/style mutation, business commands or retained MeshGenerationContext/Painter2D/mesh slices. Account for content origin, stroke width, zero size, clipping and finite inputs. With Allocate/SetNextVertex, bound tessellation and use correct winding/UVs; fill the allocated counts exactly. Cache expensive source calculations outside drawing; regenerate only invalidated geometry. Preserve the renderer's atlas/clip conventions.

For per-instance mesh modifiers, unregister the same delegate on disposal and never ClearMeshModifiers on a shared element owned by another subsystem. Additional vertex channels increase bandwidth: enable only those the effect consumes. CPU vertex edits are useful for small effects; prefer a validated GPU path when many elements deform continuously.

## Materials and filters

Author a **UI Toolkit** graph/material, not an assumed uGUI Canvas or world-surface graph. Start from the selected Editor's working UI samples. Custom filter Shader Graph authoring remains experimental in this profile; built-in filters and custom UI materials have separate capability checks. [Unity feature status](https://discussions.unity.com/t/state-of-ui-toolkit-in-unity-6-7/1736756).

Recipe: define the effect's inputs → make a static gallery sample → verify tint/alpha/UV/clipping and color space → expose only necessary runtime parameters → add animation → profile → provide a quality fallback. Use the [material/geometry qualification fixture](visual-fixtures.md#ui-material-and-geometry-gallery), including neutral sample tint, explicit gradient alpha, inherited material scope and cold content loading. Example selection treatment: USS border/focus indicator and brief LitMotion scale pulse. Example modal: opaque low-quality scrim or one bounded backdrop blur behind the modal, with identical navigation semantics.

Keep shader, material, texture and filter assets in the control/feature content directory. Reference them from UXML/USS or an explicit catalog asset dependency. No runtime Shader.Find-only dependency or Editor path load. Test content stripping and cold player load. Shared material assets are immutable; per-instance parameters use the selected UITK API or a deliberately owned material instance, released after its consumer. Do not assume Renderer.MaterialPropertyBlock works on a VisualElement.

Filters can create intermediate surfaces. Bound affected area, pass count, blur radius and nested stacks; avoid a blur per recycled row. Supply appropriate read/write margins for expanded samples and test edges under clipping. Keep input/focus geometry truthful when pixels deform. Do not assume world-space backdrop behavior. A fallback removes the expensive treatment while preserving contrast, state and interaction. Record UI CPU/GPU time, allocations, batch breaks and render-target memory in the feature's performance budget.

## Motion ownership and state transitions

Use USS for small declarative hover/focus transitions; LitMotion for coordinated, interruptible feedback. Never animate the same property through USS, native animation and LitMotion concurrently. VM state is authoritative immediately; the displayed interpolation belongs to the view. Binding adapters pass targets to that owner rather than writing around it.

[ArcMeterMotion](../examples/Optional/LitMotion/ArcMeterMotion.cs) shows first-state snap, duplicate suppression, cancellation, interpolation from the current value, unscaled time, detach snap and disposal. The screen calls `SetPresentation(visible, reducedMotion)` independently of VM numeric emissions; hidden/reduced mode cancels and snaps immediately. It starts inactive. Qualify the optional package adapter using the [verification guide](../examples/Verification/README.md). A pooled row gets a new owner and initial snap for its new identity.

For repeating decorative phase updates, use [VisibleMotionClock](../examples/Unity/UI/Motion/VisibleMotionClock.cs) per visible region. Forward effective screen visibility; the scheduler's attachment behavior does not implement navigation visibility. Pause the schedule rather than leaving an early-returning callback active. Apply the [UI/world motion and teardown fixtures](visual-fixtures.md#visibility-reduced-motion-and-teardown). [Unity scheduler lifecycle](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/UIElements.IVisualElementScheduler.html).

Project starting tokens: feedback 100–140 ms, value transition 220 ms, screen entry 220–280 ms; adjust deliberately for the art direction. Prefer opacity/transform for movement; geometry or filter animation has its own budget. Avoid perpetual attention-seeking motion. Reserve punch/shake/overshoot for meaningful events; clamp meters, preserve text legibility and avoid moving hit targets under the pointer.

Screen transition controller owns Closed/Opening/Open/Closing, desired state, handles and a generation counter. A new request cancels old handles and continues from current visuals. Completion checks generation before hiding/releasing/focusing; zero-duration follows the same finalization path. Closing disables interaction immediately; the modal owner keeps input blocking until closure and restores valid focus once. Do not send gameplay commands from an animation completion. Cap stagger totals for lists; animate visible rows only.

LitMotion supports explicit schedulers and cancellation; use unscaled time for pause menus. Sequences may orchestrate joined/staggered tracks, but one owner cancels the whole transition. Select a manual scheduler for deterministic transition tests; never drive a global dispatcher used by unrelated tests. [Configuration](https://annulusgames.github.io/LitMotion/articles/en/motion-configuration.html), [control](https://annulusgames.github.io/LitMotion/articles/en/motion-control.html), [manual time](https://annulusgames.github.io/LitMotion/articles/en/manual-motion-dispatcher.html).

Acceptance: initial/repeated targets, open-close-open, rapid reversal, timeScale zero, detach/rebind/recycle, content unload, reduced motion mid-transition, focus/pointer capture and no motion handles after teardown. Compare static screenshots and [event-timed recordings](visual-fixtures.md#event-timed-recordings) on the target backend, including the whole screen in motion. Respect the [visual direction gate](visual-fixtures.md#visual-direction-is-an-acceptance-gate); allocation-free binding syntax alone is not a performance result.
