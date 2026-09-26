#nullable enable
using System;
using System.Collections.Generic;
using System.IO;
using UnityEditor;
using UnityEngine;

namespace Workflow.Examples.Editor
{
    public sealed class IdeProjectSettings : AssetPostprocessor
    {
        [MenuItem("Workflow/Development/Regenerate IDE projects")]
        public static void Regenerate()
        {
            Unity.CodeEditor.CodeEditor.CurrentEditor.SyncAll();
        }

        private static string OnGeneratedCSProject(string path, string content)
        {
            string projectRoot = Path.GetDirectoryName(UnityEngine.Application.dataPath) ??
                throw new InvalidOperationException("Cannot locate the Unity project root.");
            string settingsPath = Path.Combine(projectRoot, "tooling/ide/owned-projects.json");
            var settings = JsonUtility.FromJson<Settings>(File.ReadAllText(settingsPath)) ??
                throw new InvalidDataException("Missing owned IDE compiler profile.");
            var owned = new Dictionary<string, string>(StringComparer.Ordinal);
            foreach (var project in settings.projects)
            {
                owned.Add(project.name, project.rootNamespace);
            }

            return IdeProjectXml.Apply(path, content, owned, settings.languageVersion, settings.nullable);
        }

        // Serialized settings DTOs; bootstrap validates names against actual owned asmdefs.
#pragma warning disable IDE1006 // Field names are the tracked JSON schema, not a runtime API.
        [Serializable]
        private sealed class Settings
        {
            public string languageVersion = string.Empty;
            public string nullable = string.Empty;
            public Project[] projects = Array.Empty<Project>();
        }

        [Serializable]
        private sealed class Project
        {
            public string name = string.Empty;
            public string rootNamespace = string.Empty;
        }
#pragma warning restore IDE1006
    }
}
