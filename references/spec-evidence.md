# Shared verification and delivery

OpenSpec owns behavior/artifacts; verification.json is the kit's small schema-2 check map. Each requirement ID lists shared check names. Define each check once, even when it covers several requirements/scenarios. No per-requirement result copies or whole-repository acceptance fingerprint.

- **Automated:** kind, executable command argument array and target; optional timeout_seconds (default 600, maximum 7200). `{python}` resolves to the current Python interpreter. Use the project's real check entrypoints, with nonempty-suite/report validation in those entrypoints. Do not wrap known failures in an exit-zero command. Commands run without a shell from the game root.
- **Manual:** kind (visual/authoring/playtest/device), procedure, target and initially pending status. After actually inspecting the result, `record-review` records the reviewer, time and inspected artifact hashes. Never record user acceptance as your own review. Keep required user/device verdicts pending until obtained.

```sh
python tooling/specs/check.py check --change NAME
python tooling/specs/check.py record-review --change NAME --check-id visual --status pass --reviewer agent --artifact docs/evidence/screen.png
python tooling/specs/ci.py --change NAME --quiet
```

`check` validates mappings without executing commands; pending manual checks are valid WIP. `check --accept` requires completed tasks and passing required manual checks, then executes every shared automated check once against the current checkout. A failed command, timeout or missing/changed review artifact fails delivery. Generated logs/results live in a fresh artifacts/verification/run-* directory; retain them through the existing CI artifact policy. The CI wrapper also runs strict OpenSpec validation and active-change mapping checks. Give each suite one CI execution owner: consolidate equivalent existing jobs into this entrypoint, while retaining distinct platform/security/release jobs. Do not list this wrapper recursively as a shared command. Explicitly select the delivered active change or archive/date-name; an empty active-change list is never success.

Read command definitions before running code from an untrusted PR; apply normal CI trust boundaries. Mapping does not establish test sufficiency. Semantic review verifies scenario coverage, appropriate manual kinds and whether existing manual verdicts still apply after changes. Reset affected manual checks to pending when behavior/visuals/targets change. Artifact hashes detect altered evidence, not stale game behavior. Existing capture freshness, authoring preservation, target-player and source-quality gates remain required.

Accept before archive. Archive reconciles behavior; it does not grant product acceptance. After archive, run strict structure validation; do not rerun expensive game checks solely because files moved. Hosted delivery CI runs the explicit archived change's commands on its checkout. Relevant implementation changes still require reruns and manual reassessment. No historical fingerprint refresh, per-archive resealing or parallel acceptance report.

Schema-1 records are historical. Migrate only active/current delivery through the [0.4 migration](upgrades/lean-0.4.0.md); do not upgrade old archives just to satisfy the new helper. Generated upstream OpenSpec integrations and its lifecycle stay unchanged.
