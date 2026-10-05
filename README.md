# Unity AI workflow kit

Opinionated professional architecture for long-lived Unity projects: modular boundaries, MVVM, scoped composition and enforceable quality gates, with source examples and task skills. **A reusable standards/source kit, not a certified project template.** Pocket Arena supplies one evaluated macOS implementation; see the [field evaluation](REVIEW.md#pocket-arena-field-evaluation--18-september-2026) for evidence and limits. Editor evaluation target: **Unity 6000.7.0b3**. CLI versions are selected per project; see the [version policy](references/toolchain.md#cli) and [beta.11 command check](verification/cli-beta11.md). See the [b3 upgrade record](references/upgrades/unity-6000.7.0b3.md) for release changes, installation checks and project-specific acceptance requirements; compiler/package setup is checked during bootstrap; runtime and platform compatibility require slice acceptance.

## Install globally (recommended)

Requires Python 3.10+. Clone separately from game workspaces, then install the two global entrypoints for Codex and Claude Code:

```sh
git clone https://github.com/brunocpf/unity-ai-workflow.git
cd unity-ai-workflow
python3 install.py install-global --agent both
python3 install.py check-global
```

Choose `codex`, `claude` or `both`. Restart/open a new client session after installation. A complete versioned copy lives in `~/.local/share/unity-ai-workflow/kits/`; the original checkout is no longer needed to start projects. Existing games keep their project-local versions.

## Start a new project

Open an empty destination folder in a new session and say:

> Use unity-workflow-start to bootstrap the foundation for [game concept, intended scope and constraints].

Bootstrap alone ends at **Foundation ready**. To request both milestones, add: “Then implement and validate the first playable slice.” **First slice accepted** is a separate status; see [milestone criteria](references/adoption.md#milestones-and-request-scope).

That is enough workflow input. The agent must follow the [bootstrap skill](skills/unity-project-bootstrap/SKILL.md), adopt the kit locally, and apply its architecture, dependency, asset and acceptance defaults without asking the user to repeat them. A request to try/test the workflow selects its evaluation profile. Product details and explicit overrides belong in the brief; technical defaults belong in the kit. The agent [asks about unresolved intent](references/clarification.md), including target platforms, supported languages and unclear mechanics, while continuing independent work; you do not need to pre-answer an architecture questionnaire.

After installation, project-root AGENTS.md and the selected client adapter route future sessions to the local standards and task skills. You can simply ask for foundation setup or the first slice without supplying the kit path. The originating kit path is no longer required for ordinary work. Global entrypoints are optional; downloading the kit alone does not install them.

**Spec-driven continuous development is the default:** bootstrap once, then evolve the same project across tasks and sessions. The agent uses pinned OpenSpec with a Unity schema to maintain [behavioral specs, scoped change plans and requirement-linked evidence](references/spec-driven-development.md), with lightweight records for small fixes. Prompts can simply request a feature, fix, balance change or visual refinement; the adopted rules supply the architecture. Use [WORKFLOW.md](WORKFLOW.md) and read only the references needed for the current task.

## Update with project review

In an adopted game, say:

> Use unity-workflow-update to check upstream for kit updates, evaluate their applicability to this project, and apply compatible workflow changes. Report deferred migrations. Also update my global kit.

For 0.3.4, the [b3 evaluation update](references/upgrades/unity-6000.7.0b3.md) updates the kit target; existing games require a separate Editor migration. For 0.3.3, the [verification-output migration](references/upgrades/verification-output-0.3.3.md) adds optional quiet output, a compact PR form and reviewed policy/history separation. For 0.3.2, the [context-efficiency migration](references/upgrades/context-efficiency-0.3.2.md) covers focused reading and a narrow project-helper fix; OpenSpec's lifecycle is unchanged.

For assessment only, say “review” instead of “apply.” The agent reviews changed requirements against the project's implementation, version pins and decisions. The installer reports file differences and protects local edits; semantic applicability requires that review. Updating global entrypoints never automatically updates games.

For project-only installation without global entrypoints, run `python3 install.py install --target /path/to/game --agent both`, then `check --target /path/to/game`. This installs six task skills and shared rules; it does not create Unity content. See [installation and update details](INSTALL.md).

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
| Install/update skills and rules | [Installer](INSTALL.md) |
| Bootstrap the Unity foundation | [Adoption](references/adoption.md) |

Engineering contract: [baseline](references/engineering-baseline.md), [assembly/module architecture](references/architecture.md), [Editor authoring](references/authoring.md), [code quality](references/code-quality.md), [local tooling/hooks](references/developer-tooling.md), [IDE setup](references/ide.md) and [code organization](references/code-organization.md).

Copyable files: [AGENTS.md](starter/AGENTS.md), [.editorconfig](starter/.editorconfig), [.gitignore](starter/.gitignore), [.gitattributes](starter/.gitattributes), [Core asmdef](starter/Game.Core.asmdef), [Unity compiler options](starter/csc.rsp), [SDK build defaults](starter/Directory.Build.props), [UI styling fixture](starter/UI/README.md), [document forms](starter/DOCUMENT-TEMPLATES.md).

Historical: [installation record](INSTALLATION.md). Maintenance: [review](REVIEW.md). Neither is routine task context.

References own policy; skills route and apply it. Approved project ADRs describe deviations. Native version/package files own resolved versions. Claims of implementation, test success or measured performance require evidence from the actual template.
