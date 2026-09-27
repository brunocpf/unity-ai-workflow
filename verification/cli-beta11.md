# Unity CLI beta.11 command check

26 September 2026, macOS arm64. This is command-surface evidence, not a required project pin or full Unity integration qualification.

- Updated the local CLI from 1.0.0-beta.10 using `unity self-update --target 1.0.0-beta.11 --yes --non-interactive`; subsequent `unity --version` returned 1.0.0-beta.11.
- Read `recompile --help`, `docs --help` and `job wait --help`. Confirmed project targeting, bounded timeouts, JSON formatting, optional strict compilation, and explicit documentation version/URL options.
- `unity docs UIElements.VisualElement --editor-version 6000.7.0b2 --url` produced the versioned UIElements.VisualElement scripting-reference URL. The unqualified VisualElement topic produced an unqualified URL instead: inspect the returned page rather than assuming resolution verifies an API.
- Recompile exit semantics and corrected dispatch/status reporting are documented in the [official beta.11 release notes](https://docs.unity.com/en-us/unity-cli/release-notes). No game project, Editor, Pipeline package or project/CI version pin was changed by this check.

Pending project qualification: actual successful/failed compilation, unreachable-Editor handling, and a detached operation's terminal success/failure through its exposed status API. Exercise these when upgrading that project's tooling; this record does not claim them. Historical beta.10 generator findings remain historical and were not rerun here.
