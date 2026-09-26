#nullable enable
using System;
using UnityEngine;
using UnityEngine.UIElements;

namespace Workflow.Examples.UI
{
    // One clock per independently visible region; all methods run on the Unity thread.
    public sealed class VisibleMotionClock : IDisposable
    {
        private readonly VisualElement _view;
        private readonly IVisualElementScheduledItem _schedule;
        private Action<float>? _renderPhase;
        private Action? _resetVisuals;
        private double _startedAt;
        private bool _visible;
        private bool _reducedMotion;
        private bool _disposed;

        public VisibleMotionClock(
            VisualElement view,
            Action<float> renderPhase,
            Action resetVisuals,
            long intervalMilliseconds = 33)
        {
            _view = view ?? throw new ArgumentNullException(nameof(view));
            _renderPhase = renderPhase ?? throw new ArgumentNullException(nameof(renderPhase));
            _resetVisuals = resetVisuals ?? throw new ArgumentNullException(nameof(resetVisuals));
            if (intervalMilliseconds <= 0)
            {
                throw new ArgumentOutOfRangeException(nameof(intervalMilliseconds));
            }

            _schedule = view.schedule.Execute(Tick).Every(intervalMilliseconds);
            _schedule.Pause();
            _view.RegisterCallback<AttachToPanelEvent>(OnAttach);
            _view.RegisterCallback<DetachFromPanelEvent>(OnDetach);
        }

        public bool IsRunning { get; private set; }

        public void SetPresentation(bool visible, bool reducedMotion)
        {
            if (_disposed)
            {
                throw new ObjectDisposedException(nameof(VisibleMotionClock));
            }

            _visible = visible;
            _reducedMotion = reducedMotion;
            Reconcile();
        }

        public void Dispose()
        {
            if (_disposed)
            {
                return;
            }

            _disposed = true;
            try
            {
                StopAndReset();
            }
            finally
            {
                _view.UnregisterCallback<AttachToPanelEvent>(OnAttach);
                _view.UnregisterCallback<DetachFromPanelEvent>(OnDetach);
                _renderPhase = null;
                _resetVisuals = null;
            }
        }

        private void OnAttach(AttachToPanelEvent evt)
        {
            if (evt.target == _view)
            {
                Reconcile();
            }
        }

        private void OnDetach(DetachFromPanelEvent evt)
        {
            if (evt.target == _view)
            {
                StopAndReset();
            }
        }

        private void Reconcile()
        {
            if (_disposed || !_visible || _reducedMotion || _view.panel == null)
            {
                StopAndReset();
                return;
            }

            if (IsRunning)
            {
                return;
            }

            _startedAt = Time.unscaledTimeAsDouble;
            IsRunning = true;
            _schedule.Resume();
        }

        private void Tick()
        {
            if (!IsRunning)
            {
                return;
            }

            try
            {
                _renderPhase!((float)(Time.unscaledTimeAsDouble - _startedAt));
            }
            catch
            {
                // Stop repeated failures without hiding the original callback exception.
                IsRunning = false;
                _schedule.Pause();
                throw;
            }
        }

        private void StopAndReset()
        {
            IsRunning = false;
            _schedule.Pause();
            _resetVisuals?.Invoke();
        }
    }
}
