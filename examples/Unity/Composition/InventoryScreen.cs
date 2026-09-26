#nullable enable
using System;
using System.Collections.Generic;
using UnityEngine.UIElements;
using Workflow.Examples.Application;
using Workflow.Examples.Presentation;
using Workflow.Examples.UI;

namespace Workflow.Examples.Composition
{
    // Owns one mounted view, ViewModel and binding adapter. The UI subsystem owns the shared library.
    public sealed class InventoryScreen : IDisposable
    {
        private readonly InventorySlot _view;
        private InventoryBinding? _binding;
        private InventorySlotViewModel? _viewModel;
        private bool _disposed;

        public InventoryScreen(VisualElement parent, UiFactory factory, IInventory inventory)
        {
            if (parent == null)
            {
                throw new ArgumentNullException(nameof(parent));
            }

            _view = factory.Create<InventorySlot>();
            try
            {
                _viewModel = new InventorySlotViewModel(inventory);
                _binding = new InventoryBinding(_viewModel, _view);
                parent.Add(_view);
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

        public void Dispose()
        {
            if (_disposed)
            {
                return;
            }

            _disposed = true;
            List<Exception>? errors = null;
            try
            {
                _binding?.Dispose();
            }
            catch (Exception error)
            {
                (errors ??= new List<Exception>()).Add(error);
            }
            _binding = null;
            try
            {
                _viewModel?.Dispose();
            }
            catch (Exception error)
            {
                (errors ??= new List<Exception>()).Add(error);
            }
            _viewModel = null;
            try
            {
                _view.RemoveFromHierarchy();
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
