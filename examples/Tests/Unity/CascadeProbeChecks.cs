#nullable enable
using System;
using System.Collections;
using UnityEngine.UIElements;

namespace Workflow.Examples.Tests
{
    // Yield from a UnityTest after the fixture is attached to a live, updating panel.
    public static class CascadeProbeChecks
    {
        public static IEnumerator Run(VisualElement fixture)
        {
            if (fixture.panel == null)
            {
                throw new InvalidOperationException("The cascade fixture needs a live panel.");
            }

            VisualElement root = fixture.Q("cascadeRoot")
                ?? throw new InvalidOperationException("Missing cascadeRoot.");
            Label heading = root.Q<Label>("heading")
                ?? throw new InvalidOperationException("Missing heading.");
            Label body = root.Q<Label>("body")
                ?? throw new InvalidOperationException("Missing body.");
            bool originalFault = root.ClassListContains("fixture-fault");
            try
            {
                root.RemoveFromClassList("fixture-fault");
                yield return null;
                yield return null;
                RequireExpected(heading, body);

                root.AddToClassList("fixture-fault");
                yield return null;
                yield return null;
                bool rejected = false;
                try
                {
                    RequireExpected(heading, body);
                }
                catch (InvalidOperationException)
                {
                    rejected = true;
                }

                if (!rejected)
                {
                    throw new InvalidOperationException("Cascade fault was not rejected.");
                }

                root.RemoveFromClassList("fixture-fault");
                yield return null;
                yield return null;
                RequireExpected(heading, body);
            }
            finally
            {
                root.EnableInClassList("fixture-fault", originalFault);
            }
        }

        private static void RequireExpected(Label heading, Label body)
        {
            Require(heading.resolvedStyle.marginTop, 12f, "heading margin-top");
            Require(heading.resolvedStyle.marginBottom, 8f, "heading margin-bottom");
            Require(heading.resolvedStyle.fontSize, 24f, "heading font-size");
            Require(body.resolvedStyle.marginTop, 4f, "body margin-top");
            Require(body.resolvedStyle.fontSize, 16f, "body font-size");
            if (body.resolvedStyle.whiteSpace != WhiteSpace.Normal)
            {
                throw new InvalidOperationException("Body must wrap.");
            }
        }

        private static void Require(float actual, float expected, string property)
        {
            if (float.IsNaN(actual) || Math.Abs(actual - expected) > 0.01f)
            {
                throw new InvalidOperationException($"{property}: expected {expected}, got {actual}.");
            }
        }
    }
}
