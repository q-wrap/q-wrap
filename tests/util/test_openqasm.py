from unittest import TestCase

from src.util import get_openqasm_version


class TestOpenQasmVersion(TestCase):
    def test_valid_version(self):
        self.assertEqual(
            get_openqasm_version("OPENQASM 2.0;\ninclude \"qelib1.inc\";\nqreg q[1];\n"),
            2)

        self.assertEqual(
            get_openqasm_version("OPENQASM 3.0;\ninclude \"stdgates.inc\";\nqubit q;\n"),
            3)
        self.assertEqual(
            get_openqasm_version("OPENQASM 3;\ninclude \"stdgates.inc\";\nqubit q;\n"),
            3)

    def test_valid_version_with_comments(self):
        self.assertEqual(
            get_openqasm_version("  //   OPENQASM 2.0;\n  OPENQASM  3.0   ;\ninclude \"stdgates.inc\";\nqubit q;\n"),
            3)

    def test_no_version(self):
        self.assertEqual(
            get_openqasm_version("include \"stdgates.inc\";\nqubit q;\n"),
            3)

    def test_invalid_version(self):
        self.assertRaises(
            ValueError,
            lambda: get_openqasm_version("OPENQASM 2;\ninclude \"qelib1.inc\";\nqreg q[1];\n")
        )  # minor version number is mandatory in OpenQASM 2

    def test_unsupported_version(self):
        self.assertRaises(
            ValueError,
            lambda: get_openqasm_version("OPENQASM 1.0;\ninclude \"qelib1.inc\";\nqreg q[1];\n"))
        self.assertRaises(
            ValueError,
            lambda: get_openqasm_version("OPENQASM 4.0;\ninclude \"qelib1.inc\";\nqreg q[1];\n"))
