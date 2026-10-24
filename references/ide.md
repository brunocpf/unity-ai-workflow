# IDE setup and compiler settings

Default editor integration: VS Code with Microsoft's Unity extension, C# and C# Dev Kit, plus a pinned Unity Visual Studio Editor package. Unity's legacy VS Code Editor package is not the default. [Official setup](https://code.visualstudio.com/docs/other/unity).

## Track the setup, regenerate the solution

1. Merge [settings](../starter/ide/settings.json), [extensions](../starter/ide/extensions.json) and [tasks](../starter/ide/tasks.json) into .vscode/. Preserve unrelated settings. These files are tracked; Unity-generated root csproj/sln/slnx files stay ignored.
2. In Unity External Tools select the installed VS Code integration and generate the owned runtime, UI, Editor and test projects. Set `dotnet.defaultSolution` to the **Unity-generated root solution filename**, not the hand-maintained tooling/dotnet/Game.sln (that one is the pure test/build workspace). The starter's Game.slnx is a placeholder to replace with the actual name. Open the Unity project root in VS Code.
3. Copy [owned-projects.json](../starter/ide/owned-projects.json) to tooling/ide/. Replace its project names and namespace roots with the actual owned asmdefs, including tests. Remove unused sample entries and add new owned assemblies as you create them. Match exact names, not a Game.* prefix that might catch a vendor assembly.
4. Copy [IdeProjectSettings](../examples/Editor/IdeProjectSettings.cs) and [IdeProjectXml](../examples/Editor/IdeProjectXml.cs) into Game.Editor. OnGeneratedCSProject adds a labeled property group **only to allowlisted projects**, preserving references, defines, target framework and other configuration. Don't hand-edit generated csproj files or add a root Directory.Build.props that changes vendor projects.
5. Use **Workflow → Development → Regenerate IDE projects**, or the VS Code task with UNITY_EDITOR set to the pinned executable while the Editor is closed. Update the task's method name if you rename the sample namespace. The menu calls the integration's public SyncAll API. Don't launch a second Editor on the same project. Reload the IDE workspace after regeneration if needed. [SyncAll](https://docs.unity3d.com/cn/current/ScriptReference/Unity.CodeEditor.IExternalCodeEditor.SyncAll.html).

The hook supplies Nullable, LangVersion, RootNamespace and TreatWarningsAsErrors. It doesn't remove extension analyzers wholesale: resolve duplicate analyzer identities narrowly. Preserve generated Unity references/generators; don't import Unity-only analyzers into Core to silence an IDE issue.

## Three compiler contexts

| Context | Settings come from |
|---|---|
| Unity Editor/player | Per-asmdef csc.rsp and analyzer arguments |
| Pure .NET projects | Hand-maintained projects + tooling/dotnet/Directory.Build.props |
| Unity IDE projects | Regeneration hook + tooling/ide/owned-projects.json |

All three must agree on the language version and nullable context for the same source. SDK/runtime versions, platform defines and analyzer binaries may differ deliberately. The [quality check](code-organization.md) compares the SDK and IDE project settings with owned-projects.json. Changing the C# profile updates all three in one change. A modern host SDK doesn't give Unity newer language support.

## Logical namespaces

Use the game's logical root plus layer/feature, for example `PocketArena.Composition` or `PocketArena.Core.Combat`. Assets/Game/Unity and other folder segments are not automatically namespace segments. Record rootNamespace per owned project; nested feature namespaces follow the module. Moving a file between tooling and Unity views must not change its namespace.

The starter disables IDE0130 and folder matching **only under owned Assets/Game C#** because its physical Unity path intentionally differs. Don't change every namespace to fit the IDE, disable naming rules globally, or suppress CS8632. [IDE0130](https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/style-rules/ide0130).

## When something looks wrong

After regenerating, Unity API completion should work in a MonoBehaviour, go-to-definition should cross from Composition into Application/Core, and `?` annotations should not raise CS8632. If they don't, check the selected solution, the owned-projects.json names and whether the hook ran. Diagnostics on a shared file can come from both the Unity and SDK copies; check the source project in the diagnostic.
