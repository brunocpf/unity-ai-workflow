#nullable enable
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Xml.Linq;
using Workflow.Examples.Editor;

internal static class IdeProjectChecks
{
    private static int _checks;

    private static void Check(bool value, string name)
    {
        if (!value)
        {
            throw new Exception(name);
        }

        _checks++;
    }

    private static void Main()
    {
        var owned = new Dictionary<string, string>(StringComparer.Ordinal) { ["Game.UI"] = "Game.UI" };
        foreach (string xmlns in new[] { "", " xmlns=\"http://schemas.microsoft.com/developer/msbuild/2003\"" })
        {
            string source = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<Project" + xmlns + ">" +
                "<PropertyGroup><DefineConstants>UNITY_EDITOR;SOME_SYMBOL</DefineConstants>" +
                "<Nullable>disable</Nullable><LangVersion>7.3</LangVersion>" +
                "<TargetFramework>netstandard2.1</TargetFramework></PropertyGroup>" +
                "<ItemGroup><Reference Include=\"UnityEngine\" /></ItemGroup>" +
                "<Import Project=\"other.props\" /></Project>";
            string changed = IdeProjectXml.Apply("/tmp/Game.UI.csproj", source, owned, "9.0", "enable");
            Check(changed == IdeProjectXml.Apply("Game.UI.csproj", changed, owned, "9.0", "enable"), "idempotence");
            string vendor = IdeProjectXml.Apply("Game.UI.Vendor.csproj", source, owned, "9.0", "enable");
            Check(vendor == source, "exact owned allowlist");
            Check(
                IdeProjectXml.Apply("vendor.csproj", "not XML", owned, "", "bad") == "not XML",
                "vendor no parse or changes");

            var root = XDocument.Parse(changed).Root!;
            var ns = root.Name.Namespace;
            var group = root.Elements(ns + "PropertyGroup").Last();
            Check((string?)group.Attribute("Label") == "WorkflowOwnedCompiler", "group label");
            Check((string?)group.Element(ns + "Nullable") == "enable", "nullable");
            Check((string?)group.Element(ns + "LangVersion") == "9.0", "language");
            Check((string?)group.Element(ns + "RootNamespace") == "Game.UI", "namespace");
            Check((string?)group.Element(ns + "TreatWarningsAsErrors") == "true", "warnings");
            Check(
                root.Descendants(ns + "DefineConstants").Single().Value == "UNITY_EDITOR;SOME_SYMBOL",
                "defines preserved");
            Check(root.Descendants(ns + "TargetFramework").Single().Value == "netstandard2.1", "framework preserved");
            Check(
                (string?)root.Descendants(ns + "Reference").Single().Attribute("Include") == "UnityEngine",
                "references preserved");
            Check((string?)root.Element(ns + "Import")?.Attribute("Project") == "other.props", "import preserved");

            string modern = IdeProjectXml.Apply("Game.UI.csproj", changed, owned, "14.0", "enable");
            var groups = XDocument.Parse(modern).Descendants(ns + "PropertyGroup");
            Check(
                groups.Count(item => (string?)item.Attribute("Label") == "WorkflowOwnedCompiler") == 1,
                "one group after profile change");
        }

        try
        {
            IdeProjectXml.Apply("Game.UI.csproj", "<Project />", owned, "9.0", "disable");
            throw new Exception("accepted invalid profile");
        }
        catch (ArgumentException)
        {
            _checks++;
        }

        try
        {
            IdeProjectXml.Apply("Game.UI.csproj", "<Other />", owned, "9.0", "enable");
            throw new Exception("accepted invalid XML root");
        }
        catch (InvalidDataException)
        {
            _checks++;
        }

        Console.WriteLine($"PASS XML: {_checks} assertions");
    }
}
