# C# quality and nullable references

Use the [owned-code EditorConfig](../starter/.editorconfig) at the Git/Unity project root: Allman formatting, mandatory braces, explicit accessibility, focused correctness/async rules and naming. Keep enums/events PascalCase (no mandatory E prefix), interfaces I-prefixed, type parameters T-prefixed and private fields _camelCase. Use var when the initializer makes the type apparent. Avoid broad all-analyzers severity changes and duplicate/conflicting rules.

Rules target Assets/Game and tooling. Don't reformat vendor/generated code or edit PackageCache. Add scoped rules for an owned embedded package when one is created. Unity serialized YAML keeps whitespace handling separate from source. Public mutable fields are not the default API; validated authoring records may expose fields deliberately.

File/member/layout conventions and the quality check are in [code organization](code-organization.md).

## Enable nullable reference types

**Nullable annotations and warnings are enabled for all owned C#, including Unity adapters/UI/Editor and tests.** EditorConfig cannot enable the compiler's nullable context.

- Copy [csc.rsp](../starter/csc.rsp) beside **each owned asmdef**, including UI, runtime, Editor and test assemblies. It enables nullable and warnings-as-errors, sets the language profile and passes the root EditorConfig to the compiler. Merge existing options deliberately. A single Assets/Game/csc.rsp does not configure child asmdefs. Don't put this strict file in Assets/csc.rsp: that is a broad fallback and can affect third-party assemblies.
- Unity uses the response file in the assembly folder, otherwise the Assets-root fallback; they are not additive. Keep common flags in sync across all owned response files. [Unity response-file lookup](https://github.com/Unity-Technologies/UnityCsReference/blob/master/Editor/Mono/Scripting/Compilers/ResponseFileProvider.cs).
- Standalone source examples keep `#nullable enable` so they can be copied safely. Once nullable is on for the Unity, SDK and IDE projects, remove redundant directives from adopted code. IDE0240 is warning-level in owned source; don't suppress it or use `#nullable disable` as an escape. SDK projects need their own Nullable setting. [IDE0240](https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/style-rules/ide0240).
- Choose the [language profile](language-profiles.md); C# 9 is temporary and C# 14 is the intended upgrade. Copy [Directory.Build.props](../starter/Directory.Build.props) to tooling/dotnet/ for SDK projects: Nullable=enable, the selected LangVersion (starter fallback 9.0), warnings as errors and build-time analysis. Pin a .NET 10 SDK in the repository-root global.json used by local and CI dotnet commands.
- Unity-generated IDE projects get nullable/language settings from [the generation hook](ide.md); never hand-edit those outputs. For the modern profile, use the [C# 14 response options](../starter/language-profiles/csharp14.rsp) and matching SDK/style configuration once the selected Editor supports it. Setting langversion can't add compiler support Unity lacks.
- New code has no blanket nullable disable, no global CS86xx suppression and no indiscriminate null-forgiving operator. Model optional values with `?`, validate external data and initialize required state through constructors/factories.
- Unity serialized references may start empty before authoring/wiring. Declare that honestly, validate in authoring and at startup, then pass required references into runtime objects. Use a narrowly justified `null!` only when an enforced initialization invariant can't be represented better. Nullable flow analysis doesn't detect a destroyed UnityEngine.Object: keep Unity-aware `== null` checks at engine boundaries; don't replace them with `is null`/`?.`.

Sources: [nullable compiler option](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/compiler-options/language#nullable), [nullable reference types](https://learn.microsoft.com/en-us/dotnet/csharp/nullable-references).

## Analyzers

Install analyzer assemblies in each compiler host; severity keys alone install nothing. The SDK starter sets analysis level 10.0-recommended; Unity may bundle a different analyzer version. Use a Roslyn-compatible Microsoft.Unity.Analyzers version in Unity. Build-time style checks need EnforceCodeStyleInBuild and explicit diagnostics. [Analyzer configuration](https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/configuration-options).

Keep `-analyzerconfig:.editorconfig` in every owned response file: without it, Unity's compiler may not apply the EditorConfig severities. The path is relative to the compiler working directory (the project root), not the asmdef folder. If nested EditorConfigs exist, pass them too or keep the enforced policy in the root file. This flag selects configuration; it doesn't install analyzers.

To include an analyzer explicitly, add `-analyzer:tooling/analyzers/Microsoft.Unity.Analyzers.dll` with the pinned DLL under tooling, or use Unity's analyzer import mechanism, not both. Don't add a DLL path that doesn't exist or copy host-SDK analyzers blindly.

Treat new owned-code compiler/analyzer warnings as merge failures. Keep justified suppressions narrow, with a reason. In existing projects, a migration baseline can isolate old warnings while rejecting new ones.

GenerateDocumentationFile enables relevant build-time diagnostics; suppress only missing XML comments (CS1591), not nullable warnings.
