import subprocess
import unittest
from unittest.mock import patch

from script.cli import main


class CliExitTests(unittest.TestCase):
    def test_selftest_exit_code_is_preserved(self):
        for code in (0, 7):
            with self.subTest(code=code), patch('script.cli.run_smoke_test', return_value=code):
                self.assertEqual(main(['test', '--no-interactive']), code)

    def test_selftest_command_failure_is_preserved(self):
        with patch('script.cli.run_smoke_test', side_effect=subprocess.CalledProcessError(2, ['docker'])):
            self.assertEqual(main(['test', '--no-interactive']), 2)
