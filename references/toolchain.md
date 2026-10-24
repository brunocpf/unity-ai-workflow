# Toolchain and compatibility

Reference Editor: **6000.7.0b3**. Keep production, 6.7 UITK evaluation and future Unity 7 profiles separate. ProjectVersion.txt and packages-lock.json are the authority for resolved versions; the reference Editor is not an automatic choice for shipping games.

Record the Editor version and modules, CLI version, Pipeline package, render pipeline, test/analyzer packages, .NET SDK and any experimental UI flags in docs/architecture.md. Don't float latest/lts, Git main or CI installer channels.

Unity 6.7's documented language baseline is C# 9. A CoreCLR player or newer host SDK doesn't provide C# 14. C# 9 is temporary; [language profiles](language-profiles.md) covers the C# 14 transition. Adopt modern syntax incrementally; compiler support, APIs, serialization, AOT and Burst compatibility are separate concerns. Candidate features: file-scoped namespaces/collection expressions; pure DTO records/init/required; small-service primary constructors; C# 14 extension members, field properties and span conversions; partial events/constructors only for justified generators. [Unity compiler](https://docs.unity3d.com/6000.7/Documentation/Manual/csharp-compiler.html), [C# 14](https://learn.microsoft.com/en-us/dotnet/csharp/whats-new/csharp-14).

## Lint

[Code quality](code-quality.md) owns nullable/compiler/analyzer/style rules; [developer tooling](developer-tooling.md) owns local setup and hooks.

Use the starter EditorConfig and a Roslyn-compatible Microsoft.Unity.Analyzers version, installed in each compiler host: Unity's analyzer import, and build-time analysis in the SDK projects. An IDE extension alone isn't enough. Keep generated/vendor code out of owned-code checks; prefer narrow suppressions and Unity-aware suppressors for serialized fields/messages. [Unity analyzers](https://github.com/microsoft/Microsoft.Unity.Analyzers), [Unity installation](https://docs.unity3d.com/6000.7/Documentation/Manual/roslyn-analyzers.html).

## CLI

Choose and record the CLI version per project. For a new project, use a current compatible release; existing projects keep their pin until an intentional upgrade. CI installs that exact version; never self-update or use a floating installer channel during a build.

Use the available Unity CLI/package skills for command syntax, discovery, installation and connection; [skill ownership](context-efficiency.md#skill-ownership) defines the fallback. Don't duplicate their bootstrap flows. The project adds these rules:

- Target the explicit game path and confirm the returned project identity. Author serialized scenes/prefabs through Editor operations so GUIDs and edits survive; C#/UXML/USS can be edited as text. Keep setup idempotent.
- Wait for package resolution and import/compilation to finish before relying on package changes. Domain reload can destroy static polling callbacks, so track long operations externally. Check compilation/Safe Mode before treating a connection failure as a package problem.
- Launching or dispatching a job is not completion. Keep the operation identity and poll its status to a terminal result with a timeout. Never redispatch a mutation just to poll it.
- Treat missing output, transport failures, timeouts and interruptions as failures, not passes. Retry only when the earlier outcome is known or the operation is idempotent.
- Fast Editor compilation is feedback, not a replacement for the quality check, tests or player builds. Read diagnostics instead of assuming a successful connection means a successful compile.
- Use the exact project Editor selector; partial versions may resolve another patch. Review generated CI installers for floating versions. Choose signed distribution or intentionally unsigned asset export explicitly; never downgrade signing silently on an authentication failure.

[CI](ci.md) owns build/test policy. For missing command providers use installed help and the [official CLI reference](https://docs.unity.com/en-us/unity-cli/unity-cli-reference); check APIs in the selected Editor's official documentation.

## Editor upgrades

Read the candidate's release notes and known issues. Try the new Editor on a separate branch or copy: resolve packages, compile, run the tests, build and launch the target, and look at graphics and content. Rebuild Content Directory content after the upgrade, since archive formats can change between 6.7 releases; keep the old build available for rollback. Review settings/metadata changes before promoting the pin. See [lifecycle](lifecycle.md) for fast Play Mode and [UI capabilities](ui-capabilities.md) for experimental features. Installed plugin skills may target older Unity versions: record project exceptions instead of editing downloaded caches.
