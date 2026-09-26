# Spec-driven continuous development

Default: project-local **OpenSpec 1.13.2**, Node **24.15.0**, the versioned `unity-game` schema and existing Unity task skills. Setup instructions and executable helpers are in [OpenSpec setup](openspec-setup.md). No architecture restatement or slash-command choreography is required from the user: ordinary feature requests trigger this process through project rules and skills.

## Authority and context

- `openspec/specs/<capability>/spec.md` owns accepted behavioral requirements and scenarios. An accepted design intent with no implementation evidence must be labeled **unverified baseline**, never presented as working functionality.
- `openspec/changes/<change>/` owns proposed deltas, design, implementation tasks and verification. The effective target during work is the accepted spec plus the active delta.
- Project rules/ADRs own architecture; native files own version pins; art/asset briefs own visual targets and provenance. Link them from specs rather than duplicating them.
- GitHub Issues/Projects, when adopted, retain work ownership, dependencies and delivery status. Link one bounded change to its issue; OpenSpec tasks are implementation steps, not a second backlog. Archiving does not close issues or prove experiential/user acceptance.
- `docs/index.md` points to current work and authority. Existing feature briefs become navigation, historical proposals or links after reconciliation; never keep competing behavioral contracts. Read only active changes, affected capability specs and relevant standards. Archive completed work; do not inject all historical plans into context.

## Select the route

**New/material behavior:** use the full change schema. **Small fix/tuning/polish:** reuse the affected spec, make the smallest delta and keep proposal/design/tasks short. **Behavior-preserving tooling/refactor/docs work:** set `skip_specs: true` in change metadata, explain preserved invariants, and use CHANGE-001 for its evidence row. This does not waive regression checks. A typo-only documentation fix can use its normal PR record without a new change.

**Bugfix:** capture actual, expected and explicitly unchanged behavior; reproduce the defect, then verify the correction and neighboring invariants. **Exploration:** record the question, bounded prototype and exit decision before committing to a production spec. **Migration:** include compatibility and recovery/rollback; a workflow upgrade does not authorize an engine/package/save migration.

## Loop

1. Inspect the actual project and linked accepted decisions. Create a bounded change; specify outcome, exclusions and stable IDs such as MOVE-001. Clarify consequential ambiguity using [clarification](clarification.md), including unresolved platforms/locales/mechanics. Record assumptions and blocked requirements. Authorization comes from the user's request, not a Ready status or generated approval label.
2. Review requirements for contradictions, missing scenarios and conflicts with existing behavior. Use normative SHALL/MUST outcomes and concrete WHEN/THEN scenarios. Full MODIFIED blocks retain unaffected scenarios. Keep titles/IDs stable; this profile uses explicit remove/add migration when retiring an ID rather than silent renaming. Removed behavior requires absence/migration checks too.
3. Plan affected pure/Unity boundaries, state/resource lifetimes, authored assets and validation. Reuse established library/architecture choices. Arrange tasks as dependency-ordered vertical slices; each owns its tests and documentation. Ready, authorized work continues without ceremonial phase approvals. Spec-only requests stop before implementation; foundation-only requests do not authorize gameplay.
4. Implement and test against the target requirements. Resolve discoveries into the owning spec/design/task, then recheck consistency. For game/UI work follow the visual brief, inspect fresh captures and iterate. Preserve Inspector edits and authored content. Add missing work when evidence or review exposes a gap; do not weaken requirements to make tests pass.
5. Produce `verification.json` mapping every changed requirement to actual evidence. Review all its scenarios, including negative/lifecycle cases. Run OpenSpec validation, independent executable checks and the kit evidence gate. Technical, visual, authoring and required user/device verdicts remain distinct. Pending manual approval remains pending; never impersonate the user as reviewer.
6. Reconcile accepted deltas and archive only after completion checks pass. Retain evidence and link it from the issue/PR. Partial completion remains active or is explicitly split into an accepted increment and remaining work. Preserve supersession links/history. Continue from this baseline next session.

## Acceptance and CI

Run `python tooling/specs/run.py validate --all --strict --no-interactive`. OpenSpec validates artifact structure, not Unity behavior. Its advisory verifier can aid semantic review but cannot replace actual test execution.

The shipped `tooling/specs/check.py` provides two modes:

- `check --change NAME`: requires unique stable delta IDs and a complete acceptance mapping; permits explicit pending outcomes during development. Checks supplied evidence paths/hashes/metadata.
- `check --change NAME --accept`: additionally requires all mapped outcomes passing, every declared check kind evidenced, completed tasks and a matching source/spec fingerprint.

Use `fingerprint --change NAME` after executing checks and reconciling artifacts. It hashes Git-tracked and nonignored files, normalizing UTF-8 line endings. It excludes evidence under `artifacts/` and `docs/evidence/`, installation receipts, and task/verification bookkeeping. Add generated Unity outputs/node_modules to Git ignores first; do not ignore authored code. LFS assets must be materialized before tests/fingerprinting. Conservative invalidation can require reassessment after unrelated changes.

Evidence entries contain `kind` (automated/visual/authoring/playtest/device), repository-relative `path`, `sha256`, actual `command_or_procedure`, `target`, `run_id`, and actual `reviewer` for manual kinds. Keep durable evidence under docs/evidence or retain it with immutable CI artifacts and restore those files when auditing. Do not recompute fingerprints around old results to disguise stale evidence. Archived fingerprints are historical, not promises about the current tree.

**This gate checks integrity and mapping; it cannot authenticate a self-reported pass or decide which check kinds are sufficient.** Semantic review must verify the required kinds/scenarios, and CI independently runs the actual mapped test/build commands and parses their results. A log file containing a failure is not passing evidence just because its hash matches. Existing [CI](ci.md), [validation](validation.md), visual freshness and deliberate-fault gates remain authoritative.

Incomplete WIP can pass mapping validation, but a delivered increment must pass acceptance checks before archive/merge under project policy. Projects using PRs must require their independent executable checks as well; branch-protection provisioning is a separate, explicitly verified step. For the delivered PR, explicitly select its active change or newly archived `archive/date-name`; do not treat an empty active-change list as success. If archiving/reconciliation changes the fingerprint, run or explicitly re-assess the affected checks against that final tree and record the new receipt before delivery. Do not refresh or current-tree-check unrelated historical archives.

## Continuous adoption

Existing projects start with the next bounded change. Reconcile known decisions and observed behavior; mark undocumented/unverified baselines honestly. Do not backfill the entire game or reinterpret historical proposals as implemented requirements. Follow [upgrade procedure](openspec-setup.md#existing-project-upgrade) and preserve selected issue/approval policies.

Sources: [OpenSpec lifecycle](https://github.com/Fission-AI/OpenSpec/blob/v1.13.2/docs/overview.md), [schema/config customization](https://github.com/Fission-AI/OpenSpec/blob/v1.13.2/docs/customization.md), [released advisory verifier](https://github.com/Fission-AI/OpenSpec/blob/v1.13.2/skills/openspec-verify-change/SKILL.md). The Unity schema and evidence gate are this kit's integration, not upstream guarantees.
