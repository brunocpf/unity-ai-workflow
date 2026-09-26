# Constructor-complete UI and content

Controls must render in UI Builder without Play Mode, a runtime ViewModel or external Initialize/ApplyAssets. Ordinary files: `Control.cs`, `Control.uxml`, `Control.uss`; descriptors are optional only for additional configuration. The private template cannot recursively instantiate its own custom type. A leaf derived from an already-rendering control (for example WaveLabel from Label) may need no private template if it has no structural assets. Give any asset-dependent or composite control its constructor-complete template; never require an external Initialize to acquire its skin.

UXML owns stylesheet references:

```xml
<ui:UXML xmlns:ui="UnityEngine.UIElements">
  <ui:Style src="InventorySlot.uss" />
  <ui:Button name="activateButton">
    <ui:Label name="title" />
  </ui:Button>
</ui:UXML>
```

Concrete implementation: [UiTemplates and control examples](../examples/README.md). The control constructor clones its registered private UXML through `UiTemplates.GetRequired(InventorySlot.TemplateId)`.

Clone once per instance, not per attachment/binding/emission; do not attach the same USS again. Expose contentContainer only for intentional user content. [ViewModels/binding adapters](ui-binding.md) provide runtime data after construction.

## Control directory contract

One reusable control per `Assets/Game/Unity/UI/Elements/<Control>/` directory: `<Control>.cs`, its private `<Control>.uxml`, `<Control>.uss`, and any control-owned shaders/materials/icons. Keep partial C# declarations and dedicated manipulators beside their owner. A leaf such as WaveLabel still gets a folder; create UXML/USS only when it needs those assets. One control does not imply one asmdef or Content Directory build: retain Game.UI and group runtime content by loading lifetime.

Screens use `UI/Screens/<Screen>/` for their visual C#, UXML/USS and mechanical binding adapter. Pure ViewModels remain in Presentation; DI/session hosts remain in Composition. Shared styles live in UI/Theme, shared behaviors in UI/Behaviors and template/catalog/loading code in UI/Content. Shared accepted media belongs in Content/UI. A preview/gallery has its own folder, not a dependency on a live gameplay screen.

```text
UI/
  Elements/UpgradeCard/
    UpgradeCard.cs
    UpgradeCard.uxml
    UpgradeCard.uss
  Elements/WaveLabel/
    WaveLabel.cs
  Screens/Arena/
    ArenaScreen.cs
    ArenaScreen.uxml
    ArenaScreen.uss
    ArenaBinding.cs
  Theme/
  Content/
```

The control UXML uses a sibling stylesheet reference, for example `src="UpgradeCard.uss"`. Catalog IDs remain stable and asset references remain GUID-based; filesystem folders are not runtime lookup keys. When migrating an existing project, move through Unity or move each asset with its existing .meta in an isolated checkout, update relative UXML/USS imports and Editor/build path strings, regenerate IDE projects, then reimport and validate Builder plus a cold content/player load. Creating fresh metadata during a move breaks this contract.

## Resolution and factory contract

UiTemplates is the only default ambient dependency exception: read-only structural UI assets, never gameplay services. A runtime UiFactory enters a synchronous context and clones/constructs controls; nested controls inherit it. Deferred factories such as ListView.makeItem must enter the owning module's context too.

- Active runtime context: dictionary lookup of already-loaded templates; missing key throws without authoring fallback.
- No context in Editor: Editor-only source resolver supports UI Builder.
- No context in player: error.
- No awaits, I/O, blocking loads, background access or nested Editor event pumping in construction scopes. Use a concrete stack-only ref struct Dispose pattern, not boxed IDisposable/AsyncLocal; async opening calls a separate synchronous factory after preload. Enforce strict nesting, main-thread access, disposal identity and stale-session rejection. Lifecycle details belong in [lifecycle](lifecycle.md).

An unscoped runtime call in the Editor is indistinguishable from authoring at lookup. Enforce factory use by checking owned constructor/CloneTree call sites and by player tests. For hosts that instantiate UXML automatically, start with an empty host and attach factory-created trees after preload, or validate an explicit integration hook. Never assume a host enters our context.

## Catalog and lifetime

1. A ScriptableObject catalog explicitly registers stable IDs → VisualTreeAssets, including nested/dynamic controls. Custom-control tags do not declare constructor-loaded template dependencies. Reject duplicate/missing IDs and template cycles.
2. Build catalog roots with Content Directories. UXML-referenced USS and assets are dependencies; no duplicate style list. Use public APIs, not internal hashed filenames. Follow the [player bootstrap and ownership contract](ui-content-loading.md): the evaluated beta cannot serialize LoadableObjectId into ordinary player scenes.
3. Preload a bounded shared control library before UI construction. Publish readiness only after complete success; release partial/late acquisitions on failure/cancellation. An independently available loading/error shell covers startup.
4. UI subsystem owns the shared-library lease. Optional large modules own their leases until all related screens, detached trees and pools are gone. Dynamic item artwork loads separately.
5. Teardown consumers first, unregister templates, then release content. Closing one screen does not unload the shared library. Structural template replacement recreates instances; ordinary themes change root tokens/classes.

## Editor adapter

Install authoring resolution before Builder construction, independent of scene bootstrap. Stable IDs/GUID mapping and lazy catalog cache; no FindAssets per control. Refresh relevant catalog/import/move/delete/code changes. The supplied [postprocessor](../examples/Editor/UiCatalogPostprocessor.cs) invalidates after UXML/USS/.asset imports, moves or deletions; the next lookup rebuilds once. Its .asset filter is conservative for deleted catalogs, and does no scanning inside import callbacks. Keep project-change invalidation as an additional path. [Unity import callback](https://docs.unity.com/en-us/engine/6000.0/script-reference/unityeditor/assetpostprocessor/onpostprocessallassets). Keep UnityEditor APIs in Editor assemblies. Builder and runtime can coexist; Application.isPlaying is not a resolver-context test.

Prove fresh Editor drag/drop, attributes/style edits, nested controls, asset moves, assembly reload and Builder during Play. Also prove cold player, missing/cancelled load, recycling and unload/reload. See [validation](validation.md) for evidence and [utilities](utilities.md) for measurement targets.

Sources: [custom controls](https://docs.unity3d.com/6000.7/Documentation/Manual/UIE-create-custom-controls.html), [UXML styles](https://docs.unity3d.com/cn/6000.0/Manual/UIE-add-style-to-uxml.html), [Content Directories](https://github.com/Unity-Technologies/UnityDataTools/blob/main/Documentation/contentdirectory-format.md). The supplied resolver/factory source has an API compile check; Unity import/runtime acceptance remains required.
