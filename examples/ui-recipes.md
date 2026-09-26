# UI extensions without changing the base architecture

| Use case | Implementation rule |
|---|---|
| Editable local settings | A draft presentation model owns edits; Apply validates and issues an Application command. Cancel discards the draft. Bind to the draft, not persisted/domain state. |
| Custom scalar field | Derive BaseField<T>, put editing visuals in its input element, and implement SetValueWithoutNotify to update visuals silently. User edits use `value` to emit ChangeEvent<T>; a model-to-view write uses SetValueWithoutNotify. Test equality suppression, keyboard focus, mixed values and label behavior. |
| Search / async item art | Cancel the old request, obtain a LatestRequest ticket, await outside construction scope, then check cancellation + ticket before publishing. Dispose rejected asset leases. An item ViewModel owns its request; each recycled view has a fresh binding scope. Reject results for old item identities. |
| ListView / TreeView | Factory in makeItem; binding adapter per visual binding lifetime; ViewModel per item/screen lifetime; dispose before rebind/unbind/destroy. The [list example](Unity/UI/InventoryListController.cs) supplies this ownership. Stable item IDs belong to data, never visual row indices. Refresh/rebuild explicitly when source membership changes. |
| Drag/drop / manipulators | Local manipulator owns registration, pointer capture and transient drag state. Handle capture loss, Escape, detach, disabled state and disposal. Emit one semantic drop proposal; Application validates it. Keyboard/gamepad uses the same command. |
| Modal / overlay | Screen owner controls focus return, input blocking, close/cancel and disposal. Put overlay in a dedicated root layer; z-index cannot bypass arbitrary clipping or parent stacking constraints. |
| Procedural controls / shaders / transitions | Use the [advanced UI guide](../references/ui-advanced.md), ArcMeter and the optional LitMotion owner; effects stay in the view. |
| Glyph effects / dialogue reveal / counters | Use the [text guide](../references/ui-text-effects.md) and WaveLabel; shaped glyphs are not string character indices. |
| UI components / rich effects | Use reusable visual behavior where verified in the selected Editor; avoid sharing mutable per-instance effect state. Effects do not own application services or navigation. Keep a supported visual fallback and device budget. |
| Localization / themes | Use [localization ownership](../references/localization.md): native authored labels and small dynamic VM projections refresh on locale change; do not rebuild controls just to change text. Apply root classes/tokens for themes. Test long strings, CJK, scaling and accessibility. |

For small settings drafts, immediate apply is allowed when reversible and deliberately documented; save debounce remains a separate persistence responsibility. Binding mode is a decision about authority, not convenience.

For a new control, copy the structural pattern, not the Inventory domain: template ID, constructor clone/query, preview attributes, semantic public API, typed Render/reset methods by default or optional Bind/Unbind/declarative bindings, owned ViewModel and scoped binding adapter, and focused acceptance tests. Do not force every control to have its own ViewModel when it only needs local visual behavior.
