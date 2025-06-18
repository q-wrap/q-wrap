import re


def get_openqasm_version(openqasm_circuit: str) -> int:
    version_pattern = r"^(?:\s|//.*\n)*OPENQASM\s+(\d+(?:\.\d+)?)\s*;"

    if match := re.match(version_pattern, openqasm_circuit):
        version = match.group(1)
        if version.startswith("2."):
            return 2
        elif version.startswith("3"):
            return 3
        else:
            raise ValueError(f"Unsupported OpenQASM version: {version}")
    else:
        return 3  # no version is specified, assume OpenQASM 3
