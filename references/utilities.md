# Reusable utilities and performance

Implementation contracts; selected [source examples](../examples/README.md) are supplied with a separate verification record. Build only pieces consumed by the current slice; keep them in feature folders within existing assemblies. Extract shared packages after proven reuse. [Lifecycle](lifecycle.md) and [UI construction](ui-construction.md) own their detailed mechanics.

## Boilerplate worth implementing once

Use feature folders inside the existing boundary assemblies; these names do not require one asmdef each. No generic Helpers or Utils folder.

| Reusable piece | Location / dependencies | Contract and acceptance |
|---|---|---|
| Session host and lifecycle bridge | Unity/Composition/Lifecycle; Editor/Lifecycle | Idempotent start/stop; fresh session token; ordered cleanup; repeated Play/Stop, failed startup and late completion tests |
| Lifetime ownership wrapper | Application/Lifetimes for pure R3/standard cancellation; engine hooks in Unity | Small wrapper over existing R3 disposable support and CancellationTokenSource. Expose token, Track and explicit teardown. Dispose resources added after closure immediately; do not swallow cleanup failures or let one failure skip all remaining cleanup. No custom reactive engine |
| Latest-result request helper | Application/Async; Unity UniTask adaptation outside pure assembly | Version each request; cancel old work and discard stale results even if cancellation is ignored. Test A finishing after B. Use only for replaceable reads/previews, never purchases or authoritative writes |
| Save queue and repository adapter | Application/Persistence contracts; Unity/Runtime/Persistence | Serialize writes, version DTOs, validate/migrate, handle corrupt data and preserve last accepted save. File adapter uses temp/replace where target supports it; platform adapters must document equivalent behavior. Keep game-specific schemas/migrations in the game |
| Content lease adapter | Unity/Runtime/Content | Explicit ownership around the chosen provider, deduplicate in-flight acquisition where justified, per-caller cancellation semantics, release failed/late results. Test two consumers, one cancelling, final release, failed acquisition. No replacement content engine |
| UI registry, context, factory and Editor resolver | Unity/UI/Content; Editor/UI | [UI construction](ui-construction.md) plus its Builder/player probes |
| ViewModel/binding lifetime and intent bridge | Presentation for pure VMs; Unity/UI/Binding for adapters | Pure ViewModels with mechanical R3 adapters by default; optional native notification wrapper; one owner per property, no duplicate commands after reuse; use R3 directly rather than a second MVVM framework |
| Visible decorative clock / value motion owner | Unity/UI/Motion for shared clock; per-control adapter beside the control | [VisibleMotionClock and ArcMeterMotion](visual-fixtures.md#visibility-reduced-motion-and-teardown); explicit effective visibility, reduced-motion reset, pause/cancel and teardown. One owner per property; no gameplay ticks |
| Clock/RNG adapters and test fakes | Core or Application boundary where used | Explicit clock/tick/random inputs; one scoped simulation driver, live/manual handoff and restoration per [scenario contract](test-scenarios.md); use R3's supported fake time/frame tooling in tests. No new scheduling library and no claim seeded Unity physics is deterministic |
| Pooled-object rental adapter | Unity/Runtime/Pooling, conditional | Wrap Unity pooling with fresh rental state/subscription scope, reset callbacks and stale async-result rejection. Pool only after allocation/frame measurements justify it |
| Localization/text and locale-preference adapters | Presentation text port + Unity/UI/Localization; Application preference port + Unity/Runtime/Localization | [Contract](localization.md#reusable-adapter-contract): single engine locale authority, owned readiness/revision/formatting, cached active data, no synchronous load in Render, invalidated stale locale/row results; baseline for text consumers |
| Diagnostics and performance markers | Unity/Runtime/Diagnostics plus minimal pure diagnostic port if needed | Structured feature/scenario/error IDs, bounded buffering, no secrets; add Unity profiler markers at important boundaries. Avoid formatting strings in hot loops and logging every reactive event |
| Acceptance scenario runner | Assets/Game/Tests + tooling/ci | Named seed/input/readiness/checkpoint sequence, exclusive clock ownership, fresh per-run capture manifest/validation, expected state assertions and cleanup. Separate capture from actual visual review; produce durable evidence |
| Asset/content validators and export presets | Unity/Editor/Validation + tooling/blender | Validate GUIDs/LFS pointers/catalogs/budgets and explicit export selections; rerunning must not duplicate assets. Keep platform-specific importer rules explicit |
| Owned IDE profile + shared quality gate | Unity/Editor/Development + tooling/ide + tooling/quality | Supplied [IDE hook](ide.md) and [syntax/coverage driver](code-organization.md); regenerate only owned compiler settings, prove semantic coverage and fault rejection |
| Build/test entrypoints and provenance writer | Unity/Editor/Build + tooling/ci | Same local/CI operations, exact versions, nonempty test reports, content-before-player ordering, artifact hashes and useful exit codes |

A lifetime wrapper handles owned disposables; it must not imply that synchronous Dispose awaits in-flight tasks. Session/module StopAsync coordinates asynchronous shutdown separately and observes failures. Use CancellationTokenSource and R3 facilities instead of inventing cancellation or subscription semantics.

Prefer concrete result types and exceptions appropriate to each boundary. Do not mandate a universal Result library, global mediator, service locator, reflection-based registration, all-purpose repository base class, or custom object pool. Domain gameplay systems are not infrastructure merely because their names sound reusable.

## Performance policy and measuring it

Targets below are design constraints to verify, not measured results:

| Operation | Expected behavior |
|---|---|
| Warm GetRequired | One bounded dictionary lookup, zero managed allocation from the lookup itself; no I/O, reflection or engine load |
| Construction context | No heap allocation/boxing for the scope; constant-time entry/exit; no AsyncLocal propagation |
| New control construction | UXML cloning can allocate; measure whole construction, not just lookup microbenchmarks |
| Idle UI | No polling/rebinding to discover unchanged state; framework background cost measured separately |
| Reactive updates | Select/deduplicate relevant values; batch coherent snapshots; no blanket per-frame ToArray/LINQ rebuilds |
| Recycled list rows | Reuse structure, replace binding scope and stable item identity; no growing handler/subscription count |
| Content | Bounded shared-library residency; large art loaded separately; report peak memory during module overlap and unload |
| Shutdown | Owner/lease counts return to baseline; native memory may not return immediately, so inspect retained references and provider state too |

Record cold startup, warm screen opening, row scrolling/rebinding, theme switching and repeated module open/close under representative loads. Capture CPU time, allocation bytes, retained memory, GPU/layout costs and loading latency. Define device-specific budgets in docs/project.md (performance budgets); do not invent universal millisecond targets. Compare before/after on the same target build and configuration. Distinguish authoring, Editor runtime and target-player numbers.

Optimize in order: avoid unnecessary work; reduce invalidation/reconstruction; bound loaded content; virtualize large data sets; then consider pooling/data structures. Avoid unsafe code, custom schedulers or aggressive cache persistence to save an unmeasured dictionary lookup. A global cache that survives sessions can conceal leaks and invalid content even if its warm timing looks good.

## Implementation order and release evidence

1. Establish assembly boundaries, shared-source test harness, lifecycle host and basic diagnostics. Prove repeated starts/stops and late-task rejection.
2. Implement the template registry/factory, authoring resolver and Content Directory adapter. Prove one standalone custom control in UI Builder and in a cold built player. Include runtime automatic-host construction paths in the audit.
3. Add localized tables/settings and the required text/preference adapter, then a pure ViewModel, R3 binding and optional native-binding comparison, virtualized row fixture, cancellation case and explicit resource cleanup. Measure allocations and opening/scrolling latency.
4. Add the save/content/asset/scenario tooling exercised by the acceptance slice. Optional utilities wait until their first real consumer.
5. Validate clean checkout, fast Play Mode, content failure, target-player output and performance budgets; tag only the capabilities proven. Document each utility's public contract, lifetime, dependencies, failure behavior, tests and measured cost in docs/architecture.md.

Utilities without linked source remain implementation requirements or conditional candidates. Supplied examples have a limited verification record; performance targets still require Unity/player measurements. The pure scope allocation check does not establish whole-UI performance.

Available reference source: [scoped context, template lookup/loading, ViewModel/binding, list recycling and latest-request guard](../examples/README.md). These do not replace the remaining utility contracts or template acceptance.
