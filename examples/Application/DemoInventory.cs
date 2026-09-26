#nullable enable
using System;
using R3;

namespace Workflow.Examples.Application
{
    // Local example state; replace Activate with an Application command in a real game.
    public sealed class DemoInventory : IInventory, IDisposable
    {
        private readonly ReactiveProperty<InventoryState> _state =
            new ReactiveProperty<InventoryState>(new InventoryState("potion", "Potion", 3));
        public Observable<InventoryState> State => _state;

        public void Activate(string itemId)
        {
            var current = _state.Value;
            if (current.ItemId != itemId || current.Quantity <= 0)
            {
                return;
            }

            _state.Value = new InventoryState(current.ItemId, current.Title, current.Quantity - 1);
        }

        public void Dispose()
        {
            _state.Dispose();
        }
    }
}
