#nullable enable
using System;
using R3;
using Workflow.Examples.Presentation;

namespace Workflow.Examples.UI
{
    // Mechanical adapter; borrows both VM and view. No Application dependency.
    public sealed class InventoryBinding : IDisposable
    {
        private readonly InventorySlotViewModel _viewModel;
        private readonly InventorySlot _view;
        private IDisposable? _subscription;
        private bool _disposed;

        public InventoryBinding(InventorySlotViewModel viewModel, InventorySlot view)
        {
            _viewModel = viewModel ?? throw new ArgumentNullException(nameof(viewModel));
            _view = view ?? throw new ArgumentNullException(nameof(view));
            try
            {
                _view.Activated += Activate;
                _subscription = _viewModel.State.Subscribe(Render);
            }
            catch (Exception error)
            {
                try
                {
                    Dispose();
                }
                catch (Exception cleanup)
                {
                    throw new AggregateException(error, cleanup);
                }
                throw;
            }
        }

        private void Render(InventorySlotState state)
        {
            if (!_disposed)
            {
                _view.Render(state.Title, state.QuantityText, state.CanActivate);
            }
        }

        private void Activate()
        {
            if (!_disposed)
            {
                _viewModel.Activate();
            }
        }

        public void Dispose()
        {
            if (_disposed)
            {
                return;
            }
            _disposed = true;
            _view.Activated -= Activate;
            try
            {
                _subscription?.Dispose();
            }
            catch (Exception error)
            {
                _subscription = null;
                try
                {
                    _view.Unbind();
                }
                catch (Exception cleanup)
                {
                    throw new AggregateException(error, cleanup);
                }
                throw;
            }
            _subscription = null;
            _view.Unbind();
        }
    }
}
