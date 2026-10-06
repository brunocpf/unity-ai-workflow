# USS conventions

For new/substantial screen styling, start with [art direction](ui-art-direction.md); these USS rules implement the chosen design and do not prescribe a minimal appearance. For version-sensitive grid/components/materials/filters, read [capability gates](ui-capabilities.md).

## USS file and cascade convention

Use these logical layers; these are project file conventions, not CSS `@layer` syntax:

1. Theme/Tokens.uss: semantic colors, spacing, typography, sizes, motion durations.
2. Theme/Base.uss: a small explicit project baseline.
3. Elements/Name/Name.uss: scoped control styles and states.
4. Screens/Name/Name.uss: screen composition/layout.
5. Theme variants and narrowly scoped accessibility/quality overrides.

Make stylesheet attachment order deliberate, but remember specificity also participates. Avoid distributing conflicting style definitions across unrelated files. Theme changes should primarily override tokens; layout code should not hard-code theme colors.

Use a root class such as `.game-ui`, theme modifiers such as `.game-ui--dark`, and semantic tokens such as `--game-color-surface`, `--game-color-focus`, `--game-space-2`. Keep a short spacing/type scale. Raw constants belong in token definitions, deliberate component geometry, or documented one-off effects, not copied through every selector.

USS supports custom properties with `var()`; supported values and parser behavior still follow the selected Unity version. [USS custom properties](https://docs.unity3d.com/6000.7/Documentation/Manual/UIE-USS-CustomProperties.html).

### Naming and specificity

- Root block: `.game-inventory-slot`.
- Private part: `.game-inventory-slot__quantity`.
- Semantic variant/state: `.game-inventory-slot--selected`, `--compact`, `--empty`.
- Element `name`: camelCase query identity, not the primary styling hook.
- Default to single-class selectors. Use a short parent/state qualifier when necessary; avoid long scene-hierarchy selectors.
- Scope styles to the component. Avoid project-wide Label/Button selectors except a carefully reviewed baseline.
- Put inherited typography defaults on the theme root where possible. A baseline `.game-ui Label` outranks a single component class; loading component USS later cannot fix that. Use a lower-specificity baseline or explicit opt-in text roles. Protect margins/type sizes with the [computed-style regression fixture](visual-fixtures.md#computed-uss-regression).
- Avoid ID selectors for appearance and specificity escalation to overcome an unknown style conflict. Inspect computed styles and remove the conflicting owner.
- Treat Unity internal class names as a versioned integration surface. Prefer public APIs or scoped supported part styling; add upgrade tests when targeting internal parts.

Treat actual USS import warnings as defects: fail owned unsupported selectors/properties. The trial hit `:last-child` and `line-height` in its generated project styles; use explicit classes/spacing and validated typography properties. Reduced-motion overrides must match the element that actually carries the mode class (root versus descendant), and cover USS hover transitions as well as LitMotion.

Unity documents the supported selector vocabulary separately from web CSS. Do not assume structural selectors, media queries, CSS variables in every context, or CSS shorthands merely because a browser accepts them. [USS selectors](https://docs.unity3d.com/6000.7/Documentation/Manual/UIE-USS-Selectors.html).

### Layout rules

A parent owns layout of its children; a component owns its internals and sensible min/preferred sizes. Use Flexbox for ordinary flow, explicit shrinking/wrapping policy, and zero min-width on shrinkable text containers where needed. Use absolute placement for genuine overlays, not as the default layout system.

Screen size classes are applied by a root layout controller based on the panel/viewport, with explicit compact/regular/wide policies. Avoid one GeometryChanged handler per child and feedback loops that alter the size being measured. Do not presume media-query support.

A root layer coordinator orders menus/modals and independent toasts, drag previews and tooltips. Use the [navigation stack policy](ui-navigation.md) for hierarchical interactive screens; passive overlays do not enter its focus stack. Keep focus/input blocking coordinated with visual ordering; z-index alone does not implement modality. Avoid unbounded arbitrary z-index numbers and cross-panel assumptions.

Use explicit text wrap/ellipsis policy. Apply the [locale/font/layout contract](localization.md): design for longer localized strings, fallback fonts, RTL, and content-driven height. Fixed-size pixel-art controls are an intentional profile, not an excuse to hard-code every screen size.

### States, animation, and inline styles

Use native pseudo-states for hover/active/focus/disabled where applicable. Use class modifiers for application state. Define precedence for selected+hover, selected+disabled, invalid+focused, and busy+disabled; test those combinations. Do not encode important state through color alone.

Declare transitions on the base selector and name only the properties that should animate. Prefer opacity/transform effects where suitable rather than continuous layout changes; profile actual cost. Handle interruption, instant completion, and reduced-motion mode. Never let a repeated reactive notification restart an animation unnecessarily.

USS owns persistent appearance. Allow inline styles only for continuous per-instance runtime values such as drag coordinates, measured placement, safe-area geometry, or a genuinely dynamic effect parameter that the chosen API requires. Encapsulate those writes in one owner; clear them on recycle so they do not override future USS unexpectedly. Discrete selection/theme/validation state should usually toggle classes.

Dynamic item icons belong to the binding/presentation surface or an asset-aware element property. Decorative static textures belong to its UXML/USS asset dependencies or a justified optional descriptor. Keep external network URLs and secret/local machine paths out of shipped USS.

For custom geometry, shaders/filters and LitMotion ownership, use [advanced UI](ui-advanced.md); for typography animation and glyph processing, use [text effects](ui-text-effects.md).

Treat `-unity-material` as an inherited treatment, not a local background: qualify nested text/controls and explicitly excluded children using the [material scope fixture](visual-fixtures.md#ui-material-and-geometry-gallery). Prefer a dedicated decorative element when the content should remain unchanged.

[Gallery source](../starter/UI/README.md); [UI acceptance](validation.md#ui-acceptance).
