# Source examples

Read only the row needed for a task. These use the temporary C#9 compatibility profile with nullable enabled, **not a released Unity project**. [Verification](Verification/README.md) distinguishes API compilation from Unity import/runtime acceptance. The authoritative design remains [construction](../references/ui-construction.md), [binding](../references/ui-binding.md), [lifecycle](../references/lifecycle.md) and [USS](../references/ui-styling.md).

| Need | Source |
|---|---|
| Exact `UiTemplates.GetRequired` behavior | [UiTemplates](Unity/UI/UiTemplates.cs), [resolver contract](Unity/UI/IUiTemplateResolver.cs), [ScopedContext](Pure/ScopedContext.cs) |
| IDs, dependency roots and owned template dictionary | [catalog](Unity/UI/UiTemplateCatalog.cs), [library](Unity/UI/UiLibrary.cs) |
| Preload actual Content Directory catalogs | [loader](Unity/UI/ContentDirectoryUiLoader.cs) |
| Safe runtime construction, including nested controls | [factory](Unity/UI/UiFactory.cs) |
| Regeneration-safe owned IDE settings | [Editor callback](Editor/IdeProjectSettings.cs), [XML transformer](Editor/IdeProjectXml.cs), [IDE setup](../references/ide.md) |
| UI Builder resolution and cache invalidation | [Editor adapter](Editor/AuthoringUiTemplates.cs), [import invalidation](Editor/UiCatalogPostprocessor.cs) |
| Constructor-complete custom element | [control](Unity/UI/Elements/InventorySlot/InventorySlot.cs), [UXML](Unity/UI/Elements/InventorySlot/InventorySlot.uxml), [USS](Unity/UI/Elements/InventorySlot/InventorySlot.uss) |
| Inspector authoring → pure gameplay config | [EnemyDefinition](Unity/Runtime/EnemyDefinition.cs), [EnemyConfig](Core/Combat/EnemyConfig.cs), [authoring contract](../references/authoring.md) |
| Pure MVVM state and commands | [ViewModel](Presentation/InventorySlotViewModel.cs), [snapshot](Presentation/InventorySlotState.cs), [application port](Application/IInventory.cs), [state](Application/InventoryState.cs), [demo service](Application/DemoInventory.cs) |
| Default mechanical R3 binding | [binding adapter](Unity/UI/InventoryBinding.cs) |
| Authored native 6.7 localized UI | [UXML](Unity/UI/Previews/Localization/LocalizationPreview.uxml), [USS](Unity/UI/Previews/Localization/LocalizationPreview.uss), [setup](#localization-fixture-setup) |
| Optional R3 → native binding | [native adapter](Unity/UI/NativeInventoryBinding.cs), [view state](Unity/UI/InventoryViewState.cs) |
| Mount/dispose a screen | [screen owner](Unity/Composition/InventoryScreen.cs) |
| Recycled rows without retained subscriptions | [list controller](Unity/UI/InventoryListController.cs) |
| Interactive authoring example | [preview window](Editor/InventoryPreviewWindow.cs) |
| Custom drawing and text effects | [ArcMeter](Unity/UI/Elements/ArcMeter/ArcMeter.cs), [WaveLabel](Unity/UI/Elements/WaveLabel/WaveLabel.cs), [preview](Unity/UI/Previews/Effects/EffectsPreview.uxml), [advanced policy](../references/ui-advanced.md) |
| Optional LitMotion value transitions | [ArcMeterMotion](Optional/LitMotion/ArcMeterMotion.cs); needs project package qualification |
| Visible decorative clock and regression fixtures | [VisibleMotionClock](Unity/UI/Motion/VisibleMotionClock.cs), [clock check](Tests/Unity/MotionClockChecks.cs), [cascade UXML](Unity/UI/Previews/Cascade/CascadeProbe.uxml), [cascade check](Tests/Unity/CascadeProbeChecks.cs), [qualification guide](../references/visual-fixtures.md) |
| Latest-result guard beyond UI | [LatestRequest](Pure/LatestRequest.cs) |
| Executable checks | [scope/request tests](Tests/PureChecks.cs), [pure ViewModel/boundary tests](Tests/ViewModelChecks.cs), [IDE XML tests](Tests/IdeProjectChecks.cs) |

## Adopt the source

These examples demonstrate architecture and API contracts. Their minimal demo appearance is not a finished-game visual target; use the project's [art direction](../references/ui-art-direction.md) when adopting controls.

Copy selected sources, not this entire directory, into the project:

| Source | Destination / assembly |
|---|---|
| Core/Combat | `Assets/Game/Core/Combat/` → Game.Core; BCL-only immutable config |
| Unity/Runtime/EnemyDefinition | `Assets/Game/Unity/Runtime/Combat/Authoring/` → Game.Unity.Runtime; asset instances in Content/Combat/Definitions |
| Pure/ScopedContext | `Assets/Game/Core/Lifetimes/` → Game.Core; no engine/R3 references |
| Pure/LatestRequest | `Assets/Game/Application/Async/` → Game.Application; the helper itself uses only System |
| Application | `Assets/Game/Application/Inventory/` → Game.Application; references R3, no Unity |
| Presentation | `Assets/Game/Presentation/Inventory/` → Game.Presentation; pure R3 + Application/Core |
| Unity/UI (preserve Elements/<Control>/) | `Assets/Game/Unity/UI/` → Game.UI; Presentation/Core, R3, Unity.Properties/UIElements; no Application use-case access |
| Optional/LitMotion | `Assets/Game/Unity/UI/Elements/ArcMeter/` for this control-owned motion adapter → Game.UI with the pinned LitMotion assembly; see verification limits |
| Unity/Composition | `Assets/Game/Unity/Composition/UI/` → Game.Composition; constructs screen/ViewModel/binding |
| Editor/IdeProjectSettings and IdeProjectXml | `Assets/Game/Unity/Editor/Development/` → Game.Editor; Editor-only, tracked profile under tooling/ide |
| Other Editor sources | `Assets/Game/Unity/Editor/UI/` → Game.Editor; Editor-only, references UI/Presentation/Application/R3 |
| Verification and console Tests | Keep outside Assets; adapt behavioral tests to the project's test assemblies |
| Tests/Unity | `Assets/Game/Tests/PlayMode/UI/` → project test assembly referencing Game.UI; coroutine helpers called by UnityTest wrappers with an owned live panel |

Use the project's pinned R3 installation; do not copy NuGet build output into Assets. Set explicit asmdef references per [architecture](../references/architecture.md). Unity supplies engine modules; package assembly names come from installed package manifests. When adopting, remap `Workflow.Examples` namespaces and using directives to the game’s recorded layer/feature namespaces; update UXML xmlns and the regeneration task’s fully qualified method too. Keep the example namespaces only in the standalone verification harness. Let Unity generate `.meta` files, then commit them.

1. Import `Elements/InventorySlot/` as one control directory, preserving sibling C#/UXML/USS. Create a **Workflow/UI Template Catalog** asset. Add ID `controls/inventory-slot`, assigning the private `InventorySlot.uxml` template. Do not put an InventorySlot tag inside that private template.
2. Open UI Builder on a separate screen UXML. Drag InventorySlot from the custom-control library; change `preview-title`. Construction resolves through the Editor adapter and the template brings its own USS. No Initialize call, ViewModel or Play Mode is involved.
3. Open **Window → Workflow Examples → Inventory**. The sample application begins with three potions; activation decrements quantity through the command and pure ViewModel and R3 binding path. This window is an authoring harness, not the runtime composition root.
4. For players, build catalog roots into a Content Directory and call `ContentDirectoryUiLoader.LoadRoots(contentPath, cancellation)` during explicit startup. It registers the directory, retrieves its catalog roots and transfers registration ownership to the returned library. Do not serialize LoadableObjectId in ordinary player scenes on the evaluated beta. Follow [content bootstrap](../references/ui-content-loading.md), including the bounded synchronous-load limitation. Explicitly catalog every nested/dynamic control template.
5. After preload, call a synchronous mount method that constructs `UiFactory(library)` and `InventoryScreen(parent, factory, inventory)`. The parent comes from an empty host for the selected PanelRenderer/legacy UIDocument profile; the example accepts a VisualElement and does not implement host setup. For a list, give an unowned ListView and screen-owned item ViewModels to InventoryListController, configure height/virtualization for the real design, and retain the controller.
6. The UI session owner cancels/awaits in-flight startup, disposes screens/list controllers and pools, then the library, which unregisters its owned directory in the default root-loading path. Clear host children/retained handles before unloading. With the advanced ID loader, the caller instead unregisters after the library releases its handles. Do not dispose the shared library when closing one screen. Connect this owner to the [session lifecycle](../references/lifecycle.md); the static reset hook cannot dispose your object graph.

## Definition example setup

Copy EnemyConfig and EnemyDefinition into their mapped assemblies. Create a **Workflow/Combat/Enemy Definition** asset, assign an authored prefab and edit its health/speed. The Unity-side startup/catalog validator calls Compile once per definition to obtain immutable pure configuration; the Unity factory separately uses Prefab. Core never receives the asset. The example validates local values and a required reference; the project adds catalog uniqueness, prefab-asset/component checks and the actual factory/preview scene. It does not create prefabs or silently save Inspector edits. See the authoring contract for the required edit/preservation acceptance.

## Effects example setup

Copy `Elements/ArcMeter/` as one directory; register `controls/arc-meter` in the same template catalog. Copy `Elements/WaveLabel/`; put EffectsPreview.uxml/.uss together in a preview directory. Open EffectsPreview.uxml in Builder: both controls have static attribute-driven visuals without runtime binding or clocks. The runtime factory/content loader uses the same catalog. The stylesheet uses literal demonstration colors; a production control consumes the project theme tokens.

ArcMeterMotion is optional source requiring the project's pinned LitMotion package. A view owner creates it, calls `SetPresentation(visible, reducedMotion)` whenever effective screen visibility/preferences change, forwards the VM's numeric target to `SetTarget(value)`, and disposes before rebind/teardown. Use `SnapTo(value)` for an explicit instant update. It starts inactive and the first state snaps. Hidden/reduced mode cancels and displays the latest target. No concurrent direct/native writer may set ArcMeter.Fill. When upgrading an older copied example, replace `SetTarget(value, reducedMotion, immediate)` with the separate policy call and SetTarget/SnapTo; the removed overload prevents silently reinterpreting its boolean arguments.

For a decorative WaveLabel, the screen can own this clock (not the control constructor). `titleRegion` and `title` are cached element references; `clock` is a screen-owned field:

```csharp
clock = new VisibleMotionClock(
    titleRegion,
    seconds =>
    {
        title.Amplitude = 0.7f;
        title.Phase = seconds * 1.5f;
    },
    () =>
    {
        title.Amplitude = 0f;
        title.Phase = 0f;
    });
clock.SetPresentation(titleIsVisible, reducedMotion);
```

Forward every visibility/preference change; hide includes hidden ancestors and screens covered by navigation. Reset is idempotent; the first eligible tick restores amplitude. Dispose the clock before releasing the elements/content. Reuse one clock for multiple decorative parameters in the same region. It uses unscaled display time, restarts local phase on resume, and never advances simulation. See [text effects](../references/ui-text-effects.md) for glyph/localization limits.

## Visual fixture setup

Copy `Previews/Cascade/` together and register its UXML as `previews/cascade-probe` when testing the Content Directory path. The UXML deliberately references component USS before the low-specificity baseline. In a UnityTest wrapper with an already loaded factory and live panel, clone with `factory.Clone("previews/cascade-probe")`, attach the returned container, then `yield return CascadeProbeChecks.Run(container)` and remove it in finally. Call `yield return MotionClockChecks.Run(panelRoot)` separately. The helpers require a panel updated by the real Unity frame loop; calling MoveNext in a tight loop cannot exercise layout or scheduling. The test harness owns/restores the panel, scene and content lease. It must fail on exceptions and have a suite timeout.

The cascade helper checks accepted computed values, activates an intentionally conflicting baseline, requires rejection, and restores the fixture. The clock helper counts actual callbacks across hidden/reduced/detached/disposed intervals. Extend both to the project's real controls and state transitions. Material/geometry, world color and recording cases are specified in [visual-fixtures.md](../references/visual-fixtures.md); this kit does not include an imported shader gallery, a world test scene or a recording producer.

## Localization fixture setup

Copy `Previews/Localization/` together. In native 6.7 Localization settings, author the agreed source/supported locales and a `UI.Common` Resource Table Collection containing nonempty `menu.title` and `menu.continue` strings. Open LocalizationPreview.uxml in Builder and select locale previews; both properties have native bindings and no VM writer. Retain sibling USS. For runtime content qualification, register its template ID and build/load it using the existing template path; separately include the localization provider data and fonts. Follow [localization acceptance](../references/localization.md#acceptance-and-ci).

This fixture supplies declarations and layout only. It contains no authored tables/settings, gameplay commands, locale preference persistence or imported Unity metadata; create those with the selected Editor during adoption. The inventory demo still illustrates its original minimal English projection; replace demo literals with the localization contract when adopting player-facing code. XML syntax checks are not proof of Builder/native binding/player behavior.

## Defaults and deliberate extension points

- **Default:** synchronous factory + preloaded shared catalog. Add feature catalogs only when measured size/lifetime warrants it. Duplicate IDs fail. Template cycles need build-time graph validation; the sample catalog does not implement that validator.
- **Default:** pure MVVM. InventorySlotViewModel owns projection, formatting and commands; InventoryBinding only maps state/intents. NativeInventoryBinding mirrors the same VM through a Unity notification wrapper. Select one binding adapter per view. Screen composition owns the VM; bindings borrow it. Source examples use ordinary constructors; the project registers these factories/owners at its VContainer roots as specified in [composition](../references/composition.md).
- **Default:** one-way game state plus validated commands. Editable settings use a separate draft and BaseField<T> semantics; see [editing recipes](ui-recipes.md). The demo's state mutation is an illustrative Application service, not a prescription to put domain rules in a ViewModel or adapter.
- **Default:** streams emit on the Unity thread. Adapt external producers at the Unity boundary using the installed R3 scheduler; do not sprinkle dispatch in each setter. Define the project's R3 error handler. Demo state is already main-thread-owned.
- **Default:** bounded catalog-root preload owns its directory registration through UiLibrary. GetRootAssets is synchronous; yielding before it does not make it asynchronous. The advanced LoadAsync alternative owns fresh Loadable handles and borrows a caller-owned directory; its Task boundary drains native completion before releasing on cancellation. Use it only with proven player ID transport. Neither path can claim immediate abort of native I/O. Never start multiple loads for the same session without single-flight coordination.
- **Default:** authoring catalog scan once after invalidation. For large projects, narrow catalog locations or generate an index; preserve asset GUID references. Project changes invalidate future lookups, not existing cloned hierarchy. Recreate preview instances after structural edits; test Builder refresh behavior.
- **Default:** one main-thread context object per static bridge, allocation-free warm scope entry. Reset allocates a new generation token; templates, controls, binding objects and subscriptions allocate at creation/rebind. No zero-allocation claim for the whole UI. Format quantities only when their value changes.
- **Default:** this small USS example is standalone for preview. Promote repeated literal colors/spacing into project theme tokens using [USS policy](../references/ui-styling.md); keep component geometry local. The larger [styling fixture](../starter/UI/README.md) demonstrates shared tokens. Enable grid/filter/material/z-index/component features only through the [capability gates](../references/ui-capabilities.md), not through this base control.

The example public reset/install methods exist for the Editor bridge. In a project, restrict their call sites to Composition/Editor (or use assembly friend access); they are not gameplay APIs. LatestRequest guards result publication but does not cancel work or undo server side effects; combine it with cancellation and dispose rejected assets.

Standalone examples explicitly enable nullable references. After adoption, verify assembly-wide nullable across all compiler hosts and remove redundant local directives (IDE0240); see [code quality](../references/code-quality.md). The independent SDK projects demonstrate layer compilation; they are verification harnesses, not a substitute for project asmdefs, full architecture checks, container registration, editor import or player acceptance.

## Screen and modal navigation

[UiNavigationStack](Unity/UI/Navigation/UiNavigationStack.cs) and [UiStackEntry](Unity/UI/Navigation/UiStackEntry.cs) implement synchronous screen/modal ownership and focus handoff while leaving Move/Submit native. See the [navigation contract](../references/ui-navigation.md) before adapting; the [isolated Play Mode runner](Verification/NavigationPlayMode/README.md) exercises the native device-input path and duplicate-router rejection.
