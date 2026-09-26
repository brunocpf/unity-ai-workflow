#nullable enable
using System;
using UnityEditor;

namespace Workflow.Examples.Editor
{
    // Invalidates only; no AssetDatabase loads/imports or runtime-session resets here.
    public sealed class UiCatalogPostprocessor : AssetPostprocessor
    {
        private static void OnPostprocessAllAssets(
            string[] importedAssets,
            string[] deletedAssets,
            string[] movedAssets,
            string[] movedFromAssetPaths,
            bool didDomainReload)
        {
            if (didDomainReload || AffectsTemplates(importedAssets) || AffectsTemplates(deletedAssets) ||
                AffectsTemplates(movedAssets) || AffectsTemplates(movedFromAssetPaths))
            {
                AuthoringUiTemplates.Invalidate();
            }
        }

        private static bool AffectsTemplates(string[] paths)
        {
            foreach (string path in paths)
            {
                // .asset is conservative: deleted catalogs cannot be queried for their type.
                if (path.EndsWith(".asset", StringComparison.OrdinalIgnoreCase) ||
                    path.EndsWith(".uxml", StringComparison.OrdinalIgnoreCase) ||
                    path.EndsWith(".uss", StringComparison.OrdinalIgnoreCase))
                {
                    return true;
                }
            }
            return false;
        }
    }
}
