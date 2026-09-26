#nullable enable
using System;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine.UIElements;
using Workflow.Examples.Application;
using Workflow.Examples.Presentation;
using Workflow.Examples.UI;

namespace Workflow.Examples.Editor
{
    // Authoring-only: deliberately exercises the Editor resolver, without runtime content.
    public sealed class InventoryPreviewWindow : EditorWindow
    {
        private DemoInventory? _inventory;
        private InventoryBinding? _binding;
        private InventorySlotViewModel? _viewModel;

        [MenuItem("Window/Workflow Examples/Inventory")]
        private static void Open()
        {
            GetWindow<InventoryPreviewWindow>("Inventory example");
        }

        public void CreateGUI()
        {
            Release();
            rootVisualElement.Clear();
            var view = new InventorySlot();
            _inventory = new DemoInventory();
            try
            {
                _viewModel = new InventorySlotViewModel(_inventory);
                _binding = new InventoryBinding(_viewModel, view);
                rootVisualElement.Add(view);
            }
            catch (Exception error)
            {
                try
                {
                    Release();
                }
                catch (Exception cleanup)
                {
                    throw new AggregateException(error, cleanup);
                }
                throw;
            }
        }

        private void OnDisable()
        {
            Release();
        }

        private void Release()
        {
            List<Exception>? errors = null;
            var binding = _binding;
            var viewModel = _viewModel;
            var inventory = _inventory;
            _binding = null;
            _viewModel = null;
            _inventory = null;
            try
            {
                binding?.Dispose();
            }
            catch (Exception error)
            {
                (errors ??= new List<Exception>()).Add(error);
            }
            try
            {
                viewModel?.Dispose();
            }
            catch (Exception error)
            {
                (errors ??= new List<Exception>()).Add(error);
            }
            try
            {
                inventory?.Dispose();
            }
            catch (Exception error)
            {
                (errors ??= new List<Exception>()).Add(error);
            }
            if (errors != null)
            {
                throw new AggregateException(errors);
            }
        }
    }
}
