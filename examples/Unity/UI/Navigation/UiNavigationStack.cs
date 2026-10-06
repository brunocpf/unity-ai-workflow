#nullable enable
using System;
using System.Collections.Generic;
using UnityEngine.UIElements;

namespace Workflow.Examples.UI.Navigation
{
    // Main-thread, single-panel menu region. Native UITK owns Move and Submit.
    // Views are dedicated full-region layers; the host must not contain unrelated UI.
    public sealed class UiNavigationStack : IDisposable
    {
        private readonly VisualElement _host;
        private readonly VisualElement _eventRoot;
        private readonly bool _hostWasFocusable;
        private readonly int _hostTabIndex;
        private readonly Action<bool> _setGameplayBlocked;
        private readonly Action _onEmptyCancel;
        private readonly List<UiStackEntry> _entries = new List<UiStackEntry>();
        private IVisualElementScheduledItem? _pendingFocus;
        private bool _disposed;
        private bool _changing;
        private int _generation;

        public UiNavigationStack(
            VisualElement host,
            Action<bool> setGameplayBlocked,
            Action onEmptyCancel)
        {
            _host = host ?? throw new ArgumentNullException(nameof(host));
            _setGameplayBlocked = setGameplayBlocked
                ?? throw new ArgumentNullException(nameof(setGameplayBlocked));
            _onEmptyCancel = onEmptyCancel ?? throw new ArgumentNullException(nameof(onEmptyCancel));
            _eventRoot = host.panel?.visualTree
                ?? throw new ArgumentException("Attach the host before creating navigation.", nameof(host));
            _eventRoot.RegisterCallback<NavigationCancelEvent>(OnCancel);
            _hostWasFocusable = host.focusable;
            _hostTabIndex = host.tabIndex;
            host.focusable = true;
            host.tabIndex = -1;
            host.Focus();
        }

        public int Count => _entries.Count;
        public UiStackEntry? Top => Count == 0 ? null : _entries[Count - 1];

        // Ownership transfers when inserted. Rejected entries remain caller-owned.
        // Teardown/callback failures after insertion do not roll back a committed change.
        public void PushScreen(UiStackEntry entry) => Push(entry, false);
        public void PushModal(UiStackEntry entry) => Push(entry, true);

        public void ReplaceScreen(UiStackEntry entry)
        {
            Validate(entry);
            if (Top?.IsModal == true)
            {
                throw new InvalidOperationException("Close modals before replacing a screen.");
            }
            Change(() =>
            {
                UiStackEntry? old = Top;
                _host.Add(entry.View);
                entry.IsModal = false;
                if (old != null)
                {
                    _entries.RemoveAt(Count - 1);
                }
                _entries.Add(entry);
                try
                {
                    old?.Dispose();
                }
                finally
                {
                    Refresh();
                }
            });
        }

        public bool Pop()
        {
            ThrowIfClosed();
            if (Count == 0)
            {
                return false;
            }
            Change(() =>
            {
                UiStackEntry old = _entries[Count - 1];
                _entries.RemoveAt(Count - 1);
                try
                {
                    old.Dispose();
                }
                finally
                {
                    Refresh();
                }
            });
            return true;
        }

        private void Push(UiStackEntry entry, bool modal)
        {
            Validate(entry);
            if (!modal && Top?.IsModal == true)
            {
                throw new InvalidOperationException("Close modals before pushing a screen.");
            }
            Change(() =>
            {
                if (Top != null)
                {
                    Top.ReturnFocus = _host.focusController?.focusedElement as VisualElement;
                }
                _host.Add(entry.View);
                entry.IsModal = modal;
                _entries.Add(entry);
                Refresh();
            });
        }

        private void Refresh()
        {
            _pendingFocus?.Pause();
            _pendingFocus = null;
            int generation = ++_generation;
            // A modal leaves the screen below it visible, but disabled. Pushed screens hide it.
            bool visible = true;
            for (int i = Count - 1; i >= 0; i--)
            {
                UiStackEntry entry = _entries[i];
                entry.View.style.display = visible ? DisplayStyle.Flex : DisplayStyle.None;
                entry.View.SetEnabled(i == Count - 1);
                visible &= entry.IsModal;
            }
            _host.focusable = Count == 0;
            _setGameplayBlocked(Count != 0);
            UiStackEntry? top = Top;
            if (top == null)
            {
                _host.Focus();
                return;
            }
            // One post-layout handoff, not a per-frame focus enforcer or input debounce.
            _pendingFocus = _host.schedule.Execute(() =>
            {
                if (_disposed || generation != _generation || Top != top)
                {
                    return;
                }
                _pendingFocus = null;
                VisualElement? target = Eligible(top, top.ReturnFocus)
                    ? top.ReturnFocus : top.InitialFocus();
                if (!Eligible(top, target))
                {
                    throw new InvalidOperationException("Provide an attached, visible, enabled focus fallback.");
                }
                target!.Focus();
            });
        }

        private static bool Eligible(UiStackEntry entry, VisualElement? target)
        {
            if (target == null || target.panel == null || !target.canGrabFocus ||
                !(target == entry.View || entry.View.Contains(target)))
            {
                return false;
            }
            for (VisualElement? node = target; node != null; node = node.parent)
            {
                if (node.resolvedStyle.display == DisplayStyle.None ||
                    node.resolvedStyle.visibility != Visibility.Visible)
                {
                    return false;
                }
            }
            return true;
        }

        private void OnCancel(NavigationCancelEvent evt)
        {
            if (_disposed)
            {
                return;
            }
            // Bubble phase lets native controls consume Cancel first (e.g. an editable field).
            // Cancel is distinct from Move's post-dispatch focus behavior.
            evt.StopPropagation();
            if (Top == null)
            {
                _onEmptyCancel();
            }
            else if (Top.DismissOnCancel)
            {
                Pop();
            }
        }

        private void Validate(UiStackEntry entry)
        {
            ThrowIfClosed();
            if (entry == null)
            {
                throw new ArgumentNullException(nameof(entry));
            }
            if (entry.IsDisposed || entry.View.parent != null || _entries.Contains(entry))
            {
                throw new InvalidOperationException("Entry must be fresh and unmounted.");
            }
        }

        private void Change(Action operation)
        {
            ThrowIfClosed();
            if (_changing)
            {
                throw new InvalidOperationException("Reentrant navigation is not supported.");
            }
            _changing = true;
            try
            {
                operation();
            }
            finally
            {
                _changing = false;
            }
        }

        private void ThrowIfClosed()
        {
            if (_disposed)
            {
                throw new ObjectDisposedException(nameof(UiNavigationStack));
            }
        }

        public void Dispose()
        {
            if (_disposed)
            {
                return;
            }
            if (_changing)
            {
                throw new InvalidOperationException("Do not dispose during a navigation callback.");
            }
            _disposed = true;
            ++_generation;
            _pendingFocus?.Pause();
            _pendingFocus = null;
            _eventRoot.UnregisterCallback<NavigationCancelEvent>(OnCancel);
            _host.focusable = _hostWasFocusable;
            _host.tabIndex = _hostTabIndex;
            List<Exception>? errors = null;
            for (int i = Count - 1; i >= 0; i--)
            {
                try
                {
                    _entries[i].Dispose();
                }
                catch (Exception error)
                {
                    (errors ??= new List<Exception>()).Add(error);
                }
            }
            _entries.Clear();
            try
            {
                _setGameplayBlocked(false);
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
