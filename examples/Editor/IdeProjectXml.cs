#nullable enable
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Xml.Linq;

namespace Workflow.Examples.Editor
{
    // BCL-only transformation, independently testable without launching Unity.
    public static class IdeProjectXml
    {
        public static string Apply(
            string path,
            string content,
            IReadOnlyDictionary<string, string> ownedProjects,
            string languageVersion,
            string nullable)
        {
            string name = Path.GetFileNameWithoutExtension(path);
            if (!ownedProjects.TryGetValue(name, out string? rootNamespace))
            {
                return content; // Vendor projects remain byte-for-byte unchanged.
            }

            if (string.IsNullOrWhiteSpace(languageVersion) || nullable != "enable" ||
                string.IsNullOrWhiteSpace(rootNamespace))
            {
                throw new ArgumentException("Invalid owned compiler profile.");
            }

            var document = XDocument.Parse(content, LoadOptions.PreserveWhitespace);
            XElement root = document.Root ?? throw new InvalidDataException("Generated project has no root.");
            XNamespace ns = root.Name.Namespace;
            if (root.Name.LocalName != "Project")
            {
                throw new InvalidDataException("Expected an MSBuild Project.");
            }

            var group = root.Elements(ns + "PropertyGroup")
                .SingleOrDefault(item => (string?)item.Attribute("Label") == "WorkflowOwnedCompiler");
            if (group != null)
            {
                group.Remove();
            }

            root.Add(new XElement(
                ns + "PropertyGroup",
                new XAttribute("Label", "WorkflowOwnedCompiler"),
                new XElement(ns + "Nullable", nullable),
                new XElement(ns + "LangVersion", languageVersion),
                new XElement(ns + "RootNamespace", rootNamespace),
                new XElement(ns + "TreatWarningsAsErrors", "true")));
            return document.ToString(SaveOptions.DisableFormatting);
        }
    }
}
