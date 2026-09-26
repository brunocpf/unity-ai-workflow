# Toolchain changes and validation record

Performed for this request on 2026-09-17 (local date):

- Upgraded Unity CLI from `1.0.0-beta.8` to `1.0.0-beta.10`.
- Installed Unity Editor `6000.7.0b1`, arm64, revision `6f112f2bea37`.
- `unity editors verify 6000.7.0b1 --architecture arm64 --format json` returned `ok: true` with editor component status `ok`.
- Removed the installed `6000.7.0a4` editor after verifying the beta installation. The final installed-editor listing contains the beta.
- Beta location: `/Applications/Unity/Hub/Editor/6000.7.0b1/Unity.app`.

Existing projects were not migrated or deleted. Registered projects DrownedMeridian, DaathUI, CrystalMenu, Lanternwell, and UnityClient still referenced the alpha when inspected. Open an isolated copy with the beta and review migration changes before changing their committed editor pin.

Installation verification is not a project compatibility test. No target modules, successful game builds, licenses, or CI runners are implied by this record.

## Current implementation status

This installation record is historical. Source examples and verification have since expanded; see [review](REVIEW.md) and [example verification](examples/Verification/README.md). The kit still requires real Unity/project acceptance before template release.

## B2 observation — 25 September 2026

The user's other session owns the 6000.7.0b2 download/install. This task made no installation changes and did not launch an Editor. CLI beta.10 listed the b2 arm64 bundle and its component-presence check returned ok, but the user reported installation in progress; presence is not completion/integrity verification. Available b2 managed assemblies passed the SDK API probes. See the [b2 upgrade record](references/upgrades/unity-6000.7.0b2.md) before adopting the completed installation. Earlier installation statements above describe 17 September only.
