# Native UI navigation — kit 0.3.6

6 October 2026, macOS arm64. Scope: workflow source, native-first policy, synchronous screen/modal reference and isolated test runner. No consuming game, installed/global kit or Editor version is migrated. OpenSpec lifecycle, artifacts/scenarios, generated integrations and existing gates are unchanged.

## Change and review

[Navigation policy](../references/ui-navigation.md) establishes native Move/Submit, one Cancel owner, semantic screen intents, gameplay gating and justified custom traversal. UI skill, binding, styling, dependencies, motion and acceptance references route to that policy. Passive overlays are separate from the menu stack. [Migration](../references/upgrades/ui-navigation-0.3.6.md) assesses existing behavior and preserves customized coordinators/tests.

The reference owns entry lifetimes, top-layer enabled/visible state, initial/restored/fallback focus, nested modals, replacement and pending-handoff cancellation. It has no raw input Move/Submit handlers or per-frame focus loop. Review corrected the empty-panel focus handoff, removed that anchor from focus eligibility while menus are open, clarified ownership after a committed change throws, and switched the fixture to the current versioned PanelRenderer reload callback. Teardown attempts all entry cleanups and releases the gate even if one throws.

Reviewed the full diff, existing control activation examples, skill routing and policy consistency before publishing. Existing InventorySlot uses native Button.clicked and needs no custom router. The earlier general overlay wording was narrowed to avoid treating toasts/tooltips as focus-stack entries. The synchronous example is explicitly not an animated/global/multi-player router.

## Runtime evidence

The [runner](../tools/run_navigation_fixture.py) creates a new project, imports the reference, enables the new Input System and per-assembly nullable/warnings-as-errors, then restarts and runs windowed Play Mode. Profile: Unity **6000.7.0b3**, built-in Input System **6.7.0**, Test Framework **1.9.0**, PanelRenderer/default UITK input, no scene EventSystem. Input states are queued through keyboard/gamepad/mouse devices and processed by Unity's normal loop. Results are asserted after processed frames.

The ten tests cover native move/disabled skipping; keyboard/controller activation and Cancel; modal/restored/fallback focus; repeated Tab containment; reopen/replacement; pending-handoff disposal; gameplay Submit gating through close; nested modal containment; native pointer activation/hidden skipping; child Cancel consumption/persistent roots; repeat; exception cleanup; and duplicate-router rejection. The negative case injects a raw Down handler plus StopImmediatePropagation, catches the ordinary final-focus assertion failure and verifies the unwanted third-button focus. Removing the mutation restores the expected second-button focus.

Batchmode did not deliver the default native UI input path in the initial local probe. That failed attempt was not reclassified as acceptance; the shipped runner requires a graphical session and does not silently substitute synthetic navigation events. Initial package requests were resolved by b3 to its built-in versions; the shipped runner explicitly requests the resolved profile rather than reporting registry versions that did not execute.

Final reviewed fresh-project run: **10 passed, 0 failed, 0 skipped** ([NUnit XML](ui-navigation-036-results.xml), [source/artifact hashes and resolved packages](ui-navigation-036-provenance.json)). No C# compiler warnings/errors appeared in configuration or Play Mode logs. The Editor emitted non-failing internal sort-index diagnostics in two modal tests, retained in the XML; this is not a claim of a diagnostic-free Editor. Full stage logs are retained locally under the task outputs/navigation-0.3.6-evidence directory.

Maintenance checks: API harness build passed with **0 warnings / 0 errors**; **61 Python tests** passed (including missing/failed/skipped/duplicate native-result rejection); link/JSON/XML/skill checks and real OpenSpec integration passed. OpenSpec checks covered both client integrations and lifecycle/evidence gates. These are local results; hosted CI is a separate execution.

## Limits and consumer follow-up

This qualifies the synchronous reference on the recorded Editor profile. It does not qualify physical hardware, target player/IL2CPP, mixed uGUI/EventSystem routing, Unity 7, native text/slider/list editing semantics, multiple panels/players, animated transitions, async preload races or continuous gameplay held-input policies. The child-Cancel test is an explicit consuming callback, not a claim that every editing control has identical Cancel behavior. Visual polish/accessibility and target-device acceptance remain project gates.

The kit CI's Python checks validate evidence rejection and installation; they do not execute Unity. A headless/CI native-input profile must be separately qualified. Existing projects should adopt the focused standards, inspect their current router, port applicable runtime cases and validate their own bindings/provider/transition policy. Updating documentation alone does not fix a game's duplicate dispatch.
