# Content Directory bootstrap

Use with [control construction](ui-construction.md). Current evaluation target: 6000.7.0b2. The earlier 6000.7.0b1 Pocket Arena trial found that a valid Editor LoadableObjectId reference did not survive ordinary player-scene serialization. This has not been retested in a b2 player. Retain the bounded root-loader default and avoid normal-scene ID fields until the selected build proves ID round-trip and cold-player loading. A successful API compile or Editor lookup is insufficient. See [b2 acceptance](upgrades/unity-6000.7.0b2.md#acceptance-after-installation).

## Default: bounded catalog-root preload

1. Build explicit UiTemplateCatalog roots with BuildPipeline.BuildContentDirectory for the player target. Include every nested/dynamic control template. Verify the build report and dependency closure.
2. Build and stage content for the exact Editor/player target; b2 changes archive compatibility, so follow [content and rollback](upgrades/unity-6000.7.0b2.md#content-and-rollback). Stage the built directory at a platform-supported local path. Resolve that path in the platform/composition layer; the loader accepts a path, not an internal hashed filename. StreamingAssets was tested on macOS; packaged/mobile/web storage needs its own integration.
3. Before constructing controls, call [ContentDirectoryUiLoader.LoadRoots](../examples/Unity/UI/ContentDirectoryUiLoader.cs). It registers that directory and calls the public GetRootAssets<UiTemplateCatalog>(directory) API, scoped to that directory rather than all registered content.
4. The returned UiLibrary owns the registration lease. Do not independently unregister that directory or unload its catalogs/templates with Resources.UnloadAsset/Destroy. Reuse the library across its dependent screens. If other systems need the same directory, give registration one shared owner with explicit consumer leases; do not register/unregister it independently per screen.
5. On shutdown, remove/dispose all consumers, detached trees, bindings and pools before disposing the library. Library disposal clears its template references, then unregisters the directory. Startup failure/cancellation follows the same release path; cleanup errors are surfaced.

This path is **synchronous native loading at an explicit startup boundary**. A preceding UniTask yield can show a loading shell but does not make GetRootAssets asynchronous or cancellable mid-call. Keep catalogs bounded, measure the blocking duration on the target, and check cancellation before/after. Do not call it in a control constructor, hot interaction, worker thread or frame update. Large/streamed content needs a separately validated asynchronous provider behind the same library contract.

Composition stores the returned library and owns each mounted screen. If mounting fails, unwind any screens already created before releasing the library. Attempt all cleanup steps and report aggregated failures; the library's own constructor failure already releases its transferred lease. Follow the [session shutdown contract](lifecycle.md).

The source default deliberately encapsulates registration ownership more tightly than Pocket Arena's host-owned registration. It has API compilation evidence; repeat the runtime lifecycle tests when adopting this adaptation.

## Advanced ID-based loading

LoadAsync(catalogIds, cancellation) remains available only when the project proves a supported build/runtime ID transport for its selected target. It borrows a caller-owned registered directory and owns its Loadable handles; release those handles before the caller unregisters the directory. This alternative must not be mixed with the root loader's owned registration. The standalone example returns Task to compile without a UniTask package dependency; adapt the outer orchestration to the project’s UniTask default without changing main-thread, drain-before-release or ownership semantics. Do not guess IDs from filenames or assume an Editor-only API exists in players.

## Required evidence

Cold player from a clean content build; missing directory/root; duplicate/missing template; cancellation before and after preload; failed construction; two consumers sharing one library; repeated mount/unmount; directory release after the last consumer; reload-disabled Play cycles. Include actual content logs and target/backend identity. The Pocket Arena trial establishes one macOS/Metal/Mono root-loading path, not all delivery platforms or asynchronous streaming.
