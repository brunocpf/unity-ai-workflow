# Project rules

Apply the kit to ordinary requests without asking the user to restate architecture. Start with the current request and affected source; consult README.md for commands/navigation and docs/project.md or docs/architecture.md for relevant decisions. Use references under docs/standards/references; Create no routine reports or duplicate status docs; `context-efficiency.md` governs minimal records, `INDEX.md` routes unfamiliar work. Real check commands live in the project README.

- Planning/project management is project-owned; do not install or require a process framework. Engineering checks run independently (engineering-checks.md).
- Bootstrap alone means Foundation ready; gameplay/First slice accepted is separate (adoption.md). Do not create a project merely because the kit is installed. Resume existing work; ordinary features do not repeat bootstrap.
- Clarify unresolved platforms, languages, mechanics or consequential choices before dependent work (clarification.md); preserve settled answers and continue independent work.
- Core/Application/Presentation stay transitively engine-independent. Use the pinned C# profile, nullable/compiler parity and full owned-code semantic/organization coverage (code-quality.md, ide.md, code-organization.md).
- Apply the professional baseline at any project size: VContainer scopes, explicit module contracts and architecture checks. R3 owns ongoing state, UniTask finite engine work; every resource has a lifetime owner and stale-result/reload handling.
- UI uses pure MVVM/mechanical R3 adapters, no Presenter layer; native binding owns authored localized properties (ui-binding.md). Controls construct complete visuals, UXML owns USS, and Builder works (ui-construction.md).
- Localize player-facing content from the first slice (localization.md). New/substantial UI needs a concrete visual target and polished representative screen; demo styling is not a target (ui-art-direction.md).
- Preserve editable scenes/prefabs, validated tuning data, GUIDs and Inspector edits (authoring.md). Factories spawn authored assets. Keep concurrent Editor workspaces separate; commit accepted assets/metadata/locks and generation provenance/budgets.
- Use selected dependency defaults and approved ADR exceptions; add utilities only for actual consumers.
- Validate affected boundaries and required delivery gates. Accelerated tests have one clock owner; captures require current-run freshness, actual inspection/refinement and applicable target-player evidence. Keep technical, visual and user verdicts distinct; report gaps honestly.
