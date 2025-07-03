import json

from qiskit import QuantumCircuit, transpile
from qiskit_ionq import IonQProvider
from qiskit_ionq.ionq_backend import IonQSimulatorBackend

from simulator import Simulator


class IonqSimulator(Simulator):
    provider = None
    backend_simulator = None
    backend_aria = None
    backend_harmony = None

    @classmethod
    def _get_provider(cls) -> IonQProvider:
        if cls.provider is None:
            try:
                with open("../data/secrets/tokens.json", "r") as file:
                    json_data = json.load(file)
                    if "ionq" in json_data:
                        token = json_data["ionq"]
                    else:
                        raise PermissionError("Missing API key for IonQ.")
            except FileNotFoundError:
                raise PermissionError("Missing file with API keys.")

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

    @classmethod
    def simulate_circuit(cls, circuit: QuantumCircuit, noisy_backend: str = None) -> dict[str, int]:
        match noisy_backend:
            case None:
                backend = cls._get_backend_simulator()
                transpiled_circuit = transpile(circuit, backend)

                if transpiled_circuit.num_qubits > 29:
                    raise ValueError("Ideal simulation with IonQ supports only up to 29 qubits.")
            case "aria-1":
                backend = cls._get_backend_aria()
                transpiled_circuit = transpile(circuit, backend)

                if transpiled_circuit.num_qubits > 25:
                    raise ValueError("IonQ Aria 1 backend supports only up to 25 qubits.")
            case "harmony":
                print("Warning: Simulation on IonQ Harmony currently takes very long.")
                backend = cls._get_backend_harmony()
                transpiled_circuit = transpile(circuit, backend)

                if transpiled_circuit.num_qubits > 11:
                    raise ValueError("IonQ Harmony backend supports only up to 11 qubits.")
            case _:
                raise ValueError(f"Unknown IonQ backend: {noisy_backend}")

        job_result = backend.run(transpiled_circuit, shots=1000).result()
        counts = job_result.get_counts()

        return {key: int(value) for key, value in counts.items()}  # convert numpy int to int for JSON serialization
