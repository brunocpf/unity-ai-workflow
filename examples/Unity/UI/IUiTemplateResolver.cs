#nullable enable
using UnityEngine.UIElements;

namespace Workflow.Examples.UI
{
    public interface IUiTemplateResolver
    {
        VisualTreeAsset GetRequired(string id);
    }
}
