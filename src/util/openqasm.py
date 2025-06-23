import re

from qiskit import qasm2, qasm3, QuantumCircuit

DEFAULT_VERSION = 2


def parse_openqasm_version_or_default(openqasm_circuit: str) -> int:
    version_pattern = r"^(?:\s|//.*\n)*OPENQASM\s+(\d+(?:\.\d+)?)\s*;"

    if match := re.match(version_pattern, openqasm_circuit):
        version = match.group(1)
        if version.startswith("2"):  # version 2 without minor version number tolerated, but specification requires 2.x
            return 2
        elif version.startswith("3"):
            return 3
        else:
            raise ValueError(f"Unsupported OpenQASM version: {version}")
    else:
        return DEFAULT_VERSION


def load_openqasm_circuit(openqasm_circuit: str, openqasm_version: int) -> QuantumCircuit:
    match openqasm_version:
        case 2:
            loaded_circuit = qasm2.loads(openqasm_circuit, custom_instructions=qasm2.LEGACY_CUSTOM_INSTRUCTIONS)
        case 3:
            loaded_circuit = qasm3.loads(openqasm_circuit)
        case _:
            raise ValueError("OpenQASM version must be 2 or 3.")

    return loaded_circuit
