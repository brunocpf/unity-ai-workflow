# Unity AI workflow kit

Opinionated architecture for long-lived Unity projects built with AI agents: modular boundaries, MVVM, scoped composition, and code quality tooling (EditorConfig, analyzers, a pre-commit hook and CI), with source examples and task skills. Reference Editor: **Unity 6000.7.0b3**. CLI versions are chosen per project; see [toolchain](references/toolchain.md#cli).

## Install globally (recommended)

Requires Python 3.9+. Clone separately from game workspaces, then install the two global entrypoints for Codex and Claude Code:

```sh
git clone https://github.com/brunocpf/unity-ai-workflow.git
cd unity-ai-workflow
python3 install.py install-global --agent both
python3 install.py check-global
```

Choose `codex`, `claude` or `both`. Restart or open a new client session after installation. A versioned copy of the kit lives in `~/.local/share/unity-ai-workflow/kits/`, so the original checkout is no longer needed to start projects. Existing games keep their own installed version.

## Start a new project

Open an empty destination folder in a new session and say:

> Use unity-workflow-start to set up a project for [game concept, intended scope and constraints].

That sets up the project: architecture, tooling, CI and docs. To also build the first playable slice, add: "Then build the first playable slice." See [request scope](references/adoption.md#request-scope).

That's all the workflow input you need. The agent follows the [bootstrap skill](skills/unity-project-bootstrap/SKILL.md), installs the kit into the project, and applies its architecture, dependency and asset defaults without asking you to repeat them. It [asks about unresolved intent](references/clarification.md), such as target platforms, supported languages and unclear mechanics, while continuing independent work.

After installation, the project's AGENTS.md and client skill folders route future sessions to the local standards. You can just ask for features, fixes or visual refinements; the kit supplies the architecture and engineering conventions. Planning tools and project management are your choice. See [WORKFLOW.md](WORKFLOW.md).

## Update a project

In a game that uses the kit, say:

> Use unity-workflow-update to check upstream for kit updates, decide which changes apply to this project, and apply them. Also update my global kit.

Say "review" instead of "apply" for an assessment only. The agent compares the new kit with the project's installed version, its Unity/package pins and its decisions. The installer reports file differences and protects local edits. Updating the global entrypoints never changes existing games.

For a project-only installation without global entrypoints, run `python3 install.py install --target /path/to/game --agent both`, then `check --target /path/to/game`. See [installation details](INSTALL.md).

| Task | Entry |
|---|---|
| Project setup / first slice | [Bootstrap skill](skills/unity-project-bootstrap/SKILL.md) |
| Gameplay feature | [Feature skill](skills/unity-feature-workflow/SKILL.md) |
| Custom control / binding / styling | [UI skill](skills/unity-ui-workflow/SKILL.md) |
| Languages / translated UI | [Localization](references/localization.md) |
| Ambiguous requirements / consequential choices | [Clarification](references/clarification.md) |
| Game UI design / visual quality | [Art direction](references/ui-art-direction.md) |
| Generate/import art or animation | [Asset skill](skills/unity-asset-workflow/SKILL.md) |
| Tests / CI | [Testing](references/testing.md), [CI](references/ci.md) |
| Dependencies / Editor upgrades | [Toolchain skill](skills/unity-toolchain-workflow/SKILL.md) |
| Resolver / controls / MVVM source | [Source examples](examples/README.md) |
| Reference navigation | [Index](references/INDEX.md) |
| Install/update skills and rules | [Installer](INSTALL.md) |

Engineering conventions: [baseline](references/engineering-baseline.md), [assembly/module architecture](references/architecture.md), [Editor authoring](references/authoring.md), [code quality](references/code-quality.md), [hooks](references/developer-tooling.md), [IDE setup](references/ide.md) and [code organization](references/code-organization.md).

Starter files: [AGENTS.md](starter/AGENTS.md), [.editorconfig](starter/.editorconfig), [.gitignore](starter/.gitignore), [.gitattributes](starter/.gitattributes), [Core asmdef](starter/Game.Core.asmdef), [Unity compiler options](starter/csc.rsp), [SDK build defaults](starter/Directory.Build.props), [UI styling examples](starter/UI/README.md), [document templates](starter/DOCUMENT-TEMPLATES.md).

## Developing the kit

```sh
python3 -m unittest discover -s tests -v
python3 tools/check_kit.py
```

The tests cover the installer; `check_kit.py` checks links, JSON/XML syntax and skill metadata. CI runs both on Linux, macOS and Windows.
