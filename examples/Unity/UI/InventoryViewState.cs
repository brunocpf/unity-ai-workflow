#nullable enable
using System;
using Unity.Properties;
using UnityEngine.UIElements;
using Workflow.Examples.Presentation;

namespace Workflow.Examples.UI
{
    [GeneratePropertyBag]
    public sealed class InventoryViewState : INotifyBindablePropertyChanged
    {
        public event EventHandler<BindablePropertyChangedEventArgs>? propertyChanged;
        [CreateProperty] public string Title { get; private set; } = "Item";
        [CreateProperty] public string QuantityText { get; private set; } = "0";

        public void Apply(InventorySlotState state)
        {
            bool titleChanged = Title != state.Title;
            bool quantityChanged = QuantityText != state.QuantityText;
            // Set the complete snapshot before publishing individual notifications.
            Title = state.Title;
            QuantityText = state.QuantityText;
            if (titleChanged)
            {
                Notify(nameof(Title));
            }

            if (quantityChanged)
            {
                Notify(nameof(QuantityText));
            }
        }

        private void Notify(string name)
        {
            propertyChanged?.Invoke(this, new BindablePropertyChangedEventArgs(name));
        }
    }
}
