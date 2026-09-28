"""Exercise real subprocess output retention and fail-closed runner behavior."""
import contextlib
import importlib.util
import io
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('verification_runner', ROOT / 'starter/openspec/tooling/ci.py')
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


class VerificationOutputTests(unittest.TestCase):
    def execute(self, script, quiet=True):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            log = root / 'full.log'
            output = io.StringIO()
            code = 0
            with contextlib.redirect_stdout(output):
                try:
                    runner.execute([sys.executable, '-u', '-c', script], root, log, 'fixture', quiet)
                except subprocess.CalledProcessError as error:
                    code = error.returncode
            return code, output.getvalue(), log.read_bytes()

    def test_quiet_success_keeps_full_stdout_and_stderr(self):
        code, summary, log = self.execute('import sys; print("line\\n" * 500); print("diagnostic", file=sys.stderr)')
        self.assertEqual(0, code)
        self.assertEqual(1, len(summary.splitlines()))
        self.assertIn('PASS fixture', summary)
        self.assertGreater(len(log.splitlines()), 500)
        self.assertIn(b'diagnostic', log)

    def test_quiet_failure_retains_code_and_bounded_actionable_tail(self):
        code, summary, log = self.execute('import sys; print("prefix\\n" * 500); print("X" * 20000); print("repair fixture", file=sys.stderr); sys.exit(9)')
        self.assertEqual(9, code)
        self.assertIn('repair fixture', summary)
        self.assertLessEqual(len(summary.splitlines()), 31)
        self.assertLess(len(summary), 8500)
        self.assertIn(b'X' * 20000, log)
        self.assertGreater(len(log.splitlines()), 500)

    def test_ascii_console_preserves_unicode_logs_in_both_modes(self):
        for quiet in (False, True):
            with self.subTest(quiet=quiet), tempfile.TemporaryDirectory() as folder:
                root = Path(folder)
                log = root / 'unicode.log'
                buffer = io.BytesIO()
                console = io.TextIOWrapper(buffer, encoding='ascii')
                with contextlib.redirect_stdout(console):
                    with self.assertRaises(subprocess.CalledProcessError) as error:
                        runner.execute([sys.executable, '-c', 'import os; os.write(1, bytes([226,156,147,10])); raise SystemExit(9)'],
                                       root, log, 'unicode', quiet)
                console.flush()
                self.assertEqual(9, error.exception.returncode)
                self.assertEqual(bytes([226,156,147,10]), log.read_bytes())
                self.assertIn(b'\\u2713', buffer.getvalue())
                console.detach()

    def test_verbose_output_is_not_truncated(self):
        code, output, log = self.execute('print("line\\n" * 100)', False)
        self.assertEqual(0, code)
        self.assertIn(log.decode(), output)

    def test_cli_preserves_child_exit_code(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            tooling = root / 'tooling/specs'
            tooling.mkdir(parents=True)
            (tooling / 'ci.py').write_bytes(Path(runner.__file__).read_bytes())
            (tooling / 'run.py').write_text('import sys; print("structural failure", file=sys.stderr); sys.exit(9)', encoding='utf-8')
            result = subprocess.run([sys.executable, str(tooling / 'ci.py'), '--change', 'fixture', '--quiet'],
                                    cwd=root, capture_output=True, text=True)
            self.assertEqual(9, result.returncode)
            self.assertIn('structural failure', result.stdout)
            logs = list((root / 'artifacts/spec-validation').glob('run-*/*.log'))
            self.assertEqual(1, len(logs))  # Later gates must not run after failure.
            self.assertIn('structural failure', logs[0].read_text())

    def test_quiet_and_verbose_run_same_gates_and_require_delivery(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            change = root / 'openspec/changes/active'
            change.mkdir(parents=True)
            (change / '.openspec.yaml').write_text('schema: unity-game')
            commands = []
            with patch.object(runner, 'execute', side_effect=lambda cmd, *args: commands.append(cmd)):
                with contextlib.redirect_stdout(io.StringIO()):
                    runner.verify(root, 'active', False)
                    count = len(commands)
                    runner.verify(root, 'active', True)
            self.assertEqual(commands[:count], commands[count:])
            self.assertEqual(3, count)
            self.assertEqual('--accept', commands[-1][-1])
            self.assertEqual(2, len(list((root / 'artifacts/spec-validation').iterdir())))

    def test_empty_active_list_still_checks_selected_delivery(self):
        with tempfile.TemporaryDirectory() as folder:
            calls = []
            with patch.object(runner, 'execute', side_effect=lambda cmd, *args: calls.append(cmd)):
                with contextlib.redirect_stdout(io.StringIO()):
                    runner.verify(Path(folder), 'archive/2026-09-27-fixture', True)
            self.assertEqual(2, len(calls))
            self.assertIn('archive/2026-09-27-fixture', calls[-1])
            self.assertEqual('--accept', calls[-1][-1])
