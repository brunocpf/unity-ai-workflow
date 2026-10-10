# CI starting recipe

Requires a real project/build profile, provisioned runner/license and implemented validation/content steps. This is not drop-in CI YAML.

When the project's selected CLI exposes `ci init`, use its generator as a starting point. From a real project, preview with `unity ci init --project-path . --provider github --target StandaloneOSX --dry-run` (substitute your target). Review the generated workflow and pin its dependencies; add the project-specific stages below. The research workspace is not a Unity project. A read-only preview was inspected against an existing registered project; no workflow was written into that project and no CI run was performed.

For GitHub Actions or equivalent, use these sequential stages:

1. Checkout the exact revision and fetch LFS content.
2. Verify pinned tools and licensing; allocate a fresh run ID/output directory and retain the expected build/scenario request. Follow [scenario evidence](test-scenarios.md); never reuse old reports/captures as current results.
3. Run the hand-maintained pure C# build/test project with its locked SDK/packages, plus compiled architecture/module checks, nullable/analyzer enforcement and the shared full-coverage quality gate (code-organization.md). Regenerate Unity IDE/analysis projects before their semantic formatting checks; the pure test solution stays separate. Require compile-item coverage and nonzero style/analyzer execution for every relevant owned project, and run the disposable semantic rejection probes. Ensure the test count is nonzero. A pure/whitespace-only fast job is useful feedback but cannot satisfy this stage.
4. Run the Edit Mode and Play Mode test commands below against an isolated checkout, including authored-reference/definition validation, nonempty localization coverage/table/format validation from [localization](localization.md#acceptance-and-ci), and applicable generation-preservation checks. Editor usability also requires the authoring workflow evidence in validation.md.
5. Build and stage output for the selected content provider through the project's implemented Editor build operation. Content Directories are required for the 6.7 UI profile; a direct-reference UI profile has no separate UI content build. Independently build/include the selected localization provider data, required locale/font/asset content and translation status checks; template loading is not localization inclusion proof.
6. Run the player build command below after staging content, then launch a smoke test on the intended platform, exercising cold localization loading and the applicable locale visual matrix.
7. Validate current-run completion, required reports and [capture manifests](test-scenarios.md) against the runner request, then upload logs, test results, captures and provenance. Upload failure diagnostics too; stale, incomplete or mismatched evidence fails the job.

Example POSIX-shell command payload, from the Git/Unity project root. The runner sets WORKFLOW_RUN_OUTPUT to the fresh directory from stage 2. The player build below must run after the content build/staging step; these lines are not the complete pipeline:

```sh
: "${WORKFLOW_RUN_OUTPUT:?Runner must supply its fresh per-run output directory}"
python3 tooling/quality/check.py --artifacts "$WORKFLOW_RUN_OUTPUT/quality"
python3 tooling/quality/test_semantic.py --artifacts "$WORKFLOW_RUN_OUTPUT/semantic-probes"
unity test . --mode EditMode --output "$WORKFLOW_RUN_OUTPUT/editmode.xml" --timeout 900
unity test . --mode PlayMode --output "$WORKFLOW_RUN_OUTPUT/playmode.xml" --timeout 900
unity build . --profile "Assets/Game/Settings/Build Profiles/Desktop.asset" --output-path "$WORKFLOW_RUN_OUTPUT/player" --timeout 1800
```

For live-Editor compile feedback and detached operations, follow the [CLI completion contract](toolchain.md#cli). A successful `recompile` is not this pipeline; a job-dispatch result is not test/build completion.

Configure the job environment with UNITY_NON_INTERACTIVE=1 and HUSKY=0; run CI checks directly. Verify the flags on the pinned CLI. Use the chosen profile's platform-appropriate output path (directory, .app, or executable), rather than assuming one works everywhere.

Use separate jobs/workspaces for parallel Unity executions. Rendering tests need a usable graphics backend. Use the Library cache and timing guidance below. Avoid running code from untrusted pull requests on a privileged persistent runner.

Before calling this CI complete, intentionally break a Core rule, a Unity compile, a known analyzer diagnostic, a behavior test, and a required content reference in disposable changes. Each should produce the expected failure and retained evidence. Then prove a clean checkout passes and launches the player.

## GitHub-hosted runner performance

Keep GitHub-hosted runners as the baseline; do not introduce self-hosted infrastructure, custom runner images or paid runner changes as an incidental optimization. Treat under five minutes as a warm-run goal to measure, not a timeout or guaranteed result. Cold imports/tool upgrades can take longer. Optimize setup/import costs before reducing test coverage.

### Library cache

Cache the project's Library separately from Editor/tool downloads. Restore after checkout/LFS and before the first project-opening Unity operation, including IDE generation. Preserve one workspace per concurrent Editor and keep cross-OS archives disabled.

Use a compatibility prefix and revision suffix, for example:

```text
compat = library-v1-{runner OS}-{runner architecture}-{runner image family}-{Editor version+revision}-{actual build target}-{configuration hash}
key = {compat}-{checked-out revision}
restore-keys = {compat}-
```

The configuration hash covers Packages/manifest.json, Packages/packages-lock.json, ProjectSettings and any external configuration that changes imports, compiler defines, render pipeline or target behavior. Include contents of local/embedded package sources when not covered by those inputs. Require expected key inputs to exist. Use the actual checked-out revision, including a PR merge revision when that is what runs. Never broaden restore prefixes across Editor, platform or configuration boundaries merely to get a hit. Bump the cache epoch (`library-v1`) when cache layout/compatibility assumptions change.

Use SHA-pinned cache restore/save actions. An exact hit, compatible-prefix restore and miss are distinct observations; `cache-hit != true` does not necessarily mean an empty cache. Cache entries are immutable, so the revision suffix permits refreshed snapshots. Save only after successful import/checks and after Unity exits; seed caches from trusted default-branch runs, respecting GitHub's branch/trust restrictions. PRs may restore compatible base caches. Do not elevate token permissions or switch to privileged PR triggers to populate them. Retain failure logs independently of whether the cache is saved.

Restore only Library, not Assets, settings, generated IDE projects, test reports, screenshots, license files or credentials. Always refresh/import, regenerate current analysis projects and execute checks on the current checkout—even for exact hits. Do not accept cached binaries as proof that changed source compiled. Cache misses are normal cold runs. Keep a scheduled/manual clean-import path that bypasses Library restoration and uses a fresh Library; never delete an active Editor's files. Keep its expected reports and checks equivalent.

Library can be large: measure restore **and save/compression** time, archive size and free disk alongside saved import time. Avoid adding cache transfer that costs more than it saves. Monitor eviction/churn; skip saving identical exact hits. Preserve the existing Editor cache rather than merging it into a per-revision Library archive. [GitHub cache matching, immutability and scope](https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching).

### Per-phase timing

Expose existing operations as named job steps, or instrument the existing wrapper with a monotonic clock around each subprocess. Record elapsed duration and outcome in a concise job summary; keep raw logs in the existing artifacts. Record failure/timeout durations too, while propagating the original exit status. Do not add a separate timing service or required project document.

Measure checkout/LFS, disk preparation, OS dependencies, Editor/tool cache restore, Library restore, provisioning/activation, first Editor import/compilation/IDE generation, pure checks, EditMode, PlayMode, semantic/formatting/organization checks, applicable content/player build, Library save and artifact upload. Use Editor logs to explain the first-launch total, and test XML to distinguish actual test duration from Editor startup. Label nested measurements; do not sum them twice. Report job wall time separately from queue time and parallel-job totals.

Compare a cold run, an exact hit and compatible restoration after a real source/asset edit. Inspect several warm runs rather than quoting the best one. Verify edited behavior is actually tested, missing/stale reports still fail, and clean imports remain runnable. Preserve full owned-code semantic coverage and required EditMode/PlayMode suites; give duplicated pure checks one execution owner without dropping Unity-dependent tests. Report the measured improvement and remaining bottleneck honestly; retain normal safe timeouts even when the performance goal is five minutes.

## Generator review

The beta.10 preview selected Ubuntu for StandaloneOSX, kept the source project's alpha pin, used a floating CLI installer and weak report handling. Correct target runner/modules, exact versions, explicit test modes, LFS and missing-report failures. Beta.12 removes the beta-channel variable from generated installers but still does not pin the CLI; retain exact acquisition/version verification. Follow [machine-result and interruption handling](toolchain.md#cli) when updating wrappers. No generated workflow was executed during research.

Build rendering tests on a graphics-capable runner, not no-graphics batch mode. License authentication is distinct from CLI/service-account authentication. Follow [validation](validation.md) for player/visual evidence and [toolchain](toolchain.md) for version policy.

## Independent engineering gates

Run independent [engineering checks](engineering-checks.md) through actual project commands. Fail on test/compile/analyzer errors, missing expected reports and timeouts. Preserve manual visual/device review where applicable; no planning artifact is a prerequisite for executing checks.

## Delivery governance

Pin action revisions, runner images/tool versions where supported and the CLI/SDK/package inputs. Use immutable release manifests and retain player/content artifacts with matching hashes; generate a dependency/license inventory. Release jobs cover the supported target matrix, migration fixtures and representative budgets. Local setup never weakens CI checks. Hooks use the shared selected-file semantic/style entrypoint; see [developer tooling](developer-tooling.md). Use [engineering baseline](engineering-baseline.md) for protected branches, compatibility and rollback requirements.
