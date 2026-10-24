# Example build projects

These SDK projects compile the examples outside Unity so they stay buildable, and run their console tests. They're for maintaining the kit; a game uses its own asmdefs and test assemblies.

- **CoreCheck, ApplicationCheck, PresentationCheck** build the pure layers as separate engine-independent projects.
- **RuntimeCheck, UiCheck, ApiCheck** compile the Unity-facing examples (EnemyDefinition, UI controls including ArcMeter, WaveLabel and VisibleMotionClock, composition, Editor code and the Play Mode test helpers) against an installed Editor's managed assemblies. Compiler warnings, including nullable warnings, fail the build.
- **PureChecks** runs the lifetime/request tests; **ViewModelChecks** runs state projection, command, disposal and assembly-boundary tests; **IdeProjectChecks** tests the generated-project XML transform. All three run on .NET 10 without Unity.
- **LitMotionCheck** compiles the optional LitMotion adapter against a project's compiled LitMotion assembly. It isn't part of ApiCheck because the kit doesn't install LitMotion.

Compiling against Unity's assemblies catches API mistakes; it doesn't run Unity import, source generators or rendering. Try the examples in a project before relying on them. The console test programs aren't NUnit; port the cases you need into the project's test assemblies.

The examples use C# 9 for compatibility. Run the projects in a scratch copy of `examples/` to keep build output out of the kit:

```sh
dotnet build Build/ApiCheck/ApiCheck.csproj -p:RestoreLockedMode=true -p:UnityManagedDir="/path/to/Editor/Managed/UnityEngine"
dotnet run --project Build/PureChecks/PureChecks.csproj --configuration Release
dotnet run --project Build/IdeProjectChecks/IdeProjectChecks.csproj --configuration Release
dotnet run --project Build/ViewModelChecks/ViewModelChecks.csproj --configuration Release -p:RestoreLockedMode=true
```

Optional LitMotion check:

```sh
dotnet build Build/LitMotionCheck/LitMotionCheck.csproj -p:RestoreLockedMode=true -p:UnityManagedDir="/path/to/Editor/Managed/UnityEngine" -p:LitMotionAssembly="/path/to/project/Library/ScriptAssemblies/LitMotion.dll"
```

This references the project's existing package; it neither installs nor redistributes LitMotion.

On macOS, UnityManagedDir is `/Applications/Unity/Hub/Editor/<version>/Unity.app/Contents/Resources/Scripting/Managed/UnityEngine`. Other installations may differ; look for `UnityEngine.UIElementsModule.dll`. The .NET 10 SDK is only needed for these projects; it doesn't change the Unity project's C# version.
