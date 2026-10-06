# Native focus and screen navigation

Read when creating/changing menus, keyboard/controller input, modal layers or screen transitions. [Binding](ui-binding.md) owns MVVM; this file owns navigation. **Default: native UITK Move and Submit, one Cancel owner per panel, a Unity-side stack for hierarchical screens/modals.** Do not add a raw Input System focus router to ordinary menus.

## One executing path per operation

| Operation | Default owner |
|---|---|
| Directional focus, Tab, navigation repeat | UITK focus controller; author focusability, layout and disabled state |
| Pointer/keyboard/controller activation | Native control activation → one semantic intent → ViewModel command |
| Cancel/back | Native control first (editing/popup); then the panel's screen coordinator |
| Open/close/replace screen, request confirmation | Pure semantic navigation request; Unity coordinator mounts/disposes views |
| Gameplay input while UI is active | Composition's gameplay gate/action-map policy; never a second UI dispatcher |

For pure UITK use its default runtime event system and the project's UI actions. For mixed uGUI/UITK, use the supported EventSystem/InputSystemUIInputModule path. Audit active input providers; do not install another provider merely to navigate a menu. Do not bind raw Submit to a ViewModel command alongside Button.clicked. Do not process Cancel independently in both a global Escape handler and the panel handler. Opening Pause and closing it need a declared ownership handoff that cannot reuse the opening press.

MVVM purity does not require putting focus traversal in Presentation/Application. Keep VisualElement references, focus restoration, pointer capture and native events at the Unity boundary. Screens expose semantic intents; native button activation reaches the same command path as pointer activation.

Custom traversal requires a concrete requirement native focus/layout cannot satisfy (e.g. an unusual spatial graph). First consider focusability/tab order or an appropriate focus ring. Keep customization scoped and prove integration/suppression against the selected Editor. **StopPropagation/StopImmediatePropagation does not guarantee cancellation of post-dispatch focus behavior.** Never paper over two owners with a debounce, arbitrary frame delay, or repeated Focus calls. Inspect the version's dispatch implementation and test final focus. Preserve intentional hold-repeat and native text/slider/list behavior.

## Stack policy

Use a stack for hierarchical menus: push Options, pop Back, replace a completed screen. Modals form a topmost substack. Only the top entry accepts input; underlying screens may remain visible behind a modal but cannot take focus or clicks. Root/persistent screens explicitly decide whether Cancel dismisses them. Separate toasts, tooltips, drag previews and HUD from the navigation stack. Tabs, parallel panes and split-screen/player-local UI need their own region/state model; do not force them through a global stack.

Each entry owns its view, binding, ViewModel and per-screen resources. The panel/library outlives entries. Dispose in dependency order; unsubscribe even when teardown fails. Record the invoking control before covering a screen. After layout, restore it if attached, visible and enabled; otherwise resolve a valid initial target. Style :focus visibly. A modal needs a full-region hit-testable scrim; z-index alone is not modality. Across panels, coordinate both focus and gameplay gates explicitly.

Transitions have one owner. Prepare/load content before committing an entry. Commit synchronously on the main thread; reject reentrant changes. Cancel stale asynchronous preparation and dispose results that lose the request-generation check. A pending focus handoff or animation completion cannot restore a popped/disposed screen. For LitMotion, follow [transition state/lifetime rules](ui-advanced.md): define when input becomes ready, coordinate removal with animation completion, cancel old handles and test rapid competing requests. Do not attach completion callbacks that mutate a newer stack.

Gameplay blocking must be authoritative for every gameplay command. UI actions stay enabled. Either gate gameplay commands/state or disable the relevant gameplay maps with a tested restoration policy. Handle held controls deliberately: continuous movement may need a neutral/release barrier on returning to gameplay; enabling an action can perform an initial-state check. Do not reinterpret the closing Submit/Cancel as a gameplay action. Multi-region blockers need owned leases/reference counts; one menu's close must not unblock another.

## Executable reference and limits

[UiNavigationStack](../examples/Unity/UI/Navigation/UiNavigationStack.cs) and [UiStackEntry](../examples/Unity/UI/Navigation/UiStackEntry.cs) implement one attached panel's dedicated, full-region menu host. The panel-root Cancel handler also receives Cancel with no focused control, allowing an optional Pause-opening callback without a parallel Escape listener. The empty host is programmatically focusable but excluded from Tab order, so the panel keeps receiving native navigation. The reference confines its own entries; other interactive roots/panels must be separately gated by composition. There must be exactly one such coordinator per panel; if empty Cancel has no meaning, pass a no-op. Construct after the host attaches; dispose before panel teardown/reload and build a new coordinator for the new root.

Pass freshly prepared entries and a focus fallback resolver. Once an entry is inserted, ownership has transferred, including if subsequent teardown/gate callbacks throw; do not retry the insertion. An entry rejected before insertion remains caller-owned. The coordinator exposes Top/Count for diagnosis. Gate callbacks should be nonthrowing, synchronous and must not navigate reentrantly. View display/enabled state belongs to the coordinator; internal control state belongs to the view.

Stack refresh is proportional to stack depth and runs only on navigation changes; focus eligibility is checked once per handoff. There is no per-frame traversal, observable snapshot rebuild or allocation loop. Keep stacks bounded and profile actual animated screens.

This is a **synchronous, zero-duration** reference, not an asynchronous animated router, service locator or reusable-control base class. It intentionally contains no Move/Submit callbacks, Input System reads, per-frame focus enforcement or content loading. Adapt the existing project coordinator rather than install a second one. [Runnable Play Mode fixture](../examples/Verification/NavigationPlayMode/README.md) demonstrates native input and lifecycle tests; [verification record](../verification/ui-navigation-036.md) bounds tested compatibility.

## Acceptance

Use a real runtime panel with the selected native input provider active. Queue device input through that provider (plus target hardware/player acceptance); direct SendEvent or calling a router method alone is insufficient. Assert final focus after event processing/layout frames, not just inside the custom callback.

Cover one press/one move, exactly-once Submit/pointer activation, keyboard/controller parity, disabled/hidden controls, Tab, repeat, initial/restored/fallback focus, modal containment, reopen/replacement, pending-focus disposal and callback teardown. Include nested modals, text/native controls consuming Cancel, gameplay gating through opening/closing and held-input policy. Test animation/preload races if present. A duplicate-router mutation must fail the ordinary navigation expectation; otherwise the test may bypass the native path. Runtime results do not replace visual :focus/readability and target-device checks.

Sources: [Unity 6.7 runtime event system](https://docs.unity.com/en-us/engine/6000.7/manual/uitoolkits/uielements/uie-support-for-runtime-ui/uie-render-runtime-ui/uie-runtime-event-system), [focus order](https://docs.unity.com/en-us/engine/6000.7/manual/uitoolkits/uielements/uie-events/uie-focus-order), [navigation event implementation](https://github.com/Unity-Technologies/UnityCsReference/blob/master/Modules/UIElements/Core/Events/NavigationEvents.cs). The source link tracks master; the runtime evidence applies only to its recorded Editor/package profile.
