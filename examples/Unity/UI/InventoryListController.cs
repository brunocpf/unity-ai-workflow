#nullable enable
using System;
using System.Collections.Generic;
using UnityEngine.UIElements;
using Workflow.Examples.Presentation;

namespace Workflow.Examples.UI
{
    // Borrows item ViewModels; their screen/module owner must outlive this controller.
    // Takes exclusive ownership of this ListView's item source and lifecycle callbacks.
    public sealed class InventoryListController : IDisposable
    {
        private readonly ListView _list;
        private readonly UiFactory _factory;
        private readonly Dictionary<VisualElement, InventoryBinding> _bindings =
            new Dictionary<VisualElement, InventoryBinding>();
        private bool _disposed;

        public InventoryListController(ListView list, UiFactory factory, List<InventorySlotViewModel> items)
        {
            _list = list ?? throw new ArgumentNullException(nameof(list));
            _factory = factory ?? throw new ArgumentNullException(nameof(factory));
            if (items == null)
            {
                throw new ArgumentNullException(nameof(items));
            }

            if (_list.itemsSource != null || _list.makeItem != null || _list.bindItem != null ||
                _list.unbindItem != null || _list.destroyItem != null)
            {
                throw new ArgumentException("Supply an unowned ListView.");
            }

            _list.makeItem = Make;
            _list.bindItem = Bind;
            _list.unbindItem = Unbind;
            _list.destroyItem = Destroy;
            try
            {
                _list.itemsSource = items;
                _list.Rebuild();
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

        private VisualElement Make() => _factory.Create<InventorySlot>();

        private void Bind(VisualElement element, int index)
        {
            Destroy(element); // Safe even when Unity rebinds without our expected unbind sequence.
            var binding = new InventoryBinding(
                (InventorySlotViewModel)_list.itemsSource[index],
                (InventorySlot)element);
            _bindings.Add(element, binding);
        }

        private void Unbind(VisualElement element, int index)
        {
            Destroy(element);
        }

        private void Destroy(VisualElement element)
        {
            if (!_bindings.TryGetValue(element, out var binding))
            {
                return;
            }

            _bindings.Remove(element);
            binding.Dispose();
        }

        public void Dispose()
        {
            if (_disposed)
            {
                return;
            }

            _disposed = true;
            // Detach delegates first so teardown cannot install fresh subscriptions.
            _list.makeItem = null;
            _list.bindItem = null;
            _list.unbindItem = null;
            _list.destroyItem = null;
            var errors = new List<Exception>();
            foreach (var binding in _bindings.Values)
            {
                try
                {
                    binding.Dispose();
                }
                catch (Exception error)
                {
                    errors.Add(error);
                }
            }

            _bindings.Clear();
            try
            {
                _list.itemsSource = null;
                _list.Rebuild();
            }
            catch (Exception error)
            {
                errors.Add(error);
            }
            if (errors.Count != 0)
            {
                throw new AggregateException(errors);
            }
        }
    }
}
