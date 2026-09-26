# Architecture and C#

**Default: a modular monolith with inward dependencies, explicit composition and MVVM presentation.** This baseline applies to prototypes, solo work and large productions. Scope controls which features exist, not whether boundaries, ownership or acceptance apply. Deliver vertical slices without creating a separate throwaway architecture.

## Assembly contract

| Assembly | Owns | Allowed project dependencies |
|---|---|---|
| Game.Core | Domain values, rules, invariants and state transitions | None |
| Game.Application | Use cases, consumer-owned ports, authoritative session state and R3 projections | Core |
| Game.Presentation | Engine-independent ViewModels, presentation snapshots, UI command coordination | Application, Core |
| Game.Unity.Runtime | Engine/platform/persistence/network/content adapters | Application, Core |
| Game.UI | Custom controls, binding/presentation adapters (including localization), view-only behavior and UI asset resolution | Presentation, Core |
| Game.Composition | Container registrations, startup/session hosts and screen/module factories | All runtime assemblies |
| Game.Editor | Authoring/build/validation tools | Needed runtime assemblies; Editor-only |
| Explicit test assemblies | Tests and test doubles | Only the boundaries under test; never referenced by production |

Core, Application and Presentation are transitively engine-independent, including all imported DLLs. Core remains dependency-free apart from supported BCL. Application and Presentation may use approved pure R3 dependencies. UI sees application behavior through ViewModels; it does not resolve or call use cases directly. Composition supplies factories across outer boundaries; UI and Runtime do not depend on one another. Editor runtime previews are test/authoring composition, not a backdoor player dependency.

Use noEngineReferences=true, autoReferenced=false, explicit references and overrideReferences=true for pure asmdefs, listing only approved precompiled dependencies. Runtime asmdefs also use explicit references/autoReferenced=false; review package dependencies. No production Assembly-CSharp. Compile the same pure sources independently in SDK projects; inspect actual compiled assembly references for transitive purity. Namespace scans alone are insufficient. [Asmdef fields](https://docs.unity3d.com/6000.7/Documentation/Manual/assembly-definition-file-format.html).

[Modules](modules.md) defines public contracts and extraction triggers; [composition](composition.md) defines scopes. Assembly-per-class and a global Shared/Utils dumping ground are not the baseline. Technical infrastructure that has no domain meaning must not accumulate in Core: move proven reusable code into an explicit foundation assembly/package with a narrow contract when warranted. The small ScopedContext example is an isolated pure helper, not a domain service.

## Rules and state

Application commands orchestrate Core rules and ports. Publish coherent read-only snapshots after accepted transitions. Mutable state has one owner; consumers cannot bypass validation through writable subjects, ScriptableObjects or public collections. Domain services are meaningful game concepts, not generic CRUD managers. Use stable typed IDs at module/save/network boundaries where mixing IDs is a risk.

Define state transitions and ownership before adding asynchronous work. Record ordering, cancellation and retry policy in the feature contract. Unity physics, navigation, rendering and device input stay in adapters. Inputs become domain commands; presentation events do not define authoritative combat/economy behavior. ScriptableObjects are validated authoring definitions, compiled into immutable pure configuration; mutable session state is created separately. Saved scenes and prefabs own authored layout/visual configuration; runtime factories spawn and wire those assets. Follow the [Editor authoring contract](authoring.md).

Do not require event sourcing, a mediator, generic repositories or a global event bus. Explicit command/query ports and scoped R3 streams are the default. Online authority, deterministic simulation and ECS are deliberate profiles with contracts; they do not bypass these boundaries. Shared mutable state or static resolution requires an ADR with a narrow, tested lifetime. UiTemplates is the sole predefined exception, limited to structural UI assets.

## Language and enforcement

Temporary compatibility profile: C#9 / netstandard2.1 with block namespaces. The modern profile adopts C#14 as soon as the selected Unity build passes its capability gates. Both enable nullable in all owned code via per-asmdef csc.rsp and SDK settings. Modern SDKs do not change Unity's language/API support. Records/init, newer syntax, reflection and generated code require compiler/serialization/AOT evidence. [Toolchain](toolchain.md) owns future CoreCLR/C#14 migration and analyzer configuration.

Prefer immutable snapshots and explicit ownership. Interfaces live at module/provider/test substitution boundaries; do not mirror every concrete class mechanically. Select allocations/LINQ based on frequency and measurement. Domain time/RNG are explicit inputs when repeatability matters; a seed does not make Unity physics deterministic.

Treat purity, dependency direction/cycles, public module surfaces and forbidden static/service-location patterns as executable architecture checks. [Validation](validation.md) and [engineering baseline](engineering-baseline.md) specify the required gates. The checked-in SDK examples prove selected boundaries; adopting projects must enforce their actual asmdefs and package graph.
