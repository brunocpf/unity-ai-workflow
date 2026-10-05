# Example verification

The API harness builds Core (including EnemyConfig), Application and Presentation as separate engine-independent projects, then RuntimeCheck (EnemyDefinition), Unity UI and Composition/Editor references against the installed Unity 6000.7.0b3 managed assemblies. The [b3 record](../../verification/unity-b3.md) reports current results; installation completion and Editor/player execution are separate. Compiler warnings (including nullable) fail these API builds. The ViewModel checks execute presentation behavior without Unity and inspect direct compiled references. The authoring cache includes explicit post-import invalidation; actual Builder/import execution remains a project acceptance case. The root-loader adaptation owns its registration; its API compile does not inherit Pocket Arena's runtime evidence automatically. The harness does not run Unity source generators/import, enforce every project module/transitive package rule, register VContainer, build content or render UI. Full analyzer enforcement is a separate adopted-project gate; this API harness disables SDK analyzers to isolate compatibility checks.

ArcMeter and WaveLabel are included in UiCheck. This checks the installed drawing and text callback API signatures; it does not prove tessellation, fresh text meshes, source-generated UXML attributes or appearance. Optional/LitMotion is excluded from ApiCheck because the kit does not install that Unity package. The separate LitMotionCheck accepts a project's actual compiled package assembly; compile/import ArcMeterMotion and run the advanced UI lifecycle/visual cases before adoption. Shader/filter recipes are guidance, not prebuilt verified graph assets. The authoring definition sample has API compilation coverage only; Inspector serialization, prefab/catalog wiring, validation diagnostics and edit preservation need actual Editor acceptance. No gameplay prefab or authoring scene is supplied by these two source files.

IdeProjectChecks exercises the BCL-only generated-project XML transform: exact owned allowlist, vendor preservation, repeatability, XML namespaces, property overrides, reference/define preservation and invalid profiles. ApiCheck also compiles the Editor callback/public regeneration API. Neither proves the selected integration invokes the callback or the IDE language service works; run [IDE capability acceptance](../../references/ide.md) in the adopted project.

The console check executables are kit maintenance probes, not the project’s NUnit runner; port the applicable cases into its test suites.

VisibleMotionClock is included in UiCheck; ApiCheck also compiles the Tests/Unity cascade and clock coroutine helpers. These are real-panel regression helpers, not console-executable Unity tests. Import the sibling cascade UXML/USS, wrap the helpers in UnityTests and run the [fixture setup](../README.md#visual-fixture-setup) before recording runtime acceptance. Shader/world/recording fixtures remain adoption contracts; no generated graph or recorder is bundled. Optional LitMotion is still outside the default harness; a separately recorded package-reference build does not prove its animation behavior.

PureChecks runs lifetime/request tests; ViewModelChecks runs state projection, commands, disposal and selected assembly-boundary checks on .NET 10. Source remains C#9-compatible until a validated modern profile is selected.

Run in a scratch copy of `examples/` to keep build outputs out of the kit. The projects have separate build directories. Package-using projects each have lockfiles. Core/PureChecks have no external package requirements.

```sh
dotnet build Verification/ApiCheck/ApiCheck.csproj -p:RestoreLockedMode=true -p:UnityManagedDir="/path/to/Editor/Managed/UnityEngine"
dotnet run --project Verification/PureChecks/PureChecks.csproj --configuration Release
dotnet run --project Verification/IdeProjectChecks/IdeProjectChecks.csproj --configuration Release
dotnet run --project Verification/ViewModelChecks/ViewModelChecks.csproj --configuration Release -p:RestoreLockedMode=true
```

Optional package API check (same scratch copy):

```sh
dotnet build Verification/LitMotionCheck/LitMotionCheck.csproj -p:RestoreLockedMode=true -p:UnityManagedDir="/path/to/Editor/Managed/UnityEngine" -p:LitMotionAssembly="/path/to/project/Library/ScriptAssemblies/LitMotion.dll"
```

This references the existing package; it neither installs nor redistributes its binary. A missing assembly fails the check. Record the project package lock alongside the compiler result.

On the reviewed macOS installation, UnityManagedDir is `/Applications/Unity/Hub/Editor/6000.7.0b3/Unity.app/Contents/Resources/Scripting/Managed/UnityEngine`. Other installations may place these assemblies elsewhere; locate `UnityEngine.UIElementsModule.dll`. SDK 10 is a harness requirement, not the Unity project's C# language profile.

Acceptance before promoting this into a project template:

- Import using separate Core/Application/Presentation/UI/Composition/Editor asmdefs and installed R3; verify generated UXML registration and property bags, then build the chosen player backend (including IL2CPP if targeted).
- Fresh Builder drag/drop, preview attribute change, nested controls, stylesheet/template/catalog reimport and move; open Builder during Play.
- Direct R3 rendering and, separately, optional native binding notifications after commands; binding/ViewModel dispose/rebind; list scroll/recycle/sort/refresh with no retained state/subscriptions. Confirm keyboard/gamepad activation.
- Missing/duplicate/cyclic catalog entries, cold Content Directory preload, partial failure, cancel during native load, owner shutdown and directory unregister after consumers are removed.
- Three Play/Stop cycles without recompilation, assembly reload and startup failure recovery. Check no duplicate callbacks and no retained leases.
- Capture and inspect the UI/game on target dimensions/devices. Measure retained objects, allocations during interaction, frame time and content load/unload separately. API compilation and pure allocation checks do not satisfy these gates.

Recorded results live in the kit's maintenance report, separate from project runtime evidence.

The root review also records compiler/analyzer and hook-orchestration probes run in disposable workspaces. Project acceptance must repeat these against its actual setup, including Unity per-assembly response discovery and real Husky/LFS wiring.

## Native localization fixture

LocalizationPreview UXML/USS demonstrates the documented native 6.7 localized binding declaration. Packaging checks XML structure and sibling stylesheet resolution. No localized tables/settings are supplied; this fixture has not been imported or exercised in UI Builder or a target player. Follow its setup and localization acceptance before reporting integration as verified. No new runtime C# helper is supplied by the localization contract.
