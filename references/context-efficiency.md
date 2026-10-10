# Focused work, minimal records

Default project documents are README.md (commands/navigation), docs/project.md (product decisions) and docs/architecture.md (implementation/authoring map). Keep localization, budgets, compatibility exceptions and visual direction as sections until they need independent ownership or substantial content. Do not generate empty documents, per-feature reports or a duplicate index/status ledger.

- Start with root rules, the current request and affected source. Open project docs only for the relevant decision/map. Select one primary kit skill; delegate mechanics using the ownership table below. Follow conditional references when the task triggers them; do not recursively read links or reread unchanged rules within a session.
- Facts have one owner: the project chooses where requirements and progress live; native locks own versions; code owns API signatures; test reports own outcomes. Design records only implementation deltas, tradeoffs and risks. Link rather than restate.
- During editing run affected checks; run delivery checks once at the completion boundary. Repeat only after relevant changes/failures or where CI requires it. Gate rejection probes belong to gate changes, setup or suspected enforcement failures, not every feature.
- Logs, hashes and command results are machine artifacts. Keep full logs, but read concise status/failure excerpts first. Use targeted file/CLI searches; do not print entire command catalogs or successful logs. Wait between compact CI status checks.
- A handoff is optional: write one only for unfinished work whose next action, blocker or ephemeral context is absent from the active tasks and code. Use the existing project record; no completion handoff or conversation transcript. Ordinary completion uses the PR/final response with links to existing results.
- Move or remove redundant active documents in a reviewed migration, preserving unique decisions, evidence and working links. Do not add a permanent consolidation report or history document merely to describe that cleanup; Git retains ordinary editorial history. Keep actual historical acceptance records labeled and intact.

Examples are optional reference material, not installed runtime frameworks. Adapt tested source for a real consumer; use the release-pinned example links or opt into the complete offline pack. Avoid inventing infrastructure when a verified helper already fits. Installed file count alone is not a token measurement; compare reads, generated prose and repeated tool calls on representative tasks.

## Skill ownership

The kit owns project policy, architecture, acceptance and tested reusable code. Upstream specialist skills own tool procedures. Discover available skills in the current client; names below are capabilities, not assumed install paths. Load only the applicable operation/reference, not every provider skill.

| Work | Procedure owner | Kit contribution |
|---|---|---|
| Unity commands, Editor connection, installation | Unity `unity-cli` skill and its discovered Pipeline instructions | `toolchain.md`: selected pins, readiness/result invariants |
| UPM changes | Unity `unity-package-management` skill | `dependencies.md`: selected libraries and compatibility gates |
| UXML/USS, drawing, custom elements | Unity `ui-uitk` skill's relevant reference | Kit UI references: MVVM/R3, content/lifetime, styling conventions, native navigation and visual acceptance |
| Asset generation/import, localization | Available provider or Unity specialist skill | Kit asset/localization contracts and project decisions |

The kit bootstrap orchestrates project setup; do not also auto-run Unity's `new-unity-project` questionnaire. Carry settled choices into delegated CLI/package operations. Reconcile differences if the user explicitly selects another bootstrap workflow.

Follow independently adopted planning tools through their own instructions; this kit neither installs them nor defines their lifecycle.

For tool procedures, project pins and verified exceptions supersede generic defaults such as latest LTS. Perform available Editor import/diagnostic/visual checks instead of adopting a manual-check fallback unnecessarily; user/device acceptance remains distinct. Surface irreconcilable conflicts before dependent work. Never patch plugin caches.

**Missing providers:** Unity plugins are optional: use installed CLI help/discovery, selected-version official docs and the kit's contracts/examples, with the same acceptance gates. Do not auto-install providers or copy manuals.
