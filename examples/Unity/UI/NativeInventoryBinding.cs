#nullable enable
using System;
using R3;
using Workflow.Examples.Presentation;

namespace Workflow.Examples.UI
{
    // Alternative binding adapter. Presentation decisions still belong to the same VM.
    public sealed class NativeInventoryBinding : IDisposable
    {
        private readonly InventorySlotViewModel _viewModel;
        private readonly InventorySlot _view;
        private readonly InventoryViewState _state = new InventoryViewState();
        private IDisposable? _subscription;
        private bool _disposed;

        public NativeInventoryBinding(InventorySlotViewModel viewModel, InventorySlot view)
        {
            _viewModel = viewModel ?? throw new ArgumentNullException(nameof(viewModel));
            _view = view ?? throw new ArgumentNullException(nameof(view));
            try
            {
                _view.Bind(_state);
                _view.Activated += Activate;
                _subscription = _viewModel.State.Subscribe(Apply);
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

        private void Apply(InventorySlotState value)
        {
            if (_disposed)
            {
                return;
            }
            _state.Apply(value);
            _view.SetInteractable(value.CanActivate);
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
