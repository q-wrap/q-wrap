from qiskit import QuantumCircuit
from qiskit_ionq import IonQProvider
from qiskit_ionq.ionq_backend import IonQSimulatorBackend

from simulator import Simulator
from util import tokens


class IonqSimulator(Simulator):
    provider = None
    backend_simulator = None
    backend_aria = None
    backend_harmony = None

    @classmethod
    def _get_provider(cls) -> IonQProvider:
        if cls.provider is None:
            token = tokens.get_token("ionq", "Missing API key for IonQ.")
            cls.provider = IonQProvider(token)

        return cls.provider

    @classmethod
    def _get_backend_simulator(cls) -> IonQSimulatorBackend:
        if cls.backend_simulator is None:
            cls.backend_simulator = cls._get_provider().get_backend("ionq_simulator")
        return cls.backend_simulator

    @classmethod
    def _get_backend_aria(cls) -> IonQSimulatorBackend:
        if cls.backend_aria is None:
            cls.backend_aria = cls._get_provider().get_backend("ionq_simulator")
            cls.backend_aria.set_options(noise_model="aria-1")
        return cls.backend_aria

    @classmethod
    def _get_backend_harmony(cls) -> IonQSimulatorBackend:
        if cls.backend_harmony is None:
            cls.backend_harmony = cls._get_provider().get_backend("ionq_simulator")
            cls.backend_harmony.set_options(noise_model="harmony")
        return cls.backend_harmony

    def simulate_circuit(self, circuit: QuantumCircuit, noisy_backend: str | None = None,
                         compilation: str | None = None) -> dict[str, int]:
        match noisy_backend:
            case None:
                backend = self._get_backend_simulator()
                circuit_to_run = self.compile_circuit(circuit, backend, "ideal", compilation)

                if circuit_to_run.num_qubits > 29:
                    raise ValueError("Ideal simulation with IonQ supports only up to 29 qubits.")
            case "aria-1":
                backend = self._get_backend_aria()
                circuit_to_run = self.compile_circuit(circuit, backend, "ionq_aria1", compilation)

                if circuit_to_run.num_qubits > 25:
                    raise ValueError("IonQ Aria 1 backend supports only up to 25 qubits.")
            case "harmony":
                print("Warning: Simulation on IonQ Harmony currently takes very long.")
                backend = self._get_backend_harmony()
                circuit_to_run = self.compile_circuit(circuit, backend, "ionq_harmony", compilation)

                if circuit_to_run.num_qubits > 11:
                    raise ValueError("IonQ Harmony backend supports only up to 11 qubits.")
            case _:
                raise ValueError(f"Unknown IonQ backend: {noisy_backend}")

        job_result = backend.run(circuit_to_run, shots=1000).result()
        counts = job_result.get_counts()

        return {key: int(value) for key, value in counts.items()}  # convert numpy int to int for JSON serialization
