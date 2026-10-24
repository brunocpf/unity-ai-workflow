# Testing

Test at the boundary you changed. Documentation-only edits don't need player builds. Keep flaky tests visible and fix them; rerunning until green hides the problem. A test run that finds zero tests is a failure, not a pass.

| Layer | What to test |
|---|---|
| Pure Core | Game rules, inventory/economy invariants, domain transitions |
| Application/R3 | Fake time/frames, initial and replayed state, cancellation, overlapping requests, recoverable errors, late results after disposal |
| Persistence | Versioned save migrations, corrupt or interrupted data, provider contracts |
| Presentation/MVVM | Projection, enabled/busy/error states, command routing, disposal/rebind and late-result rejection, all without Unity |
| Architecture | Layer/module dependencies (Core never references Unity), no service lookups from forbidden layers, scope registration |
| Edit Mode | Authoring assets and references, catalogs, serialization, localization table and format coverage |
| Play Mode | Input → rules → state → UI, scenes, pooling, cleanup |
| Player build | Content included, code stripping/AOT (IL2CPP), startup, platform input and graphics |

Run the same pure sources in the fast .NET test project and in Unity. Use fake time/frames instead of sleeps in reactive tests. Test once-only actions after a screen reopens or a pooled object is reused. Include a few whole-slice tests; mocks can't show that composition works.

In Editor input tests, route synthesized Input System devices to the Game View and restore the previous routing in teardown; Editor focus can otherwise swallow the input. Assert the resulting gameplay action, not just that an event was injected.

Fast Editor compilation tells you the code compiles, not that it behaves correctly or runs in a player. See the [CLI notes](toolchain.md#cli) for compile feedback and [CI](ci.md) for the pipeline.

## Looking at the game

Tests don't tell you whether the game looks or feels right. For visual and gameplay changes, run the game and look at it against the [visual target](ui-art-direction.md): different screen sizes, long and localized text, focus/disabled/error states, and motion. Fix what looks wrong, not just what renders incorrectly. Check assets at gameplay distance and in motion, not only up close.

For editable content, open the scene or prefab, change a value in the Inspector, play, stop and make sure the edit is still there and shared definitions weren't modified by play. See [authoring](authoring.md).

## Performance

Measure on a representative device and scenario, with warmup. Note whether you measured a development or release build. A clean small slice doesn't show that large inventories, scenes or content bundles will fit budgets; add representative load tests before relying on them. UI updates should refresh only the regions whose state changed ([binding](ui-binding.md#snapshot-size-and-render-scope)).
