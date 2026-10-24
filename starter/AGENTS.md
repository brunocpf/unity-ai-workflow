# Project rules

Apply the kit to ordinary requests without asking the user to restate architecture. Start with the current request and affected source; consult README.md for commands/navigation and docs/project.md or docs/architecture.md for relevant decisions. Use references under docs/standards/references; `INDEX.md` routes unfamiliar work. Create no routine reports or duplicate status docs (`context-efficiency.md`). Real check commands live in the project README.

- Planning/project management is the project's choice; don't install or require a process framework.
- A setup request means project setup; a playable-game request also includes the first slice (adoption.md). Don't create a project just because the kit is installed. Resume existing work; ordinary features don't repeat bootstrap.
- Clarify unresolved platforms, languages, mechanics or consequential choices before dependent work (clarification.md); keep settled answers and continue independent work.
- Core/Application/Presentation stay transitively engine-independent. Use the pinned C# profile and nullable in all owned code, with matching compiler settings across Unity, SDK and IDE projects (code-quality.md, ide.md, code-organization.md).
- Apply the professional baseline at any project size: VContainer scopes, explicit module contracts and architecture tests. R3 owns ongoing state, UniTask finite engine work; every resource has a lifetime owner and stale-result/reload handling.
- UI uses pure MVVM/mechanical R3 adapters, no Presenter layer; native binding owns authored localized properties (ui-binding.md). Controls construct complete visuals, UXML owns USS, and UI Builder works (ui-construction.md).
- Localize player-facing content from the first slice (localization.md). New/substantial UI needs a concrete visual target and a polished representative screen; demo styling is not a target (ui-art-direction.md).
- Preserve editable scenes/prefabs, validated tuning data, GUIDs and Inspector edits (authoring.md). Factories spawn authored assets. Keep concurrent Editor workspaces separate; commit approved assets/metadata/locks with their generation settings.
- Use selected dependency defaults and approved ADR exceptions; add utilities only for actual consumers.
- Test what you changed (testing.md). For visual or gameplay changes, run the game and look at the result against its target. Say plainly what you didn't get to try.
