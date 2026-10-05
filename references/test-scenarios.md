# Scenario clocks and fresh capture evidence

Use for accelerated gameplay, replay, smoke runs and visual acceptance. [Validation](validation.md) owns the broader test matrix; [CI](ci.md) owns execution. Implement these contracts in the project's scenario runner; this guide does not supply a Unity runner.

## One authoritative simulation driver

Each session has exactly one owner advancing gameplay time. Choose the mode before advancing the session:

| Mode | Owner | Other work |
|---|---|---|
| Live/player integration | The normal Update/FixedUpdate adapter | Tests send input and observe; they do not also call Tick |
| Manual/accelerated | The scenario runner advances explicit fixed steps | Live gameplay ticking/input is suspended; rendering can continue |

Composition owns a scoped handoff, for example a manual-clock lease with an owner token. Reject a second owner; release/restore in finally, including cancellation and failure. Restore previous settings rather than assumed defaults. A boolean test switch can implement a single-run fixture, but must reject overlapping runners and cannot leak into the next session. Do not disable the entire visual adapter if it also renders snapshots.

Advance the complete authoritative loop once per step: inputs → simulation/rules → committed state/events. Systems that affect gameplay (timers, cooldowns, spawns and scheduled rules) use the same simulated time. Explicitly advance their R3 time/frame providers where applicable; a fake provider alone does not stop the live PlayerLoop from ticking. Rendering/UI motion can use a separate unscaled display clock, which must not mutate authoritative state. For exact visual comparisons, also control/record display phase and rendered frame; freezing gameplay does not freeze USS, shader or UI motion. Wall-clock timeouts use real/unscaled time so a stalled or paused simulation still times out.

Accelerate by running more bounded fixed steps, yielding periodically for rendering/cancellation. Do not multiply a giant delta into rules that expect fixed steps, or combine manual stepping with increased timeScale. Changing timeScale alone does not transfer ownership. If Unity physics/Animator/root motion affects gameplay, either retain the engine-owned clock and accelerate that complete path, or qualify a manual engine simulation mode and restore its settings. Pure tick tests do not certify engine behavior or cross-platform determinism.

Required tests: while manual mode owns the session, yield several real frames **without stepping** and assert simulation tick/time/state are unchanged; advance N steps and assert the expected tick/time and outcomes; reject concurrent ownership; cancel/fail and prove live mode resumes once; repeat across Play/session restarts. Compare accelerated and normal fixed-step results where deterministic. Record mode, owner, step size/count and simulated duration. Profile frame budgets separately in real time.

## Editor readiness and capture source

For live Play Mode scenarios, a ready connection or Play flag does not establish progress. Where Pipeline supplies `frameCount`/`playerLoopTicking` through CLI status, require advancing frames over a bounded observation window when the scenario expects live execution; false outside an intentional pause signals a stalled loop. Missing fields mean unavailable capability, not success or a freeze: use the runner's observable heartbeat/tick/render checkpoint. Paused/manual scenarios follow their declared clocks and expected render progress instead. Do not introduce a second clock owner to make a stalled run pass.

Record the actual capture source (Game View, player, Scene View or desktop fallback) in producer evidence. CLI MCP capture tools can fall back to a desktop screenshot on timeout or a blocked Editor. Such images are diagnostics, not accepted game/Scene View checkpoint captures. Reject fallback/unknown source or a mismatched requested view even when dimensions, timestamp and hash look correct; use a capture adapter that can attest its source. If an API cannot establish it, use a verified direct game/player capture path. Also inspect framing; a fresh screenshot of the wrong window is not game evidence.

## Captures belong to the current run

1. The external runner creates a unique run ID and fresh output directory, using create-new semantics. Reusing a directory is an error. Pass that ID and an explicit checkpoint list to the game/capture process. Keep baselines and earlier evidence elsewhere.
2. Wait for scenario/content/layout/render readiness. For localized UI, require the requested locale, loaded table/content revision and settled fonts/layout, not merely a selected-locale notification. Capture the current Game View/player into that run directory; await completed writes/readbacks. A file merely existing is insufficient. Do not copy an earlier capture into the new run or select the newest file from a shared screenshots folder.
3. The capture process writes a manifest only after successful completion. Include run ID, source revision plus dirty-tree/content identity when relevant, player/build hash, scenario/checkpoint, seed/input profile, clock mode/tick/time, device/backend, actual resolution/locale, localization content revision/readiness when applicable, capture source/view, capture timestamp, relative file path and SHA-256. Write temporary files then finalize them; an incomplete manifest cannot pass.
4. The validator compares the manifest against the **runner's independently retained request**: exact run/build/scenario IDs and required checkpoints, no duplicates or paths outside the run directory, successful completion, nonempty decodable media with expected dimensions and matching hashes. Reject stale timestamps using a recorded filesystem-resolution tolerance, future/implausible times, missing checkpoints and mismatched provenance. Timestamps alone are insufficient; identical pixels can be legitimate newly captured static states.
5. Only validated current-run captures enter visual review. The reviewer opens the exact hashed files and records inspection/defects separately; successful capture validation is not visual approval. Upload that manifest and those files together even on a failed run, keeping failure status explicit.

For a legacy capture API that writes fixed filenames, the runner isolates its working/output location or quarantines those outputs before launching and verifies fresh producer completion. Preserve accepted baselines; never delete unrelated captures to make a check pass.

Rejection probes: pre-seed an old expected filename then skip its capture; submit a prior run's manifest; omit a checkpoint; truncate or modify media after capture; return the wrong build/resolution/locale or capture before locale readiness; time out mid-write; return a desktop fallback or unknown capture source. Each must fail with the intended reason, then a new complete run must pass. A fresh directory and nonce bind trusted producer evidence to an invocation; a validator cannot prove provenance if the producer deliberately relabels old media, so test the capture operation as well.

For short effects, extend this same run contract with [event-timed recording windows](visual-fixtures.md#event-timed-recordings), actual frame timestamps and sampling-gap rejection. Still checkpoints alone can miss the effect. Keep recording overhead outside performance acceptance.
