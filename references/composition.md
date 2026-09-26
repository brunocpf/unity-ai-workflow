# Composition and lifetime scopes

**Use constructor injection and VContainer at Unity composition roots by default.** The container owns wiring/scopes; plain C# owns behavior. Core, Application and Presentation have no VContainer attributes or references. Tests and source examples use direct construction. A game-wide manual-composition exception needs an ADR and equivalent ownership tests, not a claim that solo projects need fewer boundaries.

| Owner | Typical contents | End |
|---|---|---|
| Application root | Immutable config, diagnostics, platform adapters | Application shutdown |
| Session | Player/progression state, use cases, gameplay clock | New game/logout/session end |
| Scene/feature module | Local systems, navigation/content leases | Unload/module close |
| Screen | ViewModel, binding adapter, mounted view | Navigation close/replacement |
| Pool rental/request | Temporary behavior/subscriptions/asset handles | Return/completion/cancellation |

Not every row needs a DI child container. Use explicit disposable screen/rental owners under the corresponding scope, especially for high-churn objects. Never register a per-screen or per-player state object as an application singleton. Long-lived parents must not retain short-lived children. A dependency's lifetime must cover its consumer's lifetime.

Register dependencies in Composition and resolve only there (including typed factory implementations). Composition instantiates/rents authored prefabs and wires their view adapters; it does not rebuild ordinary character/level hierarchies or overwrite Inspector tuning. Saved definitions compile to pure configuration at startup. Follow [authoring](authoring.md) for prefab activation and editing contracts. A MonoBehaviour receives explicit wiring; a ViewModel cannot access IObjectResolver, a service locator, Unity singletons or scene searches. Prefer injected typed factories when callers create scoped objects. Keep transient disposable objects under an explicit owner; do not assume automatic cleanup for every registration category.

VContainer documents scope disposal and a caveat: disposing a scope alone does not necessarily destroy a still-live registered MonoBehaviour. Specify GameObject ownership as well. [VContainer lifetimes](https://vcontainer.hadashikick.jp/scoping/lifetime-overview).

Startup is an explicit asynchronous coordinator: validate configuration → create required services → preload required content → mount/enable dependents → publish ready. Dependencies determine order; Script Execution Order, Awake ordering and container resolution must not substitute for readiness. Boot UI can display progress/failure without depending on the content currently loading.

Shutdown rejects new work, cancels and joins/quarantines owned async work, disposes children/bindings/ViewModels, then releases services/content and directory registrations. Continue cleanup after one failure and report the aggregate. Container Dispose is not an async shutdown coordinator. Exactly one owner disposes each resource; a binding adapter borrows its ViewModel, the screen owner disposes both in order. See [lifecycle](lifecycle.md).

Prove composition with a real startup/shutdown slice, repeated sessions, missing configuration, partial startup failure and cancelled late loads. CI includes registration resolution and captive-dependency checks for selected profiles; a container existing does not prove registrations are correct.

Disposal failures must not strand sibling resources. Qualify the pinned container’s exception behavior: if its composite stops on a throwing disposer, keep externally owned instances in an explicit reverse-order lifetime that attempts every release and aggregates errors. Do not register both the container and a second owner to dispose the same instance. Pocket Arena uses RegisterInstance for externally owned services.
