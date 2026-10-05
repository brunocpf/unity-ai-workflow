# USS pattern examples

These source examples are not yet imported or visually approved in Unity. They illustrate the rules in [UI construction](../../references/ui-construction.md) and [styling](../../references/ui-styling.md).

They are implementation fixtures, not a game skin or quality benchmark. Build the production appearance from the project's [visual target](../../references/ui-art-direction.md), including its composition, assets, custom controls and interaction states.

- Tokens.uss: semantic root tokens and a light-theme override.
- InventorySlot.uss: component-scoped structure and selected/focus/disabled states.
- Gallery.uss and Gallery.uxml: a small preview tree using built-in controls; this is not the complete custom-element/R3 implementation.

Import into the selected Unity 6000.7.0b3 evaluation project, assign through a suitable rendering host with a deliberate runtime theme, check import warnings, then capture and inspect narrow/wide, light/default, focus, selected, disabled and long-text states. Replace the illustrative colors and sizes with the game's art direction. The gallery uses 6.7 gap; older editor profiles need a spacing fallback.

The example references USS from UXML, matching the production ownership rule. Production custom controls clone their template in their constructor through the documented synchronous template resolver; Content Directory preloading happens at UI/module bootstrap. This gallery does not implement that resolver or prove custom-control UI Builder compatibility.
