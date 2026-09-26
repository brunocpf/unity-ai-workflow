#nullable enable
using System;
using UnityEngine;
using UnityEngine.UIElements;

namespace Workflow.Examples.UI
{
    // Runtime resets and the Editor bridge explicitly own these static lifetimes.
    [Unity.Scripting.LifecycleManagement.NoAutoStaticsCleanup]
    public static class UiTemplates
    {
        private static ScopedContext<IUiTemplateResolver>? _context;
        private static IUiTemplateResolver? _authoring;

        [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.SubsystemRegistration)]
        private static void OnRuntimeStart()
        {
            ResetRuntime();
        }

        // Also called by the Editor lifecycle bridge. Never loads assets here.
        public static void ResetRuntime()
        {
            if (_context == null)
            {
                _context = new ScopedContext<IUiTemplateResolver>();
            }
            else
            {
                _context.Reset();
            }
        }

        public static object Generation => Context.Generation;

        public static ScopedContext<IUiTemplateResolver>.Scope Enter(IUiTemplateResolver resolver)
        {
            return Context.Enter(resolver);
        }

        public static VisualTreeAsset GetRequired(string id)
        {
            var current = Context.Current;
            if (current != null)
            {
                return current.GetRequired(id);
            }

            if (_authoring != null)
            {
                return _authoring.GetRequired(id);
            }

            throw new InvalidOperationException("Construct runtime controls through UiFactory.");
        }

#if UNITY_EDITOR
        public static void InstallAuthoringResolver(IUiTemplateResolver? resolver)
        {
            Context.CheckThread();
            _authoring = resolver;
        }
#endif

        private static ScopedContext<IUiTemplateResolver> Context => _context ??
            throw new InvalidOperationException("UI lifecycle bridge has not initialized.");
    }
}
