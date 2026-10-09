# Lean workflow 0.4.0

8 October 2026. This release simplifies project administration while preserving the selected architecture, source-quality enforcement, authoring, localization, visual iteration and OpenSpec lifecycle. The kit remains a workflow with selected tested implementations, not a certified game template.

## Changes

- Three default project documents; optional substantial contracts/ADRs/art briefs instead of required separate status, index, toolchain, dependency, compatibility and handoff documents.
- Six shorter task skills, conditional references and one owner for behavior/status/versions/results. Native locks and code remain authoritative for facts already encoded there.
- Schema-2 verification maps requirement IDs to shared commands/manual checks. Delivery executes current commands, retains full logs and generates results. record-review collects actual manual-review metadata and artifact hashes. No whole-tree acceptance fingerprint or archive resealing; a regression after a previous pass still fails because checks execute again.
- Fresh project installations omit examples by default, with release-pinned links and optional complete offline packs. Existing installations retain their pack unless explicitly changed. Global caches remain complete.
- Active-map migration supports preview, apply, already-adopted detection, preflight validation and atomic replacement. Required manual kinds remain pending; historical archives are refused. Customized project tooling/docs require the full reviewed [migration](../references/upgrades/lean-0.4.0.md), not just installer updates.

## Measured footprint

Compared source payloads from 0.3.6 commit 8da83c9 against 0.4.0, with both Codex and Claude adapters. Counts exclude root managed blocks/manifests and compare each version's default example selection.

| Measure | 0.3.6 | 0.4.0 |
|---|---:|---:|
| Project-managed payload files | 190 | 112 |
| Six task skills, whitespace-delimited words | 1,677 | 1,303 |
| Project document forms, words | 1,280 | 252 |

These measure file/context-writing surface, not actual AI session tokens or model adherence. Required OpenSpec artifact count is unchanged. Automatic logs are retained, not truncated or removed to improve these numbers. Compare equivalent real development tasks before claiming a percentage token/cost saving.

## Validation and self-review

- 67 local Python tests passed: installer rollback/collisions, optional-pack add/remove and legacy inventory, installed-link closure with/without examples, global installs, shared-command execution, current failure after prior success, timeout/missing executable, pending/failed manual review, altered/replaced artifacts, requirement/removal mappings, migration preview/apply/idempotence and invalid-input preservation. Local Python was Homebrew 3.14; CI qualifies the supported Python 3.10 runtime.
- Real OpenSpec 1.13.2 / Node 24.15.0 integration passed: Codex/Claude generated integrations, custom schema/instructions, malformed scenario and pending-review rejection, quiet/verbose delivery, new and modified capability archives, delivery after archive without changing verification, and final strict validation. Fixtures are synthetic, not Unity behavior evidence.
- Kit Markdown/config/skill checks and installed dependency-link checks passed. No C#/Unity implementation changed, so this release does not claim new Unity runtime qualification; the [0.3.6 navigation evidence](ui-navigation-036.md) retains its original scope.
- Self-review fixed stale document routes, optional-pack maintenance links, a test-discovery mistake, nonatomic migration writes and acceptance of artifacts replaced by a test command. Rechecked defaults against retained architecture/quality/UI rules and confirmed old fingerprint rules survive only as labeled historical guidance.

Remaining boundaries: manual verdict freshness/test sufficiency require semantic review; metadata cannot authenticate a claimed human review. The runner trusts reviewed command definitions and their meaningful exit/report checks. CI trust policies and game-specific target tests still apply. Actual token savings and fresh-session model behavior have not been measured.
