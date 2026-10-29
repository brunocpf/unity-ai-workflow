---
name: unity-workflow-start
description: Start a new Unity project using the user's installed Unity AI workflow. Install the kit into the project, then set it up or build the first playable slice within the requested scope. Use for a new Unity game/workspace, not ordinary changes in a project that already uses the kit.
---

The versioned kit for this entrypoint is at `{{KIT_ROOT}}`. Read its `references/adoption.md` and `README.md`; the user doesn't need to supply the kit path or repeat architectural defaults.

Use the current game workspace unless the user names another destination. Inspect it before writing; if it contains an unrelated project or is the kit itself, resolve the destination first. Preserve existing work. If `.unity-workflow/installation.json` already exists, use that project's local standards and skills without upgrading it to this global version.

For a new workspace, run this kit's `install.py doctor --target <absolute-project-path>` once and follow its guidance, then `install.py install --target <absolute-project-path> --agent {{AGENT}}`, `install.py check --target <absolute-project-path>` and `install.py scaffold --target <absolute-project-path>`, using Python 3.9+ and properly quoted paths. Then read the installed `docs/standards/PROJECT-RULES.md`, the local `unity-project-bootstrap` SKILL.md and `docs/standards/references/setup-checklist.md`. If the current session hasn't refreshed its skill list, read the file directly; later sessions find it normally.

A setup request ends after project setup; a request for a playable game includes the first slice unless the user limits it. Clarify unresolved product intent, especially target platforms and supported languages, while continuing independent work. Keep prior answers and established technical defaults.

Installing this global skill doesn't authorize creating a game; act on the user's project request. Don't initialize a game in the kit cache, silently fetch newer standards, change existing games, install unrelated providers or assume configured MCP tools.
