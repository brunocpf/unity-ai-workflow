# 0.5.0 process decoupling

Removed the shipped OpenSpec profile, pinned Node/npm graph, custom schema, requirement/evidence-map tooling, lifecycle guides and process integration test. Older versions remain available in immutable release history. Active instructions no longer prescribe planning artifacts, GitHub project management or archive workflows. Independently adopted process tools remain project-owned.

Preserved architecture, runtime examples, quality tooling, semantic coverage, rejection probes, visual freshness, single-clock tests, authored-content checks and CI guidance. Extracted optional command logging from the former runner without its lifecycle dependencies. Existing projects must inventory and preserve actual engineering commands before removing wrappers.

Validation passed: 47 Python tests (installer/global installation, native-navigation result validation and standalone command output); eight skill schemas; 522 Markdown links, 25 JSON and 20 XML/configuration files; diff whitespace checks. The process-specific tests were removed with their implementation, rather than counted as retained engineering coverage.

A disposable actual v0.4.1 → 0.5.0 → v0.4.1 round trip passed for both clients, preserving project-owned requirements, OpenSpec integration and check scripts. A permanent installer regression also covers dry-run preservation, managed legacy removal and idempotence. Existing modified-managed-file rejection remains tested. Default managed payload decreased from 113 to 94 files.

Self-review traced command ownership from the removed map runner to standalone local/CI entrypoints, checked missing-provider and independently retained process routes, and removed a leftover OpenSpec example and CI heading. Historical process guides are referenced at v0.4.1 instead of being shipped as current instructions. No consuming game was migrated. No Unity/runtime source changed; instruction checks are not live-agent or game acceptance. No token savings measured.
