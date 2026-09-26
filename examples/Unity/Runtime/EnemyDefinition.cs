#nullable enable
using System;
using UnityEngine;
using Workflow.Examples.Combat;

namespace Workflow.Examples.Authoring
{
    [CreateAssetMenu(menuName = "Workflow/Combat/Enemy Definition")]
    public sealed class EnemyDefinition : ScriptableObject
    {
        [SerializeField, Tooltip("Stable content ID. Keep it when renaming the asset; catalog validation rejects duplicates.")]
        private string _id = "enemy.scout";

        [SerializeField, Min(1)]
        private int _maxHealth = 20;

        [SerializeField, Min(0f), Tooltip("World units per simulation second.")]
        private float _moveSpeed = 3f;

        [SerializeField, Tooltip("Authored prefab asset; validate its required view components in the project validator.")]
        private GameObject? _prefab = null;

        public GameObject Prefab => _prefab != null ? _prefab :
            throw new InvalidOperationException($"Enemy definition '{name}' ({_id}) requires a prefab.");

        // Call from authoring/build validation and session startup, not per frame or spawn.
        // The Unity-side factory retains Prefab; only this value object crosses into Core.
        public EnemyConfig Compile()
        {
            _ = Prefab;
            try
            {
                return new EnemyConfig(_id, _maxHealth, _moveSpeed);
            }
            catch (ArgumentException error)
            {
                throw new InvalidOperationException($"Enemy definition '{name}' ({_id}): {error.Message}", error);
            }
        }
    }
}
