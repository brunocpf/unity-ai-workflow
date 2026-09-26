# Client compatibility evidence

Installer release: 0.1.0. This record distinguishes file/layout checks from actual client discovery and game acceptance.

| Check | Result |
|---|---|
| Standard-library installer regression suite | 21 cases passed locally on macOS; CI covers Linux/macOS/Windows |
| Codex project skill discovery | Pass: all six enabled project skills via app-server skills/list (0.158.0-alpha.2.1) |
| Claude Code project skill discovery | Pass: all six project commands in stream-json initialization (2.1.198) |
| Model invocation and workflow behavior | Not tested by the installer suite |
| Unity foundation/player/visual acceptance | Separate project milestones; not claimed by installation |

See [installation and manual client checks](../INSTALL.md#verify-discovery-separately). Provider plugins, MCP connections, account permissions and Unity package compatibility require independent setup and evidence.

Recorded 26 September 2026 on macOS arm64 using isolated client settings and a disposable game workspace. [Sanitized discovery results](client-discovery.json). The probes initialized clients and inspected their skill inventories without requesting model execution. Instruction import paths are covered by installation checks; runtime instruction loading and model behavior still require the manual checks above.

## Global entrypoints — 0.2.0

On 26 September 2026, both `unity-workflow-start` and `unity-workflow-update` were discovered at user scope in an empty workspace by Codex 0.158.0-alpha.2.1 and Claude Code 2.1.198. [Sanitized global results](global-discovery.json). Codex used isolated configuration while retaining the real user skill directory. Claude used real user skills with hooks/MCP disabled; its bare mode did not enumerate these commands, so the successful check used normal skill discovery. No model turn was requested.

The expanded installer suite has 31 cases, including independent cached installation, global conflicts, retry after rollback, independent project versions and read-only assessment. All passed locally on macOS. CI runs the same suite on all three operating systems. This evidence establishes installation/discovery, not the quality of a model's applicability review or Unity acceptance.
