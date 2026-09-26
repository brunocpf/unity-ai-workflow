# Tests, visual iteration and evidence

Choose checks at the changed boundary; documentation-only edits do not require all player builds. The first template release must prove actual checks fail on known faults, then pass from a clean checkout. Missing/empty required suites are failures, not skips disguised as passes. Keep flakes visible; rerunning until green is not acceptance.

| Layer | Cases |
|---|---|
| Pure Core | Inventory/economy invariants and domain transitions |
| Application/R3 | Fake time/frame boundaries, initial/replayed state, cancellation, overlapping requests, recoverable errors, late delivery/disposal |
| Persistence adapters | Versioned DTO migrations, corrupt/interrupted data and provider contract tests |
| Presentation/MVVM | Projection, enabled/busy/errors, command routing, disposal/rebind and late result rejection without Unity |
| Architecture | Layer/module DAG, compiled transitive purity, forbidden service lookup, public contract and scope registration checks |
| Edit Mode | Import presets, authoring assets, GUIDs/references, catalogs, serialization, localization table/format coverage |
| Play Mode | Input → rules → state → UI, scenes, pooling, cleanup |
| Target player | Content, stripping/AOT, startup, platform input and graphics |
| Performance | Representative device/scenario, warmup, duration, allocation and memory budgets |
| Selected profiles | Network loss/reconnect, streaming, save upgrades, accessibility |

Use the same pure sources in the fast .NET harness and Unity. Fake time/frames replace sleeps in reactive tests. Test once-only actions after screen reopen/pool reuse. Include a few whole-slice tests; mocks cannot establish correct composition. In Editor input tests, explicitly route synthesized Input System devices to Game View and restore the prior routing during teardown; Editor focus can otherwise consume the input. Assert the resulting gameplay action, not just event injection. Separate compile, behavior, discovery and infrastructure failures. [CI](ci.md) owns commands; [lifecycle](lifecycle.md) owns reload cases.

## Scenario ownership and evidence

For accelerated runs and captures, implement [single-clock ownership and capture freshness](test-scenarios.md). Manual stepping suspends live gameplay ticks; current-run manifests must reject earlier screenshots before visual review. Run the contract’s known-fault probes when introducing this runner (normally in the first slice) and when changing it; setup-only bootstrap does not require a gameplay capture runner.

## Visual acceptance

New game/screen design follows [ui-art-direction.md](ui-art-direction.md). Establish the target before treating the first implementation as acceptable. Retain separate technical and visual verdicts; inspection must assess design quality as well as broken rendering. A generic or visibly underfinished screen can pass every functional test and still fail this gate.

Capture the actual Game view or target player, then open and inspect it against the brief. For motion inspect recordings or sampled frames. Use fixed seed/camera/resolution/quality/locale/input/checkpoint and explicit readiness for content, fonts/layout and shaders. Store revision/device/backend/scenario/time and capture hashes.

Loop: initial capture → specific defect → change → rerun affected tests/same capture → inspect comparison → alternate states → accept or repeat. If already acceptable, probe additional states instead of cosmetic churn. Respect agreed time/credit budgets; exhaustion is not success. Preserve previous accepted output and do not automatically bless changed screenshot baselines.

Image diffs need declared tolerances/masks for known nondeterminism; never mask the defect under test. Pair screenshots with behavior tests; inspect the built player before final acceptance. Capture assets/rigs at gameplay distance and in motion, not only closeups.

## IDE and code-quality acceptance

Follow [IDE capability checks](ide.md) after regeneration: Unity completion, cross-assembly navigation, no CS8632 for valid nullable annotations, intended analyzer/formatter behavior and logical namespaces. Confirm owned Unity/SDK/generated profiles agree and vendor projects remain untouched. The [organization/coverage gate](code-organization.md) must reject faults in pure and Unity-only source plus missing coverage; extension installation and formatter exit code alone are insufficient. Mark observed capability separately from configured files and tests still pending.

## Editor authoring acceptance

Use the [authoring contract](authoring.md). For the first template release, and affected content/generator changes, verify the actual editing workflow:

- Open the saved gameplay scene: inspect the environment/camera/lighting and edit a boundary or placement with useful gizmos. Open a representative character prefab/variant and preview its visuals without booting game services.
- Change enemy speed/health and an upgrade amount in their definitions without C# edits. Play and verify the changed behavior, then stop; mutable session state must not have dirtied shared definitions.
- Add or duplicate a definition using existing behavior, give it a new stable ID and register it through authored data. It becomes available without updating a hard-coded roster. Duplicate IDs, missing prefab components and invalid values fail preflight with useful asset/field diagnostics.
- Move an arena object and change a prefab/definition field; save, reopen, reimport, run setup/regeneration in its supported mode and build. Assert the edits and GUID/variant references survive. Compare against the pre-run authored snapshot, including pre-existing uncommitted edits, rather than assuming the working tree began clean.
- Run a generator twice: the second run makes no unexpected changes; only its declared replaceable outputs change. Unowned asset collisions fail safely. In an isolated fixture, prove an unauthorized overwrite would fail the preservation check.

Retain an authoring map, steps and before/after evidence. Automated asset/value/reference comparisons support this gate; a human/agent must also exercise and inspect the actual Editor authoring surfaces. Restore temporary evaluation edits deliberately. A code-created test scene or a passing player smoke test does not prove the saved project is useful to edit. Profile-specific exceptions retain an equivalent tuning/preview path.

## UI acceptance

- Builder: fresh-start drag/drop, attribute/USS edits, nested controls, moves/reloads, Builder during Play; no runtime ViewModel or external Initialize needed for visuals.
- Binding: one writer, semantic command once, coherent multi-property updates, detach/rebind, virtualized row identities and stale results.
- Content: cold load, missing/cancelled catalog, unload/reload, shared ownership and correct teardown; [UI construction](ui-construction.md).
- Rendering/input: sizes/aspect/safe areas, long/empty/localized/RTL content, fallback fonts, theme, disabled/loading/error states; pointer capture/cancel, keyboard/gamepad focus, touch where relevant, modal restoration.
- Effects/motion: rapid reversal, paused time, stale completion, detach/recycle, reduced motion changed mid-transition, lower-quality shader/filter fallback, bounded surfaces and no remaining handles; test real graphics backend.
- Visual implementation: demonstrate the [selected custom drawing, surface and animation treatments](ui-advanced.md#expected-rendering-and-motion) on the actual primary screen and controls. A design document listing techniques or installed packages is not implementation evidence.
- Text processing: stable repeated repaint, shaped-script/emoji/rich-text coverage, changing fonts/locale/layout, no clip or hit-test drift, reduced-motion baseline; use the [text gallery cases](ui-text-effects.md).

Each reusable control needs an authoring/player gallery covering applicable variants and combinations. Large lists need scrolling/recycling performance. Accessibility compliance or game feel cannot be established by screenshots alone.

For materials, tint/alpha, cascade changes and motion, adopt the concrete [effects fixtures](visual-fixtures.md): neutral/default comparisons, computed USS fault rejection, zero hidden-screen callbacks, UI/world reduced-motion teardown and event-window recordings. A technical pass and a visual acceptance decision are separate results.

## Localization acceptance

Apply the [localization gate](localization.md#acceptance-and-ci) from the first text-bearing slice: agreed scope, nonempty key/translation coverage, real format rules, selection/persistence, late-result/lifecycle checks, Builder and cold-player fonts/content. Inspect fresh supported-locale and pseudolocale captures; retain translation review status separately from functional/visual results. Disposable missing-key/translation/format faults must fail shared validation.

## Asset review

3D: scale/pivot/silhouette, material/UV seams, collisions, LODs and missing shaders. Animation: contacts, foot slip, penetration, root drift, loop/blend/interruption and gameplay timing. Pixel: palette, pivot/frame/direction consistency, tile/atlas seams and camera shimmer. Textures: neutral albedo, data-map channels, tiling, alpha edges, compression/memory.

Required evidence moves from ignored artifacts to retained CI/versioned storage. Feature/asset records link durable reports, captures, acceptance state and remaining defects. Use [document forms](../starter/DOCUMENT-TEMPLATES.md).

## Release gates beyond a single slice

Apply the [engineering baseline](engineering-baseline.md) to all selected capabilities. Add provider contract tests and save/content migration fixtures from [reliability](reliability.md); test both expected denials and infrastructure failures. Required architecture checks inspect actual assemblies and meaningful known-fault changes, including an engine dependency inserted into Presentation. [Code quality](code-quality.md) covers nullable/analyzer/format failure probes. Hooks provide early feedback; CI remains authoritative.

Record whether performance came from a release or development player, real-time or accelerated simulation, and whether each counter was valid. Unavailable/implausible-zero allocation counters are unknown, not zero; obtain a supported measurement separately. Accelerated full-run tests verify state flow, not real-time frame budgets. Keep engine shutdown warnings visible and attributed with evidence; disable unused renderer effects instead of suppressing missing/stripped shader warnings.

A clean slice is initial evidence, not proof that large inventories, scenes, content bundles or concurrent requests meet budgets. Add representative load/scaling fixtures before accepting the corresponding production capability. Retain the supported target/backend matrix and upgrade regression set.

UI performance acceptance includes [small view-state projections](ui-binding.md#snapshot-size-and-render-scope): verify unrelated model changes do not refresh another region, and measure before/after on representative screens.

Acceptance is requirement-based: follow [spec traceability](spec-driven-development.md#acceptance-and-ci), including invalidating affected evidence after a behavioral change. Test success alone cannot close unmapped or manually unverified requirements.
