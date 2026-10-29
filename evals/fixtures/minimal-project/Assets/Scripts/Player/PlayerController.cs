using UnityEngine;
using UnityEngine.InputSystem;

namespace Skyforge.Player
{
    [RequireComponent(typeof(Rigidbody))]
    public sealed class PlayerController : MonoBehaviour
    {
        [SerializeField] private float _moveSpeed = 5f;
        [SerializeField] private int _maxHealth = 100;

        private Rigidbody _body;
        private Vector2 _move;

        public int MaxHealth => _maxHealth;
        public int Health { get; private set; }
        public int Level { get; set; } = 1;
        public int Gold { get; set; }

        private void Awake()
        {
            _body = GetComponent<Rigidbody>();
            Health = _maxHealth;
        }

        private void Update()
        {
            var keyboard = Keyboard.current;
            if (keyboard == null)
            {
                _move = Vector2.zero;
                return;
            }

            _move = new Vector2(
                (keyboard.dKey.isPressed ? 1f : 0f) - (keyboard.aKey.isPressed ? 1f : 0f),
                (keyboard.wKey.isPressed ? 1f : 0f) - (keyboard.sKey.isPressed ? 1f : 0f));
        }

        private void FixedUpdate()
        {
            var velocity = new Vector3(_move.x, 0f, _move.y) * _moveSpeed;
            _body.linearVelocity = new Vector3(velocity.x, _body.linearVelocity.y, velocity.z);
        }

        public void TakeDamage(int amount)
        {
            Health = Mathf.Max(0, Health - amount);
        }
    }
}
