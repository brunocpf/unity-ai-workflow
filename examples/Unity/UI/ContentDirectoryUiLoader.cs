#nullable enable
using System;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;
using Unity.Loading;

namespace Workflow.Examples.UI
{
    // LoadRoots owns registration; LoadAsync borrows a separately registered directory.
    public static class ContentDirectoryUiLoader
    {
        // Default for the 6000.7.0b2 evaluation profile; inherited from the b1 workaround.
        // Bounded synchronous preload, outside control constructors; b2 player proof is pending.
        // UiLibrary receives the directory lease, including ownership on constructor failure.
        public static UiLibrary LoadRoots(string directoryPath, CancellationToken cancellation)
        {
            if (string.IsNullOrWhiteSpace(directoryPath))
            {
                throw new ArgumentException("A built content directory path is required.", nameof(directoryPath));
            }
            var generation = UiTemplates.Generation; // Enforces main-thread initialization.
            cancellation.ThrowIfCancellationRequested();
            var directory = ContentLoadManager.RegisterContentDirectory(directoryPath);
            if (!directory.IsValid)
            {
                throw new InvalidOperationException("UI directory registration failed.");
            }
            var lease = new DirectoryLease(directory);
            try
            {
                var catalogs = ContentLoadManager.GetRootAssets<UiTemplateCatalog>(directory);
                cancellation.ThrowIfCancellationRequested();
                if (!ReferenceEquals(generation, UiTemplates.Generation))
                {
                    throw new OperationCanceledException("UI session changed during preload.");
                }
                if (catalogs.Length == 0)
                {
                    throw new InvalidOperationException("UI directory has no catalog roots.");
                }
                return new UiLibrary(catalogs, lease);
            }
            catch (Exception error)
            {
                try
                {
                    lease.Dispose(); // Idempotent if UiLibrary already released it.
                }
                catch (Exception cleanup)
                {
                    throw new AggregateException(error, cleanup);
                }
                throw;
            }
        }

        // Advanced path only: callers must prove how valid IDs reach the target player.
        // The b1 scene-ID transport failed; qualify it in a b2 player before selecting this path.
        // Caller owns directory registration until the returned library is disposed.
        public static async Task<UiLibrary> LoadAsync(
            IReadOnlyList<LoadableObjectId> catalogIds, CancellationToken cancellation)
        {
            var generation = UiTemplates.Generation; // Main thread, before any await.
            var lease = new CatalogLease();
            try
            {
                var catalogs = new List<UiTemplateCatalog>(catalogIds.Count);
                foreach (var id in catalogIds)
                {
                    cancellation.ThrowIfCancellationRequested();
                    var pending = lease.Add(id);
                    var catalog = await pending.Handle.LoadAsync();
                    // Native operation is drained before cancellation releases its handle.
                    cancellation.ThrowIfCancellationRequested();
                    if (!ReferenceEquals(generation, UiTemplates.Generation))
                    {
                        throw new OperationCanceledException("UI session changed during load.");
                    }

                    if (catalog == null)
                    {
                        throw new InvalidOperationException("UI catalog load failed.");
                    }

                    catalogs.Add(catalog);
                }
                cancellation.ThrowIfCancellationRequested();
                return new UiLibrary(catalogs, lease);
            }
            catch (Exception error)
            {
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

        private sealed class DirectoryLease : IDisposable
        {
            private ContentDirectoryHandle _directory;
            private bool _disposed;

            public DirectoryLease(ContentDirectoryHandle directory)
            {
                _directory = directory;
            }

            public void Dispose()
            {
                _ = UiTemplates.Generation; // Native directory operations remain on the owner thread.
                if (_disposed)
                {
                    return;
                }
                _disposed = true;
                ContentLoadManager.UnregisterContentDirectory(_directory);
                _directory = default;
            }
        }

        private sealed class CatalogHandle
        {
            // Keep one storage location even if Loadable is a mutable value type.
            public Loadable<UiTemplateCatalog> Handle;

            public CatalogHandle(LoadableObjectId id)
            {
                Handle = new Loadable<UiTemplateCatalog>(id);
            }
        }

        private sealed class CatalogLease : IDisposable
        {
            private readonly List<CatalogHandle> _handles = new List<CatalogHandle>();

            public CatalogHandle Add(LoadableObjectId id)
            {
                var entry = new CatalogHandle(id);
                _handles.Add(entry);
                return entry;
            }

            public void Dispose()
            {
                List<Exception>? errors = null;
                while (_handles.Count != 0)
                {
                    int last = _handles.Count - 1;
                    var entry = _handles[last];
                    _handles.RemoveAt(last);
                    try
                    {
                        entry.Handle.Release();
                    }
                    catch (Exception error)
                    {
                        (errors ??= new List<Exception>()).Add(error);
                    }
                }
                if (errors != null)
                {
                    throw new AggregateException(errors);
                }
            }
        }
    }
}
