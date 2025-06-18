TRAINED_MODEL_LOCATION = r"..\..\training_env\mqt-predictor\src"

import sys

sys.path.insert(0, TRAINED_MODEL_LOCATION)

import mqt.predictor
import mqt.bench
from qiskit import QuantumCircuit
import qiskit.qasm3

from selector import Selector
import util


class MqtPredictor(Selector):
    def select_device(self, openqasm_circuit: str):
        match util.get_openqasm_version(openqasm_circuit):
            case 2:
                loaded_circuit = qiskit.qasm2.loads(openqasm_circuit)
            case 3:
                loaded_circuit = qiskit.qasm3.loads(openqasm_circuit)
            case _:
                raise ValueError("Unsupported OpenQASM version")

        compiled_circuit, compilation_information, quantum_device = mqt.predictor.qcompile(
            loaded_circuit, figure_of_merit="expected_fidelity"
        )

        return compiled_circuit, compilation_information, quantum_device
