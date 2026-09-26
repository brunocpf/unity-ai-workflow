#nullable enable
using System;

namespace Workflow.Examples.Combat
{
    public sealed class EnemyConfig
    {
        public EnemyConfig(string id, int maxHealth, float moveSpeed)
        {
            if (string.IsNullOrWhiteSpace(id))
            {
                throw new ArgumentException("A stable enemy ID is required.", nameof(id));
            }
            if (maxHealth <= 0)
            {
                throw new ArgumentOutOfRangeException(nameof(maxHealth));
            }
            if (float.IsNaN(moveSpeed) || float.IsInfinity(moveSpeed) || moveSpeed < 0f)
            {
                throw new ArgumentOutOfRangeException(nameof(moveSpeed));
            }
            Id = id;
            MaxHealth = maxHealth;
            MoveSpeed = moveSpeed;
        }

        public string Id
        {
            get;
        }
        public int MaxHealth
        {
            get;
        }
        public float MoveSpeed
        {
            get;
        }
    }
}
