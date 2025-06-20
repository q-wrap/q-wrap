from unittest import TestCase

from src.util import parse_openqasm_version_or_default


class TestOpenQasmVersion(TestCase):
    def test_valid_version(self):
        self.assertEqual(
            parse_openqasm_version_or_default("OPENQASM 2.0;\ninclude \"qelib1.inc\";\nqreg q[1];\n"),
            2)
        self.assertEqual(
            parse_openqasm_version_or_default("OPENQASM 2;\ninclude \"qelib1.inc\";\nqreg q[1];\n"),
            2
        )

        self.assertEqual(
            parse_openqasm_version_or_default("OPENQASM 3.0;\ninclude \"stdgates.inc\";\nqubit q;\n"),
            3)
        self.assertEqual(
            parse_openqasm_version_or_default("OPENQASM 3;\ninclude \"stdgates.inc\";\nqubit q;\n"),
            3)

        self.assertEqual(
            parse_openqasm_version_or_default(
                "  //   OPENQASM 2.0;\n  OPENQASM  3.0   ;\ninclude \"stdgates.inc\";\nqubit q;\n"),
            3)

    def test_default_version(self):
        self.assertEqual(
            parse_openqasm_version_or_default("include \"stdgates.inc\";\nqubit q;\n"),
            2)

    def test_invalid_version(self):
        self.assertRaises(
            ValueError,
            lambda: parse_openqasm_version_or_default("OPENQASM 1.0;\ninclude \"qelib1.inc\";\nqreg q[1];\n"))
        self.assertRaises(
            ValueError,
            lambda: parse_openqasm_version_or_default("OPENQASM 4.0;\ninclude \"qelib1.inc\";\nqreg q[1];\n"))
