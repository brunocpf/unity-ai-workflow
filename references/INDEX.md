# Read by task

Current kit migration: [0.5 decoupling](upgrades/decoupling-0.5.0.md). Load it for adoption, not ordinary feature work.

Do not read this entire directory. References below are authoritative by subject; project-specific decisions belong in the game's docs.

| Task | Required reference | Conditional reference |
|---|---|---|
| Skill delegation / provider conflicts | [Skill ownership](context-efficiency.md#skill-ownership) | Available client skill inventory |
| Session start / resumption / context cost | [Context discipline](context-efficiency.md) | Current issue/change; optional unfinished-work note |
| Foundation / first slice | [Milestones and adoption](adoption.md#milestones-and-request-scope), [architecture](architecture.md), [repository](repository.md), [toolchain](toolchain.md) | [Dependencies](dependencies.md), selected [profile](profiles.md) |
| Unclear requirements / user choices | [Clarification](clarification.md) | [Dependencies](dependencies.md) for framework tradeoffs |
| Languages / translated UI / locale testing | [Localization](localization.md) | [Binding](ui-binding.md), [text effects](ui-text-effects.md) |
| Project standards / release | [Engineering baseline](engineering-baseline.md) | [Modules](modules.md), [reliability](reliability.md) |
| Scenes / prefabs / tuning / generation | [Editor authoring](authoring.md) | [Repository](repository.md), [validation](validation.md) |
| Composition / scopes | [Composition](composition.md) | [Lifecycle](lifecycle.md) |
| IDE / autocomplete / regeneration | [IDE setup](ide.md) | [Code organization and coverage](code-organization.md) |
| Source organization / formatting coverage | [Code organization](code-organization.md) | [Code quality](code-quality.md), [IDE setup](ide.md) |
| C# / lint / hooks | [Code quality](code-quality.md), [developer tooling](developer-tooling.md) | [Language profiles](language-profiles.md) |
| Pure rules / application | [Architecture](architecture.md) | [R3/async](reactive.md), [utilities](utilities.md) |
| Custom control / loading | [UI construction](ui-construction.md) | [Lifecycle](lifecycle.md), [binding](ui-binding.md), [content bootstrap](ui-content-loading.md) |
| New screen / game UI design / visual quality | [Art direction](ui-art-direction.md) | [Advanced UI](ui-advanced.md), [asset pipeline](assets.md), [visual fixtures](visual-fixtures.md) |
| Menus / focus / screen stacks | [Native navigation](ui-navigation.md) | Actual input-provider tests |
| Styling / modern UITK | [USS](ui-styling.md) | [Capability gates](ui-capabilities.md) for modern features |
| Custom drawing / shaders / motion | [Advanced UI](ui-advanced.md) | [Capability gates](ui-capabilities.md), [text effects](ui-text-effects.md) |
| Text rendering / reveal / counters | [Text effects](ui-text-effects.md) | [Advanced UI](ui-advanced.md) |
| Effects / cascade / motion qualification | [Visual fixtures](visual-fixtures.md) | [Scenario clocks / fresh captures](test-scenarios.md) |
| Particle effects / VFX Graph | [VFX authoring and setup](vfx.md) | [Dependencies](dependencies.md), [visual fixtures](visual-fixtures.md) |
| 3D asset | [Asset contract](assets.md), [3D pipeline](assets-3d.md) | [Motion reference](assets-motion.md) |
| Textures / sprites / pixel art | [Asset contract](assets.md), [2D pipeline](assets-2d.md) | [Validation](validation.md) |
| CI / builds | [CI](ci.md) | [Toolchain](toolchain.md), [validation](validation.md) |
| Standalone check execution | [Engineering checks](engineering-checks.md) | Existing local/CI commands |
| Tests / visual review | [Validation](validation.md) | [Scenario clocks / fresh captures](test-scenarios.md); [lifecycle](lifecycle.md) for reload/resource issues |
| Workflow kit update | [Applicability and updates](workflow-updates.md) | Project contracts, ADRs and native version pins |
| Package decision | [Dependencies](dependencies.md) | [Optional libraries](dependencies-optional.md), [profiles](profiles.md) |
| Shared helpers / optimization | [Utilities](utilities.md) | [Lifecycle](lifecycle.md), affected feature reference |

Sources remain beside version-sensitive claims. Historical observations live in the kit's installation/review records, not task instructions.

Concrete implementations: [source examples](../examples/README.md), [UI extension recipes](../examples/ui-recipes.md).
