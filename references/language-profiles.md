# Language profiles and transition

C# 9 is a **temporary compatibility profile**, not the long-term coding standard. The intended modern profile is C# 14 on a Unity build that supports it. Unity's roadmap confirms the direction but not a date; check the exact release's compiler/runtime/backend support before switching. [Unity announcement](https://unity.com/blog/unite-seoul-keynote-2026-recap).

| Profile | Use | Compiler/style |
|---|---|---|
| Compatibility | 6000.7.0b3 reference Editor | C# 9, netstandard2.1 pure compile, block namespaces |
| Modern evaluation | An alpha/preview Editor with C# 14 support | C# 14, modern style overlay |
| Modern production | A supported production Editor with C# 14 | Same modern conventions on the shipping platforms |

At bootstrap check the requested/installed Editor and its release notes, and compile a small file using the C# 14 features you plan to use. For a prototype prefer the modern profile once an Editor supports it. Do not reinstall/upgrade every project merely because a newer Editor exists. Commit the selected profile and pins in docs/architecture.md (toolchain section; native locks own versions); both Unity and pure harness compile the same language/API-compatible sources.

Modern defaults: file-scoped namespaces, target-typed construction and collection expressions when clear, readonly structs/records for appropriate pure values, required/init for non-Unity DTOs when validated, primary constructors for small stateless services, and C#14 field-backed properties/extensions when they simplify a concrete API. Avoid blanket rewrites or forcing every feature into the newest syntax. Unity serialization, generators, reflection/stripping, Burst and each player backend remain distinct compatibility checks.

To switch to the modern profile, set the SDK LangVersion and tooling/ide/owned-projects.json languageVersion to 14.0, regenerate IDE projects and confirm [all three compiler contexts](ide.md) agree, adopt [modern EditorConfig options](../starter/language-profiles/csharp14.editorconfig) into the existing owned-code section and adopt the [C#14 csc.rsp options](../starter/language-profiles/csharp14.rsp) beside each owned asmdef. Editing generated Unity csproj files or upgrading the host SDK doesn't give Unity C# 14. Keep nullable enabled in both profiles.

Migration: upgrade branch → exact Editor/packages/modules → compile/import and generated code → pure/VM tests → content/player/backend builds → check reload, performance and visuals → ADR/migration notes → merge. Do not retain C#9-only style restrictions after the project has legitimately promoted its modern profile.
