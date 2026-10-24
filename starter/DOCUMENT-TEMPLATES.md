# Project documents

Create three entrypoints; omit unused sections. These hold project-specific facts, not copies of kit standards.

## README.md

- Setup and actual check/build/run commands.
- Links to project decisions, architecture and existing project records.
- Any setup gaps (for example, CI not yet wired). Use the project's existing progress tracking for everything else.

## docs/project.md

- Premise, intended scope and the current slice.
- Agreed platforms/devices/input, languages and accessibility.
- Save/network requirements and target performance budgets.
- Visual direction, references and the approved visual target.
- Unresolved product decisions and what they block.

## docs/architecture.md

- Source/module map, boundaries, state/lifetime owners and cross-module invariants.
- Editor entry scenes, prefabs, tuning definitions and generation ownership.
- Links to native tool/package locks, actual setup scripts and check commands.
- Localization/content/provider ownership and relevant compatibility exceptions.
- Material decisions with rationale/revisit triggers; extract an ADR only when it needs independent history.

## Conditional records

A substantial module API, art bible, asset batch, localization pipeline or compatibility matrix can have its own document. Split when it has an independent owner/change cadence or obscures the entrypoint, not because a template lists it. Generation settings (prompt, seed, model, job ID) stay beside approved source assets. Keep only fields relevant to that asset type.

No required per-feature artifacts, status tables or completion reports. Keep a short continuation note only when unfinished work needs context absent from the code and existing records.
