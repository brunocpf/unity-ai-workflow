# Project setup checklist

The working list for setup scope. It condenses the setup references so that project setup doesn't start by reading all of them: work down this page and open a linked reference only for the decision named beside it. Don't bulk-read `references/` (no `cat references/*.md`). The first playable slice continues in [adoption](adoption.md#first-playable-slice).

## 1. Check the machine once

Run `python3 <kit>/install.py doctor --target <game>` and follow its `guidance`. If it reports no Unity CLI or Editor and the user hasn't named an Editor path, write the project files directly, skip Editor import/compile/test/build checks, and list the commands still to run in README.md. Don't search the disk for other editors, interpreters or caches.

Ask only for missing product intent (target platforms, languages, unclear scope; see [clarification](clarification.md)). Continue with everything that doesn't depend on the answer.

## 2. Install and scaffold

```sh
python3 <kit>/install.py install --target <game> --agent <client>
python3 <kit>/install.py check --target <game>
python3 <kit>/install.py scaffold --target <game> --profile csharp9
```

`scaffold` places the EditorConfig, Git files, Husky hook, VS Code settings and the tooling/dotnet, tooling/ide and tooling/quality folders. Merge anything it lists under `merge` by hand. Use `--profile csharp14` only when the pinned Editor supports it ([language profiles](language-profiles.md)), then adopt its EditorConfig overlay as `next_steps` says.

## 3. Unity project and pins

- With a Unity CLI, create the project through it ([CLI rules](toolchain.md#cli)). Without one, write ProjectSettings/ProjectVersion.txt with the chosen pin and Packages/manifest.json with real package ids.
- Record the Editor, CLI, render pipeline and .NET SDK in docs/architecture.md. A shipping project needs a production Unity release, not a beta.
- Dependencies for setup: Input System, Unity Test Framework and the localization implementation, plus R3, UniTask and VContainer once code uses them. Open [dependencies](dependencies.md) only to choose beyond that.

## 4. Assemblies

Replace `Game` with the project's logical root namespace. Every owned asmdef uses explicit references and `autoReferenced: false`; the pure three also set `noEngineReferences: true` and `overrideReferences: true` ([architecture](architecture.md) owns the rules).

| Folder under Assets/Game | Assembly | References |
|---|---|---|
| Core | Game.Core | none |
| Application | Game.Application | Core |
| Presentation | Game.Presentation | Application, Core |
| Unity/Runtime | Game.Unity.Runtime | Application, Core |
| Unity/UI | Game.UI | Presentation, Core |
| Unity/Composition | Game.Composition | all runtime assemblies |
| Unity/Editor | Game.Editor (Editor only) | needed runtime assemblies |
| Tests/EditMode, Tests/PlayMode | Game.Tests.EditMode / .PlayMode | the boundaries under test; `UNITY_INCLUDE_TESTS` |

Create only the assemblies setup uses; add the rest with the first feature that needs them. Then rerun `scaffold` (it adds `csc.rsp` beside each new asmdef, using the profile already recorded in tooling/ide/owned-projects.json) and replace the sample names in tooling/ide/owned-projects.json and tooling/quality/coverage.json with the real ones. Include at least one real test, such as an architecture test that Core references no Unity assembly.

## 5. Pure SDK build and hooks

- Pin a .NET 10 SDK in root global.json. Create tooling/dotnet/Game.sln with SDK projects that compile the same Core/Application/Presentation sources plus a test project, and add tooling/quality/CodeOrganization.
- Run `dotnet tool restore`, `dotnet husky install` and `git lfs install --local` when those tools exist; otherwise list them in README.md. Details: [developer tooling](developer-tooling.md), [IDE setup](ide.md) (the regeneration hook goes into Game.Editor).

## 6. Startup scene and documents

- Save one bootstrap scene with the composition root and add it to the build profile. No gameplay systems, polished screens or production assets in setup scope ([authoring](authoring.md) when creating prefabs or definitions).
- Write README.md, docs/project.md and docs/architecture.md from the [document templates](../starter/DOCUMENT-TEMPLATES.md): real commands, platforms, languages, proposed first slice, pins and source map.

## 7. CI

Add one workflow for the chosen provider: quality check, pure build/tests, Edit Mode and Play Mode tests, player build, artifacts. Use `unity ci init --dry-run` as a starting point when the CLI offers it, and pin every action and installer ([CI](ci.md)).

## Done when

The kit check passes, the scaffolded tooling names match the real assemblies, README.md lists working commands (or the exact steps still blocked on a missing tool), and every check that the machine can run has run.
