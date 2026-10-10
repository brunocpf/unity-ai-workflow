---
name: unity-workflow-update
description: Check, assess or update the Unity AI workflow installed in the current project. Compare a candidate kit with the project's version, decide which changes apply, preserve local decisions and separate standards updates from game or Unity/package migrations.
---

The locally cached candidate kit is at `{{KIT_ROOT}}`. Read its `references/workflow-updates.md`. The current game's `.unity-workflow/installation.json`, local standards, native locks, project contracts and ADRs describe the installed baseline; do not assume the global candidate is newer or suitable.

For a request about new upstream changes, inspect `https://github.com/brunocpf/unity-ai-workflow` and fetch a candidate into a separate temporary checkout, pinning its exact commit. Do not mutate the installed cache or pull into the game. The bundled cache works offline; if upstream is unavailable, report that freshness is unknown rather than calling it current.

Run the candidate's `install.py assess --target <absolute-project-path>` using an available Python 3.10+ interpreter. Read the changed policies/examples and affected project implementation; classify each change as applicable now, deferred, not applicable or requiring a separate migration, with reasons and evidence. File hashes alone cannot make that decision. Keep applicability decisions in the existing project record or final response; no separate upgrade report.

Checking/reviewing stops with the assessment. When updating is requested, apply the compatible standards update using a dry run first, preserve project exceptions, and validate affected boundaries. If the candidate imposes incompatible policies, defer that version or make the required project ADR/migration explicit before applying it. Never claim a partial mix is an unmodified upstream version. Engine/package/save migrations require their own authorized scope and tests.

For a global-only update, no game manifest is needed: review the candidate, run its `install.py install-global` and `check-global`, and report the installed version. The updater may install a reviewed new global candidate when explicitly requested, but global updates never update existing projects automatically. Do not require the user to restate architecture or already resolved choices. If no project installation manifest exists, inspect the manual adoption and reconcile ownership instead of guessing a baseline or overwriting it.
