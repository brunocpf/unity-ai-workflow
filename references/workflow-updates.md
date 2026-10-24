# Update a project's kit

Global entrypoints and project-local standards have independent versions. A new kit version is a candidate for an existing game, not an automatic migration. The project's `.unity-workflow/installation.json`, its docs and its ADRs describe what's installed.

1. For "check for updates", look at the upstream repository and fetch a candidate into a separate checkout. Note its commit and kit.json version. Don't fetch into the game. If you're offline, say you couldn't check upstream.
2. Run `python3 /candidate/install.py assess --target /game`. It's read-only and lists added/changed/removed files plus local edits. Read the actual old and new content and the affected project code/docs; the file list alone doesn't tell you what applies. If it reports the linked install layout from kit 0.6, follow its message to convert the project to copied files first.
3. Decide for each meaningful change: **apply now**, **defer**, **not applicable** or **separate migration**. Consider the game's Unity/C# and package pins, renderer/platforms, features and project decisions. For example, an installer fix may apply immediately; a VFX policy changes nothing for a game without particle effects; a new Editor API needs that Editor version.
4. Review-only requests stop there. An update request covers compatible kit changes, not unrelated engine/package/content migrations. Run `install.py update --target /game --dry-run`, resolve conflicts without overwriting local edits, then apply the update and run `check`.
5. The installer updates the managed standards as a whole. Keep project exceptions in ADRs/rules outside the managed files rather than cherry-picking policy files. If a new rule conflicts with the project, defer it or adopt it with a documented exception.

Summarize the versions, what changed, what you applied or deferred, and any conflicts in the PR or final response.

To update global entrypoints, run a candidate's `install.py install-global`; it creates a new versioned cache and changes only the global skills. Existing games stay unchanged. `check-global` checks the current global installation. Old caches stay in place; don't edit them or point active skills at a working directory.
