#nullable enable
using System;
using System.Collections.Generic;
using UnityEngine.UIElements;

namespace Workflow.Examples.UI
{
    // Owns one provider lease. Dispose only after every consumer/pool is removed.
    public sealed class UiLibrary : IUiTemplateResolver, IDisposable
    {
        private readonly Dictionary<string, VisualTreeAsset> _templates;
        private readonly object _generation;
        private IDisposable? _contentLease;
        private bool _disposed;

        // Transfers lease ownership, including failure. Catalogs must be loaded first.
        public UiLibrary(IEnumerable<UiTemplateCatalog> catalogs, IDisposable contentLease)
        {
            _contentLease = contentLease ?? throw new ArgumentNullException(nameof(contentLease));
            try
            {
                _generation = UiTemplates.Generation;
                _templates = new Dictionary<string, VisualTreeAsset>(StringComparer.Ordinal);
                foreach (var catalog in catalogs)
                {
                    if (catalog == null)
                    {
                        throw new ArgumentException("Missing catalog.");
                    }

                    catalog.AddTo(_templates);
                }
            }
            catch (Exception error)
            {
                var lease = _contentLease;
                _contentLease = null;
                try
                {
                    lease?.Dispose();
                }
                catch (Exception cleanup)
                {
                    throw new AggregateException(error, cleanup);
                }
                throw;
            }
        }

        public void EnsureAlive()
        {
            if (_disposed)
            {
                throw new ObjectDisposedException(nameof(UiLibrary));
            }

            if (!ReferenceEquals(_generation, UiTemplates.Generation))
            {
                throw new InvalidOperationException("UI library belongs to a previous session.");
            }
        }

        public VisualTreeAsset GetRequired(string id)
        {
            EnsureAlive();
            if (!_templates.TryGetValue(id, out var asset) || asset == null)
            {
                throw new InvalidOperationException($"UI template not preloaded: {id}");
            }

            return asset;
        }

        public void Dispose()
        {
            _ = UiTemplates.Generation; // Also enforces main-thread ownership.
            if (_disposed)
            {
                return;
            }

            _disposed = true;
            _templates.Clear();
            var lease = _contentLease;
            _contentLease = null;
            lease?.Dispose();
        }
    }
}
