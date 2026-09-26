# Persistence, failures and external boundaries

## State and persistence

Application owns save/load use cases; a repository port describes domain-relevant operations. Versioned DTOs are separate from domain entities, ViewModels, reactive objects and Unity serialization. Use the selected JSON adapter from [dependencies](dependencies-optional.md); no all-purpose repository framework.

Serialize writes per save slot/profile. Snapshot coherently before encoding; distinguish accepted gameplay state from durable persisted state. Define when UI may report "saved" and what happens if persistence fails. Local file adapters write a temporary file, flush as supported, and replace atomically where the platform supports it, retaining the last accepted backup. Other targets need a documented equivalent. Never assume desktop filesystem behavior on Web/console/mobile.

A save envelope identifies schema version, revision and compatible content IDs; add integrity checks where useful, without claiming an unsigned checksum prevents tampering. Validate sizes/ranges/IDs before accepting data. Migrate through tested explicit versions. Keep representative historical fixtures and test forward migration, corrupt/truncated data, interrupted writes, full storage and unsupported future versions. Preserve recoverable user data; do not silently overwrite an unknown/corrupt save with defaults.

Remote/cloud saves add conflict policy and idempotency/version tokens. Multiple devices require a product decision about merging or choosing a revision. Async cancellation does not roll back committed remote writes.

## Command and failure policy

Expected denials use feature-specific typed outcomes (for example insufficient funds, inventory full, conflict). Cancellation follows the async contract; programming faults and broken infrastructure surface as exceptions at the owning boundary. Do not catch everything and return success/default state. Avoid a universal Result wrapper that obscures useful domain outcomes.

Commands state their concurrency policy: serialize, reject while pending, idempotent duplicate, or latest-result-wins for replaceable reads. Busy/validation state in a ViewModel improves UX; Application must still enforce authority. Retry only failures known to be transient, with bounded attempts, timeout/backoff and an idempotency strategy for side effects. Surface exhausted retries and allow designed recovery. Timeouts do not prove the original operation stopped.

## Diagnostics and trust

Use structured events with feature/scenario/operation IDs and correlation, severity, and an observable failure outcome. Adapt logs/profiler/error reporting at the Unity boundary; keep pure ports small. Measure startup, save latency, content residency, frame/allocation budgets and active resource counts. Logging every frame or retaining unbounded histories is not observability.

Validate external input, network messages, save data, downloaded content and generated assets at their trust boundary. Clients do not own server-authoritative currency/entitlements. Credentials and signing keys stay outside source and generated prompts. Log useful diagnostics without personal data/tokens; retention and consent follow the chosen product/platform requirements. Add network/storage/provider contract tests with failure injection instead of relying solely on mocks.

For content/live services record version compatibility, rollout, rollback, offline/degraded behavior and support diagnostics. These are required when the feature exists, not a requirement to add a backend to every game.
