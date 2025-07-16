from iqm.qiskit_iqm import IQMFakeApollo
from qiskit import QuantumCircuit

from simulator import Simulator


class IqmSimulator(Simulator):
    backend_apollo = None

    @classmethod
    def _get_backend_apollo(cls) -> IQMFakeApollo:
        if cls.backend_apollo is None:
            cls.backend_apollo = IQMFakeApollo()
        return cls.backend_apollo

    def simulate_circuit(self, circuit: QuantumCircuit, noisy_backend: str | None = None,
                         compilation: str | None = None) -> dict[str, int]:
        match noisy_backend:
            case None:
                raise ValueError("IQM does not support noise-free simulation.")
            case "apollo":
                backend = self._get_backend_apollo()
                circuit_to_run = self.compile_circuit(circuit, backend, "iqm_apollo", compilation)

                if circuit_to_run.num_qubits > 20:
                    raise ValueError("IQM Apollo backend supports only up to 20 qubits.")
            case _:
                raise ValueError(f"Unknown IQM backend: {noisy_backend}")

        job_result = backend.run(circuit_to_run, shots=1000).result()

        return job_result.get_counts()
