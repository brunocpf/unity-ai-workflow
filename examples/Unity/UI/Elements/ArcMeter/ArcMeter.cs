#nullable enable
using System;
using UnityEngine;
using UnityEngine.UIElements;

namespace Workflow.Examples.UI
{
    // Constructor-complete control; its private template supplies the drawing surface and USS.
    [UxmlElement]
    public partial class ArcMeter : VisualElement
    {
        public const string TemplateId = "controls/arc-meter";
        private readonly VisualElement _surface;
        private float _fill = 0.65f;
        private float _thickness = 6f;

        public ArcMeter()
        {
            AddToClassList("game-arc-meter");
            pickingMode = PickingMode.Ignore;
            UiTemplates.GetRequired(TemplateId).CloneTree(this);
            _surface = this.Q<VisualElement>("surface") ?? throw new InvalidOperationException("Missing surface.");
            _surface.generateVisualContent += Draw;
        }

        [UxmlAttribute]
        public float Fill
        {
            get => _fill;
            set
            {
                float next = float.IsNaN(value) || float.IsInfinity(value) ? 0f : Mathf.Clamp01(value);
                if (_fill == next)
                {
                    return;
                }
                _fill = next;
                _surface.MarkDirtyRepaint();
            }
        }

        [UxmlAttribute]
        public float Thickness
        {
            get => _thickness;
            set
            {
                float next = float.IsNaN(value) || float.IsInfinity(value) ? 6f : Mathf.Clamp(value, 1f, 32f);
                if (_thickness == next)
                {
                    return;
                }
                _thickness = next;
                _surface.MarkDirtyRepaint();
            }
        }

        private void Draw(MeshGenerationContext context)
        {
            Rect bounds = context.visualElement.contentRect;
            float radius = (Mathf.Min(bounds.width, bounds.height) - _thickness) * 0.5f;
            if (_fill <= 0f || radius <= 0f || float.IsNaN(radius) || float.IsInfinity(radius))
            {
                return;
            }

            Painter2D painter = context.painter2D;
            painter.strokeColor = resolvedStyle.color;
            painter.lineWidth = _thickness;
            painter.lineCap = LineCap.Round;
            painter.BeginPath();
            painter.Arc(bounds.center, radius, Angle.Degrees(-90f), Angle.Degrees(-90f + 360f * _fill));
            painter.Stroke();
        }
    }
}
