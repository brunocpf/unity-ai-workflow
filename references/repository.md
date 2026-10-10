# Repository and Git

Git root = Unity project root. CLI examples run there; outputs go to ignored `artifacts/`. Create only used feature folders.

```text
Game/                                # Git + Unity project root
  AGENTS.md                          # Short mandatory rules and routing
  README.md                          # Setup, supported targets, real commands
  .editorconfig
  .gitattributes
  .gitignore
  .vscode/                           # Tracked settings, recommendations and regeneration task
  .agents/skills/                     # Project-owned task workflows
  global.json                        # Pinned dotnet CLI SDK; not Unity language configuration
  .config/dotnet-tools.json           # Pinned local Husky.NET and tooling
  .husky/                            # Verify-only hooks; LFS integration preserved
  .github/workflows/                  # Or chosen provider, not several unused ones
  docs/
    project.md                       # Product/platform/locale/visual decisions and budgets
    architecture.md                  # Source/ownership map, authoring locations, exceptions
    standards/
      references/                    # Task-specific policy; do not preload the directory
      starter/                       # Configuration/tooling sources, not extra project docs
      examples/                      # Optional offline reference pack (--examples all)
    evidence/                        # Retained manual evidence when not stored in CI
    # Split ADRs, module contracts or art/asset briefs only when independently maintained.
  tooling/
    bootstrap/                       # Idempotent local setup/provision checks
    ci/                              # Same validation/build entrypoints as local
    hooks/                           # Staged verification, no implicit rewriting
    ide/                             # Owned assembly/namespace/compiler profile
    quality/                         # Coverage gate + syntax-aware organization checker
    dotnet/
      Game.Core/                     # Hand-authored SDK harness, shared sources
      Game.Application/              # Hand-authored SDK harness
      Game.Presentation/             # Pure ViewModels; shared Unity sources
      Game.Tests/                    # Fast pure/reactive tests
    blender/                         # Versioned export and validation operations
    analyzers/                       # Acquisition/config tools, not random DLL copies
  SourceAssets/                      # Outside Unity import tree
    Localization/                    # Glossary/translator exchange with one import authority
    UI/<screen-or-family>/           # Reference/concept images and editable visual targets
    Characters/<asset-id>/
    Props/<asset-id>/
    Textures/<asset-id>/
    PixelArt/<asset-id>/
    MotionReferences/<asset-id>/
  asset-registry/                    # Machine-readable IDs, hashes, lineage
  Assets/
    Game/
      Core/
        Game.Core.asmdef
        csc.rsp                      # Also beside every other owned asmdef
        Inventory/
        Combat/
        Quests/
      Application/
        Game.Application.asmdef
        Inventory/
        Combat/
        Persistence/
      Presentation/                  # Pure MVVM; no Unity references
        Game.Presentation.asmdef
        Inventory/
      Unity/
        Runtime/                     # Engine adapters; feature folders inside
          Game.Unity.Runtime.asmdef
          Combat/Authoring/          # Definition/placement adapter C# types, not Core
        UI/
          Game.UI.asmdef
          Theme/
          Elements/<Control>/        # Control.cs + private .uxml/.uss + owned assets
          Screens/<Screen>/          # Screen visuals/styles + mechanical binding
          Behaviors/
          Localization/              # Engine text adapter implements pure Presentation ports
          Content/
        Composition/
          Game.Composition.asmdef
        Editor/
          Game.Editor.asmdef          # Editor-only
      Content/
        Characters/<asset-id>/       # Authored prefab/variants + accepted visual assets
        Combat/Definitions/          # Enemy/weapon/wave/upgrade .asset instances
        Props/<asset-id>/
        UI/
        Localization/<module>/       # Authored resource tables and localized assets
        Audio/
        VFX/
      Generated/<feature>/           # Only explicitly replaceable generator-owned outputs
      Settings/                      # Input, render, build profiles, catalogs
        Localization/                # Native settings own locales in 6.7
      Scenes/                        # Bootstrap, gameplay, galleries/smoke scenes
      Tests/
        EditMode/                    # Explicit test asmdef
        PlayMode/                    # Explicit test asmdef
    ThirdParty/                      # Only dependencies that require asset import
  Packages/
    manifest.json
    packages-lock.json
    com.studio.shared/               # Optional embedded package while developing
  ProjectSettings/
  artifacts/                         # Ignored local reports/builds/captures
```

[Authoring](authoring.md) defines authored versus replaceable asset ownership; an AI-created asset is not automatically safe to overwrite. Keep source grouped by feature inside layers. UI templates/USS share one folder with their owning control or screen (see [control directory contract](ui-construction.md#control-directory-contract)); accepted generated media goes in Content. Shared helpers use feature folders from [utilities](utilities.md), not a generic Utils directory or mandatory new assembly.

## Version control rules

- Commit Assets and required .meta files, settings, package manifest/lock, build profiles and hand-maintained tooling csproj files. Preserve GUIDs when moving or replacing referenced content.
- Use Force Text where supported and visible metadata. Do not blanket-ignore DLLs, csproj files or StreamingAssets. Starter [.gitignore](../starter/.gitignore) is root-layout-specific.
- Put binary sources/media in LFS or immutable artifact storage; starter [.gitattributes](../starter/.gitattributes) defines typical extensions. Fetch actual LFS content before import and fail preflight on unresolved pointer files. Add scoped exceptions for binary .asset files, not a global rule.
- Short feature branches, protected main, checks appropriate to the changed boundary. Keep code/content/metadata that implement one feature together.
- Concurrent Unity work uses separate worktrees, Editor sessions and Library directories. One writer per live scene/prefab/binary source. Never share mutable Library caches.
- Configure and test UnityYAMLMerge before adding a merge driver; import/test merged assets even after conflict-free merges. Reconcile package manifest/lock via Package Manager. Binary conflicts require selecting/reauthoring a candidate.
- Retain release/PR evidence externally; approved visual baselines can be committed in runtime test fixtures or tooling fixtures with LFS. Do not rely on an ignored local screenshot path.
- Keep secrets/signing out of PR jobs and untrusted work off privileged persistent runners.

A template tag identifies a tested toolchain and slice. New games instantiate it; active games receive reviewed upgrade changes. Extract shared UPM packages after demonstrated reuse, with runtime/editor/test boundaries. Each game release records commit, template baseline, versions, asset/catalog hashes and build profile.

Sources: [Unity version control](https://docs.unity3d.com/Manual/Versioncontrolintegration.html), [Git LFS](https://git-lfs.com/), [worktrees](https://git-scm.com/docs/git-worktree).

Local setup and hook policy: [developer tooling](developer-tooling.md). Shared ownership/version/release policy: [engineering baseline](engineering-baseline.md).
