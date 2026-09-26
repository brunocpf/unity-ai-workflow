#nullable enable
using System;
using System.Threading;

namespace Workflow.Examples
{
    // Instance-owned machinery; UiTemplates supplies the only static facade.
    public sealed class ScopedContext<T> where T : class
    {
        private readonly int _threadId = Thread.CurrentThread.ManagedThreadId;
        private object _generation = new object();
        private T? _current;
        private long _nextId;
        private long _topId;

        public object Generation
        {
            get
            {
                CheckThread();
                return _generation;
            }
        }

        public T? Current
        {
            get
            {
                CheckThread();
                return _current;
            }
        }

        public Scope Enter(T value)
        {
            CheckThread();
            if (value == null)
            {
                throw new ArgumentNullException(nameof(value));
            }

            long id = checked(++_nextId);
            var scope = new Scope(this, _generation, id, _topId, _current);
            _topId = id;
            _current = value;
            return scope;
        }

        public void Reset()
        {
            CheckThread();
            _current = null;
            _topId = 0;
            _generation = new object();
        }

        public void CheckThread()
        {
            if (Thread.CurrentThread.ManagedThreadId != _threadId)
            {
                throw new InvalidOperationException("Context accessed off its owner thread.");
            }
        }

        private void Exit(object generation, long id, long previousId, T? previous)
        {
            CheckThread();
            // Old scopes cannot resurrect a previous session's assets.
            if (!ReferenceEquals(generation, _generation))
            {
                return;
            }

            if (_topId != id)
            {
                throw new InvalidOperationException("Scope copied, disposed twice or out of order.");
            }

            _topId = previousId;
            _current = previous;
        }

        public ref struct Scope
        {
            private ScopedContext<T>? _owner;
            private readonly object _generation;
            private readonly long _id;
            private readonly long _previousId;
            private T? _previous;

            internal Scope(ScopedContext<T> owner, object generation, long id,
                long previousId, T? previous)
            {
                _owner = owner;
                _generation = generation;
                _id = id;
                _previousId = previousId;
                _previous = previous;
            }

            public void Dispose()
            {
                if (_owner == null)
                {
                    throw new InvalidOperationException("Scope already disposed.");
                }

                _owner.Exit(_generation, _id, _previousId, _previous);
                _owner = null;
                _previous = null;
            }
        }
    }
}
