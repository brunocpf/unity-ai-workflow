"""Run one engineering command with complete logs and optional concise output."""
import argparse
import math
import codecs
import os
import signal
import threading
from pathlib import Path
import subprocess
import sys
import tempfile


def emit(message, end='\n', flush=True, file=None):
    stream = file if file is not None else sys.stdout
    encoding = getattr(stream, 'encoding', None) or 'utf-8'
    # Legacy Windows consoles cannot render all UTF-8 diagnostics. Escape only
    # the presentation; logs retain the original subprocess bytes.
    safe = message.encode(encoding, errors='backslashreplace').decode(encoding)
    print(safe, end=end, flush=flush, file=stream)


def execute(command, root, log, label, quiet=False, timeout=None):
    """Retain complete combined output; quiet mode affects presentation only."""
    decoder = codecs.getincrementaldecoder('utf-8')(errors='replace')
    with log.open('wb') as output:
        try:
            process = subprocess.Popen(command, cwd=root, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                       start_new_session=os.name != "nt")
        except OSError as error:
            output.write(str(error).encode('utf-8'))
            emit(f'FAIL {label}: could not start; log: {log}', flush=True)
            raise
        expired = threading.Event()

        def expire():
            if process.poll() is None:
                expired.set()
                if os.name == 'nt':
                    subprocess.run(['taskkill', '/F', '/T', '/PID', str(process.pid)],
                                   capture_output=True, timeout=10)
                else:
                    try:
                        os.killpg(process.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass

        timer = threading.Timer(timeout, expire) if timeout is not None else None
        if timer:
            timer.daemon = True
            timer.start()
        with process:
            for chunk in iter(lambda: process.stdout.read1(8192), b''):
                output.write(chunk)
                output.flush()
                if not quiet:
                    emit(decoder.decode(chunk), end='', flush=True)
            if not quiet:
                emit(decoder.decode(b'', final=True), end='', flush=True)
            code = process.wait()
        if timer:
            timer.cancel()
        if expired.is_set():
            emit(f'FAIL {label}: timeout; log: {log}')
            raise subprocess.TimeoutExpired(command, timeout)
    emit(f'{"PASS" if code == 0 else "FAIL"} {label}: exit {code}; log: {log}', flush=True)
    if code:
        if quiet:
            # Bound bytes as well as lines: a compiler can emit a huge single line.
            with log.open('rb') as output:
                output.seek(0, 2)
                output.seek(max(0, output.tell() - 8192))
                tail = output.read().decode('utf-8', errors='replace').splitlines()[-30:]
            emit('\n'.join(tail), flush=True)
        raise subprocess.CalledProcessError(code, command)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path.cwd())
    parser.add_argument('--quiet', action='store_true')
    parser.add_argument('--timeout', type=float, default=600)
    parser.add_argument('command', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ['--'] else args.command
    if not command or not math.isfinite(args.timeout) or args.timeout <= 0:
        parser.error('Provide a command after -- and a positive finite timeout.')
    root = args.root.resolve()
    try:
        output = root / 'artifacts/verification'
        output.mkdir(parents=True, exist_ok=True)
        logs = Path(tempfile.mkdtemp(prefix='run-', dir=output))
        execute(command, root, logs / 'command.log', 'command', args.quiet, args.timeout)
    except subprocess.CalledProcessError as error:
        return error.returncode if error.returncode > 0 else 128 - error.returncode
    except subprocess.TimeoutExpired:
        return 124
    except OSError as error:
        emit(f'Verification infrastructure failure: {error}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
