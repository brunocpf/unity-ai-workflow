# Client compatibility evidence

Installer release: 0.1.0. This record distinguishes file/layout checks from actual client discovery and game acceptance.

| Check | Result |
|---|---|
| Standard-library installer regression suite | 20 cases passed locally on macOS; CI covers Linux/macOS/Windows |
| Codex project skill discovery | Pass: all six enabled project skills via app-server skills/list (0.158.0-alpha.2.1) |
| Claude Code project skill discovery | Pass: all six project commands in stream-json initialization (2.1.198) |
| Model invocation and workflow behavior | Not tested by the installer suite |
| Unity foundation/player/visual acceptance | Separate project milestones; not claimed by installation |

See [installation and manual client checks](../INSTALL.md#verify-discovery-separately). Provider plugins, MCP connections, account permissions and Unity package compatibility require independent setup and evidence.

Recorded 26 September 2026 on macOS arm64 using isolated client settings and a disposable game workspace. [Sanitized discovery results](client-discovery.json). The probes initialized clients and inspected their skill inventories without requesting model execution. Instruction import paths are covered by installation checks; runtime instruction loading and model behavior still require the manual checks above.
