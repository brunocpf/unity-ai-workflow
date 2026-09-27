# Context and asset contract templates

Copy the relevant section into the game's docs. Empty fields are intentionally project-specific; resolve them during bootstrap or feature planning.

## Project contract

- Game premise and player experience:
- Agreed launch platforms and primary first-slice acceptance target; later platform candidates:
- Minimum devices, input requirements and graphics APIs for those targets:
- Render pipeline and exact editor version:
- Production/evaluation profile and experimental features:
- Input devices and accessibility goals:
- Source language, supported locale codes/regions, launch versus later translation scope:
- Accepted answers with affected contract; pending questions, what they block and any provisional assumptions:
- Save/network/offline requirements:
- Frame-time, CPU/GPU memory, startup, download budgets:
- Art direction and accepted reference examples:
- CLI/editor/package/analyzer/Blender version authorities:
- Authorized milestone scope: foundation only / foundation and first slice / later increment:
- Foundation status, setup evidence and unresolved setup blockers:
- First vertical slice: planned scope, separate acceptance status/evidence and deferred checks:

## Feature spec

Use the executable templates in [OpenSpec setup](../references/openspec-setup.md) and the [spec-driven process](../references/spec-driven-development.md). Canonical behavior lives in openspec/specs; proposed deltas, design, tasks and verification live in openspec/changes. Do not copy a second feature-spec form into docs/features. Existing briefs become navigation or explicitly historical context after reconciliation.

Keep stable requirement IDs, observable scenarios, linked project constraints and the active issue/change. The shipped verification.json template owns requirement/evidence mapping; pending outcomes remain pending until actual checks and required reviews finish.

## Visual design brief

- Player's main decision, primary action and screen focal area:
- Exact inspected reference images and what each contributes:
- Compared visual directions; selected composition/control language and reason:
- High-fidelity target image, aspect ratio, representative content and concept status:
- Shapes, imagery/surfaces, type hierarchy and meaningful visualizations of game state:
- Signature controls: visual feature → drawing/gradient/material/filter/motion mechanism → assets/parameters → lifetime owner → actual player evidence:
- Primary control family and focus/hover/press/selected/disabled treatment:
- Key event feedback, transitions and reduced-motion equivalents:
- Asset/tool choices needed to achieve the target; constraints and budget:
- Representative Unity screen to finish before expanding content; planned visual iteration effort:
- Fresh player comparison, biggest mismatch, correction and remaining visual gaps:

Apply [art-direction policy](../references/ui-art-direction.md); for a small project this may be a compact section with image links, not a separate design document for every control.

## Localization contract

- Source language, enabled launch locales/regions, later scope and user decision:
- Native/package version, settings asset, table/key ownership and stable IDs:
- Provider/build inclusion, active/fallback preload and offline failure policy:
- Single selected-locale/persistence authority, startup order and change/loading behavior:
- Native versus VM text writers; pure adapter readiness/revision contract:
- Fonts/licenses/glyph coverage, shaping/RTL/layout, localized art/audio/subtitles:
- Translation/glossary/import authority, AI draft versus reviewed status:
- Validation command, rejected missing/invalid fixtures, supported-locale player captures and budgets:

Follow [localization](../references/localization.md); a source-only release still declares its language and tests expansion.

## Editor authoring record

- Entry scenes, prefab/variant families and preview/gallery locations:
- Tuning definitions/catalogs, units, stable IDs and validation command:
- Definition-to-pure-config boundary and session refresh policy:
- Generated versus authored paths and generator ownership manifest:
- Edit/tune/add-content tasks completed without C# changes:
- Play/reopen/reimport/regenerate/build preservation evidence:
- Exceptions, alternative preview/tuning path and remaining gaps:

## Architecture decision

- Decision ID, title, date, status:
- Context and constraints:
- Decision:
- Alternatives considered:
- Consequences and affected modules:
- Compatibility evidence:
- Revisit trigger:

## Asset brief and provenance

- Stable asset ID, revision, owner, state:
- Gameplay role and viewing distance:
- Art-bible references and approved concept hashes:
- Physical dimensions, forward/up axes, pivot:
- Mesh triangles by LOD; materials/submeshes; collider budget:
- Texture dimensions, formats, UV density/padding, channel meanings:
- Rig type, skeleton version, required bones/sockets, max influences:
- Clip names, duration/FPS, loop/additive/root-motion policy:
- Pixel dimensions, palette, PPU, directions, frame map/timing if 2D:
- Provider/model/version, prompt, parameters, seed where available:
- Provider job ID and actual cost; source/output SHA-256:
- Blender/source-tool/exporter version and export preset:
- Source files, accepted export paths, Unity GUID/import preset:
- Provenance/license record for intended use:
- Technical metrics and acceptance capture:
- Known limitations, review result, replacement history:

Keep the machine-readable equivalent alongside the asset registry. Do not store credentials or expiring download URLs as the retrieval authority. Source files and hashes are the durable record.

## Motion brief

- Character/skeleton version and reference clip ID:
- Action, duration, sampling FPS:
- Start/end poses and loop policy:
- Root trajectory versus in-place movement:
- Contact windows for feet/hands/weapons:
- Anticipation/action/recovery timing:
- Retarget method, bone map, rest-pose correction:
- Maximum permitted pose error after curve simplification:
- Gameplay interruption/blending requirements:
- Foot-slip, penetration, root-drift and silhouette acceptance:

## Compatibility entry

- Capability:
- Editor full version/revision and package version:
- Public/source documentation and date checked:
- Required project flag:
- Target/platform/backend tested:
- Probe scene/test and result:
- Supported / experimental / unavailable / roadmap:
- Fallback:
- Recheck trigger:

## Project navigation (docs/index.md)

- Active issue/PR, OpenSpec change and current handoff (links, not copied status):
- Affected source/module and Editor authoring entrypoints:
- Applicable decisions and visual/asset target:
- Real validation-command location and retained evidence location:

Keep this a small routing page; canonical documents own their facts.

## Session handoff

- Objective and current acceptance status:
- Branch/revision, dirty work and active issue/OpenSpec change:
- Key decisions with links:
- Exact checks run and result paths:
- Open issue and most likely next investigation:
- Next concrete action:
- Required external input, if any:

Avoid storing transcripts. Preserve only information necessary to resume accurately.

## Visual iteration record

- Target/reference image IDs and intended player experience:
- Scenario, revision/build, device/backend, resolution, locale:
- Run ID, expected checkpoint list, fresh output directory and completed capture manifest:
- Seed, camera, readiness signal, simulation checkpoint/input sequence:
- Locale/content revision and font/layout readiness when capturing localized UI:
- Clock owner/mode, fixed step/count, simulated time versus real duration:
- Capture hashes/timestamps and freshness/provenance validation result:
- Capture or recording paths and confirmation they were inspected:
- Defect against the brief and priority:
- Proposed change and expected observable improvement:
- Before/after evidence and affected behavior tests:
- Alternate states checked:
- Design review: composition/focus, identity/asset finish, hierarchy/legibility, feedback, consistency/completeness; each meets target / needs revision / unverified with visible evidence:
- Technical result and visual result separately; verdict owner (agent/user), date and any superseded acceptance:
- Accept/repeat decision, remaining criteria, budget remaining:

## Reactive feature contract

- State owner and read-only projection:
- Commands versus events; initial/replayed state policy:
- Subscription scope and teardown/rebind behavior:
- Clock/frame provider and scaled/unscaled timing; live/manual owner and handoff/restore tests:
- Main-thread boundary:
- Overlapping-work/cancellation/side-effect policy:
- Recoverable versus terminal errors:
- Virtual-time, lifecycle, and late-delivery test cases:

## Custom-control acceptance contract

- Control type and stable template ID; source UXML/USS:
- Catalog/module membership, including nested and dynamic controls:
- Authoring resolver readiness/invalidation; Builder during Play Mode:
- Runtime preload boundary and structural-asset lease owner:
- Constructor-complete behavior and authoring attributes:
- Missing/cancelled-load behavior and shutdown ordering:
- UI Builder drag/drop, style/attribute edits, reload evidence:
- Cold-player, recycling, module unload/reload evidence:

## Module contract

- Responsibility, owned state/invariants and maintainership role:
- Public commands/queries/snapshots; expected denial/failure outcomes:
- Allowed module dependencies, consumed ports and provider adapters:
- Startup/readiness/scope/shutdown and resource ownership:
- Save/content/network schema versions and supported migrations:
- Extensibility points and public API compatibility:
- Contract/integration/load tests, budgets and retained evidence:

## Engineering status and release record

- Baseline requirement / applicable profile:
- Implemented entrypoint and owner:
- Exact command / tool versions / revision:
- Passing evidence and deliberate-fault rejection evidence:
- Remaining gap or concrete not-applicable reason:
- Template/release version, supported targets/backends:
- Dependency/license inventory and artifact/content hashes:
- Compatibility/migration/rollback procedure and retained artifacts:
