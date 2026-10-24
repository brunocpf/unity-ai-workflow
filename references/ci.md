# CI

CI needs a real project, a build profile and a runner with a Unity license. This page describes the pipeline shape; it is not drop-in YAML.

When the project's CLI exposes `ci init`, use it as a starting point: `unity ci init --project-path . --provider github --target StandaloneOSX --dry-run` (substitute your target). Review the generated workflow, pin its dependencies (it may use a floating CLI installer) and add the stages below.

## Stages

1. Check out the revision and fetch LFS content.
2. Install the pinned CLI/Editor and activate the license.
3. Run the pure C# build and tests from the hand-maintained SDK solution, plus the [quality check](code-organization.md).
4. Run the Edit Mode and Play Mode tests.
5. Build the content the selected profile needs (Content Directories for the 6.7 UI profile, localization data, fonts).
6. Build the player.
7. Upload test results, logs and the player build.

Example commands from the project root:

```sh
python3 tooling/quality/check.py
unity test . --mode EditMode --output artifacts/editmode.xml --timeout 900
unity test . --mode PlayMode --output artifacts/playmode.xml --timeout 900
unity build . --profile "Assets/Game/Settings/Build Profiles/Desktop.asset" --output-path artifacts/player --timeout 1800
```

Fail the job when a test command fails or produces no results file. Set `UNITY_NON_INTERACTIVE=1` and `HUSKY=0` in the job environment. Use the profile's platform-appropriate output path (directory, .app or executable).

Run the fast pure checks on every PR. Editor tests and player builds can run on every PR or only on main, depending on how long they take. Use separate jobs/workspaces for parallel Unity runs. Tests that render need a graphics-capable runner, not no-graphics batch mode. Don't run untrusted pull-request code on a privileged persistent runner.

## Library cache

Caching Unity's `Library` folder saves most of the import time on GitHub-hosted runners. Cache it separately from Editor downloads, and restore it after checkout and before the first Unity operation.

```text
key = library-{OS}-{Editor version}-{build target}-{hash of Packages/packages-lock.json and ProjectSettings}-{revision}
restore-keys = library-{OS}-{Editor version}-{build target}-{same hash}-
```

Don't share caches across Editor versions, platforms or package changes. Save the cache only after a successful run, from the default branch. Restore only `Library`, never Assets, settings, credentials or license files. If a cached run behaves strangely, rerun without the cache. [GitHub dependency caching](https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching).

## Releases

Pin action revisions, runner images, CLI/SDK versions and packages. Tag releases and keep the player builds, symbols and configuration needed to diagnose or roll back a release. Keep signing and secrets in trusted jobs only. Hooks give early feedback; CI is the check that counts. See [developer tooling](developer-tooling.md) and [toolchain](toolchain.md#cli).
