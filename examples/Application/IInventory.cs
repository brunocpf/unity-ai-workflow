#nullable enable
using R3;

namespace Workflow.Examples.Application
{
    // Implement this port with the game's use case. This file has no Unity dependency.
    public interface IInventory
    {
        Observable<InventoryState> State
        {
            get;
        }

        void Activate(string itemId);
    }
}
