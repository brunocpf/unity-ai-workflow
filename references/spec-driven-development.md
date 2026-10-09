# Spec-driven continuous development

Use project-local OpenSpec through `python tooling/specs/run.py`; setup/version pins live in [setup](openspec-setup.md). Ordinary requests trigger this process; no user command choreography or repeated architecture prompt is needed.

## Authority and context

- `openspec/specs/<capability>/spec.md`: accepted behavioral requirements. Accepted intent without implementation evidence is an **unverified baseline**, not working functionality.
- `openspec/changes/<change>/`: proposed deltas, design, tasks and verification. The current target is baseline plus active delta.
- GitHub Issues/Projects retain delivery ownership, priority and status. Link the issue; tasks are implementation steps, not a second backlog. Archiving does not close issues or grant user acceptance.
- Architecture/ADRs, native locks and visual/asset briefs retain their authority; link rather than copy them. Consolidate redundant feature briefs after preserving unique decisions.

## Select the route

New behavior uses the change schema. Small fixes/tuning/polish keep its artifacts concise. Behavior-preserving tooling/refactors use `skip_specs: true`, preserved invariants and CHANGE-001 evidence; regression checks still apply. Typo-only docs can use the normal PR record. Bugs specify actual, expected and unchanged behavior. Exploration records a bounded question and exit decision. Migrations include compatibility/recovery without authorizing unrelated upgrades.

## Loop

1. Read current project decisions, affected capability specs and active change. Clarify consequential unknowns before dependent work using [clarification](clarification.md). Authorization comes from the request, not generated readiness labels.
2. Specify observable SHALL/MUST outcomes and WHEN/THEN scenarios with stable IDs. Review contradictions and missing cases. Full MODIFIED blocks preserve unaffected scenarios; retire IDs through explicit removal/addition. Removed behavior needs absence/migration checks.
3. Plan affected boundaries, lifetimes, authored assets and validation kinds. Reuse established architecture; link decisions rather than repeating standards. Arrange dependency-ordered slices with tests. Continue authorized work without ceremonial phase approvals; spec-only and foundation-only scope remain limited.
4. Implement, test and reconcile discoveries into the owning artifacts. Inspect fresh visual output and iterate when relevant; preserve authored edits. Do not weaken requirements to fit failing tests.
5. Map changed IDs/scenarios to shared checks in verification.json using [evidence checks](spec-evidence.md). Keep technical, visual, authoring and required user/device verdicts distinct; pending acceptance stays pending.
6. After required checks/verdicts pass, reconcile specs and archive. Validate the final delivered tree. Partial work stays active or is explicitly split; retain evidence/provenance and resume from this baseline next session.

## Acceptance and CI

[Evidence checks](spec-evidence.md) owns shared commands, manual verdicts and delivery checks. OpenSpec structure checks and the kit's integrity checker do not replace independent tests or semantic/manual review. Read that reference when defining verification, implementing gates or delivering a change; no need to reload unchanged gate internals during each edit.

## Continuous adoption

Start with the next bounded change, not a whole-game backfill. Preserve known decisions and label unverified intent. Use the [existing-project upgrade](openspec-setup.md#existing-project-upgrade). [Context discipline](context-efficiency.md) keeps context focused without skipping OpenSpec artifacts or requirements.

Sources: [OpenSpec lifecycle](https://github.com/Fission-AI/OpenSpec/blob/v1.13.2/docs/overview.md), [schema/config](https://github.com/Fission-AI/OpenSpec/blob/v1.13.2/docs/customization.md). Unity-specific evidence rules are kit additions.
