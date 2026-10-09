# Language profiles and transition

C# 9 is a **temporary compatibility profile**, not the long-term coding standard. The intended modern profile is C# 14 on a Unity build that supports it. The user expects an upcoming alpha; treat that as a planning input and verify the exact release's compiler/runtime/backend support at adoption. The published Unity roadmap confirms the direction, not an acceptance result or guaranteed date. [Unity announcement](https://unity.com/blog/unite-seoul-keynote-2026-recap).

| Profile | Use | Compiler/style |
|---|---|---|
| Compatibility | 6000.7.0b3 evaluation target; [b3 API compilation](../verification/unity-b3.md) passes, project Editor/player acceptance remains required | C# 9, netstandard2.1 pure compile, block namespaces |
| Modern evaluation | Selected alpha/preview that proves C#14 support | C# 14, verified API targets/backends, modern style overlay |
| Modern production | Promoted supported build after project release gates | Same modern conventions with the validated shipping matrix |

At bootstrap inspect the requested/installed Editor and release notes, then prove a representative compiler/API probe. For a workflow trial prefer the modern evaluation profile once available and validated. Do not reinstall/upgrade every project merely because a newer Editor exists. Commit the selected profile and pins in docs/architecture.md (toolchain section; native locks own versions); both Unity and pure harness compile the same language/API-compatible sources.

Modern defaults: file-scoped namespaces, target-typed construction and collection expressions when clear, readonly structs/records for appropriate pure values, required/init for non-Unity DTOs when validated, primary constructors for small stateless services, and C#14 field-backed properties/extensions when they simplify a concrete API. Avoid blanket rewrites or forcing every feature into the newest syntax. Unity serialization, generators, reflection/stripping, Burst and each player backend remain distinct compatibility checks.

After proving the modern profile, set the SDK LangVersion and tooling/ide/owned-projects.json languageVersion to 14.0, regenerate IDE projects and verify [three-host parity](ide.md), adopt [modern EditorConfig options](../starter/language-profiles/csharp14.editorconfig) into the existing owned-code section and adopt the [C#14 csc.rsp options](../starter/language-profiles/csharp14.rsp) beside each owned asmdef and validate Unity's compiler configuration. Do not merely edit generated Unity csproj files or upgrade the host SDK and claim engine support. Keep nullable enabled in both profiles.

Migration: isolated upgrade branch → exact Editor/packages/modules → language/API/serialization probes → compile/import and generated code → pure/VM tests → content/player/backend builds → reload/performance/visual regression → ADR/migration notes → promote template tag. Do not retain C#9-only style restrictions after the project has legitimately promoted its modern profile.
