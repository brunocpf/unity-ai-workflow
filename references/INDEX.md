# Read by task

Don't read this entire directory. References below are authoritative by subject; project-specific decisions belong in the game's docs.

| Task | Required reference | Conditional reference |
|---|---|---|
| Skill delegation / provider conflicts | [Skill ownership](context-efficiency.md#skill-ownership) | Available client skill inventory |
| Session start / resumption / context cost | [Context discipline](context-efficiency.md) | Current issue; optional continuation note |
| Project setup / first slice | [Adoption](adoption.md), [architecture](architecture.md), [repository](repository.md), [toolchain](toolchain.md) | [Dependencies](dependencies.md), selected [profile](profiles.md) |
| Unclear requirements / user choices | [Clarification](clarification.md) | [Dependencies](dependencies.md) for framework tradeoffs |
| Languages / translated UI / locale testing | [Localization](localization.md) | [Binding](ui-binding.md), [text effects](ui-text-effects.md) |
| Project standards / release | [Engineering baseline](engineering-baseline.md) | [Modules](modules.md), [reliability](reliability.md) |
| Scenes / prefabs / tuning / generation | [Editor authoring](authoring.md) | [Repository](repository.md), [testing](testing.md) |
| Composition / scopes | [Composition](composition.md) | [Lifecycle](lifecycle.md) |
| IDE / autocomplete / regeneration | [IDE setup](ide.md) | [Code organization](code-organization.md) |
| Source organization / formatting | [Code organization](code-organization.md) | [Code quality](code-quality.md), [IDE setup](ide.md) |
| C# / lint / hooks | [Code quality](code-quality.md), [developer tooling](developer-tooling.md) | [Language profiles](language-profiles.md) |
| Pure rules / application | [Architecture](architecture.md) | [R3/async](reactive.md), [utilities](utilities.md) |
| Custom control / loading | [UI construction](ui-construction.md) | [Lifecycle](lifecycle.md), [binding](ui-binding.md), [content bootstrap](ui-content-loading.md) |
| New screen / game UI design / visual quality | [Art direction](ui-art-direction.md) | [Advanced UI](ui-advanced.md), [asset pipeline](assets.md) |
| Menus / focus / screen stacks | [Native navigation](ui-navigation.md) | [Navigation tests](../examples/Tests/Unity/Navigation/README.md) |
| Styling / modern UITK | [USS](ui-styling.md) | [UI capabilities](ui-capabilities.md) for modern features |
| Custom drawing / shaders / motion | [Advanced UI](ui-advanced.md) | [UI capabilities](ui-capabilities.md), [text effects](ui-text-effects.md) |
| Text rendering / reveal / counters | [Text effects](ui-text-effects.md) | [Advanced UI](ui-advanced.md) |
| Particle effects / VFX Graph | [VFX authoring and setup](vfx.md) | [Dependencies](dependencies.md) |
| 3D asset | [Asset pipeline](assets.md), [3D pipeline](assets-3d.md) | [Motion reference](assets-motion.md) |
| Textures / sprites / pixel art | [Asset pipeline](assets.md), [2D pipeline](assets-2d.md) | [Art direction](ui-art-direction.md) |
| CI / builds | [CI](ci.md) | [Toolchain](toolchain.md), [testing](testing.md) |
| Tests / looking at the result | [Testing](testing.md) | [Lifecycle](lifecycle.md) for reload/resource issues |
| Kit update | [Updating the kit](workflow-updates.md) | Project ADRs and native version pins |
| Package decision | [Dependencies](dependencies.md) | [Optional libraries](dependencies-optional.md), [profiles](profiles.md) |
| Shared helpers / optimization | [Utilities](utilities.md) | [Lifecycle](lifecycle.md), affected feature reference |

Sources stay beside version-sensitive claims.

Concrete implementations: [source examples](../examples/README.md), [UI extension recipes](../examples/ui-recipes.md).
