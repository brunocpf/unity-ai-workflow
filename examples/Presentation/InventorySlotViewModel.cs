#nullable enable
using System;
using System.Globalization;
using R3;
using Workflow.Examples.Application;

namespace Workflow.Examples.Presentation
{
    // Owner-thread-only. Borrows the use case; owns projection and subscription.
    public sealed class InventorySlotViewModel : IDisposable
    {
        private readonly IInventory _inventory;
        private readonly ReactiveProperty<InventorySlotState> _state =
            new ReactiveProperty<InventorySlotState>(new InventorySlotState("Item", "0", false));
        private IDisposable? _subscription;
        private string _itemId = string.Empty;
        private int _quantity;
        private bool _disposed;

        public Observable<InventorySlotState> State => _state;

        public InventorySlotViewModel(IInventory inventory)
        {
            _inventory = inventory ?? throw new ArgumentNullException(nameof(inventory));
            try
            {
                _subscription = inventory.State.Subscribe(Project);
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

        private void Project(InventoryState source)
        {
            if (_disposed)
            {
                return;
            }
            string quantity = _quantity == source.Quantity
                ? _state.Value.QuantityText
                : source.Quantity.ToString(CultureInfo.InvariantCulture);
            _quantity = source.Quantity;
            _itemId = source.ItemId;
            var next = new InventorySlotState(source.Title, quantity,
                !string.IsNullOrEmpty(source.ItemId) && source.Quantity > 0);
            var previous = _state.Value;
            if (previous.Title != next.Title || previous.QuantityText != next.QuantityText ||
                previous.CanActivate != next.CanActivate)
            {
                _state.Value = next;
            }
        }

        public void Activate()
        {
            if (!_disposed && _state.Value.CanActivate)
            {
                // UI gating improves UX; the use case must revalidate the command.
                _inventory.Activate(_itemId);
            }
        }

        public void Dispose()
        {
            if (_disposed)
            {
                return;
            }
            _disposed = true;
            try
            {
                _subscription?.Dispose();
            }
            catch (Exception error)
            {
                _subscription = null;
                _itemId = string.Empty;
                try
                {
                    _state.Dispose();
                }
                catch (Exception cleanup)
                {
                    throw new AggregateException(error, cleanup);
                }
                throw;
            }
            _subscription = null;
            _itemId = string.Empty;
            _state.Dispose();
        }
    }
}
