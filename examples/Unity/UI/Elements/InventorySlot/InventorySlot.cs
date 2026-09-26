#nullable enable
using System;
using Unity.Properties;
using UnityEngine.UIElements;

namespace Workflow.Examples.UI
{
    [UxmlElement]
    public partial class InventorySlot : VisualElement
    {
        public const string TemplateId = "controls/inventory-slot";
        private readonly Label _title;
        private readonly Label _quantity;
        private bool _presented;
        private readonly Button _button;
        private string _previewTitle = "Item";
        public event Action? Activated;

        public InventorySlot()
        {
            AddToClassList("game-inventory-slot");
            UiTemplates.GetRequired(TemplateId).CloneTree(this);
            _title = this.Q<Label>("title") ?? throw new InvalidOperationException("Missing title.");
            _quantity = this.Q<Label>("quantity") ?? throw new InvalidOperationException("Missing quantity.");
            _button = this.Q<Button>("activateButton") ?? throw new InvalidOperationException("Missing button.");
            _button.clicked += OnActivated;
            ShowPreview();
        }

        [UxmlAttribute]
        public string PreviewTitle
        {
            get => _previewTitle;
            set
            {
                _previewTitle = value;
                if (!_presented)
                {
                    ShowPreview();
                }
            }
        }

        // Default R3 binding path. Private children remain encapsulated.
        public void Render(string title, string quantityText, bool canActivate)
        {
            if (dataSource != null)
            {
                throw new InvalidOperationException("Remove native binding before direct presentation.");
            }

            _presented = true;
            if (_title.text != title)
            {
                _title.text = title;
            }

            if (_quantity.text != quantityText)
            {
                _quantity.text = quantityText;
            }
            SetInteractable(canActivate);
        }

        // Optional native-binding path. Use exactly one binding adapter per control instance.
        public void Bind(InventoryViewState state)
        {
            if (state == null)
            {
                throw new ArgumentNullException(nameof(state));
            }

            Unbind();
            _presented = true;
            dataSource = state;
            _title.SetBinding("text", new DataBinding
            {
                dataSourcePath = new PropertyPath(nameof(InventoryViewState.Title)),
                bindingMode = BindingMode.ToTarget
            });
            _quantity.SetBinding("text", new DataBinding
            {
                dataSourcePath = new PropertyPath(nameof(InventoryViewState.QuantityText)),
                bindingMode = BindingMode.ToTarget
            });
        }

        public void Unbind()
        {
            _title.ClearBinding("text");
            _quantity.ClearBinding("text");
            dataSource = null;
            _presented = false;
            ShowPreview();
        }

        public void SetInteractable(bool enabled)
        {
            _button.SetEnabled(enabled);
        }

        private void ShowPreview()
        {
            _title.text = _previewTitle;
            _quantity.text = "0";
            _button.SetEnabled(true);
        }

        private void OnActivated()
        {
            Activated?.Invoke();
        }
    }
}
