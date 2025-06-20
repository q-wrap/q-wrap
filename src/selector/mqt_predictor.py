import sys

# mqt.predictor imported in MqtPredictor.set_model_path() to set the model path dynamically
import mqt.bench.devices
from qiskit import qasm2, qasm3, QuantumCircuit

from selector import Selector
import util


class MqtPredictor(Selector):
    @classmethod
    def set_model_path(cls, model_path: str):
        sys.path.insert(0, model_path)
        cls.model = __import__("mqt.predictor", fromlist=["predictor"])

    @classmethod
    def select_device(cls, openqasm_circuit: str, openqasm_version: int) \
            -> tuple[QuantumCircuit, list[str], mqt.bench.devices.Device]:
        if not hasattr(cls, "model"):
            raise ValueError("Model path not set. Call set_model_path() before using this method.")

        match openqasm_version:
            case 2:
                loaded_circuit = qasm2.loads(openqasm_circuit)
            case 3:
                loaded_circuit = qasm3.loads(openqasm_circuit)
            case _:
                raise ValueError("OpenQASM version must be 2 or 3.")

        compiled_circuit, compilation_information, quantum_device = cls.model.qcompile(
            loaded_circuit, figure_of_merit="expected_fidelity"
        )

        return compiled_circuit, compilation_information, quantum_device
