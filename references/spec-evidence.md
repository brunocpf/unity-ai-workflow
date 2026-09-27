# Spec evidence and delivery checks

Read when planning check kinds, recording evidence, changing gates or delivering/archiving an increment. The [daily loop](spec-driven-development.md) owns behavior and scope.

Run `python tooling/specs/run.py validate --all --strict --no-interactive`. OpenSpec validates artifact structure, not Unity behavior. Its advisory verifier can aid semantic review but cannot replace actual test execution.

The shipped `tooling/specs/check.py` provides two modes:

- `check --change NAME`: requires unique stable delta IDs and a complete acceptance mapping; permits explicit pending outcomes during development. Checks supplied evidence paths/hashes/metadata.
- `check --change NAME --accept`: additionally requires all mapped outcomes passing, every declared check kind evidenced, completed tasks and a matching source/spec fingerprint.

Use `fingerprint --change NAME` after executing checks and reconciling artifacts. It hashes Git-tracked and nonignored files, normalizing UTF-8 line endings. It excludes evidence under `artifacts/` and `docs/evidence/`, installation receipts, and task/verification bookkeeping. Add generated Unity outputs/node_modules to Git ignores first; do not ignore authored code. LFS assets must be materialized before tests/fingerprinting. Conservative invalidation can require reassessment after unrelated changes. Fingerprints describe working-tree paths/content: deletion or archive invalidates prior evidence, but staging identical content does not.

Evidence entries contain `kind` (automated/visual/authoring/playtest/device), repository-relative `path`, `sha256`, actual `command_or_procedure`, `target`, `run_id`, and actual `reviewer` for manual kinds. Keep durable evidence under docs/evidence or retain it with immutable CI artifacts and restore those files when auditing. Do not recompute fingerprints around old results to disguise stale evidence. Archived fingerprints are historical, not promises about the current tree.

**This gate checks integrity and mapping; it cannot authenticate a self-reported pass or decide which check kinds are sufficient.** Semantic review must verify the required kinds/scenarios, and CI independently runs the actual mapped test/build commands and parses their results. A log file containing a failure is not passing evidence just because its hash matches. Existing [CI](ci.md), [validation](validation.md), visual freshness and deliberate-fault gates remain authoritative.

Incomplete WIP can pass mapping validation, but a delivered increment must pass acceptance checks before archive/merge under project policy. Projects using PRs must require their independent executable checks as well; branch-protection provisioning is a separate, explicitly verified step. For the delivered PR, explicitly select its active change or newly archived `archive/date-name`; do not treat an empty active-change list as success. If archiving/reconciliation changes the fingerprint, run or explicitly re-assess the affected checks against that final tree and record the new receipt before delivery. Do not refresh or current-tree-check unrelated historical archives.
