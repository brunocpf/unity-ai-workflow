# Native navigation integration fixture

From the kit root, with a licensed Unity 6000.7.0b3 Editor and a graphical desktop:

```sh
python3 tools/run_navigation_fixture.py \
  --editor /path/to/Unity \
  --workspace /absolute/new/disposable-navigation-run
```

On macOS the executable is inside `Unity.app/Contents/MacOS/Unity`. The workspace must not exist. The runner creates an isolated project, copies only the navigation reference/fixture, enables nullable and the new Input System, creates PanelSettings with the default theme, then restarts before Play Mode. It pins the b3 built-in Input System 6.7.0 and Test Framework 1.9.0. It retains per-stage logs, fresh NUnit XML and the resolved package lock; nonzero Editor exits, missing/partial/skipped/failed test coverage fail the runner. It never edits an existing game or installs an Editor.

The Play Mode run is **windowed**: on the recorded b3/macOS profile, batchmode did not exercise the default UITK device-input path. Do not turn that into a passing synthetic-event fallback. Headless CI needs a separately qualified graphical/native-input profile. Routine Python kit CI validates the runner's result rejection; it does not run Unity.

The fixture uses PanelRenderer, its versioned reload callback, an attached panel and native default input handling. It has no EventSystem or custom focus ring. Authored sibling UXML/USS supplies test layout; Resources is a fixture dependency shortcut, not a replacement for the kit's production content-library pattern. Queued keyboard/gamepad/mouse states are processed by the native player loop; tests do not dispatch NavigationMoveEvent manually or call InputSystem.Update. Test input settings/devices are restored on teardown.

Cases cover native movement/disabled skipping, keyboard/gamepad activation and Cancel, nested screen/modal containment, Tab, restored/invalidated focus, reopen/replacement/disposal, pending focus cancellation, pointer activation, hidden controls, child Cancel consumption, persistent-root Cancel, gameplay Submit gating on close, held repeat and exception cleanup. The mutation adds a raw Down action that focuses the second button plus a propagation-stopping callback. The ordinary final-focus assertion must fail, and focus must end on the third button; after removing the mutation, native Down must reach the second button normally.

This tests synchronous zero-duration navigation. It does not certify animated transitions, async content preparation, physical controllers, every native editing control, multiple panels/players, target builds, or continuous gameplay held-input policies. Extend the consuming game's existing tests for those features. [Navigation contract](../../../references/ui-navigation.md) and [recorded evidence](../../../verification/ui-navigation-036.md) define scope.
