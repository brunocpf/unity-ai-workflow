#nullable enable
using System;
using System.Collections;
using UnityEngine;
using UnityEngine.UIElements;
using Workflow.Examples.UI;

namespace Workflow.Examples.Tests
{
    // The caller owns the live panel. No private-field reflection or global time changes.
    public static class MotionClockChecks
    {
        public static IEnumerator Run(VisualElement panelRoot)
        {
            if (panelRoot.panel == null)
            {
                throw new InvalidOperationException("Motion checks need a live panel.");
            }

            var region = new VisualElement();
            int ticks = 0;
            float phase = -1f;
            using var clock = new VisibleMotionClock(
                region,
                value =>
                {
                    ticks++;
                    phase = value;
                },
                () => phase = 0f,
                intervalMilliseconds: 1);
            panelRoot.Add(region);
            try
            {
                yield return RequireQuiet(clock, () => ticks);
                clock.SetPresentation(true, false);
                yield return RequireAdvancing(() => ticks);

                clock.SetPresentation(false, false);
                region.style.display = DisplayStyle.None;
                yield return RequireQuiet(clock, () => ticks);
                RequireReset(phase);
                region.style.display = DisplayStyle.Flex;
                clock.SetPresentation(true, false);
                yield return RequireAdvancing(() => ticks);

                clock.SetPresentation(true, true);
                yield return RequireQuiet(clock, () => ticks);
                RequireReset(phase);
                clock.SetPresentation(true, false);
                clock.SetPresentation(true, false);
                yield return RequireAdvancing(() => ticks);

                region.RemoveFromHierarchy();
                yield return RequireQuiet(clock, () => ticks);
                RequireReset(phase);
                panelRoot.Add(region);
                yield return RequireAdvancing(() => ticks);
                clock.Dispose();
                clock.Dispose();
                yield return RequireQuiet(clock, () => ticks);
                RequireReset(phase);
            }
            finally
            {
                region.RemoveFromHierarchy();
            }
        }

        private static IEnumerator RequireAdvancing(Func<int> ticks)
        {
            int initial = ticks();
            double deadline = Time.realtimeSinceStartupAsDouble + 2;
            while (ticks() == initial && Time.realtimeSinceStartupAsDouble < deadline)
            {
                yield return null;
            }

            if (ticks() == initial)
            {
                throw new InvalidOperationException("Visible motion did not advance within two seconds.");
            }
        }

        private static IEnumerator RequireQuiet(VisibleMotionClock clock, Func<int> ticks)
        {
            int initial = ticks();
            for (int frame = 0; frame < 8; frame++)
            {
                yield return null;
            }

            if (clock.IsRunning || ticks() != initial)
            {
                throw new InvalidOperationException("Inactive motion continued invoking callbacks.");
            }
        }

        private static void RequireReset(float phase)
        {
            if (phase != 0f)
            {
                throw new InvalidOperationException("Motion did not restore its static phase.");
            }
        }
    }
}
