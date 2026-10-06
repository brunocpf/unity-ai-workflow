#nullable enable
using System;
using UnityEngine.UIElements;

namespace Workflow.Examples.UI.Navigation
{
    // Construct only after content is ready. Lifetime owns bindings, VM and per-screen leases.
    public sealed class UiStackEntry : IDisposable
    {
        private readonly IDisposable _lifetime;
        private bool _disposed;

        public UiStackEntry(
            VisualElement view,
            Func<VisualElement?> initialFocus,
            IDisposable lifetime,
            bool dismissOnCancel = true)
        {
            View = view ?? throw new ArgumentNullException(nameof(view));
            InitialFocus = initialFocus ?? throw new ArgumentNullException(nameof(initialFocus));
            _lifetime = lifetime ?? throw new ArgumentNullException(nameof(lifetime));
            DismissOnCancel = dismissOnCancel;
        }

        public VisualElement View { get; }
        public Func<VisualElement?> InitialFocus { get; }
        public bool DismissOnCancel { get; }
        internal VisualElement? ReturnFocus { get; set; }
        internal bool IsModal { get; set; }
        internal bool IsDisposed => _disposed;

        public void Dispose()
        {
            if (_disposed)
            {
                return;
            }
            _disposed = true;
            try
            {
                _lifetime.Dispose();
            }
            finally
            {
                View.RemoveFromHierarchy();
                ReturnFocus = null;
            }
        }
    }
}
