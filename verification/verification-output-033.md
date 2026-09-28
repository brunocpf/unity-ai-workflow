# Verification output qualification — 0.3.3

27 September 2026. Optional presentation improvements over 0.3.2; no OpenSpec pin, schema, scenario, evidence-format or acceptance-rule change.

- Full local suite: 54 tests passed. Six output tests exercise complete stdout/stderr retention, concise success, byte/line-bounded failure excerpts, verbose output, identical gate selection, unique log directories and explicit delivery checking with no active changes. A real runner subprocess preserved child exit 9 and stopped before later gates.
- Real pinned OpenSpec pilot: quiet and verbose execution both accepted valid synthetic evidence and rejected pending evidence; schema/instructions, first/follow-up archive and final strict validation passed. Synthetic fixtures are not game-test or owner-acceptance evidence.
- Disposable 0.3.2 → 0.3.3 assess/dry-run/update/check preserved a custom project runner, PR form and policy document. New starter files were installed only in managed standards. Existing projects must merge compatible presentation changes explicitly.
- Repository link/config and diff checks passed. Review confirmed no changes to upstream integrations, lifecycle/artifact requirements, the evidence checker or existing independent gates. CI runs the unit and real-CLI probes on Linux, macOS and Windows; consult the published commit's Actions result.

No Unity project or model-driven game task was executed. Game-specific runner adoption, owner acceptance, log-upload retention and token savings remain project-level qualification. Historical receipts are not refreshed by this release.
