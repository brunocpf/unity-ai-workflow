# Session lifecycle and fast Play Mode

**Selected solution: instance-owned services/resources; explicit lifecycle callbacks for the static UI bridge.** AutoStaticsCleanup is optional for independent simple Unity-side fields, not the mixed runtime/authoring registry. For the selected 6.7 API, mark the manually managed UiTemplates and AuthoringUiTemplates bridge classes with `Unity.Scripting.LifecycleManagement.NoAutoStaticsCleanup`; their explicit callbacks remain responsible for reset and event cleanup. This records ownership for the lifecycle analyzer, not a blanket suppression for arbitrary statics. Never combine reset mechanisms on a field or add Unity attributes to Core/Application/Presentation.

Baseline: domain reload disabled, scene reload enabled. New Unity 6.6 projects default to this; inspect existing projects. No-scene-reload is a separately tested profile. Static constructors/initializers and InitializeOnLoad are not per-Play initialization. [6.6 release](https://discussions.unity.com/t/unity-6-6-is-now-available/1735357), [AutoStaticsCleanup](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/Unity.Scripting.LifecycleManagement.AutoStaticsCleanupAttribute.html).

## Host and cleanup

UnitySessionHost in Composition owns stopped → starting → ready → stopping transitions, cancellation and services. Start/stop tolerate partial startup; stop rejects new work. Each session gets a fresh reference-identity token. Late completions may not publish into another session even when cancellation is ignored.

Teardown: stop input/presentation → cancel and join/quarantine operations → dispose bindings/ViewModels/consumers → clear template references → release provider handles/registration. The root UI library owns its directory registration; the advanced ID path releases handles before the caller unregisters. Continue remaining cleanup if one step fails; report failures. Synchronous Dispose is not an async join: StopAsync coordinates task completion or quarantines late results.

Use a small Unity bridge: SubsystemRegistration resets transient context before scenes; normal host destruction/application shutdown and Editor exiting-Play/before-assembly-reload hooks invoke teardown. Editor hooks live in Game.Editor through an explicit bridge. Do not rely on ordering between unrelated attributed callbacks. Resetting references is a guard, not disposal. [SubsystemRegistration](https://docs.unity3d.com/6000.7/Documentation/ScriptReference/RuntimeInitializeLoadType.SubsystemRegistration.html).

## UI runtime versus authoring

Keep the authoring resolver separate from runtime context. Clear runtime context on entry/exit; preserve or deterministically re-register authoring support. Rebuild authoring caches after relevant imports/code reload. Static initializers must not load assets.

Construction scopes are main-thread-only and synchronous. Use a session token plus monotonic scope IDs/depth to reject stale, copied/double-disposed or out-of-order scopes without restoring old context. Keep essential checks in players; format diagnostics only on failure. Ref structs alone do not ensure correct disposal. No scopes across awaits or Play transitions.

AutoStaticsCleanup restores annotated members; readonly collections are cleared, not repopulated. Do not annotate a lookup table expecting entries to survive. For future CoreCLR upgrades, audit references that retain old code/assets and use the verified lifecycle APIs; old roadmap dates are not compatibility guarantees.

## Acceptance

At least three Play/Stop cycles without recompilation, Builder open, no duplicate handlers, cancelled preload completing late, failed construction followed by clean startup, released owner/lease references, and player startup/shutdown. Test no-scene-reload only if supported. Inspect Project Auditor Domain Reload findings. Pair resource counts with retained-memory evidence; native memory need not return immediately.

Default scope composition and captive-dependency rules: [composition](composition.md).
