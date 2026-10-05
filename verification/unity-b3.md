# Unity beta 3 qualification — kit 0.3.4

5 October 2026. Editor **6000.7.0b3 arm64**, revision **ad717268ad45**, macOS 26.5.1. CLI **1.0.0-beta.11** is the local installation tool, not a universal kit pin. [Migration and known issues](../references/upgrades/unity-6000.7.0b3.md).

## Local installation

Installation completed successfully for the Editor and all 14 module entries. `unity editors verify` reports every component present. Matched the previous installation: Android support with OpenJDK 17.0.18+8, NDK r27c, CMake 3.22.1, SDK build tools 36.0.0, platform tools 37.0.1, SDK platforms 34/36/37 and command-line tools 16.0; iOS; Mac IL2CPP; Windows Mono. This structural check does not independently verify signatures or target builds.

After confirming no Editors were running, beta 2 was uninstalled successfully. Its installation directory is absent; final CLI inventory contains only 6000.7.0b3 arm64. No default Editor alias had been configured, so none was changed. Existing game version pins were not edited; opening a b2-pinned game now requires its reviewed migration or reinstalling b2.

The executable reports 6000.7.0b3. A new disposable project created with `-batchmode -nographics -quit -createProject` completed import and exited 0; its ProjectVersion.txt records the expected revision. Startup logged an unavailable access token before successfully obtaining the local license; this did not prevent the smoke run. This is a headless empty-project check, not rendered or game-specific acceptance.

## Kit probes

| Check | Result | Limit |
|---|---|---|
| Core/Application/Presentation/Runtime/UI/Composition/Editor API harness | Pass, zero warnings/errors | C#9/netstandard2.1 against installed b3 assemblies; SDK analyzers disabled by this compatibility harness |
| Pure lifetime/request checks | 15 pass | .NET execution, not player timing |
| ViewModel/boundary checks | 18 pass | Pure projection/commands/disposal and assembly boundaries |
| IDE XML transform | 28 assertions pass | Does not verify IDE completion or Editor callback execution |
| Installer/spec/output tests | 55 pass | Kit behavior, not game acceptance |
| OpenSpec 1.13.2 on Node 24.15.0 | Pass | Both client integrations, schema, scenarios, evidence rejection, quiet/verbose checks and two archive cycles; synthetic evidence |
| Repository links/configuration/diff | Pass | Packaging consistency |

SDK 10.0.301 ran the harnesses from a scratch examples directory with existing dependency locks. The first ViewModel invocation through an absolute `/tmp` path produced an incomplete NuGet reference graph; forcing locked restore from the physical scratch working directory resolved it without source or lock changes. The first OpenSpec attempt correctly rejected the shell's Node 17; rerunning with its pinned Node 24.15.0 passed. Neither was an Editor regression.

## Remaining project acceptance

No existing game was opened or migrated. Builder, source-generated UXML registration/property bags, graphics, localized Resource Tables, optional LitMotion integration, reload-disabled sessions, analyzer fault rejection in Unity, content archives/cold-player loading and platform player builds were not executed. WaveLabel and drawing APIs compile; no new rendered or performance result is claimed. The separate native localization probe remains historical b2 evidence. Module presence is not target-build qualification. Follow the migration checklist before changing a project's Editor/CI pins.
