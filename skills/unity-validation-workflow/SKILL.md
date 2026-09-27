---
name: unity-validation-workflow
description: Run or implement Unity tests, CI/build checks, visual acceptance and regression evidence for this workflow.
---

References resolve under `docs/standards/references/` (or `references/` at the kit root). Follow project rules, the active change and `context-efficiency.md`; load only sections triggered by this task.

Use `clarification.md` if acceptance behavior is ambiguous rather than inventing a passing interpretation. Read `localization.md` for text/content/locale validation and the supported-language matrix.

Use established project check commands; read affected cases in `validation.md`. Include `engineering-baseline.md` for template/release acceptance and `code-quality.md` for compiler/analyzer gates. For IDE/regeneration or formatting/organization coverage add `ide.md` and `code-organization.md`. For runner/build changes add `ci.md`; for acceleration/capture evidence add `test-scenarios.md`; for version/API issues add `toolchain.md`; for Play/session leaks add `lifecycle.md`.

Use documented project entrypoints, or implement the missing check within scope. Separate discovery/infrastructure failures from failing behavior. Run capture scenarios and actually inspect outputs; refine observed defects and rerun affected checks. Retain durable reports and before/after evidence.

For visual acceptance/evaluations, apply `ui-art-direction.md` to the actual screen and its target/reference images. Judge composition, identity, hierarchy, feedback and completeness separately from functional passes. User rejection reopens visual acceptance; do not defend it with test counts or successful captures.

Runtime success does not establish authoring usability. For authored content or generation changes run the authoring-edit and preservation checks in validation.md.

For a first template/CI implementation prove required gates reject deliberate faults, then pass from a clean checkout. For an ordinary change select affected boundaries rather than rebuilding every platform.

Apply `spec-driven-development.md`; use `spec-evidence.md` when defining verification or delivering the increment.
