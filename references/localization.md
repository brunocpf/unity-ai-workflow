# Localization from the first slice

**Localization is baseline infrastructure for player-facing text, even when the first release has one language.** Keep Core rules, saves and network data language-independent. Ask for source language, supported locale codes/regions and launch versus later coverage using [clarification](clarification.md); do not invent a translation scope. Record the contract in `docs/project.md (language scope) and docs/architecture.md (localization ownership)`. Build the infrastructure while answers are pending; don't add languages nobody asked for.

## Select the installed API generation

| Profile | Default |
|---|---|
| Unity 6.7 | Built-in **Localization Runtime**, namespace `Unity.Localization`, with Resource Table Collections for strings/assets. Use native UITK localization bindings for authored labels. |
| Older Editor/profile | Pin a compatible `com.unity.localization` release; package 1.5 uses `UnityEngine.Localization`, separate String/Asset Tables and different settings/provider APIs. Follow that version's documentation. |
| Addressables or translation exchange required | For native 6.7, use `com.unity.localization` 2.0 for Addressables and the documented CSV/XLIFF import/export integration. Don't add it just to localize a label. |

The 6.7 manual documents this built-in/package split. In the 6.7 API, `InitializeAsync`, `SelectedLocale` and `PreloadBehavior` are static, while `GetLocale` is an instance member; don't infer signatures from XML summaries or old package samples. [Native overview](https://docs.unity.com/en-us/engine/6000.7/manual/localization), [legacy UITK binding](https://docs.unity3d.com/Packages/com.unity.localization@1.5/manual/UIToolkit.html).

## Authoring and content

- Create Localization settings through Project Settings and keep the asset in `Assets/Game/Settings/Localization/`. In native 6.7, locales live inside these settings. Author Resource Table Collections under `Assets/Game/Content/Localization/<module>/`; keep control C#/UXML/USS together in their existing control directory. UI Builder selects the table entry for each localized property. [Setup](https://docs.unity.com/en-us/engine/6000.7/manual/localization/get-started), [locales](https://docs.unity.com/en-us/engine/6000.7/manual/localization/locales).
- Partition tables by feature/lifetime, such as `UI.Common`, `UI.Inventory` and narrative chapter. Use stable semantic keys such as `menu.continue` and `inventory.capacity`; preserve table/entry identities through renames and translation round trips. Add speaker/context, variables, tone and meaningful size constraints. Do not use English prose as identity or duplicate identical messages across every control.
- Store complete sentences in tables. Use named Smart String variables and locale-specific plurals/conditions, not English fragments joined in C#. Send raw numbers/dates to formatting; display culture follows the selected locale while save/network serialization stays invariant. User content is data, never trusted format syntax. [Smart Strings](https://docs.unity.com/en-us/engine/6000.7/manual/scripting/smart-strings).
- Default to the native built-in table/file path for local strings, and directly referenced localized assets for small local content. Record providers and build inclusion explicitly; use an existing content adapter for larger/remote assets. The 6.7 beta documents JSON file tables as the default player format and `PlayModeSource.GeneratedFiles` for testing the real file path; the fast Editor source-asset mode doesn't show what the player will load. **UI Content Directories load templates; localization tables, fonts and localized media need their own build inclusion.** Check the actual provider/build setup in a player build before release.
- Keep translator exchange/glossary/source files under `SourceAssets/Localization/`. Choose one editable authority and a controlled, validated import/export path; preserve manually reviewed translations. AI translations are drafts marked as such until a person reviews them. A narrative tool integrates through one authoritative translation pipeline rather than duplicating catalogs.
- Do not bake translatable words into generated sprites/textures. Prefer a text overlay; use localized assets for unavoidable signs, cultural variants, audio/subtitles and layouts that actually differ. Treat them like other generated media ([assets](assets.md)).

## UI Toolkit, MVVM and R3 ownership

Every property still has one writer. Native localization does not replace MVVM or make Unity types part of Presentation.

| Content | Default writer and boundary |
|---|---|
| Fixed authored label, tooltip or localized image | Native localized binding in the control/screen UXML; the VM and Render method never overwrite that property. |
| Game-dependent message, quantity or denial | VM chooses the semantic key/arguments and uses an injected pure text port; its small snapshot carries the resulting display string. Unity implements the locale/table/formatter adapter; ordinary R3 binding maps the final value. |
| Substantial declarative Smart String UI | Explicit alternative: the VM exposes the decided key/primitive variables; a mechanical adapter updates the native localized binding's variables. Native binding is the only text writer. No duplicate VM-formatted string for that property. |
| Animated counter or text effect | Retain the same locale/formatting policy; the view owns only interpolation/glyph rendering. Follow [text effects](ui-text-effects.md). |

For native 6.7, this is a complete localized property declaration inside a co-located UXML template; the template also references its sibling USS. Create the `UI.Common` table and `menu.continue` entry first:

```xml
<ui:UXML xmlns:ui="UnityEngine.UIElements" xmlns:loc="Unity.Localization">
    <ui:Style src="ContinueButton.uss" />
    <ui:Button name="continue" class="continue-button">
        <Bindings>
            <loc:LocalizedString property="text" table="UI.Common" entry="menu.continue" />
        </Bindings>
    </ui:Button>
</ui:UXML>
```

Use UI Builder's Add binding action to author localized properties; localized reference types implement UITK binding and update on locale changes. Dynamic C# binding can use `LocalizedString.SetReference` and `SetBinding`; stable declarations belong in UXML. No new Initialize call or service lookup in custom-control constructors. Binding readiness is separate from constructing the tree. [Native UITK localization](https://docs.unity.com/en-us/engine/6000.7/manual/localization/translations/localize-ui-toolkit).

An example declaration is in [LocalizationPreview](../examples/Unity/UI/Previews/Localization/LocalizationPreview.uxml). Its [setup](../examples/README.md#localization-preview-setup) needs authored tables/settings; it isn't a configured localization project or a finished visual design.

### Reusable adapter contract

Implement only the helpers consumed by the first slice:

- **Pure text port**, for example `IUiText` in Presentation: format a stable message ID plus a small typed argument value, and expose replaying readiness/locale-content revision. No Unity locale, table handle or formatter type crosses the boundary. The VM combines relevant state with a ready revision, deduplicates inputs, then formats; tests inject a fake. Error codes become keys in Presentation, not localized domain exceptions.
- **Unity text adapter** in `Unity/UI/Localization` (Game.UI implements the Presentation port without a Runtime → Presentation dependency): initialize native settings, preload required strings, resolve/format through Unity and publish ready revisions on the Unity thread. A synchronous format contract is valid only after its required data is ready; a provider that remains asynchronous needs an explicit asynchronous port/latest-request policy. Never block loading from Render, a constructor or an R3 projection. The beta's synchronous `GetLocalizedString` can return empty when data isn't loaded yet, so don't treat empty text as ready.
- **Locale preference adapter** in `Unity/Runtime/Localization`, implementing an Application settings port: default to immediate language apply through a settings VM → Application command. The engine's active Localization settings own the selected locale. Persist a locale code through the project's settings repository; supply a startup selector and disable any competing preference writer. Use saved supported choice → device match → project/source locale, with explicit validated fallbacks. A pure observable mirrors the engine selection; it is not a second authority.
- Native `LanguageDropdown`/`LanguageRadioButtonGroup` are a deliberate shortcut for view-local immediate preferences: they directly select the locale. If used, make that the sole selection path and bridge persistence once; do not add a competing VM setter. A draft Apply/Cancel settings page needs the normal VM-controlled field. [Native language controls](https://docs.unity.com/en-us/engine/6000.7/manual/localization/translations/localize-ui-toolkit).

Composition ensures both adapters use the same active native settings and explicit readiness boundary; UI and Runtime never reference each other. Engine-owned static APIs stay behind these adapters, with no project static localization service or ViewModel lookup. One session scope owns these adapters, their engine event subscriptions, preload state and cached formatting data; screen/row scopes own subscriptions and localized asset leases. Cancel or invalidate old locale/row requests and reject late delivery after reuse/disposal. During switching, keep a declared loading/last-good policy and publish coherent text within each small region; do not rebuild the screen tree. Declare command behavior while language data is pending. Fast Play Mode must recreate scopes without retaining old event handlers.

## Performance, fonts and layout

Preload first-screen strings for the active locale and its fallback chain; load later modules on demand. Avoid all-language/all-voice preload. Cache only bounded, reusable formats/results and invalidate them on locale/content revision. Format when displayed inputs change, not every frame; virtualized lists must not retain one binding per offscreen data item. Parsed Smart Strings are disposable pooled objects and formatter instances have thread constraints; reuse them only behind a measured, owned adapter. [Formatting performance](https://docs.unity.com/en-us/engine/6000.7/manual/scripting/smart-strings/performance).

Use UITK/TextCore font assets with licensed glyph coverage and fallback chains for the agreed scripts. The modern Advanced Text Generator supports shaping but doesn't support static font assets in the documented profile; check font generation, atlas growth and stripping in a player build. Set text language direction deliberately; RTL text does not automatically define navigation/layout mirroring. Test mixed-script text, IME, graphemes and reveal effects. [Advanced Text Generator](https://docs.unity.com/en-us/engine/6000.7/manual/uitoolkits/uielements/uie-work-with-text/uie-get-started-with-text), [language direction](https://docs.unity.com/en-us/engine/6000.7/manual/uitoolkits/uielements/uie-work-with-text/language-direction).

USS uses flexible sizes, wrapping and tested minimums; avoid fixed English-sized widths or automatic shrinking as the universal fix. Localize accessible names, validation messages and input hints as well as visible labels. Separate icon meaning from text length; mirror only directional artwork/navigation that the design calls for. Document pseudolocales as test tools, not supported translations.

## Tests and CI

- An Edit Mode test checks tables against owned UXML, authored assets and dynamic C#/VM keys: missing keys, duplicate identities, malformed formats/argument mismatches, fallback cycles and missing required translations. Allowlist intended regional fallbacks and intentionally empty entries. Scanning for string literals helps review but won't find everything. Never copy source text into untranslated locales to make a check pass.
- Pure tests cover message choice, arguments, formatting and re-projection on locale change; unrelated state changes shouldn't refresh text. Integration tests cover real plural rules (zero/one/many and locale-specific categories), number/date formats, selection/persistence/fallback, and a switch with unchanged gameplay state.
- UI Builder preview should work before Play Mode. Try locale switching, reopening screens, recycled rows and repeated sessions. Check a player build for built tables, fallback fonts and localized assets; the Editor's warm data can hide missing content.
- Look at representative screens in each supported locale and in an expansion pseudolocale, including CJK/RTL scripts if supported, the smallest layout, focus/input and animated text.
- Run the table check in CI. Keep an eye on startup/switch time and font/table memory against the project's budgets.
