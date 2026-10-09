# Unity policy for spec-driven development

Use project-local OpenSpec through `python tooling/specs/run.py`. The generated operation skill and CLI-returned instructions own artifact order, context reads, implementation tracking, spec reconciliation and archive mechanics. [Skill ownership](context-efficiency.md#skill-ownership) handles provider selection, operation boundaries and missing integrations; [setup](openspec-setup.md) owns provisioning. This reference contains only project extensions.

## Authority and scope

Accepted capability specs own behavior; baseline plus active deltas define the current target. Intent without implementation evidence is an **unverified baseline**. GitHub Issues/Projects retain delivery ownership, priority and status; link the issue instead of creating a second backlog. Architecture/ADRs, native locks and visual/asset decisions retain their authority; link rather than copy them.

New behavior uses the unity-game schema. Small fixes/tuning/polish keep its artifacts concise. Behavior-preserving tooling/refactors use `skip_specs: true`, preserved invariants and CHANGE-001 evidence. Typo-only docs can use the normal PR record. Migrations include compatibility/recovery without authorizing unrelated upgrades. Clarify consequential unknowns using [clarification](clarification.md).

## Unity extensions

- Stable requirement IDs connect scenarios to shared checks; retire IDs through explicit removal/addition. Removed behavior needs absence/migration checks. Preserve upstream artifact/scenario rules; do not weaken requirements to fit failing tests.
- Design records affected boundaries, lifetimes, authored assets and risks, reusing the established architecture. Tasks include affected tests, visual iteration and authoring preservation; no parallel feature brief or completion report.
- Map changed requirements/scenarios in verification.json using [evidence checks](spec-evidence.md). Keep technical, visual, authoring and required user/device verdicts distinct. Stock OpenSpec structure/readiness does not prove game acceptance.
- Before completed-work archive, pass required checks and verdicts. Partial work stays active or is explicitly split. Archiving neither closes issues nor grants user acceptance; cancellation must not sync abandoned behavior into accepted specs.

Start adoption with the next bounded change, not a whole-game backfill. Preserve known decisions and label unverified intent. See [existing-project upgrade](openspec-setup.md#existing-project-upgrade).
