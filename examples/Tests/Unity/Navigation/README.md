# Navigation Play Mode tests

Play Mode tests for [UiNavigationStack](../../../Unity/UI/Navigation/UiNavigationStack.cs) using real native input. Copy this folder into a project's Play Mode tests (for example `Assets/Game/Tests/PlayMode/UI/Navigation/`) together with the navigation sources, and adjust the asmdef references to the project's UI assembly.

The tests need the new Input System enabled and PanelSettings with a theme. `NavigationSetup.Configure` (Editor folder) enables the Input System and creates the PanelSettings; update its paths to wherever you copied the folder. Run them **windowed**: on the 6.7 beta, batch mode doesn't drive UI Toolkit's default device input, so headless CI needs a runner with a graphical session.

The tests use PanelRenderer with an attached panel and native default input handling, with no EventSystem or custom focus ring. The sibling UXML/USS supplies test layout; loading it from Resources is a shortcut for tests, not the production content-library pattern. Keyboard/gamepad/mouse states are queued through the Input System and processed by the player loop; the tests don't dispatch NavigationMoveEvent manually or call InputSystem.Update. Input settings and devices are restored in teardown.

Cases cover native movement and disabled skipping, keyboard/gamepad activation and Cancel, nested screen/modal containment, Tab, restored/invalidated focus, reopen/replacement/disposal, pending focus cancellation, pointer activation, hidden controls, child Cancel consumption, persistent-root Cancel, gameplay Submit gating on close, held repeat and exception cleanup.

These tests cover synchronous, zero-duration navigation. Add your own tests for animated transitions, async content preparation, physical controllers, multiple panels/players and target builds. See the [navigation reference](../../../../references/ui-navigation.md).
