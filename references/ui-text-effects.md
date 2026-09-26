# Text effects and post-processing

Use UITK TextElement/Label and TextCore font assets. Use [localization ownership](localization.md#ui-toolkit-mvvm-and-r3-ownership): presentation selects dynamic message semantics; authored labels can use native localized bindings. Glyph animation, rendering and display clocks belong to the view. Read [advanced UI](ui-advanced.md) for shader/filter and motion ownership.

## Choose the effect

| Need | Preferred path |
|---|---|
| Typography, static outline/shadow, semantic emphasis | USS and deliberately supported rich-text tags |
| Character wave, wobble, tint, local emphasis | `TextElement.PostProcessTextVertices` |
| Typewriter/dialogue reveal | Reveal shaped text by semantic cluster boundaries; no repeated Substring or incomplete markup |
| Shimmer, dissolve, large-scale continuous deformation | Qualified UITK text-compatible shader; preserve font coverage/atlas conventions |
| Composite glow or distortion | Bounded filter around the relevant text group, with a readable fallback |
| Damage/reward number | Pooled label + owned LitMotion transform/opacity; optional short glyph accent |
| Score/counter interpolation | Animate a display value, update text only when its displayed value changes |

The available 6000.7.0b2 assemblies API-compile the supplied WaveLabel callback; earlier b1 inspection established the same signature. They expose `PostProcessTextVertices` as `Action<TextElement.GlyphsEnumerable>`. Glyphs expose vertex slices, text ranges, line and kind; `SetTints` can change outline/shadow tint. Pass both tints together when changing both; repeated calls rebuild from the element baseline rather than accumulating overrides. The public reference source documents the callback and shaped-text access. Verify the exact installed build when upgrading. [Unity TextElement source](https://github.com/Unity-Technologies/UnityCsReference/blob/master/Modules/UIElements/Core/TextElement.cs). API presence was also checked directly against the installed DLL/XML; this is distinct from rendered acceptance. [Glyph contracts](https://github.com/Unity-Technologies/UnityCsReference/blob/master/Modules/UIElements/Core/Text/TextElementEnumerators.cs).

## Vertex effect contract

[WaveLabel](../examples/Unity/UI/Elements/WaveLabel/WaveLabel.cs) is a constructor-complete Label subclass. Its attributes provide a static Builder preview; no runtime Initialize or animation subscription is needed. Each callback shifts a whole glyph quad from that invocation's geometry. It retains no vertex slices, allocates no per-glyph managed collections, and leaves UV/tint data intact. It intentionally warps all visible quads, including inline sprites; a text-only variant must explicitly use the generator's supported glyph classification.

An owner may animate Phase through LitMotion or the shared [VisibleMotionClock](../examples/Unity/UI/Motion/VisibleMotionClock.cs). Set Amplitude to zero for reduced motion and stop the phase driver; a stopped phase alone leaves a deformed baseline. Never start a forever loop in the element constructor. Pause/cancel clocks when hidden, detached, unbound or recycled; display:none does not by itself cancel a package motion handle. The sample has no automatic clock, so idle previews do no recurring work. The [clock example setup](../examples/README.md#effects-example-setup) shows restoration and visibility ownership.

Request repaint when effect parameters change. Avoid MarkDirtyText every animation tick: it also invalidates layout. Qualify that repaint invokes fresh post-processing in the selected build; capture repeated frames at a fixed phase to detect accumulating deformation. Changes to text/font/layout must invalidate any derived glyph mapping. Do not modify text, style, hierarchy or layout inside the callback. If multiple effects coexist, one view-owned ordered pipeline composes them; do not overwrite another owner's callback or restore a stale delegate snapshot.

Reserve space for the maximum deformation; post-processing does not enlarge layout or magically update links, selection/caret and hit testing. Default animated text to non-editable decorative labels. For interactive linked text, keep glyph positions stable or explicitly validate interaction geometry. Never degrade readability of instructions, errors, settings or vital HUD numbers.

## Localization and reveal

A glyph index is neither a C# char index nor necessarily one grapheme. Surrogates, combining marks, ligatures, RTL/bidi ordering, inline sprites and font fallbacks break that shortcut. For dialogue, obtain the fully localized/shaped text, map the chosen logical reading progression to grapheme boundaries and glyph text ranges, then reveal all vertices belonging to a cluster together. The sample wave uses spatial phase and needs no string-index mapping; it is not a multilingual reveal implementation.

Use Advanced Text Generator for the selected modern profile. Its parsedText requires attachment and resolved styles; wait for layout readiness before building mappings. Text ranges index parsed text, not raw rich-text markup. Handle a glyph spanning multiple clusters as a unit and define inline-sprite timing. Changing locale/width/font cancels/rebuilds the reveal mapping. Keep a skip action that immediately reveals the full line, plus an accessible complete-text presentation; experimental accessibility support needs target testing. User-entered text must not become trusted formatting markup.

## Fast counters and budgets

Ordinary VM strings remain the default for dynamic game values. For measured high-frequency counters, let the VM expose the numeric target and formatting policy; a view formatter renders the interpolated display value without changing game state. Where appropriate, use the selected build's SetText overloads and reusable buffers. Avoid reading .text back each tick, redundant writes and reformatting unchanged rounded values. Localization, event listeners and first-time buffer/font growth can still allocate; measure warm and cold paths instead of promising zero allocations. Do not tween a critical authoritative value without also making its current meaning clear.

Limit animated glyph count and concurrent labels. Keep static text static, pool transient labels with a full reset, and prefer a GPU treatment when CPU mesh processing is the measured bottleneck. Do not globally allocate huge font atlases to hide first-use stalls; preload the required locale/font coverage and test dynamic fallback.

Acceptance gallery: empty/long/wrapped/ellipsized text, CJK, Arabic/RTL, mixed bidi, combining accents, emoji/ZWJ, fallback fonts, rich tags/sprites, DPI/scale, outline/shadow, clipped edges and font/locale changes during motion. Verify repeat repaint does not drift, reduced motion restores baseline, pooled reuse has no previous effect, and cold player content includes every font/material/shader dependency. Record CPU mesh/text/layout cost, GPU cost, allocations and atlas growth. [Shared visual acceptance](validation.md#ui-acceptance).
