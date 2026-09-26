using System;
using System.IO;
using System.Linq;
using System.Text.Json;
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp;
using Microsoft.CodeAnalysis.CSharp.Syntax;

namespace Workflow.Tooling
{
    internal static class Program
    {
        // Verification only. File selection/ownership belongs to the invoking coverage gate.
        private static int Main(string[] args)
        {
            if (args.Length < 1)
            {
                Console.Error.WriteLine("Usage: CodeOrganization files.json [preprocessor symbols ...]");
                return 2;
            }

            string[] files = JsonSerializer.Deserialize<string[]>(File.ReadAllText(args[0])) ?? Array.Empty<string>();
            if (files.Length == 0)
            {
                Console.Error.WriteLine("No source files selected.");
                return 2;
            }

            int failures = 0;
            var options = new CSharpParseOptions(LanguageVersion.Preview, preprocessorSymbols: args.Skip(1));
            foreach (string file in files.Distinct(StringComparer.Ordinal))
            {
                string source = File.ReadAllText(file);
                var tree = CSharpSyntaxTree.ParseText(source, options, file);
                var root = tree.GetCompilationUnitRoot();
                var lines = tree.GetText().Lines;
                void Report(SyntaxNode node, string id, string message)
                {
                    int line = node.GetLocation().GetLineSpan().StartLinePosition.Line + 1;
                    Console.Error.WriteLine($"{file}({line}): {id}: {message}");
                    failures++;
                }

                foreach (var error in tree.GetDiagnostics().Where(item => item.Severity == DiagnosticSeverity.Error))
                {
                    Console.Error.WriteLine(error.ToString());
                    failures++;
                }

                var types = root.DescendantNodes().OfType<MemberDeclarationSyntax>()
                    .Where(node => (node is BaseTypeDeclarationSyntax || node is DelegateDeclarationSyntax) &&
                        (node.Parent is BaseNamespaceDeclarationSyntax || node.Parent is CompilationUnitSyntax))
                    .ToArray();
                if (types.Length > 1)
                {
                    Report(
                        root,
                        "ORG001",
                        "One top-level type per file; private nested helpers may stay with their owner.");
                }

                foreach (var type in types)
                {
                    string name = type is BaseTypeDeclarationSyntax declared ? declared.Identifier.ValueText :
                        ((DelegateDeclarationSyntax)type).Identifier.ValueText;
                    string stem = Path.GetFileNameWithoutExtension(file);
                    bool partial = type is TypeDeclarationSyntax declaration &&
                        declaration.Modifiers.Any(SyntaxKind.PartialKeyword);
                    if (stem != name && !(partial && stem.StartsWith(name + ".", StringComparison.Ordinal)))
                    {
                        Report(type, "ORG002", "Filename must match its type; partials may use Type.Part.cs.");
                    }
                }

                foreach (var block in root.DescendantNodes().OfType<BlockSyntax>())
                {
                    if (block.Statements.Count > 0 && (
                        tree.GetLineSpan(block.OpenBraceToken.Span).StartLinePosition.Line ==
                        block.Statements[0].GetLocation().GetLineSpan().StartLinePosition.Line ||
                        tree.GetLineSpan(block.CloseBraceToken.Span).EndLinePosition.Line ==
                        block.Statements.Last().GetLocation().GetLineSpan().EndLinePosition.Line))
                    {
                        Report(block, "ORG003", "Expand nonempty statement blocks onto separate lines.");
                    }

                    for (int i = 1; i < block.Statements.Count; i++)
                    {
                        if (block.Statements[i - 1].GetLocation().GetLineSpan().EndLinePosition.Line ==
                            block.Statements[i].GetLocation().GetLineSpan().StartLinePosition.Line)
                        {
                            Report(block.Statements[i], "ORG003", "Separate statements need separate lines.");
                        }
                    }
                }

                foreach (var type in root.DescendantNodes().OfType<TypeDeclarationSyntax>())
                {
                    for (int i = 1; i < type.Members.Count; i++)
                    {
                        var before = type.Members[i - 1];
                        var after = type.Members[i];
                        int end = before.GetLocation().GetLineSpan().EndLinePosition.Line;
                        int start = after.GetLocation().GetLineSpan().StartLinePosition.Line;
                        if (end == start)
                        {
                            Report(after, "ORG004", "Separate member declarations need separate lines.");
                            continue;
                        }

                        if (Compact(before) && Compact(after))
                        {
                            continue;
                        }

                        bool blank = Enumerable.Range(end + 1, Math.Max(0, start - end - 1))
                            .Any(index => string.IsNullOrWhiteSpace(lines[index].ToString()));
                        if (!blank)
                        {
                            Report(
                                after,
                                "ORG004",
                                "Separate members with a blank line; fields/simple properties may group.");
                        }
                    }
                }

                foreach (var node in root.DescendantNodes())
                {
                    int count = node switch
                    {
                        ArgumentListSyntax arguments => arguments.Arguments.Count,
                        ParameterListSyntax parameters => parameters.Parameters.Count,
                        InitializerExpressionSyntax initializer => initializer.Expressions.Count,
                        _ => 0
                    };
                    var span = node.GetLocation().GetLineSpan();
                    bool configuration = node is InitializerExpressionSyntax init &&
                        init.IsKind(SyntaxKind.ObjectInitializerExpression) && count > 1;
                    if (count > 1 && span.StartLinePosition.Line == span.EndLinePosition.Line &&
                        (configuration || lines[span.StartLinePosition.Line].Span.Length > 120))
                    {
                        Report(node,
                            "ORG005",
                            "Split long argument/parameter lists and object configuration across lines.");
                    }
                }
            }

            Console.WriteLine($"Organization: {files.Length} files, {failures} violations.");
            return failures == 0 ? 0 : 1;
        }

        private static bool Compact(MemberDeclarationSyntax member)
        {
            return member is FieldDeclarationSyntax || member is EventFieldDeclarationSyntax ||
                member is PropertyDeclarationSyntax property &&
                (property.ExpressionBody != null || property.AccessorList != null &&
                    property.AccessorList.Accessors.All(accessor => accessor.Body == null && accessor.ExpressionBody == null));
        }
    }
}
