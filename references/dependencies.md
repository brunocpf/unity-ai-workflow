# Dependency defaults and adoption policy

Project defaults, researched September 2026. Resolve and test exact releases for the selected editor/target; documentation versions below are sources, not package pins. Install only the selected profile.

## Default stack

For general-purpose projects, use **R3 + UniTask + LitMotion**, the Unity Input System, UI Toolkit with R3 MVVM, the selected Unity localization implementation, and Unity Test Framework. Use **Cinemachine 3** in the camera-enabled profile. **VContainer** is the standard Unity composition/scoping container; pure code and tests retain ordinary constructor injection. Follow [composition](composition.md). Put engine-dependent libraries in Unity assemblies.

| Need | Preferred choice | Boundary and reason to add it |
|---|---|---|
| State changes, UI observation, event composition | **R3** (third party) | Application/presentation streams; keep Core rules ordinary synchronous C#. Expose read-only state and explicit commands. See [reactive ownership](reactive.md). |
| Finite async Unity operations | **UniTask** (third party) | Unity adapters/binding: loading, transitions and orchestration. Keep pure public ports on standard Task/ValueTask where asynchronous work is required. |
| Procedural value animation | **LitMotion** (third party) | Presentation motion and game-object feedback, with one handle owner. Use native USS transitions for simple style-state transitions. |
| Camera composition, tracking and blends | **Cinemachine 3** (Unity package) | Add when camera behavior exists. A fixed camera needs no framework. Core emits camera intentions, never Cinemachine objects. |
| Devices, action maps, rebinding | **Input System** (Unity package) | Default for interactive projects; adapter converts device input to commands. UI and gameplay action-map ownership must be explicit; [native UITK navigation](ui-navigation.md) owns ordinary UI Move/Submit. |
| Menus, HUDs, UI documents | **UI Toolkit + pure R3 ViewModels + project element library** | Thin R3 binding adapters for VM state; native localization bindings for authored text/assets, optional native binding for other declarative screens/forms. No additional MVVM framework. |
| Player-facing languages/text/assets | **Native Unity 6.7 Localization Runtime**; compatible localization package on older profiles | Baseline even for a single source language. Native UITK bindings, pure text ports, no Unity dependency in Presentation. See [localization](localization.md) for the version-gated provider/package choice. |
| Runtime composition/scopes | **VContainer** (third party) | Default for application/session/module roots; use explicit lightweight owners for screens/rentals. Keep resolution inside the composition root. Core has no container attributes. |
| Authored particle effects | **VFX Graph** (Unity package) | Preferred over Shuriken; qualify target/renderer support and document fallback exceptions. See [VFX setup and ownership](vfx.md). |
| Tests | **Unity Test Framework + a pinned .NET test harness** | Select NUnit for the harness as well unless an established repository already uses another runner. Keep framework references in tests only. |

Sources for capabilities: [UniTask](https://github.com/Cysharp/UniTask), [LitMotion](https://github.com/annulusgames/LitMotion), [Cinemachine 3](https://docs.unity3d.com/Packages/com.unity.cinemachine@3.1/manual/index.html), [Input System](https://docs.unity3d.com/Packages/com.unity.inputsystem@1.14/manual/index.html), [VContainer](https://vcontainer.hadashikick.jp/). R3 mechanics are in [reactive ownership](reactive.md); test gates are in [validation](validation.md).

## Responsibility boundaries

R3 owns ongoing application/presentation signals; UniTask finite engine operations; USS simple style transitions; LitMotion procedural motion; Animator clips/skeleton playback; Timeline authored sequences; Cinemachine camera pose. Never let two systems drive the same property without an explicit handoff. [Reactive ownership](reactive.md) and [UI binding](ui-binding.md) define the mechanics.

LitMotion installation documentation lists Burst/Collections/Mathematics requirements. For Unity 6.6+ verify whether the selected editor supplies a built-in module rather than blindly adding an older package; validate the resolved combination. Check actual UITK binding support before copying uGUI samples. [LitMotion installation](https://github.com/annulusgames/LitMotion/blob/main/docs/articles/en/installation.md).

For Unity 6.7, qualify UniTask's Editor assemblies (including its tracker) as well as runtime/player code before accepting a pin. Upstream [2.5.11](https://github.com/Cysharp/UniTask/releases/tag/2.5.11) includes a TreeView deprecation fix for Unity 6.2+; it is a candidate to test, not evidence of a verified 6.7 integration. Record the exact package/commit, failing API and corrected Editor/player results. Do not disable all Editor tooling or edit PackageCache as a permanent workaround; prefer a verified upstream release, or a versioned patch with an owner and removal condition.

Read [optional libraries](dependencies-optional.md) only when the required capability is outside this stack.

## Presets

- **First mechanics slice:** standard architecture/scopes, Core, Application, Presentation when UI exists, R3, UniTask, VContainer, Input System, localization for player-facing text and tests. Add LitMotion when motion is consumed. This is a delivery stage, not a reduced architecture.
- **Default polished game:** above plus LitMotion, UITK component library, qualified content/localization providers; Cinemachine when camera behavior is required and VFX Graph when particle effects are planned. Resolve its compatible package during foundation setup; prove the effects in the slice.
- **3D character game:** default plus Cinemachine, Animator, Animation Rigging, AI Navigation as needed. Tripo/Blender pipeline supplies validated clips/meshes. Animancer requires a recorded controller-maintenance reason.
- **Pixel-art game:** default plus Unity's appropriate 2D/pixel-perfect tools, PixelLab pipeline, sprite import/atlas rules. A camera package is optional for a static screen game.
- **Narrative game:** default plus Yarn Spinner integrated with the existing localization authority, Timeline when cinematic sequences exist.
- **Online game:** choose authority, latency budget, topology and hosting first; then select one networking profile. Reconnection, version mismatch, server validation and multi-client tests become mandatory.

Presets describe desired capabilities. The bootstrap creates a resolved manifest containing only the selected packages and their actual compatible versions. No floating `main`, `current`, or `latest` Git references in a template release.

Installing the polished-game preset does not establish polish. Apply the [visual target and review](ui-art-direction.md) during the first playable UI slice; a mechanics scaffold is an intermediate stage, not the final visual deliverable.

## Adoption gate

Maintain `docs/dependencies.md` with one record per direct dependency:

```text
Capability / selected package / exact version or commit
Owner assembly / package source / upstream documentation
Reason built-in or existing tools are insufficient
License identifier and any redistribution or seat constraints
Editor + C# + render pipeline + target + backend compatibility tested
Transitive requirements and generated-code/analyzer requirements
Acceptance scene/test + last validated template release
Replacement boundary / upgrade notes / known issues
```

Use UPM for Unity packages and a controlled, documented import path for pure .NET dependencies. Never import the same assembly via both a UPM package and a loose DLL. Inspect asmdefs and transitive references: a pure library cannot silently pull in UnityEngine. Pin the fast-test harness to the same pure dependency versions as the game.

Before merging an addition, run the smallest proving slice in the exact editor and target backend: build, launch, exercise its real feature, and unload/reload it. For generated code/reflection/serialization, include the stripped IL2CPP target where applicable. For a tween, test cancellation and pooling; for async, test timeout and scene exit; for cameras, test ownership transitions; for networking, test separate clients. Record observed results, not a generic “Unity supported” badge.

When a consequential choice remains unclear, [ask with a recommendation](clarification.md). The default answer to a new alternative is “use the selected package.” Reopen the decision only for a missing capability, measured problem, license constraint, maintenance problem, or target incompatibility. An ADR explains the exception and the affected profile. Avoid two tween libraries, two DI containers, or two general event buses in a new project; legacy migration can temporarily have both with explicit boundaries and removal criteria.

Project-owned adapters and helpers are specified in [utilities](utilities.md). They wrap selected library/engine primitives and must not become duplicate cancellation, reactive, pooling, content or DI frameworks.
