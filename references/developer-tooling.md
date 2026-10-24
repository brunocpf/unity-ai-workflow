# Developer setup and Git hooks

**Default: repository-local Husky.NET with a check-only pre-commit hook, backed by CI.**

## Set up once

1. Create a Git repository if needed. Create tooling/dotnet/Game.sln from the hand-maintained Core/Application/Presentation/test projects; pin the SDK in repository-root global.json and lock dependencies. Keep this pure solution separate from the generated Unity IDE solution. Set up the [IDE integration](ide.md) and the [quality check](code-organization.md) first; the hook needs both. Document Python 3.9+ (`python3` on macOS/Linux, `python` on Windows), .NET and Git LFS alongside the Unity CLI.
2. Copy the [tool manifest](../starter/hooks/dotnet-tools.json) to .config/dotnet-tools.json, the [task runner](../starter/hooks/task-runner.json) to .husky/task-runner.json, the [hook](../starter/hooks/pre-commit) to .husky/pre-commit and the [staged-file script](../starter/hooks/check_staged.py) to tooling/hooks/check_staged.py. Husky 0.9.1 is the reference pin. Merge existing manifests/hooks instead of replacing them.
3. Run `dotnet tool restore`, then `dotnet husky install`. Keep hook files executable. Keep generated .husky/_ files local per the tool's ignore guidance. Don't run installers on every restore/build or change global Git configuration.
4. Run `git lfs install --local` after choosing the hooks path. Keep existing pre-push behavior so `git lfs pre-push` still receives its arguments/stdin. Don't overwrite a custom hook. When the project tracks binary assets, a missing LFS install is a setup problem, not a warning to ignore.

[Husky installation](https://alirezanet.github.io/Husky.Net/guide/getting-started.html), [task runner](https://alirezanet.github.io/Husky.Net/guide/task-runner.html).

## What the hook does

The hook checks staged owned C# only and never auto-fixes or restages files. It refuses partially staged C# files because `dotnet format` reads the working tree, not the Git index; stage whole files instead. It calls tooling/quality/check.py with the staged files. If the generated Unity projects are missing, regenerate them.

Formatting fixes are explicit developer/agent actions followed by diff review. CI sets `HUSKY=0` and runs the checks directly on everything; hooks can be bypassed, so CI is the check that counts.

Git worktrees share some configuration: make sure hooks resolve in each checkout, and never share Library folders between them.
