# Adopt and release

## Install before bootstrap

Installing the workflow is separate from both Unity milestones. From the kit checkout run `python3 install.py install --target /path/to/game --agent codex|claude|both` (choose one value, not the literal alternatives), then `python3 install.py check --target /path/to/game`. The installer copies the shared standards/examples, adds client discovery paths and preserves existing instruction content. It does not create the game, apply compiler settings or provision tools. Bootstrap can install the workflow as its first step when not yet adopted; the user's bootstrap request already authorizes that prerequisite.

## Milestones and request scope

**Bootstrap means foundation setup.** A setup/bootstrap-only request ends after milestone 1. A request to build a playable game, implement the first slice or test the workflow end to end includes both milestones unless explicitly limited to setup. When both are authorized, continue across the checkpoint without another approval request. Preserve any larger requested scope beyond that checkpoint. Clarify only genuinely ambiguous scope.

### Foundation ready

- Establish the project, native version/package locks, source/assembly boundaries, selected composition/dependency setup, Git conventions, local rules/skills and navigable project docs. Record targets, locale scope and the proposed first slice.
- Wire nullable/compiler parity, IDE regeneration, owned-code quality/coverage gates, test/build entrypoints, hooks and CI configuration. Verify actual Editor import/compile, pure compilation, IDE capabilities and meaningful setup/architecture and deliberate-fault probes for installed gates. Empty suites or copied configuration are not passing evidence.
- Create only the saved startup/smoke assets and fixtures needed to verify setup. Confirm they open/run and retain authored changes. Gameplay systems, polished screens, generated production assets and end-to-end localization/content integration belong to milestone 2; do not build speculative frameworks to fill those slots.
- Record results in docs/engineering-status.md and a resumable next step. Required setup checks blocked by provisioning remain **foundation incomplete**. Planned slice checks are **deferred to first slice**, never passed or not applicable. Foundation ready verifies setup, not gameplay integration or a reusable template release.

### First slice accepted

Implement the scoped playable loop and only the shared helpers it consumes, using the established foundation. Prove the selected composition, authored content, UI, localization and asset/content paths together. Run relevant pure/Editor/lifecycle tests, a clean-checkout target-player build and launch, visual inspection/refinement and authoring-edit preservation. Apply [validation](validation.md) and [art direction](ui-art-direction.md); record technical and visual verdicts separately. Missing required evidence leaves the slice unaccepted.

A small slice retains the professional standard without implementing every optional integration. Template release additionally requires the applicable [release gates](engineering-baseline.md#change-and-release-discipline); foundation completion alone never qualifies it.

## Bootstrap contract

The user supplies a game brief and this kit's entrypoint, not a restatement of architecture. Treat invoking the kit as selecting its defaults. Read and apply them; do not merely copy unread files or leave their decisions for a later prompt.

- Required input is a game concept; use the current workspace as destination unless specified. Identify the intended project scope and select its first playable vertical slice and record both in docs/project.md; never shrink the intended product or relax architecture because the first slice is small. Apply [clarification](clarification.md) whenever intent is ambiguous, including target platforms, supported locales and unclear mechanics; ask before committing dependent work. Technical exceptions become ADRs; do not reopen established kit decisions routinely.
- A workflow trial/prototype starts from the 6.7 evaluation baseline; prefer the modern evaluation profile when the selected build passes language-profiles.md. Check local availability and record the chosen pin. A shipping project needs a validated production baseline; do not silently treat the beta as production-approved. If target platforms are unspecified, ask before making platform-dependent choices. For a local trial, recommend the host desktop as the first acceptance target; use it once selected by the user or covered by their explicit delegation. Record launch targets and later candidates separately; the development host does not determine either.
- Derive the art/game profile from the brief. Default a conventional 2D trial to URP's 2D Renderer. Apply [game UI art direction](ui-art-direction.md): establish a concrete visual target and realize a representative polished screen in the first slice before expanding levels/screens. Select dependencies and asset tools to meet that target and the functional requirements, rather than installing every optional library or exercising every generation service.
- Establish [localization](localization.md) with the first player-facing text: confirm language scope, author tables/settings and prove the selected UITK/provider path. Do not defer localization to a narrative profile or a later rewrite.
- The [professional baseline](engineering-baseline.md), architecture, source layout, UI presentation, lifecycle, code style, Git, documentation and acceptance come from their canonical references. Establish project-specific facts and command paths once. User prompts need only describe behavior, style, scope and exceptions.
- Bootstrap installs all six lightweight task skills, the root rules and the local standards copy. Use relevant specialized references during work. Subsequent tasks inherit these rules through project-root AGENTS.md; they do not require the original conversation or kit path.
- For an end-to-end workflow trial (not a setup-only request), complete milestone 2: run a playable acceptance slice with the selected integrations, inspect actual visual output against its target, iterate on quality gaps and record kit gaps. Record visual and technical verdicts separately. Apply validation.md; do not require the user to separately request polish, tests, visual review, CI entrypoints or lifecycle checks. For later scoped feature requests, validate the affected boundaries without repeating full bootstrap.

## Continuous development

Bootstrap once; evolve the same project through features, fixes, balancing, content and polish. A brief can describe a long-term game without specifying every future detail. Record the product scope and current milestone in docs/project.md; keep feature acceptance in docs/features/.

- On resumption, read root rules, docs/index.md, the relevant feature and latest applicable handoff; inspect actual source, authored assets and working-tree changes before editing. Reconcile stale notes with implementation and evidence. Prior chat history is optional context, not required project memory.
- Complete the authorized increment through implementation, affected tests and visual refinement. Intermediate slices are checkpoints, not permission to leave requested scope unfinished; a future backlog is not authorization to implement unrelated features.
- Preserve existing contracts, accepted art, Inspector edits and resolved decisions. Evolve them deliberately; record material architectural changes as ADRs. Do not regenerate the project or upgrade its toolchain as a side effect of an ordinary feature request.
- Keep docs/index.md pointing to current work. When work spans sessions, maintain a compact handoff under docs/handoffs/: objective, implemented/verified/pending state, evidence and rerun commands, blockers and next action. Replace stale status rather than accumulating transcripts or duplicating standards.
- Ask only about newly unresolved intent. Subsequent prompts describe the desired change; the repository supplies architecture, conventions and prior answers. Existing projects adopt kit updates through reviewed changes, not automatic overwrites.

## Adoption steps

1. Confirm target platforms and the primary acceptance target using the clarification policy; select project name/path, render pipeline and production/evaluation profile accordingly. Inspect the destination. Generate Unity-owned settings/assets using the selected Editor/CLI.
2. Install or verify the workflow using the installer above. It preserves the references/starter/examples layout under docs/standards and tracks the baseline in .unity-workflow/installation.json. Record that version/hash in docs/toolchain.md; historical reports are not project authority.
3. Establish the [Editor authoring defaults](authoring.md), authoring map and scoped generation ownership. Save the startup/smoke assets needed for foundation checks; add gameplay scenes, prefabs and tuning definitions with their slice consumers. Ordinary setup/build must preserve authored edits.
4. Keep the installer-managed instruction routing intact; do not replace root AGENTS.md/CLAUDE.md with starter files. Merge starter .editorconfig, .gitignore and .gitattributes into the project root; copy Directory.Build.props to tooling/dotnet/ and set the language profile and SDK pin. Follow code-quality.md and developer-tooling.md for nullable enforcement, analyzer installation and local hook setup. Place the Core asmdef beside Core sources and merge the selected csc.rsp beside every owned asmdef; retain explicit analyzer configuration and prove its effect in the Editor compiler; never assume inheritance from Assets/Game. Adopt ide.md and code-organization.md: track VS Code configuration, install the owned-project generation hook, keep the Unity and pure SDK solutions separate, and install the shared full-coverage quality entrypoint. Import chosen UI fixtures through Unity so it creates metadata.
5. Verify all six skills in the selected client: .agents/skills for Codex, .claude/skills for Claude Code, both when selected. Skills read docs/standards/references; the shared rules are docs/standards/PROJECT-RULES.md. File-integrity checks and live client discovery are separate. No global installation is required.
6. Create project-specific docs below. Implement scripts and put real commands in the project README; starter prose is not executable automation.
7. Run the Foundation ready checks above and record the milestone status. Stop here for setup-only scope.
8. When authorized, implement and validate milestone 2 from the existing foundation. Record First slice accepted only after its gates pass; qualify a template release separately against its supported target matrix.

| Project document | Owns |
|---|---|
| docs/index.md | Task navigation and executable command locations |
| docs/project.md | Scope, targets, inputs, save/network requirements, selected profiles; accepted answers, pending questions and what they block |
| docs/engineering-status.md | Foundation and first-slice status separately; requirement → milestone/owner/command/evidence/gap |
| docs/modules/ | Module public contracts, state/lifetimes/dependencies and compatibility |
| docs/authoring.md | Where to edit/preview scenes, prefabs, definitions and procedural content; generator ownership and preservation checks |
| docs/architecture.md | Actual source map, boundaries, lifetimes and implemented helpers |
| docs/toolchain.md | Template baseline, SDK/Editor/CLI/modules/packages; native lockfile authorities |
| docs/dependencies.md | Selected libraries, owners, version/license/compatibility evidence |
| docs/compatibility.md | Capability → exact version/flag/platform → test evidence/fallback |
| docs/art-direction.md | Player focus, inspected reference images, selected composition/control language, concrete visual target, asset/motion decisions and visual acceptance evidence |
| docs/localization.md | Source/supported locales, table/provider ownership, selection/fallback, font/layout policy and translation/visual evidence |
| docs/performance-budgets.md | Device/scenario budgets and measured results |
| docs/decisions/ | Exceptions and material decisions |
| docs/features/, docs/assets/ | Behavior contracts and asset briefs |
| docs/handoffs/ | Resumable state, evidence and next action |

Use [document forms](../starter/DOCUMENT-TEMPLATES.md) as needed. Avoid transcripts and duplicated policy. Mark proposed/implemented/verified separately. Promote required captures/reports from ignored artifacts to retained CI or a versioned evidence store and link durable locations/hashes.

Environment/build reproducibility requires pinned tools and accepted files. Hosted generation is not reproducible merely because prompts/seeds are saved: archive accepted outputs. Bitwise-identical builds are a separate requirement.
