---
name: unity-workflow-start
description: Start a new Unity project using the user's installed Unity AI workflow. Install its pinned project-local skills and standards, then bootstrap the foundation or implement the first slice within the requested scope. Use for a new Unity game/workspace, not ordinary changes in an already adopted project.
---

The complete, versioned kit for this entrypoint is at `{{KIT_ROOT}}`. Read its `references/adoption.md` and `README.md`; the user need not supply the kit path or repeat architectural defaults.

Use the current game workspace unless the user names another destination. Inspect it before writing; if it contains an unrelated project or is the kit itself, resolve the destination first. Preserve existing work. If `.unity-workflow/installation.json` already exists, use that project's local standards and skills without upgrading it to this global version.

For a new workspace, run this cached kit's `install.py install --target <absolute-project-path> --agent {{AGENT}}`, followed by `install.py check --target <absolute-project-path>`, using an available Python 3.10+ interpreter and properly quoted paths. Then read the installed `docs/standards/PROJECT-RULES.md` and the local `unity-project-bootstrap` SKILL.md. If the current session has not refreshed its skill inventory, read the file directly; later sessions use normal discovery.

Follow the adopted milestone contract: bootstrap/setup alone ends at Foundation ready; a requested playable game or end-to-end trial includes First slice accepted unless scope limits it. The milestone checkpoint adds no approval gate; selected OpenSpec operation boundaries still apply (references/context-efficiency.md#skill-ownership). Clarify unresolved product intent, especially target platforms and supported languages, while continuing independent work. Preserve prior answers and established technical defaults.

Installation of this global skill alone authorizes no game creation. Act on the user's project request. Do not initialize a game in the kit cache, silently fetch newer standards, alter existing games, install unrelated providers or assume configured MCP tools. Record project-local version/evidence; leave unfinished work in its existing tasks.
