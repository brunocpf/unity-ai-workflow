#nullable enable
using System;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UIElements;

namespace Workflow.Examples.UI
{
    [CreateAssetMenu(menuName = "Workflow/UI Template Catalog")]
    public sealed class UiTemplateCatalog : ScriptableObject
    {
        [Serializable]
        public sealed class Entry
        {
            public string Id = string.Empty;
            public VisualTreeAsset? Template;
        }

        [SerializeField] private Entry[] _entries = Array.Empty<Entry>();

        public void AddTo(Dictionary<string, VisualTreeAsset> destination)
        {
            foreach (var entry in _entries)
            {
                if (entry == null || string.IsNullOrWhiteSpace(entry.Id) || entry.Template == null)
                {
                    throw new InvalidOperationException($"Invalid UI entry in {name}.");
                }

                if (destination.ContainsKey(entry.Id))
                {
                    throw new InvalidOperationException($"Duplicate UI ID: {entry.Id}");
                }

                destination.Add(entry.Id, entry.Template);
            }
        }
    }
}
