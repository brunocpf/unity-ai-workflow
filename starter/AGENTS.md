# Project rules

Apply these project rules and referenced defaults to ordinary game requests without requiring the user to repeat the architecture.

Read docs/index.md and the current feature/asset brief when they exist. If docs/index.md is absent, only the workflow may be installed: use adoption.md for a requested bootstrap, and do not claim foundation readiness or create the project merely because these instructions loaded. Reference policy lives in docs/standards/references/INDEX.md; load only the relevant subject. Approved ADRs record deviations. Real validation commands live in the project README.

- Bootstrap alone targets Foundation ready; First slice accepted is separate. Follow adoption.md#milestones-and-request-scope for scope and evidence. Continue through both when authorized; setup-only requests stop after foundation checks.
- Default to continuous development: resume existing project state, complete the requested increment, preserve authored work and update a concise handoff when work spans sessions. Follow adoption.md#continuous-development; do not repeat bootstrap for ordinary changes.
- Ask about unresolved intent, including target platforms, languages and mechanics, before dependent implementation; use clarification.md. Preserve prior answers and settled defaults, explain consequential tradeoffs, and continue independent work while awaiting replies.
- Core/Application/Presentation are transitively engine-independent; compile the same sources in Unity and tooling. Use the pinned C# profile.
- R3 owns ongoing state, UniTask engine-side finite work. Every subscription/request/resource has a lifetime owner; handle stale results and fast Play Mode explicitly.
- UI uses pure MVVM with mechanical R3 binding adapters; native binding is the default for authored localized properties and optional for other state. No separate Presenter layer. Follow ui-binding.md.
- Localize player-facing text/assets from the first slice; use localization.md for the pinned native/package API, agreed languages, single locale authority, fonts and acceptance.
- Custom controls construct complete visuals; UXML owns USS. Follow ui-construction.md for the scoped asset-only resolver exception and Builder compatibility.
- New/substantial UI follows ui-art-direction.md: a concrete visual target, a polished representative screen early, and comparison-based visual acceptance separate from technical checks. Kit demo styling is not the game's visual target.
- Apply the professional baseline regardless of team/game size. Use VContainer composition roots, explicit module contracts and required architecture checks.
- Keep authored content editable in Unity: saved scenes/prefabs and validated tuning definitions; factories spawn those assets. Follow authoring.md; setup/build preserves authored changes.
- Align Unity, SDK and generated IDE compiler settings; enable nullable everywhere owned. Follow code-quality.md, ide.md and code-organization.md; require full semantic coverage and organization checks.
- Use selected dependency defaults; record and validate exceptions. Implement utilities only for actual consumers.
- Commit accepted content, metadata and native locks. Preserve GUIDs; separate concurrent Editor workspaces. Generated media follows asset briefs, provenance and agreed budgets.
- Validate the changed boundary. Accelerated tests have one clock owner; captures must pass current-run freshness checks. Visual changes require actual inspection, defect-driven refinement and target-player evidence. Report unverified behavior separately.
