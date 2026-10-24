# Code organization and the quality check

Formatting, code organization, analyzers and compilation each catch different problems. See [code quality](code-quality.md) for diagnostics and [IDE setup](ide.md) for compiler/namespace settings.

## Source conventions

- One top-level class/struct/record/interface/enum/delegate per matching filename. Partial declarations may use Type.Part.cs. Private nested implementation helpers stay with their owner; intentional public nested API types are reviewed as part of that owner. Assembly attributes/global imports may have dedicated files.
- One statement per line. Expand nonempty statement blocks. Required braces come from the configured style; no compressed constructor bodies or several assignments on one line.
- Blank lines separate constructors, methods and nested types. Related fields/events/simple properties may form compact groups. Keep accessors consistently formatted.
- Keep multi-property object configuration multiline. Wrap long parameter/argument lists (the supplied check uses 120 columns). Break long fluent chains and complex expressions at meaningful boundaries; don't split string literals or URLs just to hit a width. Formatting doesn't replace readability review.
- Logical namespaces follow the owning module, not every Assets/Unity directory segment. See [IDE setup](ide.md). Vendor and generated source keep their own organization.

[CodeOrganization](../starter/quality/CodeOrganization/Program.cs) uses Roslyn's parser, not regular expressions. It checks top-level types (including delegates and file-scoped namespaces), filename/partial naming, compressed statements, member spacing and long list/configuration layout. It is read-only and fails on syntax errors. It is not a compiler or formatter and never rewrites files.

## The quality check

Bootstrap copies the [quality directory](../starter/quality/check.py) into tooling/quality/, including CodeOrganization and [coverage.json](../starter/quality/coverage.json). Set the actual solution paths, owned project names and `pureSourceRoots`. Add the CodeOrganization project to the hand-maintained SDK solution; it imports tooling/dotnet/Directory.Build.props for the same language/nullability/analyzer policy.

Run `python3 tooling/quality/check.py` from the project root (`python` on Windows), or pass specific files for quick feedback. The pre-commit hook calls the same script with staged files; CI runs it on everything.

The script:

1. Finds owned C# under Assets/Game and tooling (skipping `.g.cs`/`.generated.cs`).
2. Reads each owned project's compile items and settings through MSBuild, and fails if nullable, language version or warnings-as-errors differ from tooling/ide/owned-projects.json.
3. Fails if an owned file isn't compiled by any project. Pure Core/Application/Presentation files must be in both the Unity and SDK projects; tooling files must be in an SDK project.
4. Runs CodeOrganization on the files.
5. Runs `dotnet format --verify-no-changes` against the Unity and SDK solutions, passing individual repository-relative file paths. (Directory filters and absolute paths can silently match nothing in `dotnet format`.)

`dotnet format` can exit successfully even when it failed to load the workspace, so the script also fails on workspace-load warnings. If the formatter can't load the generated Unity solution, fix the references/SDK problem rather than switching to a whitespace-only check. [dotnet format options](https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-format).

`python3 tooling/quality/test_organization.py` runs the [checker's own tests](../starter/quality/test_organization.py); run it after changing the checker or upgrading the SDK.

The quality check covers formatting and organization only. Unity compilation and tests are separate CI steps; a passing format check is not a passing build.
