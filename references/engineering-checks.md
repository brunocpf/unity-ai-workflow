# Independent engineering checks

The project README names actual local and CI commands. Checks must run without a planning framework, change identifier, requirement map or archive state. Use the project's existing automation; no new runner or report format is mandatory.

Preserve coverage for pure tests and boundaries; Unity runtime/UI/Editor/test semantic analysis and organization; Edit/Play Mode integration; target-player build/launch; authoring edit preservation; and affected lifecycle, localization, input and performance behavior. [Validation](validation.md) selects relevant cases; [CI](ci.md) defines runner requirements. Fast checks must not claim full Unity semantic validation. Run current code, fail on nonzero exits, timeouts, missing expected reports or uncovered owned assemblies. Prove rejection when establishing/changing gates. Keep expected test counts/report parsing in the actual project suites, not a generic log wrapper.

Visual work additionally requires fresh captures, inspection and iteration against the target. [Scenario checks](test-scenarios.md) retain single-clock ownership and stale-capture rejection. Report manual/device/user checks as passed, failed or pending with actual observations and relevant artifacts; command success does not grant those verdicts. Recheck evidence affected by subsequent edits. Summarize in the existing project record or final response, without a compulsory evidence ledger.

## Optional concise command output

Adapt [run.py](../starter/verification/run.py) into tooling/verification/run.py only if existing tooling lacks full-log retention and bounded summaries:

```sh
python3 tooling/verification/run.py --quiet --timeout 600 -- dotnet test tooling/dotnet/Game.Tests/Game.Tests.csproj
```

Run from the game root or pass `--root /absolute/game`. Replace the example with the project's real command. Commands are argument arrays, not shell strings; invoke an interpreter explicitly for scripts. Default timeout is 600 seconds; set a realistic bound for each build/test. Quiet and verbose modes execute identically, save complete combined output in a fresh artifacts/verification/run-*/command.log, preserve child failure codes (signals map to shell convention), and return 124 on timeout. An absent command/executable fails. No automatic retries. Retain/upload logs even when CI fails.

This wrapper executes one command; it does not discover suites, validate reports or certify game acceptance. Existing aggregate scripts must propagate every child's failure. Each suite has one execution owner; keep distinct platform/security jobs and avoid duplicate runs merely to populate receipts.
