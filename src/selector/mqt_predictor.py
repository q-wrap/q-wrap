import sys

# mqt.predictor imported in MqtPredictor.set_model_path() to set the model path dynamically
import mqt.bench
from qiskit import QuantumCircuit
import qiskit.qasm3

from selector import Selector
import util


class MqtPredictor(Selector):
    @classmethod
    def set_model_path(cls, model_path: str):
        sys.path.insert(0, model_path)
        cls.model = __import__("mqt.predictor", fromlist=["predictor"])

    @classmethod
    def select_device(cls, openqasm_circuit: str):
        if not hasattr(cls, "model"):
            raise ValueError("Model path not set. Call set_model_path() before using this method.")

        match util.get_openqasm_version(openqasm_circuit):
            case 2:
                loaded_circuit = qiskit.qasm2.loads(openqasm_circuit)
            case 3:
                loaded_circuit = qiskit.qasm3.loads(openqasm_circuit)
            case _:
                raise ValueError("Unsupported OpenQASM version")

        compiled_circuit, compilation_information, quantum_device = cls.model.qcompile(
            loaded_circuit, figure_of_merit="expected_fidelity"
        )

        return compiled_circuit, compilation_information, quantum_device
