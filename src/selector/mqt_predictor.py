import sys

# mqt.predictor imported in MqtPredictor.set_model_path() to set the model path dynamically
import mqt.bench.devices
from qiskit import QuantumCircuit

from selector import Selector


class MqtPredictor(Selector):
    @classmethod
    def set_model_path(cls, model_path: str):
        sys.path.insert(0, model_path)
        cls.model = __import__("mqt.predictor", fromlist=["predictor"])

    @classmethod
    def select_device(cls, circuit: QuantumCircuit) -> tuple[QuantumCircuit, list[str], mqt.bench.devices.Device]:
        if not hasattr(cls, "model"):
            raise ValueError("Model path not set. Call set_model_path() before using this method.")

        compiled_circuit, compilation_information, quantum_device = cls.model.qcompile(
            circuit, figure_of_merit="expected_fidelity"
        )

        return compiled_circuit, compilation_information, quantum_device
