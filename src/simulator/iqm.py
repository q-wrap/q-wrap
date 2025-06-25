from iqm.qiskit_iqm import IQMFakeApollo
from qiskit import QuantumCircuit, transpile

from simulator import Simulator


class IqmSimulator(Simulator):
    backend_apollo = None

    @classmethod
    def _get_backend_apollo(cls) -> IQMFakeApollo:
        if cls.backend_apollo is None:
            cls.backend_apollo = IQMFakeApollo()
        return cls.backend_apollo

    def simulate_circuit(self, circuit: QuantumCircuit, noisy_backend: str = None):
        match noisy_backend:
            case None:
                raise ValueError("IQM does not support noise-free simulation.")
            case "apollo":
                backend = self._get_backend_apollo()
                transpiled_circuit = transpile(circuit, backend)

                if transpiled_circuit.num_qubits > 20:
                    raise ValueError("IQM Apollo backend supports only up to 20 qubits.")
            case _:
                raise ValueError(f"Unknown backend: {noisy_backend}")

        job = backend.run(transpiled_circuit, shots=1000)
        return job.result().get_counts()
