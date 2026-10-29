# Adopt the kit

## Install

From the kit checkout run `python3 install.py doctor --target /path/to/game` to see which tools exist, then `python3 install.py install --target /path/to/game --agent codex|claude|both` (choose one value) and `python3 install.py check --target /path/to/game`. The installer copies the standards into `docs/standards/` and the task skills into the client skill folders. It preserves existing instruction text, and it does not create the game, change compiler settings or install tools. A bootstrap request already authorizes installing the kit as its first step when the project doesn't have it yet.

## Request scope

A setup or bootstrap request means project setup: the foundation described below. A request to build a playable game includes setup plus the first playable slice, unless the user limits it. Don't add an approval step between the two. Clarify only genuinely ambiguous scope.

### Project setup

- Create the project, native version/package locks, source/assembly boundaries, composition/dependency setup, Git conventions and the three project documents. Record target platforms, languages and the proposed first slice in docs/project.md.
- Wire nullable/compiler settings, IDE regeneration, the quality check, test/build commands, hooks and CI. Confirm the project imports and compiles in the Editor, the pure solution builds and the tests run.
- Create only the startup scene and assets the project needs to open and run. Gameplay systems, polished screens and production assets belong to the first slice; don't build speculative frameworks ahead of it.
- Put real commands and any setup gaps in README.md.

### First playable slice

Implement the scoped playable loop and only the shared helpers it uses, on top of the project setup. Bring the selected composition, authored content, UI, localization and asset paths together in one working loop. Run the relevant tests, build and launch the target player, and look at the result against the [art direction](ui-art-direction.md) target. Keep refining until the slice looks and plays the way the brief describes. A small slice still follows the professional standard; it does not need every optional integration.

## Bootstrap contract

The user supplies a game brief and this kit's entrypoint, not a restatement of architecture. Treat invoking the kit as selecting its defaults. Read and apply them; don't copy unread files or leave their decisions for a later prompt.

- Required input is a game concept; use the current workspace as destination unless specified. Record the intended scope and the first playable vertical slice in docs/project.md. Never shrink the intended product or relax architecture because the first slice is small. Apply [clarification](clarification.md) whenever intent is ambiguous, including target platforms, supported locales and unclear mechanics. Technical exceptions become ADRs; don't reopen established kit decisions routinely.
- A prototype starts from the 6.7 evaluation baseline; prefer the modern language profile when the selected Editor supports it (see [language profiles](language-profiles.md)). Record the chosen pin. A shipping project needs a production-ready Unity version; don't treat a beta as production-approved. If target platforms are unspecified, ask before making platform-dependent choices. For a local prototype, suggest the host desktop as the first target.
- Derive the art/game profile from the brief. Default a conventional 2D game to URP's 2D Renderer. Apply [game UI art direction](ui-art-direction.md): establish a concrete visual target and finish a representative polished screen in the first slice before expanding levels/screens. Select dependencies and asset tools to meet that target and the functional requirements, rather than installing every optional library.
- Set up [localization](localization.md) with the first player-facing text: confirm the language scope, author tables/settings and use the selected UITK/provider path. Don't defer localization to a later rewrite.
- The [professional baseline](engineering-baseline.md), architecture, source layout, UI presentation, lifecycle, code style, Git and documentation come from their references. Record project-specific facts and command paths once. Later prompts need only describe behavior, style, scope and exceptions.
- Bootstrap installs the task skills, the root rules and the local standards copy. Later sessions inherit these rules through project-root AGENTS.md; they don't need the original conversation or kit path.

## Continuous development

Bootstrap once; evolve the same project through features, fixes, balancing, content and polish. A brief can describe a long-term game without specifying every future detail. Keep product scope in docs/project.md and decisions in the existing project docs. No planning framework or per-feature document set is required.

- On resumption, read root rules and the current request, then relevant project decisions/source maps; inspect actual source, authored assets and working-tree changes before editing. Prior chat history is optional context, not required project memory.
- Complete the requested increment through implementation, affected tests and visual refinement. A future backlog is not authorization to implement unrelated features.
- Preserve existing contracts, approved art, Inspector edits and resolved decisions. Evolve them deliberately; record material architectural changes as ADRs. Don't regenerate the project or upgrade its toolchain as a side effect of an ordinary feature request.
- Use the project's existing way of tracking work. Add a short continuation note only when unfinished work has context not already recorded in code or tasks.
- Ask only about newly unresolved intent. Existing projects adopt kit updates through reviewed changes, not automatic overwrites.

## Setup steps

For setup scope, work from the [setup checklist](setup-checklist.md); the steps below are the reasoning behind it.

1. Confirm target platforms using the clarification policy; select project name/path, render pipeline and Unity version accordingly. Inspect the destination. Generate Unity-owned settings/assets using the selected Editor/CLI. If its help exposes `projects create --with-pipeline`, use it for agent-driven setup, and confirm the Pipeline package actually installed (see [CLI](toolchain.md#cli)); otherwise install it separately. Don't reinstall it every session.
2. Install the kit with the installer above. It tracks the installed version in `.unity-workflow/installation.json`.
3. Set up the [Editor authoring defaults](authoring.md): saved scenes, prefabs and tuning definitions that designers can edit. Add gameplay scenes, prefabs and definitions alongside the features that use them. Setup and builds must preserve authored edits.
4. Keep the installer-managed instruction routing intact; don't replace root AGENTS.md/CLAUDE.md with starter files. Run `python3 install.py scaffold --target /path/to/game` to place the starter EditorConfig, Git files, hooks, VS Code settings and tooling folders, then merge anything it lists under `merge` and set the SDK pin. Follow [code quality](code-quality.md) and [developer tooling](developer-tooling.md) for nullable settings, analyzers and the pre-commit hook. Place the Core asmdef beside Core sources and copy csc.rsp beside every owned asmdef. Follow [IDE setup](ide.md) and [code organization](code-organization.md): track VS Code configuration, install the IDE project hook, keep the Unity and pure SDK solutions separate, and install the quality check. Import chosen UI starter files through Unity so it creates metadata.
5. Confirm the skills appear in the selected client: .agents/skills for Codex, .claude/skills for Claude Code. Skills read docs/standards/references; the shared rules are docs/standards/PROJECT-RULES.md.
6. Create the project documents below and wire [CI](ci.md). Put real commands in the project README.
7. Stop here for setup-only scope. Otherwise build the first playable slice.

Default to the three [project documents](../starter/DOCUMENT-TEMPLATES.md): README.md, docs/project.md and docs/architecture.md. Keep authoring, localization, dependency rationale, compatibility and budgets as sections; native lockfiles own exact versions. Split a document only for substantial independently maintained content. Project management is outside this kit. Don't generate status matrices, feature briefs, handoffs or completion reports.

Keep generated asset sources and their generation settings beside the accepted assets; regenerating hosted output rarely reproduces it exactly.
