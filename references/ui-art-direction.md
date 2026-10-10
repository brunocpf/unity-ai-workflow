# Game UI art direction and quality

Required for new game UI, substantial screen design and visual evaluation. For a local fix, retain the project's established visual target and review the affected area. Invoking the kit selects a **distinctive game interface with deliberate art direction** as the default. Small scope limits the number of screens/assets; it does not lower their finish. Professional architecture says nothing about a corporate visual style.

## Establish a visible target

Before building out multiple screens, establish these in docs/project.md (visual direction), extracting an art-direction document only when substantial; use the [project form](../starter/DOCUMENT-TEMPLATES.md#docsprojectmd). Use the game brief and established choices; [ask early](clarification.md) when visual intent or constraints are ambiguous. Continue independent exploration while awaiting answers. Ordinary design work needs no extra approval gate.

1. Identify the player's main decision, the screen's focal area and the information needed at that moment. Separate persistent, contextual and secondary controls. Choose a composition around play; a header/sidebar/card layout is a considered option, not an automatic scaffold.
2. Inspect a small set of relevant visual references or existing accepted project screens. Save/link the exact images and identify what each contributes: composition, shape language, material treatment, information hierarchy or motion. Palette names and a font pair alone are not an art direction. References set ambition; create original output.
3. For a new game's primary screen, compare two compact visual directions with meaningfully different composition or control treatment, then select one with a short rationale. Thumbnails suffice for comparison. Changing only colors/fonts is not an alternative. Reuse an already established direction for later screens.
4. Produce one high-fidelity target at the intended aspect ratio with representative gameplay content, usable text sizes, a distinctive primary interaction and the surrounding game world. Use an existing accepted render, an original mockup or image generation where suitable. A gray wireframe or isolated button does not establish the final bar. Mark mockups as concepts; never submit them as player evidence.
5. Realize that screen in Unity as an early playable slice **before expanding all levels/screens**. Compare a fresh player capture with the target at the same scale. Correct composition, visual assets and controls as needed; carry the established language into later screens.

Use this work alongside necessary gameplay/toolchain setup. Do not spend the whole effort on architecture and leave art direction to a final color pass. Reserve implementation/asset and visual-iteration effort in the plan. If constraints prevent the target, narrow scope with the existing authorization or report the visual gap; do not relabel an unfinished interface as polished.

Keep reference/concept images and editable design sources under `SourceAssets/UI/<screen-or-family>/`, with provenance and links from the art-direction document. Approved runtime art follows the content layout; control C#/UXML/USS remains together in its existing control directory. Retain target images separately from actual player evidence so comparisons cannot silently substitute one for the other.

## Choose assets for the intended finish

For an illustrated brief, image generation is a default candidate for scene art, hero motifs, textured surfaces and distinctive sprite assets. Use available capabilities within the task budget. Vector/procedural work is appropriate for precise icons, diagrams, masks, borders and deliberately vector-led art. Choose by the target appearance, not merely because SVG/code is faster to produce. A vector-only direction must meet the same visual target; a tool list or the presence of original artwork is not quality evidence.

Derive runtime text, values, interaction geometry and states in Unity. Generated mockup text remains reference; do not flatten a functional interface into one image. Keep decorative raster layers separate from live controls, request actual alpha where needed, and qualify imports through the [asset pipeline](assets-2d.md). Use authorable, reusable control/content directories, not one-off painted screenshots as UI implementations.

## Build a game-specific visual language

Develop the screen as a complete composition. Make its gameplay area and main action immediately legible; use supporting detail to express the world without competing with play. Quiet styles can have strong shape, spacing, imagery and hierarchy. Brightness, gradients or animation quantity do not measure quality.

| Area | Expected design decision | Common weak substitute |
|---|---|---|
| Composition | Intentional focal hierarchy, scale, rhythm and relationship between world and UI | Website masthead + boxed play area + unrelated sidebar by habit |
| Information | Visualize useful relationships: capacity slots, route consequences, progress, urgency; retain precise text where needed | Every mechanic represented only by a small label and fraction |
| Controls | A coherent custom vocabulary for the game's frequent actions and primary states | Recolored stock buttons/cards copied across all screen roles |
| Identity | Recognizable silhouettes, motifs, iconography and asset treatment carried through the interface | Theme expressed only in the title font and a few tiny illustrations |
| Depth and grouping | Deliberate surfaces, layering, edge treatment, occlusion or graphic separation suited to the style | Uniform rectangles with arbitrary shadows, or undifferentiated flat empty areas |
| Feedback | Clear focus/hover/press/selection; satisfying action anticipation/confirmation and state transitions | Generic fades everywhere, a click with no visible consequence, or constant decorative motion |

The technical default is [rich custom rendering and coordinated motion](ui-advanced.md#expected-rendering-and-motion): actively use Painter2D/custom geometry, gradients, layered surfaces, shaders/filters and LitMotion where they realize the chosen design. Primary controls should have deliberate shape/detail, surface treatment and expressive states. Select and implement that combination during the first screen; ordinary colored rectangles and typography alone are not the default endpoint. Do not require every effect on every element, but do not treat the entire advanced rendering layer as optional polish to omit.

The kit's minimal source controls and styling galleries demonstrate implementation contracts. **They are not visual targets for a finished game.** Adapt their architecture to the selected design rather than inheriting their demo appearance.

## Acceptance is comparison-based

Review actual player captures and relevant motion windows against the target and game brief. Record the following dimensions as **meets target / needs revision / unverified**, with specific evidence, in the existing review record or final response (link inspected artifacts and concise observations; no separate iteration report):

- Composition and gameplay focus: primary decision and action read clearly; screen regions have deliberate proportions.
- Identity and asset finish: imagery, shapes, surfaces and typography form a cohesive game-specific interface at playing distance.
- Hierarchy and legibility: key information dominates; secondary copy, state and focus remain readable at target sizes.
- Interaction and feedback: the player can distinguish available/selected/disabled actions and see satisfying consequences in motion.
- Consistency and completeness: representative screens and important states reach the same finish, including empty/error/locked/results states.

Keep usability/technical results alongside this review, not in place of it. Correct clipping, valid captures, passing tests and a licensed custom font cannot establish visual acceptance. Do not average away a weak dimension with a numerical score. An assessment must name visible evidence and the next concrete improvement, not just call the UI “clean,” “cohesive” or “polished.”

Treat the first implementation as provisional until the comparison is complete. When it falls short, identify the largest visible mismatch, make a substantive correction and inspect the same scenario again. A layout/art/control redesign may be necessary; adding glow to a weak composition is not a sufficient iteration. Once the target is met, probe alternate states instead of making arbitrary cosmetic changes to meet an iteration count. See [visual iteration](validation.md#visual-acceptance) and [effect qualification](visual-fixtures.md).

If the whole screen still resembles a generic website/admin template after substituting its title and icons, revisit composition and interaction language unless that aesthetic is explicitly intended. This is a review prompt, not an automated detector or a ban on efficient layouts. Deliberate minimalism is valid when the visual evidence supports it; do not infer a minimalist constraint from “small,” “professional,” “cozy” or “non-pixel.”

User visual rejection supersedes an earlier agent verdict. Preserve technical passes, reopen visual acceptance and identify superseded images/video. Report `technical: passed; visual: needs revision` when appropriate. A kit trial must evaluate the desired visual outcome as well as engineering compliance, without requiring another “make it look good” prompt.
