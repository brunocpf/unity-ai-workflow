# Unity 6000.7.0b2 evaluation update

Updated 25 September 2026. Current kit evaluation target: **6000.7.0b2 arm64**, CLI **1.0.0-beta.10**. This updates the standards/examples target; it does not migrate existing games or certify a shipping template. [Toolchain](../toolchain.md) owns general version policy.

## Release delta

Read the incremental b2 section, not the cumulative 6.7 feature list. Relevant changes: UI template creation/unpacking fixes preserve names and nested overrides and avoid a circular-reference overwrite; resolved overflow and ExposedReference assignment are corrected. Dynamic font atlases no longer enter builds merely because Builder is open. Other changes include SerializeReference fixes, an Awaitable/Task.Delay cancellation fix, URP 2D depth/stencil behavior, and Android AGP 9.1.1. Optional Authentication moves to 3.8.0; do not install it without a game requirement. [Official b2 notes](https://unity.com/releases/editor/beta/6000.7.0b2).

Known b2 issues still include sole-child unparenting assertions, slow player UnloadUnusedAssets and duplicate simulated touch events. Entries labeled fixed in b3 are not b2 fixes. Qualify applicable cases; do not suppress assertions globally. [Known issues](https://unity.com/releases/editor/beta/6000.7.0b2).

## Content and rollback

B2 writes LZ4 archives using format version 9. Older archives remain readable, but older Editors cannot read these new archives. [Archive change](https://unity.com/releases/editor/beta/6000.7.0b2).

Build player and content with the same qualified toolchain. Keep pre-upgrade content for rollback; rebuild with the older toolchain if reverting. Never overwrite the only accepted older artifacts. Key content caches by Editor, target and content configuration, retain build/content hashes, and run cold-load/unload checks after rebuilding. This applies to artifact production/compatibility; it is not evidence that scene serialization of LoadableObjectId was fixed.

## Defaults retained

- **C#9/netstandard2.1 compatibility + nullable** remains the current profile. The 6.7 compiler reference still specifies C#9; bundled .NET10 tooling and experimental CoreCLR do not qualify C#14. Follow [language profiles](../language-profiles.md). [Compiler reference](https://docs.unity3d.com/6000.7/Documentation/Manual/csharp-compiler.html).
- **Bounded catalog-root preload** remains the Content Directory default. The earlier b1 scene-ID transport failure has not been rerun in a b2 player. Keep the workaround until an explicit round-trip/player probe succeeds; do not describe it as a newly confirmed b2 defect. [Loading contract](../ui-content-loading.md).
- **PanelRenderer, constructor-complete controls, R3/MVVM, native localization and modern UI capability gates** remain. B2 API availability does not replace Builder, rendered or lifetime acceptance.
- **Explicit analyzer configuration** remains. The b1 `-analyzerconfig:.editorconfig` finding is carried forward pending b2 compiler/IDE rejection probes; no analyzer behavior was inferred from the API build.

## Evidence recorded for this update

The user's other session owns the b2 download/install. Local CLI inventory and component-presence verification reported b2, and the app metadata identified b2, but those are not installation-completion or integrity guarantees. This task did not install, uninstall or launch an Editor, migrate a project, or interrupt the download.

The available b2 managed assemblies were used for SDK API checks. Treat these as evidence for those available files; rerun against the completed installation before promoting a project baseline. Portable results are in [b2 checks](../../examples/Verification/b2-checks.json).

| Check | Result | Limit |
|---|---|---|
| Core/Application/Presentation/Runtime/UI/Composition/Editor API harness | Pass; zero compiler warnings/errors | C#9 SDK compilation against available b2 DLLs; not Unity import/source generators |
| Pure lifetime/request checks | 15 pass | .NET harness, not player timing |
| ViewModel and assembly-boundary checks | 18 pass | Pure execution, not UI rendering |
| IDE project XML checks | 28 assertions pass | Transform behavior, not IDE completion or callback execution |
| Native localization probe | Pass; zero warnings/errors | LocalizedString/SetBinding and settings signatures; no table/locale/player validation |

Historical b1/Pocket Arena results remain dated and labeled b1. Optional LitMotion package integration was not rerun for b2. No new performance numbers, full semantic-project coverage or rendered acceptance are claimed here.

## Acceptance after installation

In an isolated adoption project, verify the completed Editor/modules/packages and generated IDE projects. Then:

1. Import/compile with the actual Editor, run nullable/analyzer fault rejection, and check generated custom-control registration. Exercise reload-disabled sessions and cleanup.
2. In Builder/UI Stage, create and unpack nested templates, inspect preserved names/overrides and confirm source assets remain intact. Check live USS overflow, multiple exposed references and the sole-child detach case without suppressing failures.
3. Build fresh content and the target player together. Verify catalog roots, dependent templates, cold startup, cancellation, unload and fresh run captures. Retest scene-ID transport separately before adopting ID-based loading.
4. Exercise localized text/font loading and text effects. Compare a build with Builder open against the intended font/content inclusion, then inspect the player and record budgets.
5. Run applicable platform/package cases: touch simulation and real-device input, 2D depth/stencil, managed-reference authoring, or asynchronous cancellation. Preserve the existing architecture/authoring/visual gates.

Record pass/fail/not-run per capability and target. Promote a project pin only with its required evidence; selecting this kit's evaluation target is not equivalent to passing those gates.
