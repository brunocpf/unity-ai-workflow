# Visual effects

**Prefer VFX Graph over the classic Particle System (Shuriken)** for authored particle effects. Use Shuriken only for a documented target/renderer limitation, required feature or measured performance/maintenance advantage. Do not choose it merely because its API is easier to generate. Simple UI feedback still uses UITK drawing/materials/filters or LitMotion where appropriate; the preference does not turn every animation into a particle graph.

## Dependency and setup

VFX Graph is the Unity package `com.unity.visualeffectgraph`, not a universally installed Editor feature. URP projects generally add it explicitly; HDRP includes it as a dependency. Inspect the actual resolved manifest and compatible render-pipeline version before adding/upgrading it. [Unity installation guide](https://docs.unity3d.com/Packages/com.unity.visualeffectgraph@17.7/manual/GettingStarted.html).

When the planned game uses particle effects, resolve and lock the compatible VFX Graph dependency during foundation setup; if effects enter scope later, add it with that feature. Verify package import/compilation during setup and a representative effect in the target player during slice acceptance. Installing this workflow's skills never installs Unity packages. The version in a documentation URL is not a package pin.

Qualify the selected renderer, graphics API and device capabilities, including compute support; do not infer support from the platform name alone. For URP 2D, prove the selected graph output/Shader Graph path, sorting and lighting behavior in a saved fixture. Record a fallback before committing to an unsupported target. [Requirements](https://docs.unity3d.com/Packages/com.unity.visualeffectgraph@17.7/manual/System-Requirements.html).

## Authoring and ownership

- Save graphs/subgraphs, materials and effect prefabs as editable assets under the project's content layout. Expose meaningful parameters and event names; provide scene/Inspector previews. Validate parameter contracts before runtime use.
- Unity presentation adapters translate gameplay events into effect requests. Core outcomes never depend on GPU particle simulation, collisions or readback. Keep spawn budgets, lifetime and pooling ownership explicit.
- Reuse authored graph assets; instance parameters belong to the effect owner. Test reset/replay, overlapping bursts, scene exit, pooling and teardown without leaked effects or stale parameters. Graph events and cleanup semantics must be verified for the selected graph; Shuriken's StopEmittingAndClear is not a VFX Graph API.
- Budget concurrent instances, particle capacity, overdraw, GPU time and buffers. Check bounds/culling, off-screen return, transparent sorting and shader inclusion in a cold player. Greater particle counts are not a quality target.
- Apply reduced motion and quality levels without changing gameplay. Preserve readable danger/hit feedback with restrained alternatives. Capture and inspect representative bursts, sustained load, low/high quality and supported devices; performance counters and deterministic visual expectations must match the selected simulation path.

Use [asset acceptance](assets.md), [validation](validation.md) and [visual fixtures](visual-fixtures.md). Keep Shuriken tint/alpha fixtures for projects that actually select that fallback; add graph-output/material fixtures for VFX Graph rather than pretending one proves the other.
