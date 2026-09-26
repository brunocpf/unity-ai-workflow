# OpenSpec setup and upgrades

OpenSpec is a **development dependency**, never a Unity package or player dependency. The kit supplies a pinned npm manifest/lock, local launcher, custom schema/templates and structural evidence gate. Workflow installation still only copies passive standards; requested foundation setup or an explicitly authorized workflow migration activates them.

## New foundation

From the game root after installing the kit:

```sh
python3 docs/standards/starter/openspec/setup.py --target . --dry-run
python3 docs/standards/starter/openspec/setup.py --target .
```

Select Node 24.15.0 (declared in tooling/specs/.node-version). Use an installed version manager or provision that version in CI. Verify **both** `node --version` and `npm --version`/npm's runtime; a stale npm executable can use a different Node. `WORKFLOW_NODE` can point the Python launcher at an explicit Node binary. The launcher rejects version mismatches; it never installs/upgrades automatically.

Install the exact dependency graph from the tooling directory, using the selected Node's npm:

```sh
cd tooling/specs
npm ci --ignore-scripts
cd ../..
python3 tooling/specs/run.py init --tools codex,claude --profile core --no-animation
python3 tooling/specs/run.py schema validate unity-game
```

Select only clients actually adopted by the game (`codex`, `claude`, or both). Init generates OpenSpec client integrations separately from the six Unity skills; preserve root instruction routing and inspect the diff. The Unity config already exists, so init retains it. Commit config, schema, generated selected-client files, package manifest/lock, .node-version and helper scripts. Ignore node_modules. Verify live client discovery in a new session; source files alone do not prove it.

Setup staging preflights collisions and refuses different existing files. It does not merge a project's existing OpenSpec config/schema; inspect/reconcile such projects explicitly. Do not run init/update with force to bypass ownership. Two agents must not stage/init the same workspace concurrently.

## Normal use

The Unity skills select the process automatically. The agent uses the pinned launcher for OpenSpec operations, including `new change NAME`, `status --change NAME --json`, and `instructions ARTIFACT --change NAME --json`. New changes inherit the unity-game schema. Follow the installed instruction content and [development loop](spec-driven-development.md), preserving authorized scope.

Create verification.json from the schema template as pending during planning. After implementation, run real checks, inspect results, populate evidence and the fingerprint, then:

```sh
python3 tooling/specs/run.py validate --all --strict --no-interactive
python3 tooling/specs/check.py check --change NAME --accept
python3 tooling/specs/run.py archive NAME --yes
python3 tooling/specs/run.py validate --all --strict --no-interactive
```

After archive, select the returned `archive/date-name` for the delivered increment, reconcile final-tree evidence/fingerprint, and run acceptance mode again before delivery. PR CI must select that change explicitly; an empty active-change list is not a bypass.

Archive is authorized as part of completing an authorized change only after its checks and required product verdicts pass. Cancellation/abandonment must be labeled separately; never sync abandoned behavior into current specs. Do not use direct archive to evade the evidence gate. Stock OpenSpec does not enforce this kit's acceptance policy; PR CI/review must enforce it independently.

## Existing-project upgrade

1. Preserve current working changes and inspect the installed manifest, active issue, accepted decisions and existing CI. Fetch a reviewed kit candidate; run its `install.py assess`, review applicability, then `update --dry-run`, `update` and `check`. See [workflow updates](workflow-updates.md). Managed-file conflicts require reconciliation.
2. Record process adoption as a bounded workflow migration. Preserve the game's engine/packages, source, authored assets and existing evidence. Historical Foundation ready remains historical; record the new process setup status separately.
3. Stage the profile, provision pinned local tooling and initialize selected-client integrations as above. If OpenSpec already exists, map its authority/config first. Keep one canonical behavior location; preserve existing decisions until deliberately reconciled. Rename or replace neither root AGENTS.md nor installed standards.
4. Link the current issue to one active change. Move only its relevant accepted requirements into canonical specs, explicitly identifying unverified intent versus observed behavior. Put new/provisional behavior in deltas. Existing feature briefs become links or historical context; keep supersession/provenance. Do not manufacture specs or issue tickets for the entire backlog.
5. Integrate spec validation in the existing hosted CI job with pinned Node and `npm ci` working-directory tooling/specs. Run mapping checks for active ready/implementing changes. Require acceptance mode for the increment declared delivered by the PR, plus its independent test jobs and manual verdicts. Capture the active change's evidence before archive; archived records retain their tested revision. Never treat no active change after archive as proof of acceptance.
6. Prove missing mappings, stale inputs, failed executable tests and required-but-pending manual review fail the appropriate gate. Verify generated client discovery, continuation, a follow-up delta and archive reconciliation. Record unmet infrastructure requirements honestly, then commit the migration in its own PR/change. No gameplay rewrite is required.

## Reproducibility and maintenance

OpenSpec 1.13.2 and Node 24.15.0 are evaluated pins, not floating latest. Review future security/compatibility releases through the toolchain workflow. Update the tooling lock in place and qualify CLI/schema/integration behavior before regenerating client files. OpenSpec update can read user-global profile settings; inspect generated differences and preserve the project's selected clients/workflows. Kit standards, copied project-owned profile/helper files and generated OpenSpec integrations have distinct ownership: the kit installer does not silently overwrite active project tooling.

The launcher disables telemetry for its own calls. This is not a claim about commands run outside it. Generated upstream skills may show bare `openspec` examples; project rules require substituting the pinned launcher. Framework skill instructions cannot broaden user authorization or replace project-specific acceptance ownership.
