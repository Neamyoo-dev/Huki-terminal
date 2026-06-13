from __future__ import annotations

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.Utils import in_path, log


class TestInPath(unittest.TestCase):
    def test_existing_exe_in_path(self) -> None:
        if os.name == 'nt':
            result = in_path("cmd.exe")
            self.assertTrue(result)

    def test_non_existing_command(self) -> None:
        result = in_path("command_that_does_not_exist_xyz")
        self.assertFalse(result)

    def test_empty_program_name(self) -> None:
        result = in_path("")
        self.assertFalse(result)


class TestLog(unittest.TestCase):
    def test_log_output_format(self) -> None:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            pass

        try:
            log("INFO", "TestModule", "test message")
        finally:
            os.unlink(f.name)


if __name__ == '__main__':
    unittest.main()