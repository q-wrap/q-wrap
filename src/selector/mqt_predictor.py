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
    def _check_for_model(cls):
        if not hasattr(cls, "model"):
            raise ValueError("Model path not set. Call set_model_path() before using this method.")

    @classmethod
    def select_device(cls, circuit: QuantumCircuit) -> tuple[QuantumCircuit, list[str], mqt.bench.devices.Device]:
        cls._check_for_model()

        compiled_circuit, compilation_information, quantum_device = cls.model.qcompile(
            circuit, figure_of_merit="expected_fidelity"
        )

        return compiled_circuit, compilation_information, quantum_device

    @classmethod
    def compile_for_device(cls, circuit: QuantumCircuit, device_name: str) -> QuantumCircuit:
        cls._check_for_model()

        compiled_circuit, *_ = cls.model.rl.qcompile(circuit, figure_of_merit="expected_fidelity",
                                                     device_name=device_name)

        return compiled_circuit
