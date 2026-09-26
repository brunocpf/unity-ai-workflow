# MVVM, binding and input

**Default: MVVM with pure R3 ViewModels and thin Unity binding adapters.** Model is Core/Application; Game.Presentation owns ViewModels; Game.UI owns views and binding. No parallel Presenter layer. A ViewModel owns presentation decisions and command coordination, never a VisualElement or Unity asset handle. This separation follows the usual MVVM responsibility split; R3 and UITK are the chosen implementation. [MVVM responsibilities](https://learn.microsoft.com/en-us/dotnet/architecture/maui/mvvm).

```text
Application state → ViewModel → immutable presentation snapshot
                                  ↓ binding adapter (R3 or native UITK)
                             custom element + UXML + USS
                                  ↓ semantic intent
Application command ← ViewModel ← binding adapter
```

One ViewModel per screen or independently stateful feature. Rows get their own ViewModel when identity/editing/behavior warrants it; plain decorative controls do not. Screen ownership is explicit: dispose binding, then ViewModel, then remove view and release content. Recycling replaces the row binding; row ViewModels belong to the data/screen lifetime, not accidentally to a reusable visual slot.

## Ownership and testability

ViewModels consume Application ports and optional pure presentation services (formatting, localization, navigation requests). They select coherent state, map errors, manage editable drafts, expose enabled/busy/validation state and issue commands. They use Task/ValueTask/cancellation for pure asynchronous coordination. The Unity boundary handles PlayerLoop/scheduler adaptation. Rules and final authorization remain in Application/Core.

Binding adapters subscribe and map already-decided values/actions. They do not select inventory items, format quantities, validate purchases, decide retries or own application services. All those decisions must be testable without constructing Unity UI. View behavior owns focus, pointer capture, animation and layout. Use narrowly defined navigation intents/ports instead of giving a ViewModel a scene manager.

Every visual property has one writer. Use either direct R3 mapping or native binding for that property, never both. Likewise, coordinate USS/LitMotion/Animator ownership. Reusable elements expose typed value APIs and semantic intents; no external private-child queries or service lookup. [Constructor-complete controls](ui-construction.md) remain usable in Builder without ViewModels or Play Mode.

## Snapshot size and render scope

**View states must be small snapshots scoped to the visual element they render.** Our adapter calls that element's Render method for each emission; a large screen-wide snapshot makes unrelated changes repeat work throughout the view. Keep only displayed values and command availability, not full domain state, entity collections or asset graphs. Split independently changing regions (HUD, inventory rows, settings, results) into separate projections; select and deduplicate their inputs before formatting or allocating snapshots. Preserve coherence for fields that must change together.

Render only the affected region. Reuse unchanged row data, virtualize large lists, and cache child queries. Test that unrelated application changes do not emit/render a region; profile allocations and UI update cost on representative screens. This bounds memory and refresh work and keeps interaction responsive. UITK retains its visual tree and can invalidate individual properties; an emission does not inherently rebuild every node or force a complete GPU repaint.

## Binding choice

**R3 adapter is the default:** subscribe to a replaying ViewModel state, call the view's Render/SetValue API, forward semantic events to ViewModel commands, and dispose symmetrically. State projection/formatting stays in the ViewModel. For authored localized labels/assets, **native localization binding is the default**; the VM does not write those properties. [Localization](localization.md#ui-toolkit-mvvm-and-r3-ownership) defines dynamic text ports, locale ownership and the optional native Smart String path. Native binding is otherwise a deliberate alternative for forms and substantial declarative screens; MVVM does not require a particular binding engine.

For native binding, use a Unity-side notifying wrapper that mirrors the ViewModel snapshot with Unity.Properties attributes. Assign all fields before notifying changed properties. The wrapper owns no use cases or second set of presentation rules. Core/Application/Presentation remain free of Unity interfaces. Unity documents CreateProperty and INotifyBindablePropertyChanged for native sources. [Binding sources](https://docs.unity3d.com/6000.7/Documentation/Manual/UIE-runtime-binding-define-data-source.html).

Stable native bindings normally live in UXML/Builder; C# SetBinding is for dynamic bindings or an explicit code-authored adapter. Clear owned bindings/dataSource on release; preserve structural declarations across rebinding where appropriate. Do not assume binding to ReactiveProperty.Value makes UITK observe R3. Avoid per-frame polling; measure update and subscription costs on representative screens rather than assuming either engine is faster.

The [source examples](../examples/README.md) use one pure InventorySlotViewModel with two interchangeable binding adapters. The native wrapper is optional. No canonical ICommand package, ViewModel base class, mediator or global navigation bus is required. Add a reusable command abstraction only for repeated tested needs; explicit methods with busy/cancellation policy are the default.

UI Builder preview uses constructor structure, attributes and optional authoring data. Runtime VM binding alone does not provide application state in Builder; authored localization bindings can preview configured table entries without a runtime VM. For editable BaseField<T> controls use SetValueWithoutNotify on model reflection and one semantic change event for user edits.

## Input and editing policy

One-way presentation plus commands is the default for inventory, combat, purchases, and other authoritative game state. Two-way binding is appropriate for a local editable draft, not unrestricted mutation of game rules.

| Situation | Pattern |
|---|---|
| Health/currency HUD | Read-only state → view; no view-to-domain setter |
| Settings | Bind a local draft; validate/apply explicitly, or document immediate apply |
| Text input | Preserve editing buffer, caret and IME composition; commit at the designed point |
| Search/autocomplete | Debounce and latest-result policy; distinguish cancellation from server side effects |
| Purchase/submit | Prevent duplicate execution; show pending/success/error; command remains authoritative |
| Slider preview | Local continuous preview; commit/persist at a declared boundary |
| Drag/drop | Manipulator owns pointer capture and cancel; application validates the final move |
| Multiplayer data | UI reflects authoritative/predicted states explicitly; no visual callback owns authority |

Keyboard/gamepad intent should enter the same command path as pointer intent. Do not make a control work only through one callback attached to a visual child.

Screen/ViewModel/binding ownership follows [reactive](reactive.md). UI acceptance follows [validation](validation.md); appearance and modern capability gates follow [styling](ui-styling.md).
