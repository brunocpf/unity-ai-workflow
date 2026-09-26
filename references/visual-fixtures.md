# Effects qualification fixtures

Read when introducing a material, custom drawing, motion or a shared style change. These fixtures supplement [visual acceptance](validation.md#visual-acceptance); each adopted feature records **configured / behavior-tested / player-inspected / accepted** separately. Omit inapplicable fixtures with a reason. An effect is optional even when the engine supports it.

## UI material and geometry gallery

Create an authored gallery with adjacent default-renderer and candidate-material copies of the same tree. Use the project's real Content Directory, fonts and panel theme. Start with the effect disabled and neutral white RGBA multiplication; an installed “Basic” sample need not be neutral. Then inspect the active effect and fallback.

| Probe | Required result |
|---|---|
| White/gray/color swatches, icon and antialiased text | Neutral mode preserves tint and glyph coverage; no white boxes or colored sample tint |
| Transparent → translucent → opaque gradient over contrasting art | Explicit gradient **alpha keys**, with the expected background visible; color keys alone do not define transparency |
| Nested parent opacity: 1, 0.5, 0 | Descendant geometry, textures and text attenuate consistently; zero is invisible |
| Rounded clip, scrolled clip, scaled panel and padded procedural border | No escaped pixels, seams or clipped required content; hit targets remain truthful |
| Candidate on parent; nested label/button; child with `-unity-material: none` | Inherited treatment has the intended scope; explicitly excluded content stays unaffected |
| Fresh player content load, unload, reload | All dependencies survive stripping/loading; no missing/white fallback material |
| Reduced motion and low-quality mode, switched during the effect | Static readable state immediately; animated shader treatment removed or demonstrably frozen |

`-unity-material` is inherited by descendants. Default decorative materials to a dedicated non-picking visual child/sibling behind the content; apply one to a whole control tree only when every descendant treatment is intentional. Keep authored decorative parts in the control's UXML. A shader using global `_Time` continues independently of a cancelled CPU tween. Test the actual fallback assignment, not just a settings flag. [Unity material property](https://docs.unity.com/en-us/engine/6000.7/manual/uitoolkits/uielements/uie-uss/properties/supported-properties).

Prefer supported UI Shader Graph authoring. If a pinned engine requires private generation APIs or template patching, isolate them in an explicit Editor authoring action: record Editor/package versions and source hashes, validate the expected signature/anchors exactly, fail before changing accepted outputs on drift, generate into staging, then import/validate and promote only owned outputs. Preserve the template's clipping, opacity, glyph, texture and gradient paths. Commit generated shader/material dependencies and provenance; neither runtime startup nor a normal player build regenerates them. A package upgrade requires renewed qualification. Do not copy a whole vendor template into the generic kit as an unqualified shader default.

Known-fault probes in a disposable fixture: introduce a colored half-alpha multiply; remove gradient alpha keys; assign the material to the common screen ancestor; drop a cold-load dependency. The relevant comparison or load gate must detect each fault. Engine import/compilation success alone cannot detect incorrect colors or distracting motion.

## Sprite and particle color gallery

Save a scene using the selected renderer/backend with a neutral white soft-edge texture, SpriteRenderer instances and ParticleSystems side by side. Supply distinct renderer tint/alpha and particle start/over-lifetime colors. Test red, cyan and white at alpha 0, 0.25 and 1 over dark, light and colored backgrounds; include overlapping and flipped sprites, atlas packing and the actual batching/instancing mode.

The shader must consume the renderer's actual color source: SpriteRenderer instance tint and ParticleSystem vertex color are separate integration paths. Inspect the installed pipeline shader/includes; do not assume mesh vertex color already contains sprite tint. Define straight/premultiplied/additive blending deliberately. Multiply alpha once according to that convention; transparent input must contribute nothing. For additive effects compare their contribution above the background, without requiring identical appearance to alpha blending. Keep material variants explicit when the two renderers need different input paths; do not mutate a shared asset per instance.

Use declared image tolerances and unsaturated patches; bright bloom can hide missing tint. Repeat with supported bloom on/off. Fault probe: ignore sprite tint, then separately ignore particle color/alpha; each must fail its corresponding comparison. This complements [source texture alpha checks](assets-2d.md), which cannot prove shader output.

## Computed USS regression

Import the [cascade fixture](../examples/Unity/UI/Previews/Cascade/CascadeProbe.uxml) with its sibling styles. Its baseline deliberately loads **after** component USS. After attachment/layout, [CascadeProbeChecks](../examples/Tests/Unity/CascadeProbeChecks.cs) requires component margin/type values to win. The temporary fault class enables a broad `.fixture-fault Label` selector: the same assertions must fail. Assert the resolved numbers independently; do not compute expected values from the stylesheet under test.

Port this case to real card/heading/error text with the actual runtime theme and Builder preview. Assert representative margins, font sizes, wrapping and state combinations. A class-plus-type baseline can outrank a single component class regardless of file order. Correct the baseline's ownership/specificity; do not respond by adding IDs or inline overrides. See [USS policy](ui-styling.md#naming-and-specificity).

## Visibility, reduced motion and teardown

The screen owner passes **effective presentation visibility** (including hidden ancestors/covered screens) and the current reduced-motion preference to its effects. A panel attachment alone is insufficient. Pause schedules and cancel handles when hidden; an early return inside a callback still pays the callback cost. A closing transition may remain presented until its bounded completion; disabling input is a separate concern.

Use [VisibleMotionClock](../examples/Unity/UI/Motion/VisibleMotionClock.cs) for a shared decorative clock per independently visible region. It starts inactive, stops on detach/dispose/hidden/reduced motion, and resumes from a fresh local phase. Its reset callback restores static visual parameters; it does not change gameplay. Use [ArcMeterMotion](../examples/Optional/LitMotion/ArcMeterMotion.cs) for value interpolation, with the same explicit visibility policy. Do not allocate a new clock per label or run both owners on one property.

Test visible → hidden while still attached → visible → reduced motion → normal → detach/reattach → dispose, including duplicate policy calls. Count actual paint-driving callbacks over several frames: hidden/reduced/disposed intervals must have **zero** callbacks; eligible intervals must eventually advance. Assert reset visuals and no duplicate schedules/handles. [MotionClockChecks](../examples/Tests/Unity/MotionClockChecks.cs) supplies a bounded coroutine for the clock using a caller-owned live panel.

World effects receive the same preference at the Unity presentation boundary. Decorative ambient particles stop emission or freeze according to the documented art policy; essential hit/danger/interaction feedback retains a legible static or restrained substitute. Test particles already alive, trails, queued bursts and screen/world transitions. For Shuriken, host teardown uses `StopEmittingAndClear` (including owned children); VFX Graph uses its separately verified graph stop/reset and pooling contract from [VFX ownership](vfx.md). Both release owned effects/material instances; reduced motion never changes simulation outcomes. Assert particle counts/active handles after teardown, not only enabled flags. Restore test preferences/time/input in finally.

## Event-timed recordings

Extend the project's [fresh capture runner](test-scenarios.md#captures-belong-to-the-current-run) with a short motion scenario. No general-purpose recorder is supplied by this kit. Arm recording and acknowledge readiness **before** issuing each action. Drive the normal input/command path and record the actual resulting event/accepted action marker, not only the intended input time.

| Event | Minimum observed window | Inspect |
|---|---|---|
| Upgrade purchase | 0.2 s before → 0.8 s after | Exactly one response; flash/stagger settles; no whole-screen synchronized pulse |
| Dash | 0.2 s before → 0.6 s after | Trail/ring starts with dash and releases; readable player position |
| Hit, death, pickup (separate occurrences) | 0.2 s before → 0.8 s after | Impact/readability, correct tint, no stale or missing effect |
| Screen reversal / reduced-motion switch | Before → through completion/fallback | No stale completion, jump, lingering shader animation or invisible-screen work |

Adapt event names/durations to the feature. Record actual frame index, monotonic display timestamp, simulation tick/time, file/hash and associated event occurrence IDs. Preserve original frame timestamps in an index/sidecar and the finalized run manifest. A fixed-FPS export must report any duplicated/dropped frames; it does not create new evidence. Label accelerated simulation in any demo. Keep at least one real-time observation for timing acceptance.

Choose sampling from the **shortest effect**, not a universal 15 fps cap. Starting requirement: at least three distinct rendered samples within its visible interval and a maximum gap no greater than one-third its duration. A 100 ms flash needs about 30 fps or higher plus event alignment; longer effects may need less. Validate actual gaps/coverage, not requested FPS. If readback cannot meet them, fail the motion case or use a lower-overhead recorder; never silently claim the effect was inspected.

Reject an omitted actual-event marker, duplicated/out-of-order timestamps or frame IDs, a recording starting after the event, insufficient before/after coverage and excessive sampling gaps, in addition to the standard provenance/media checks. Force each fault once when adopting/changing the recorder. Inspect the event windows and a complete composed screen in motion, then record a visual verdict. A valid manifest establishes evidence integrity, not aesthetic acceptance.

Recording, GPU readback and PNG/video encoding runs are excluded from gameplay performance acceptance. Run the same representative gameplay separately with recording disabled; retain build/settings/counter validity. After a visual correction, rebuild and inspect affected states, mark earlier screenshots/demo as superseded, and rerun performance only when the changed rendering cost or an unresolved concern warrants it.

## Visual direction is an acceptance gate

Apply [game UI art direction](ui-art-direction.md) first. These fixtures qualify implementation of the target; passing them does not establish a strong design. Restraint concerns distracting motion and focus, not a requirement for sparse, flat or generic screens.

Use hierarchy, contrast, spacing and event feedback before continuous ornament. Default to restrained, local, event-driven motion. No continuous synchronized sweeps across buttons, tags, frames and labels. An intentional ambient signature effect needs an art rationale, motion review in the complete screen and a static alternative. Technical qualification does not make an effect desirable.

When a user rejects a treatment, remove its active assignments and inherited reach; retained experiment assets must be clearly inactive in the authoring record. Supersede old evidence and update the deliverable. A style-only change needs affected import/cascade/player checks, not automatically the unchanged C# suites.
