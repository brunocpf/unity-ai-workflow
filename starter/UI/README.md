# USS pattern examples

These files illustrate the rules in [UI construction](../../references/ui-construction.md) and [styling](../../references/ui-styling.md). They are starting points, not a game skin. Build the production appearance from the project's [visual target](../../references/ui-art-direction.md).

- Tokens.uss: semantic root tokens and a light-theme override.
- InventorySlot.uss: component-scoped structure and selected/focus/disabled states.
- Gallery.uss and Gallery.uxml: a small preview tree using built-in controls; not the complete custom-element/R3 implementation.

Import them into the project through a rendering host with a deliberate runtime theme, check import warnings, and look at narrow/wide, light/default, focus, selected, disabled and long-text states. Replace the illustrative colors and sizes with the game's art direction. The gallery uses the 6.7 `gap` property; older Editors need a spacing fallback.

The example references USS from UXML, matching the production ownership rule. Production custom controls clone their template in their constructor through the synchronous template resolver; Content Directory preloading happens at UI/module bootstrap. This gallery doesn't implement that resolver.
