#nullable enable
using System;
using UnityEngine.UIElements;

namespace Workflow.Examples.UI
{
    public sealed class UiFactory
    {
        private readonly UiLibrary _library;

        public UiFactory(UiLibrary library)
        {
            _library = library ?? throw new ArgumentNullException(nameof(library));
        }

        public T Create<T>() where T : VisualElement, new()
        {
            _library.EnsureAlive();
            using var scope = UiTemplates.Enter(_library);
            return new T();
        }

        public TemplateContainer Clone(string id)
        {
            _library.EnsureAlive();
            using var scope = UiTemplates.Enter(_library);
            return UiTemplates.GetRequired(id).CloneTree();
        }
    }
}
