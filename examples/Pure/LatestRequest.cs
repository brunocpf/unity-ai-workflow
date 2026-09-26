#nullable enable
using System;

namespace Workflow.Examples
{
    // Owner-thread-only. Complements cancellation; it does not stop underlying work.
    public sealed class LatestRequest : IDisposable
    {
        private long _version;
        private bool _disposed;

        public Ticket Begin()
        {
            if (_disposed)
            {
                throw new ObjectDisposedException(nameof(LatestRequest));
            }

            return new Ticket(this, checked(++_version));
        }

        public void Dispose()
        {
            _disposed = true;
        }

        public readonly struct Ticket
        {
            private readonly LatestRequest? _owner;
            private readonly long _version;

            internal Ticket(LatestRequest owner, long version)
            {
                _owner = owner;
                _version = version;
            }

            public bool IsCurrent => _owner != null && !_owner._disposed &&
                                     _owner._version == _version;
        }
    }
}
