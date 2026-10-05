# Unity 6000.7.0b3 evaluation update

5 October 2026. Evaluation target: **6000.7.0b3 arm64**. Existing project pins change only through a qualified project migration. CLI versions remain project-owned; this update does not change OpenSpec, architecture or acceptance policy.

## Release delta

Incremental changes since b2 include lower VisualElement memory usage and faster transition hashing; fixes for built-in localization returning empty strings in Play Mode, runtime grid enablement, backdrop-filter previews, SVG gradient inheritance, nested UXML creation, template names and initial nested PanelRenderer reload callbacks. Input fixes address duplicated simulated touches and stuck macOS keys. Sequential command-line builds with activeBuildProfile now compile for the intended platform. PhysicsCore2D gains contact/query improvements. These are release-note claims, not measured kit performance or project acceptance. [Official b3 notes](https://unity.com/releases/editor/beta/6000.7.0b3).

Known issues include a malformed-stylesheet deletion crash, grey Tile Palette rendering without domain reload, and Hash128 precompiled-plugin loading failures; fixes labeled b4 are not in b3. Slow player UnloadUnusedAssets remains listed. Review applicable platform/package risks before adoption. Optional package updates include Physics 2D 1.1.0 and Netcode for GameObjects 3.0.0; do not introduce unrelated dependencies or silently accept major upgrades. [Known issues/package changes](https://unity.com/releases/editor/beta/6000.7.0b3).

## Retained defaults

Keep the current compatibility language profile and nullable/compiler parity; this release does not qualify C#14. Keep bounded catalog-root preload until the chosen build proves scene-ID transport and cold-player loading. Preserve the earlier explicit analyzer configuration pending actual rejection probes. Follow the [b2 archive transition and rollback rules](unity-6000.7.0b2.md#content-and-rollback); preserve accepted old content and rebuild content/player together. Earlier API checks do not establish new Editor/rendered behavior.

## Acceptance after installation

1. Assess the current project/worktree, native Editor/CLI/package pins and installed modules; use an isolated migration branch/checkout. Install b3 beside the old Editor until local verification completes. Removal of the old installation is separate from project migration: an unchanged b2 project still requires b2 or its own reviewed upgrade. Rollback may require reinstalling b2 and restoring its matching content artifacts.
2. Import/compile in b3; regenerate IDE/analysis projects, run owned semantic checks and applicable analyzer/nullable rejection probes. Exercise reload-disabled teardown and package compatibility.
3. Exercise localized UI in Play Mode and the built player, grid layouts, filter rendering/zoom, SVG gradients, nested templates/names, initial nested PanelRenderer reload callbacks, dynamic-height list reordering and sole-child detach. Inspect actual captures against the accepted visual target; release notes are not results.
4. Build content/player with the same qualified toolchain; check cold loading, cancellation/unload and current-run capture provenance. Qualify sequential platform/profile builds and input/device scenarios where used. Retest any content-ID workaround separately before removing it.
5. Review package-lock/settings diffs and run existing Core, Editor, Play Mode and target-player gates. Record actual pass/fail/not-run and remaining user/device verdicts. Update CI Editor/module/cache pins and runner availability with the project migration; do not merely change ProjectVersion.txt.

Local installation and harness evidence is recorded in [b3 verification](../../verification/unity-b3.md). It does not certify the game, rendered UI or shipping targets.
