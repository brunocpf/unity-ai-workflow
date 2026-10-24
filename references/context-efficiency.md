# Focused work, minimal records

Default project documents are README.md (commands/navigation), docs/project.md (product decisions) and docs/architecture.md (implementation/authoring map). Keep localization, budgets, compatibility exceptions and visual direction as sections until they need independent ownership or substantial content. Don't generate empty documents, per-feature reports or a duplicate index/status ledger.

- Start with root rules, the current request and affected source. Open project docs only for the relevant decision/map. Select one primary kit skill; delegate tool mechanics using the ownership table below. Follow conditional references when the task triggers them; don't recursively read links or reread unchanged rules within a session.
- Facts have one owner: the project chooses where requirements and progress live; native locks own versions; code owns API signatures. Design notes record only decisions, tradeoffs and risks. Link rather than restate.
- While editing, run the checks for what you changed; run the full checks once before finishing. Repeat only after relevant changes or failures.
- Read concise status/failure output first; use targeted file/CLI searches; don't print entire command catalogs or successful logs.
- A handoff note is optional: write one only for unfinished work whose next action, blocker or context isn't already in the tasks and code. Ordinary completion uses the PR or final response.
- When cleaning up redundant documents, keep unique decisions and working links. Don't add a report describing the cleanup; Git keeps the history.

Examples are optional reference material, not installed runtime frameworks. Adapt tested source for a real consumer; use the release-pinned example links or install the complete example pack. Reuse an existing helper before inventing new infrastructure.

## Skill ownership

The kit owns project policy, architecture and tested reusable code. Upstream specialist skills own tool procedures. Discover available skills in the current client; names below are capabilities, not assumed install paths. Load only the applicable operation/reference, not every provider skill.

| Work | Procedure owner | Kit contribution |
|---|---|---|
| Unity commands, Editor connection, installation | Unity `unity-cli` skill and its Pipeline instructions | `toolchain.md`: selected pins, completion rules |
| UPM changes | Unity `unity-package-management` skill | `dependencies.md`: selected libraries and compatibility notes |
| UXML/USS, drawing, custom elements | Unity `ui-uitk` skill's relevant reference | Kit UI references: MVVM/R3, content/lifetime, styling conventions, native navigation and art direction |
| Asset generation/import, localization | Available provider or Unity specialist skill | Kit asset/localization contracts and project decisions |

The kit bootstrap orchestrates project setup; don't also auto-run Unity's `new-unity-project` questionnaire. Carry settled choices into delegated CLI/package operations. Reconcile differences if the user explicitly selects another bootstrap workflow.

Follow independently adopted planning tools through their own instructions; this kit neither installs them nor defines their lifecycle.

For tool procedures, project pins and recorded exceptions take precedence over generic defaults such as latest LTS. Use the Editor's import, diagnostics and screenshots yourself rather than asking the user to check things you can check. Surface irreconcilable conflicts before dependent work. Never patch plugin caches.

**Missing providers:** Unity plugins are optional: use installed CLI help, selected-version official docs and the kit's contracts/examples. Don't auto-install providers or copy manuals.
