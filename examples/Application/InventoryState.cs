#nullable enable

namespace Workflow.Examples.Application
{
    public readonly struct InventoryState
    {
        public string ItemId
        {
            get;
        }
        public string Title
        {
            get;
        }
        public int Quantity
        {
            get;
        }

        public InventoryState(string id, string title, int quantity)
        {
            ItemId = id;
            Title = title;
            Quantity = quantity;
        }
    }
}
