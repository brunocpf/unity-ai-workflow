# Task workflow

Default to continuous development across sessions: set up the project, build the first playable slice, then keep extending, testing and refining the same project. See [request scope](references/adoption.md#request-scope) and [continuous development](references/adoption.md#continuous-development).

Use a short project AGENTS.md for invariants, focused skills for procedures, and CI for executable checks. Installing the kit doesn't create a project; see [adoption](references/adoption.md).

1. Follow [context discipline](references/context-efficiency.md). Read project rules and the relevant feature/asset reference. [Clarify unresolved intent](references/clarification.md) before dependent work; keep known answers and continue independent work while waiting. Select a skill from the [index](references/INDEX.md); don't load every reference.
2. Implement the requested behavior in bounded steps. For project setup, follow adoption.md. For gameplay work, implement the requested increment within the [professional baseline](references/engineering-baseline.md) using the chosen architecture and dependency defaults. New game UI follows [art direction](references/ui-art-direction.md): set the visual target and finish a representative screen early. Check uncertain APIs against the pinned Editor.
3. Run tests for what changed ([testing](references/testing.md)). For visual work, run the game and look at the result against its target; fix design gaps as well as rendering bugs.
4. Update changed contracts/ADRs and commit implementation, metadata and relevant docs together.

The first playable slice should include pure Core/Application/Presentation, scoped composition, a representative game screen with MVVM/R3-driven custom controls that meets its visual target, selected content and [localized text](references/localization.md) in a player build, asset import, meaningful tests and CI. With the 6.7 UI profile, make sure Content Directories and UI Builder both work. Implement reusable helpers only when the slice uses them; see the [infrastructure list](references/utilities.md).

Optional [profiles](references/profiles.md) add dependencies and tests for specific kinds of games; listing a profile doesn't mean it's implemented.
