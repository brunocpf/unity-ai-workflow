# Project documents

Create three entrypoints; omit unused sections. These hold project-specific facts, not copies of kit standards.

## README.md

- Setup and actual check/build/run commands.
- Links to project decisions, architecture and existing project records.
- Foundation/first-slice milestone once established, with result links and remaining setup gaps. Use the project’s existing progress tracking.

## docs/project.md

- Premise, intended scope and current acceptance slice.
- Agreed platforms/devices/input, languages and accessibility.
- Save/network requirements and target performance budgets.
- Visual direction, inspected references and accepted visual target.
- Unresolved product decisions and what they block.

## docs/architecture.md

- Source/module map, boundaries, state/lifetime owners and cross-module invariants.
- Editor entry scenes, prefabs, tuning definitions and generation ownership.
- Links to native tool/package locks, actual setup scripts and check commands.
- Localization/content/provider ownership and relevant compatibility exceptions.
- Material decisions with rationale/revisit triggers; extract an ADR only when it needs independent history.

## Conditional records

A substantial module API, art bible, asset batch, localization pipeline or compatibility matrix can have its own document. Split when it has an independent owner/change cadence or obscures the entrypoint, not because a template lists it. Asset provenance stays machine-readable beside accepted source assets; generation tools collect IDs, settings and hashes where possible. Keep only relevant fields for that asset type.

No required per-feature artifacts, status tables or completion reports. Keep a short continuation note only when unfinished work needs context absent from the code and existing records.
