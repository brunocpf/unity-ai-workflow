#nullable enable
using System;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine.UIElements;
using Workflow.Examples.UI;

namespace Workflow.Examples.Editor
{
    // Authoring cache survives Play transitions; BeforeReload removes its registrations.
    [Unity.Scripting.LifecycleManagement.NoAutoStaticsCleanup]
    [InitializeOnLoad]
    public static class AuthoringUiTemplates
    {
        private static readonly Resolver Source = new Resolver();

        static AuthoringUiTemplates()
        {
            UiTemplates.ResetRuntime();
            UiTemplates.InstallAuthoringResolver(Source);
            EditorApplication.projectChanged -= Source.Invalidate;
            EditorApplication.projectChanged += Source.Invalidate;
            EditorApplication.playModeStateChanged -= OnPlayState;
            EditorApplication.playModeStateChanged += OnPlayState;
            AssemblyReloadEvents.beforeAssemblyReload -= BeforeReload;
            AssemblyReloadEvents.beforeAssemblyReload += BeforeReload;
        }

        internal static void Invalidate()
        {
            Source.Invalidate();
        }

        private static void OnPlayState(PlayModeStateChange state)
        {
            if (state == PlayModeStateChange.ExitingPlayMode ||
                state == PlayModeStateChange.ExitingEditMode)
            {
                UiTemplates.ResetRuntime();
            }
            // Do not clear authoring support while Builder is open.
        }

        private static void BeforeReload()
        {
            Source.Invalidate();
            UiTemplates.ResetRuntime();
            UiTemplates.InstallAuthoringResolver(null);
            EditorApplication.projectChanged -= Source.Invalidate;
            EditorApplication.playModeStateChanged -= OnPlayState;
            AssemblyReloadEvents.beforeAssemblyReload -= BeforeReload;
        }

        private sealed class Resolver : IUiTemplateResolver
        {
            private Dictionary<string, VisualTreeAsset>? _cache;

            public void Invalidate()
            {
                _cache = null;
            }

            public VisualTreeAsset GetRequired(string id)
            {
                if (_cache == null)
                {
                    var next = new Dictionary<string, VisualTreeAsset>(StringComparer.Ordinal);
                    // One scan per invalidation, never one scan per control.
                    foreach (string guid in AssetDatabase.FindAssets("t:UiTemplateCatalog"))
                    {
                        string path = AssetDatabase.GUIDToAssetPath(guid);
                        var catalog = AssetDatabase.LoadAssetAtPath<UiTemplateCatalog>(path);
                        if (catalog != null)
                        {
                            catalog.AddTo(next);
                        }
                    }
                    _cache = next;
                }
                if (!_cache.TryGetValue(id, out var template) || template == null)
                {
                    throw new InvalidOperationException($"Authoring catalog lacks '{id}'.");
                }

                return template;
            }
        }
    }
}
