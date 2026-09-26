#nullable enable
using System;
using LitMotion;
using UnityEngine;
using UnityEngine.UIElements;
using Workflow.Examples.UI;

namespace Workflow.Examples.UI.Motion
{
    // One owner per ArcMeter. Create/dispose it with the screen or recycled-row binding.
    public sealed class ArcMeterMotion : IDisposable
    {
        private readonly ArcMeter _view;
        private MotionHandle _motion;
        private float _target;
        private bool _hasTarget;
        private bool _visible;
        private bool _reducedMotion;
        private bool _disposed;

        public ArcMeterMotion(ArcMeter view)
        {
            _view = view ?? throw new ArgumentNullException(nameof(view));
            _target = view.Fill;
            _view.RegisterCallback<DetachFromPanelEvent>(OnDetach);
        }

        public void SetPresentation(bool visible, bool reducedMotion)
        {
            if (_disposed)
            {
                throw new ObjectDisposedException(nameof(ArcMeterMotion));
            }
            _visible = visible;
            _reducedMotion = reducedMotion;
            if (!visible || reducedMotion)
            {
                Cancel();
                _view.Fill = _target;
            }
        }

        public void SetTarget(float value) => ApplyTarget(value, false);

        public void SnapTo(float value) => ApplyTarget(value, true);

        public void Dispose()
        {
            if (_disposed)
            {
                return;
            }
            _disposed = true;
            Cancel();
            _view.UnregisterCallback<DetachFromPanelEvent>(OnDetach);
        }

        private void ApplyTarget(float value, bool immediate)
        {
            if (_disposed)
            {
                throw new ObjectDisposedException(nameof(ArcMeterMotion));
            }
            float next = float.IsNaN(value) || float.IsInfinity(value) ? 0f : Mathf.Clamp01(value);
            bool snap = !_hasTarget || immediate || !_visible || _reducedMotion || _view.panel == null;
            if (_hasTarget && next == _target && !snap)
            {
                return;
            }
            _hasTarget = true;
            _target = next;
            Cancel();
            if (snap || _view.Fill == next)
            {
                _view.Fill = next;
                return;
            }
            _motion = LMotion.Create(_view.Fill, next, 0.22f)
                .WithEase(Ease.OutQuad)
                .WithScheduler(MotionScheduler.UpdateIgnoreTimeScale)
                .Bind(_view, static (value, view) => view.Fill = value);
        }

        private void OnDetach(DetachFromPanelEvent evt)
        {
            if (evt.target == _view)
            {
                Cancel();
                _view.Fill = _target;
            }
        }

        private void Cancel()
        {
            if (_motion.IsActive())
            {
                _motion.Cancel();
            }
            _motion = default;
        }
    }
}
