# Professional engineering baseline

This kit defines durable project standards independently of team size or game scope. It is a specification with selected verified examples, not a certification or a fully implemented production template. Foundation ready verifies setup; First slice accepted verifies the initial gameplay integration. Follow the separate [milestone criteria](adoption.md#milestones-and-request-scope). A small acceptance slice does not replace the planned game or excuse omitted release gates.

## Required baseline

| Area | Required capability | Evidence before template release |
|---|---|---|
| Architecture | Inward layer/module boundaries, pure Presentation MVVM, explicit scopes | Separate pure compilation; compiled dependency/cycle/API checks reject a planted violation |
| Editor authoring | Saved scenes/prefabs, validated editable definitions, safe generation | Inspector/layout edits work without C# and survive Play/reimport/build; [authoring contract](authoring.md) |
| Composition | VContainer roots, readiness and owned shutdown | Real startup + partial failure + repeated session tests |
| Source quality | Nullable all-owned code, pinned analyzer/style/organization rules, explicit asmdefs | Complete semantic coverage; compiler/analyzer/format/organization gates reject faults |
| IDE | Tracked setup, generated Unity solution, three-host compiler parity | Completion/navigation/diagnostics after regeneration; vendor settings preserved |
| Rules and integration | Deterministic rule tests where applicable; use-case and provider contract tests | Nonempty suites, failure paths, actual composed slice |
| UI | Testable ViewModels, mechanical binding, authoring support, selected content path | Pure VM tests; Builder, recycling and cold-player evidence |
| Localization | Agreed language scope, table-backed player text, one locale authority and provider/font ownership | [Localization acceptance](localization.md#acceptance-and-ci): nonempty coverage, rejected missing/invalid entries, Builder and cold-player locale evidence |
| Visual design | Distinctive game UI, a concrete visual target and consistent screen/control language | [Art-direction acceptance](ui-art-direction.md) against actual player output; composition, identity, hierarchy, feedback and completeness judged separately from technical tests |
| Persistence | Versioning, recovery and migration if persistent data exists | Old-save fixtures, corrupt/interrupted-write recovery |
| Operations | Structured failures, bounded resources, exclusive simulation driver and target budgets | Fault injection, clock-handoff tests, fresh capture evidence and representative profiling |
| Assets | Reimportable accepted content, lineage, budgets and stable identifiers | Provider output archived; import/rig/alpha/visual checks |
| Delivery | Local/CI parity, locked inputs, content/player provenance, rollback | Clean build/launch and immutable release manifest |
| Evolution | Module contracts, ADRs, template version and migrations | Reviewed compatibility changes and upgrade procedure |

Implement a project status table mapping each requirement to commands, owners and evidence. Not applicable requires a concrete reason; unavailable licensing/CI/platforms remain explicit gaps. Do not fill a table with aspirations and call the baseline implemented. [Validation](validation.md) owns test detail; [CI](ci.md) owns the execution pipeline.

## Change and release discipline

A feature contract defines observable behavior, affected module APIs, migrations, failure paths and acceptance before substantial implementation. AI inspects the existing implementation and local instructions, [clarifies unresolved intent](clarification.md), chooses the owning module, then works within the contract. Do not invent a parallel framework or reopen established dependencies for each feature. Update changed contracts and test evidence in the same change; ADRs cover genuine deviations, not routine code decisions.

Main stays buildable. Keep changes reviewable, with risk/compatibility notes for public APIs, save schemas, content IDs and package upgrades. Assign module/asset ownership as roles even for one developer; shared repositories can enforce these through CODEOWNERS and protected-branch checks. Review generated asset replacements and visual-baseline updates as deliberate product changes.

Every template release has an immutable version/tag, verified target matrix, dependency inventory/licenses, known limitations and migration notes. New games pin that release. Upgrading an existing game uses a reviewed migration branch with save/content/backward-compatibility tests; never overwrite its rules or locks from a moving kit directory. Retain shipped binaries/content, symbols, configuration and provenance needed to diagnose or roll back a release. Secret/signing operations run only in trusted jobs.

CI is tiered: fast pure/architecture checks on normal changes; relevant Editor/player/visual suites on impacted boundaries; full supported-target clean/compatibility/performance checks for release. Flaky tests need a tracked owner and removal/fix criteria; repeated reruns do not make failures disappear.

## Scope and flexibility

Module count, network topology, simulation style and rendering profile follow the game. Standards for isolation, ownership, reliability and evidence remain. Add interfaces at real substitution boundaries; add packages at actual capability boundaries. Do not add microservices, a universal message bus, event sourcing or generic framework layers merely to look enterprise-grade. Extensibility means explicit contracts and safe change, backed by tests.
