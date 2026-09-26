#nullable enable
namespace Workflow.Examples.Presentation
{
    // Coherent, immutable UI projection. No Unity types or application mutation surface.
    public readonly struct InventorySlotState
    {
        public string Title
        {
            get;
        }
        public string QuantityText
        {
            get;
        }
        public bool CanActivate
        {
            get;
        }

        public InventorySlotState(string title, string quantityText, bool canActivate)
        {
            Title = title;
            QuantityText = quantityText;
            CanActivate = canActivate;
        }
    }
}
