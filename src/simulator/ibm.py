import json

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_ibm_runtime.fake_provider import FakeMontrealV2, FakeWashingtonV2

from simulator import Simulator


class IbmSimulator(Simulator):
    backend_simulator = None
    backend_montreal = None
    backend_washington = None

    @classmethod
    def _get_backend_simulator(cls) -> AerSimulator:
        if cls.backend_simulator is None:
            cls.backend_simulator = AerSimulator()
        return cls.backend_simulator

    @classmethod
    def _get_backend_montreal(cls) -> FakeMontrealV2:
        if cls.backend_montreal is None:
            cls.backend_montreal = FakeMontrealV2()
        return cls.backend_montreal

    @classmethod
    def _get_backend_washington(cls) -> FakeWashingtonV2:
        if cls.backend_washington is None:
            cls.backend_washington = FakeWashingtonV2()
        return cls.backend_washington

    @classmethod
    def _refresh_qpu_backends(cls):
        try:
            with open("../data/secrets/tokens.json", "r") as file:
                json_data = json.load(file)
                if "ibm" in json_data:
                    token = json_data["ibm"]
                else:
                    raise PermissionError("Missing API key for IBM.")
        except FileNotFoundError:
            raise PermissionError("Missing file with API keys.")

        service = QiskitRuntimeService(channel="ibm_cloud", token=token)

        cls._get_backend_montreal().refresh(service)
        cls._get_backend_washington().refresh(service)

    def simulate_circuit(self, circuit: QuantumCircuit, noisy_backend: str = None):
        match noisy_backend:
            case None:
                backend = self._get_backend_simulator()
                transpiled_circuit = transpile(circuit, backend)
            case "montreal":
                backend = self._get_backend_montreal()
                transpiled_circuit = transpile(circuit, backend)

                if transpiled_circuit.num_qubits > 27:
                    raise ValueError("IBM Montreal backend supports only up to 27 qubits.")
            case "washington":
                backend = self._get_backend_washington()
                transpiled_circuit = transpile(circuit, backend)

                if transpiled_circuit.num_qubits > 127:
                    raise ValueError("IBM Washington backend supports only up to 127 qubits.")
            case _:
                raise ValueError(f"Unknown IBM backend: {noisy_backend}")

        job_result = backend.run(transpiled_circuit, shots=1000).result()

        return job_result.get_counts()
