#nullable enable
using UnityEngine;
using UnityEngine.UIElements;

namespace Workflow.Examples.UI
{
    // Static authoring preview by default. An optional view-owned clock drives Phase.
    [UxmlElement]
    public partial class WaveLabel : Label
    {
        private float _phase;
        private float _amplitude = 2f;

        public WaveLabel()
        {
            AddToClassList("game-wave-label");
            text = "Ready";
            PostProcessTextVertices += Deform;
        }

        [UxmlAttribute]
        public float Phase
        {
            get => _phase;
            set
            {
                float next = float.IsNaN(value) || float.IsInfinity(value) ? 0f : value;
                if (_phase == next)
                {
                    return;
                }
                _phase = next;
                MarkDirtyRepaint();
            }
        }

        [UxmlAttribute]
        public float Amplitude
        {
            get => _amplitude;
            set
            {
                float next = float.IsNaN(value) || float.IsInfinity(value) ? 0f : Mathf.Clamp(value, 0f, 8f);
                if (_amplitude == next)
                {
                    return;
                }
                _amplitude = next;
                MarkDirtyRepaint();
            }
        }

        private void Deform(TextElement.GlyphsEnumerable glyphs)
        {
            if (_amplitude == 0f)
            {
                return;
            }
            foreach (TextElement.Glyph glyph in glyphs)
            {
                var vertices = glyph.vertices;
                if (vertices.Length == 0)
                {
                    continue;
                }
                // Spatial phase keeps each quad rigid; no character-index/UTF-16 assumptions.
                float offset = Mathf.Sin(_phase + vertices[0].position.x * 0.08f) * _amplitude;
                for (int i = 0; i < vertices.Length; i++)
                {
                    Vertex vertex = vertices[i];
                    vertex.position.y += offset;
                    vertices[i] = vertex;
                }
            }
        }
    }
}
