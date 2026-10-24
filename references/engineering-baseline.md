# Professional engineering baseline

This kit defines durable project standards independently of team size or game scope. It is a set of conventions and tested examples, not a finished production template. A small first slice does not replace the planned game.

## Required baseline

| Area | Required capability |
|---|---|
| Architecture | Inward layer/module boundaries, pure Presentation MVVM, explicit scopes; a compiled dependency check keeps layers honest |
| Editor authoring | Saved scenes/prefabs, editable definitions validated at startup, generation that preserves edits ([authoring](authoring.md)) |
| Composition | VContainer roots, readiness and owned shutdown |
| Source quality | Nullable in all owned code, pinned analyzer/style/organization rules, explicit asmdefs |
| IDE | Tracked setup, generated Unity solution, matching compiler settings across Unity, SDK and IDE projects |
| Rules and integration | Unit tests for game rules and use cases; contract tests for providers |
| UI | Testable ViewModels, mechanical binding, UI Builder support, selected content path |
| Localization | Agreed language scope, table-backed player text, one locale authority, provider/font ownership ([localization](localization.md)) |
| Visual design | Distinctive game UI with a concrete visual target and a consistent screen/control language ([art direction](ui-art-direction.md)) |
| Persistence | Versioning, recovery and migration if persistent data exists |
| Operations | Structured failures, bounded resources, one owner for simulation time, target performance budgets |
| Assets | Reimportable content, stable identifiers, budgets, generation sources kept |
| Delivery | Same checks locally and in CI, locked inputs, reproducible builds, rollback |
| Evolution | Module contracts, ADRs, versioned migrations |

[Testing](testing.md) covers what to test; [CI](ci.md) covers the pipeline.

## Change discipline

Before substantial work, be clear about observable behavior, affected module APIs, migrations and failure paths. Inspect the existing implementation and local instructions, [clarify unresolved intent](clarification.md), choose the owning module, then work within it. Don't invent a parallel framework or reopen established dependencies for each feature. Update changed contracts and tests in the same change; ADRs cover genuine deviations, not routine code decisions.

Main stays buildable. Keep changes reviewable, with risk/compatibility notes for public APIs, save schemas, content IDs and package upgrades. Shared repositories can use CODEOWNERS and protected branches. Review generated asset replacements as deliberate product changes.

Upgrading an existing game uses a reviewed branch with save/content compatibility tests; never overwrite its rules or locks from a moving kit directory. Flaky tests get fixed or removed, not rerun until green.

## Scope and flexibility

Module count, network topology, simulation style and rendering profile follow the game. Add interfaces at real substitution boundaries and packages at actual capability boundaries. Don't add microservices, a universal message bus, event sourcing or generic framework layers to look enterprise-grade. Extensibility means explicit contracts and safe change, backed by tests.
