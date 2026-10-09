---
name: unity-validation-workflow
description: Run or implement Unity tests, CI/build checks, visual acceptance and regression evidence for this workflow.
---

Use project rules and the active OpenSpec change. Reference names below resolve under `docs/standards/references/` (or `references/` in the kit); load only the concern being changed.

Use available Unity CLI skills for Editor operations (`context-efficiency.md#skill-ownership`); this skill owns acceptance, not command syntax. Use existing project check entrypoints and the active change's shared verification map. Read `spec-evidence.md` when planning/delivering checks; acceptance runs declared automated checks and records full machine logs.

1. Select affected cases from `validation.md`. Use `ci.md` for runner/build work, `code-organization.md`/`ide.md` for quality coverage, `test-scenarios.md` for clock/capture provenance, and `lifecycle.md` for reload/resource regressions.
2. Execute meaningful checks and inspect failures. Gate rejection probes are required for setup, changed gates or doubtful enforcement—not every ordinary feature. Distinguish infrastructure failures from behavior failures.
3. For visual work, inspect actual output against the accepted target (`ui-art-direction.md`) and refine defects. For authored content/generators, test Editor edit preservation. For localization, test the affected locale/font/provider contract.
4. Record actual manual verdicts with record-review; automation cannot grant user acceptance. Keep command output in artifacts and summarize results/gaps in the existing change/PR. Don't write a parallel acceptance matrix or completion handoff.

Use `engineering-baseline.md` for template/release qualification; ordinary changes need affected-boundary checks rather than every supported platform. Archive does not waive required acceptance.
