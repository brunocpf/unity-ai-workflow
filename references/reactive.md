# R3 and async ownership

Application commands validate Core transitions; read-only R3 state/event projections drive pure ViewModels. Keep writable subjects/properties private. Use coherent snapshots for multi-field state; native UI binding requires the [presentation bridge](ui-binding.md), not direct ReactiveProperty.Value observation.

## Integration

Pin pure R3 and matching R3.Unity plus transitive dependencies. The documented Unity route installs pure NuGet dependencies separately from the Unity UPM integration. Application explicitly references approved pure DLLs and mirrors them in the fast harness; Core's starter asmdef stays dependency-free. R3.Unity never enters pure assemblies. [R3 installation](https://github.com/Cysharp/R3#unity).

R3 uses TimeProvider/FrameProvider and test fakes; OnErrorResume need not terminate a subscription. Define recoverable versus terminal errors and route failures to diagnostics; do not mechanically port Rx/UniRx assumptions. [R3 semantics](https://github.com/Cysharp/R3#readme).

## Decisions per feature

- State replays current values; event streams do not replay historical effects by default.
- Select/deduplicate inputs before formatting [small, element-scoped view snapshots](ui-binding.md#snapshot-size-and-render-scope); avoid per-frame polling where notifications exist. Keep ordering explicit for saves/spending/network authority.
- Latest-result policy for replaceable previews/search; serialized writes for saves/spending; reject duplicate nonrepeatable submissions. Cancellation does not undo side effects or guarantee underlying work stopped.
- One authoritative rules clock; choose scaled/unscaled/real-time providers explicitly. [Accelerated tests](test-scenarios.md) take exclusive ownership before manual stepping and suspend the live driver. Marshal engine-facing updates to the intended PlayerLoop/thread.
- Use UniTask for finite engine operations and Task/ValueTask for pure async ports. Do not duplicate R3 state in async reactive properties. Do not repeatedly await single-consumption task values without a documented sharing mechanism. [UniTask](https://github.com/Cysharp/UniTask).

| Owner | Subscription lifetime |
|---|---|
| Session | End/new session |
| Scene | Unload |
| Pooled entity | One rental; dispose at despawn/disable |
| UI ViewModel | Screen/feature/item lifetime; dispose when its owner closes |
| UI binding adapter | One view binding; dispose before rebind/detach per owner |
| VisualElement-local behavior | Declared attachment or longer owner; reattachment-safe |
| Request | Completion/cancellation/timeout |

Destroy-only disposal is insufficient for pooled entities or detached UI. VisualElement is not a Component. Use existing R3 ownership primitives; wrappers and stale-result helpers follow [utilities](utilities.md). Test initial emission, equal values, timing boundaries and late delivery using fake time/frames; session static/reset behavior belongs in [lifecycle](lifecycle.md).
