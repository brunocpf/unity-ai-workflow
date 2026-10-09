# Modules and extensibility

A feature module owns a coherent game capability: inventory, combat, progression, dialogue, world streaming. Keep its folders aligned across Core/Application/Presentation and the relevant Unity layers. The repository remains one deployable game by default; modularity does not imply services or distributed infrastructure.

## Public contract

Record meaningful module boundaries in docs/architecture.md; extract docs/modules/<name>.md only for a substantial independently maintained public contract. Document invariants and ownership, link code for signatures rather than reproducing it:

- Responsibility, owning state and invariants; explicit non-owned concerns.
- Public commands, queries, immutable/read-only snapshots and notification semantics.
- Consumed ports, provider adapters and allowed module dependencies.
- Scope/startup prerequisites, readiness, shutdown and failure behavior.
- Save/content/network schemas and compatibility policy, where applicable.
- Acceptance fixtures, performance budgets and change owner/maintainer role.

Publish the smallest API consumers need. Do not expose mutable collections, implementation entities or provider-specific handles across unrelated modules. Put ports beside their consumer; an adapter implements the port and owns translation. Use one authoritative source for shared concepts; isolate a small shared domain vocabulary only when multiple modules actually need it.

Cross-module commands go through the public use-case surface. Notifications report committed outcomes and cannot secretly define ordering for transactions. An Application coordinator owns operations spanning modules, including rollback/compensation or partial-success policy. Do not create circular dependencies or synchronous event cascades that mutate several owners unpredictably.

## Physical boundaries

Start with explicit layer assemblies and feature namespaces. Types not part of a module API are internal where possible; same-assembly feature boundaries need architecture tests on compiled type references. Split a module into its own Core/Application/Presentation assemblies when independent ownership, API enforcement, compile cost or reuse warrants it. The dependency direction remains unchanged. This is an extraction criterion, not permission for cross-feature access before extraction.

Extract shared UPM packages when reuse has a real consumer and compatibility tests. Runtime/editor/tests are separate; public APIs have versioning and a migration note. Do not move a game-specific system into a framework merely because another game might eventually use it.

## Extension mechanisms

| Change | Default mechanism |
|---|---|
| New item/enemy/ability variant | Validated authoring definitions mapped to domain config; stable IDs |
| New gameplay rule | Explicit strategy/policy at the actual variation point; domain tests |
| New platform/provider | Adapter behind existing consumer-owned port; shared contract tests |
| New screen | Pure ViewModel + view/binding adapter; navigation composition registration |
| New feature module | Module contract + acyclic registrations + integration slice |
| Save/content format change | Explicit version and supported migration/compatibility window |
| Modding / live patching | Separate trust/version/lifetime profile, not arbitrary runtime reflection |

Registrations are explicit and discoverable. Runtime scanning, implicit convention registration and string-based service lookup need demonstrated value plus AOT/stripping tests. Avoid enormous feature switches and subclass trees; use composition without replacing understandable domain code with a generic rules engine.
