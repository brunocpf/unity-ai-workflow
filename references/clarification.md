# Clarify unresolved decisions

**Ask the user when intent or requirements are ambiguous.** First inspect the brief, project docs, existing behavior and accepted answers. Apply established kit/project defaults when they fit. An unspecified implementation detail is not automatically an ambiguous requirement; an unanswered product choice must not silently become one of the AI's architectural assumptions.

This applies at bootstrap and whenever new uncertainty appears during design, implementation, testing, art generation or review. Do not wait until the end to reveal a decision that could change the result.

## What to ask

| Unresolved choice | Example question / next step |
|---|---|
| Target platforms | “Which platforms should the game support at launch—Windows, macOS, Linux, web, Android/iOS, console or XR—and which is the primary target for the first slice?” Resolve ambiguous labels such as “PC” and ask about minimum devices/input where they affect rendering, performance, dependencies or CI. Keep later platform candidates separate. Do not infer targets from the development machine. |
| Audience and localization | “Which languages and regional variants should the game support at launch, and which is the source language?” Ask separately about voice only if relevant; never infer these from the user's location or chat language. |
| Gameplay semantics | “Does a failed placement consume energy, or only a successful placement? I recommend charging only on success because it makes experimentation forgiving.” Resolve before encoding the rule and its acceptance tests. |
| Scope or constraints | “Is this a workflow trial or a project intended to ship?” Ask if existing context does not resolve the distinction; architecture remains the kit baseline either way. |
| Visual or interaction direction | “Should the map feel like an illustrated travel journal or a nautical instrument panel? The first better supports the relaxed tone.” Use concrete references when they help. |
| Dependency/framework fit | “The selected networking default assumes a server, but the brief asks for offline peer play. Which hosting constraint should we prioritize?” Investigate compatibility first; recommend one option and explain the player, maintenance or cost consequence. |
| Generation budget or external service | “May this asset pass use paid generation, and what is its credit budget?” Ask only if the scope/budget is not already authorized; preserve prior limits. |
| Conflicting requirements or review feedback | State the conflicting behaviors and ask which should win. Do not quietly discard one or claim both are satisfied. |

Do not make users choose between unfamiliar library names without guidance. Use the [selected dependency](dependencies.md) when it meets known needs. Ask about a consequential departure or an unresolved constraint, not whether to use R3, UniTask, VContainer, MVVM or tests on every project. Research can resolve technical uncertainty; the user resolves product preferences and tradeoffs that remain unclear.

## Conversation and execution

1. Ask the smallest useful batch, normally one to three short questions. Give a recommendation and meaningful alternatives when appropriate; allow a free-text answer. Use the environment's question tool when available, otherwise ask plainly in conversation.
2. Explain why each answer matters. Ask at the point it can affect a decision, before committing dependent work. Continue independent work, such as repository inspection, infrastructure or unrelated features, while awaiting a reply.
3. A pending question is not an answer or approval. For unresolved behavior, target platforms, supported languages, paid-service scope or consequential technical choices, leave dependent work pending. For an optional preference, after a reasonable opportunity to respond, a reversible provisional choice may be stated and recorded; never report it as user-approved. Do not introduce a separate permission gate for ordinary authorized work.
4. Record accepted answers and the affected contract in `docs/project.md`, the feature brief or art/localization document. Record pending questions with what they block and any provisional assumption. ADRs are for material technical deviations, not every answer.
5. On resume, read those records and reuse decisions. Ask again only if new evidence creates a conflict or changes the tradeoff. Report any remaining unanswered requirement and its practical impact in the handoff.

The user's game brief remains enough to start. Clarification discovers missing product intent; it must not require the user to restate the kit or fill a large architecture questionnaire.
