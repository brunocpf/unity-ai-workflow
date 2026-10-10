# Shared-cache release verification — 0.6.0

2026-10-10, macOS arm64. Distribution-only change; no Unity runtime behavior changed and no consuming game was modified.

- 64 installer/verification tests passed locally, including 17 shared-cache cases: reuse, independent pins, fresh-machine restore, exact-commit archive/hash validation, offline rejection, corruption/ownership collisions, mode conversion, Git-index cleanup and transactional rollback.
- Kit link/JSON/XML/skill checks and all eight skill frontmatter validations passed. Whitespace diff check passed.
- Live Codex 0.162.0-alpha.17.2 app-server `skills/list` discovered all six linked project skills in a disposable shared project.
- Live Claude Code 2.1.284 stream-json initialization discovered all six linked project commands in the same disposable project, with hooks/MCP disabled.
- Probes performed discovery only: no model turn, runtime instruction-import behavior or Unity acceptance was tested. Initial Codex probe had no configuration directory; creating its isolated CODEX_HOME resolved that probe setup failure.

Self-review covered pin provenance, cache reuse with global installs, unmanaged-content preservation, link ownership, rollback after reverting pins, Git tracking and fresh-clone recovery. Filesystem checks are not a claim about game behavior. Windows requires directory-symlink permission; tests explicitly skip where unavailable and vendoring remains the documented alternative. Hosted matrix results are recorded on the release commit's GitHub Actions run.

Migration and limits: [shared-cache adoption](../references/upgrades/shared-cache-0.6.0.md), [installation](../INSTALL.md). Cache garbage collection is intentionally manual because other projects/worktrees may still use old snapshots. Download tests use exact-commit archive fixtures. A fresh project successfully fetched and restored published commit f58feb0 from GitHub into an empty second cache. The initial hosted Linux run exposed a fixture cleanup race with background Git maintenance; disposable source repositories now disable automatic maintenance. No installer assertion failed in that run.

Windows CI also exposed extended-path prefixes in readlink results and an ANSI-default test fixture. Link comparison now normalizes Windows prefixes/case with explicit drive/UNC regression coverage; the fixture appends bytes without assuming system encoding.
