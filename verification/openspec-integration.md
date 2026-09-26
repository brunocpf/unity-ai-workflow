# OpenSpec integration qualification — kit 0.3.0

26 September 2026, macOS arm64. Evaluated OpenSpec 1.13.2 with Node 24.15.0.

The real-CLI disposable pilot (`python tools/check_openspec_integration.py`) installs the locked dependency graph, initializes Codex and Claude integrations, validates the custom schema, retrieves artifact instructions, archives a new capability and a subsequent modified requirement, then strictly validates the reconciled baseline. It rejects an invalid scenario heading, pending acceptance and a pre-archive fingerprint. Fixtures label their evidence as synthetic; they are not game test results.

Unit tests cover mapping completeness, missing/modified evidence, pending/failed requirements, manual reviewer metadata, unfinished tasks, duplicate IDs, removed behavior, stale code/specs, archive reconciliation, binary/text hashing and collision-safe staging. Existing installer tests remain required. CI runs these checks and the real CLI pilot on Linux, macOS and Windows; consult the exact commit's GitHub Actions result for hosted execution status.

[Client discovery receipt](openspec-discovery.json): Codex 0.158.0-alpha.2.1 reported all six Unity and six OpenSpec project skills enabled with repo scope. Claude Code 2.1.198 reported the same twelve project skills. This used inventory/initialization, with no model turn; it does not prove an agent follows every instruction.

These checks qualify tooling structure and integration. They do not qualify Unity gameplay, visual quality, target devices or user acceptance. The evidence gate deliberately leaves actual test execution/result parsing and semantic/manual review to independent project gates. A project adopting this version must wire those gates into its existing CI and validate rejection behavior there.
