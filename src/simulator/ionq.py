import json

from qiskit import QuantumCircuit
from qiskit_ionq import IonQProvider

from simulator import Simulator


class IonqSimulator(Simulator):
    backend = None

    @classmethod
    def _set_backend(cls):
        if cls.backend is None:
            try:
                with open("../data/secrets/tokens.json", "r") as file:
                    json_data = json.load(file)
                    if "ionq" in json_data:
                        cls.TOKEN = json_data["ionq"]
                    else:
                        raise PermissionError("Missing API key for IonQ.")
            except FileNotFoundError:
                raise PermissionError("Missing file with API keys.")

            cls.backend = IonQProvider(cls.TOKEN).get_backend("ionq_simulator")

    @classmethod
    def simulate_circuit(cls, circuit: QuantumCircuit, noisy_backend: str = None):
        match noisy_backend:
            case None:
                if circuit.num_qubits > 29:
                    raise ValueError("Ideal simulation with IonQ supports only up to 29 qubits.")
                noisy_backend = "ideal"
            case "aria-1":
                if circuit.num_qubits > 25:
                    raise ValueError("IonQ Aria-1 backend supports only up to 25 qubits.")
            case "harmony":
                if circuit.num_qubits > 11:
                    raise ValueError("IonQ Harmony backend supports only up to 11 qubits.")
            case _:
                raise ValueError(f"Unknown IonQ backend: {noisy_backend}")

        cls._set_backend()
        job = cls.backend.run(circuit, shots=1000, noise_model=noisy_backend)
        counts = job.get_counts()

        return {key: int(value) for key, value in counts.items()}  # convert numpy int to int for JSON serialization
