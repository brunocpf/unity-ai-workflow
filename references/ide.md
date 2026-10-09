# IDE bootstrap and compiler parity

Default editor integration: VS Code with Microsoft's Unity extension, C# and C# Dev Kit, plus a compatible pinned Unity Visual Studio Editor package. Unity's legacy VS Code Editor package is not the default. [Official setup](https://code.visualstudio.com/docs/other/unity).

## Track the setup, regenerate the solution

1. Merge [settings](../starter/ide/settings.json), [extensions](../starter/ide/extensions.json) and [tasks](../starter/ide/tasks.json) into .vscode/. Preserve unrelated user/project settings. These files are tracked; Unity-generated root csproj/sln/slnx files remain ignored. Extension recommendations do not install or prove capability; record installed/tested versions in docs/architecture.md (toolchain section; native locks own versions).
2. In Unity External Tools select the installed VS Code integration; generate the required owned runtime, UI, Editor and test projects. Set `dotnet.defaultSolution` to the **observed Unity-generated root solution filename**, not the hand-maintained tooling/dotnet/Game.sln. The latter is the pure test/build workspace. The starter's Game.slnx is a bootstrap value to replace with the actual name/format. Open the Unity project root in VS Code.
3. Copy [owned-projects.json](../starter/ide/owned-projects.json) to tooling/ide/. Replace its exact project names and logical namespace roots with the actual owned asmdefs, including tests. Remove unused sample entries; new owned assemblies must be added. Match exact names, not a Game.* prefix that might capture a vendor assembly. Reconcile this allowlist with the real asmdef inventory at bootstrap and after assembly changes.
4. Copy [IdeProjectSettings](../examples/Editor/IdeProjectSettings.cs) and [IdeProjectXml](../examples/Editor/IdeProjectXml.cs) into Game.Editor. OnGeneratedCSProject appends/replaces a labeled property group **only for allowlisted projects**. It preserves references, defines, target framework and unrelated configuration. No hand edits to generated csproj files and no root Directory.Build.props that accidentally changes vendor projects.
5. Use **Workflow → Development → Regenerate IDE projects**, or the supplied VS Code process task with UNITY_EDITOR set to the pinned executable while the Editor is closed. Update the task’s fully qualified method name if renaming the sample namespace. The menu calls the selected integration's public SyncAll API. Do not launch a second Editor on the same project. After regeneration reload the IDE workspace when required and verify the selected solution. [SyncAll](https://docs.unity3d.com/cn/current/ScriptReference/Unity.CodeEditor.IExternalCodeEditor.SyncAll.html).

The hook supplies Nullable, LangVersion, RootNamespace and TreatWarningsAsErrors. It has an independently tested XML transformation; actual callback invocation depends on the selected integration package and must be proven in Unity. It does not remove extension analyzers wholesale: resolve duplicate analyzer identities narrowly and keep the selected compatible set. Preserve generated Unity references/generators; do not import Unity-only analyzers into Core merely to silence an IDE issue.

## Three compiler contexts

| Context | Settings authority | Proof |
|---|---|---|
| Unity Editor/player | Owned per-asmdef csc.rsp, actual analyzer arguments | Actual Editor/player compile and rejection probes |
| Pure .NET harness | Hand-maintained projects + tooling/dotnet/Directory.Build.props | Evaluated properties, pure build/analyzers/tests |
| Unity IDE projects | Regeneration hook + tooling/ide/owned-projects.json | Evaluated generated properties and live language-service behavior |

All three must agree on the chosen language version and nullable context for the same owned source. SDK/runtime versions, platform defines and compatible analyzer binaries may differ deliberately. The [quality driver](../starter/quality/check.py) compares evaluated SDK/IDE properties with the owned profile, requires warnings-as-errors and verifies pure-source coverage in both workspaces; the Unity argument/fault gate independently checks the response files. Changing the C# profile updates all three in one change. An extension or modern host SDK does not grant Unity newer language support.

## Logical namespaces

Use the game's logical root plus layer/feature, for example `PocketArena.Composition` or `PocketArena.Core.Combat`. Assets/Game/Unity and other repository layout segments are not automatically namespace segments. Record rootNamespace per asmdef/owned generated project; nested feature namespaces follow the module contract. Moving a file between tooling and Unity shared-source views must not change its namespace.

The starter disables IDE0130 and folder matching **only under owned Assets/Game C#** because its physical Unity path is intentionally different. Do not change every namespace to fit the IDE, disable naming rules globally, or suppress CS8632. Tooling/owned embedded packages need their own explicit policy. [IDE0130](https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/style-rules/ide0130).

## Capability acceptance

After deleting/regenerating ignored IDE outputs, prove: Unity API completion/hover in a MonoBehaviour; go-to-definition from Composition into Application/Core and from UI into Presentation; nullable `?` accepted without CS8632; deliberate nullable dereference reported; the chosen Unity analyzer appears in an appropriate Unity assembly; the selected formatter obeys the repository EditorConfig. Inspect source locations in diagnostics to distinguish Unity and SDK copies of shared files.

Also prove a vendor project is unchanged by the hook, a second regeneration is stable, language/nullable parity survives it, and the pure test workspace remains independently usable. Retain extension/package versions, selected solution, effective compiler properties and observed completion/navigation evidence. A successful dotnet format command or installed extension alone is not IDE acceptance. The confirmed trial findings are nullable mismatch and IDE0130; further language-service capability checks are still separate evidence.
