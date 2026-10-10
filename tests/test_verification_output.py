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
spec = importlib.util.spec_from_file_location('verification_runner', ROOT / 'starter/verification/run.py')
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

    def cli(self, root, *arguments):
        return subprocess.run([sys.executable, runner.__file__, '--root', str(root), *arguments],
                              capture_output=True, text=True)

    def test_cli_failure_code_and_full_logs(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            result = self.cli(root, '--quiet', '--', sys.executable, '-c', 'print("fault"); raise SystemExit(9)')
            self.assertEqual(9, result.returncode)
            self.assertIn('fault', result.stdout)
            self.assertEqual('fault', next((root / 'artifacts/verification').glob('run-*/*.log')).read_text().strip())

    def test_success_modes_use_fresh_logs_and_project_cwd(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for options in [[], ['--quiet']]:
                result = self.cli(root, *options, '--', sys.executable, '-c', 'from pathlib import Path; print(Path.cwd())')
                self.assertEqual(0, result.returncode, result.stderr)
            logs = list((root / 'artifacts/verification').glob('run-*/*.log'))
            self.assertEqual(2, len(logs))
            self.assertTrue(all(Path(p.read_text().strip()) == root.resolve() for p in logs))

    def test_timeout_missing_executable_and_empty_command_fail(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            result = self.cli(root, '--timeout', '0.2', '--quiet', '--', sys.executable, '-c', 'import time; time.sleep(20)')
            self.assertEqual(124, result.returncode)
            self.assertEqual(1, self.cli(root, '--', str(root / 'missing')).returncode)
            self.assertEqual(2, self.cli(root).returncode)
            for timeout in ['0', '-1', 'nan', 'inf']:
                self.assertEqual(2, self.cli(root, '--timeout', timeout, '--', sys.executable).returncode)
