# Unity AI workflow kit

Opinionated professional architecture for long-lived Unity projects: modular boundaries, MVVM, scoped composition and enforceable quality gates, with source examples and task skills. **A reusable standards/source kit, not a certified project template.** Pocket Arena supplies one evaluated macOS implementation; see the [field evaluation](REVIEW.md#pocket-arena-field-evaluation--18-september-2026) for evidence and limits. Current evaluation target: **Unity 6000.7.0b2 / CLI 1.0.0-beta.10**. See the [b2 upgrade record](references/upgrades/unity-6000.7.0b2.md) for release changes, fresh API/pure checks and pending Editor/player acceptance; compiler/package setup is checked during bootstrap; runtime and platform compatibility require slice acceptance.

## Start a new project

Open the destination folder in a new session and say:

> Use the Unity workflow kit at `<absolute-kit-path>/README.md` to bootstrap the foundation for [game concept, intended scope and constraints].

Bootstrap alone ends at **Foundation ready**. To request both milestones, add: “Then implement and validate the first playable slice.” **First slice accepted** is a separate status; see [milestone criteria](references/adoption.md#milestones-and-request-scope).

That is enough workflow input. The agent must follow the [bootstrap skill](skills/unity-project-bootstrap/SKILL.md), adopt the kit locally, and apply its architecture, dependency, asset and acceptance defaults without asking the user to repeat them. A request to try/test the workflow selects its evaluation profile. Product details and explicit overrides belong in the brief; technical defaults belong in the kit. The agent [asks about unresolved intent](references/clarification.md), including target platforms, supported languages and unclear mechanics, while continuing independent work; you do not need to pre-answer an architecture questionnaire.

After adoption, project-root AGENTS.md routes future sessions to the local standards and task skills. The originating kit path is no longer required for ordinary work. There is no global installation requirement; a downloaded kit does not automatically apply to an unrelated project.

**Continuous development is the default:** bootstrap once, then evolve the same project across tasks and sessions. Prompts can simply request a feature, fix, balance change or visual refinement; the adopted rules supply the architecture. Use [WORKFLOW.md](WORKFLOW.md) and read only the references needed for the current task.

| Task | Entry |
|---|---|
| Foundation / first slice / template release | [Bootstrap skill](skills/unity-project-bootstrap/SKILL.md) |
| Gameplay feature | [Feature skill](skills/unity-feature-workflow/SKILL.md) |
| Custom control / binding / styling | [UI skill](skills/unity-ui-workflow/SKILL.md) |
| Languages / translated UI | [Localization](references/localization.md) |
| Ambiguous requirements / consequential choices | [Clarification](references/clarification.md) |
| Game UI design / visual quality | [Art direction](references/ui-art-direction.md) |
| Generate/import art or animation | [Asset skill](skills/unity-asset-workflow/SKILL.md) |
| Tests / visual review / CI | [Validation skill](skills/unity-validation-workflow/SKILL.md) |
| Dependencies / editor upgrades | [Toolchain skill](skills/unity-toolchain-workflow/SKILL.md) |
| Concrete resolver / controls / MVVM | [Source examples](examples/README.md) |
| Reference navigation | [Index](references/INDEX.md) |
| Install kit into a project | [Adoption](references/adoption.md) |

Engineering contract: [baseline](references/engineering-baseline.md), [assembly/module architecture](references/architecture.md), [Editor authoring](references/authoring.md), [code quality](references/code-quality.md), [local tooling/hooks](references/developer-tooling.md), [IDE setup](references/ide.md) and [code organization](references/code-organization.md).

Copyable files: [AGENTS.md](starter/AGENTS.md), [.editorconfig](starter/.editorconfig), [.gitignore](starter/.gitignore), [.gitattributes](starter/.gitattributes), [Core asmdef](starter/Game.Core.asmdef), [Unity compiler options](starter/csc.rsp), [SDK build defaults](starter/Directory.Build.props), [UI styling fixture](starter/UI/README.md), [document forms](starter/DOCUMENT-TEMPLATES.md).

Historical: [installation record](INSTALLATION.md). Maintenance: [review](REVIEW.md). Neither is routine task context.

References own policy; skills route and apply it. Approved project ADRs describe deviations. Native version/package files own resolved versions. Claims of implementation, test success or measured performance require evidence from the actual template.
