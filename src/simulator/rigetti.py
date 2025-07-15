from qiskit import QuantumCircuit

from simulator import Simulator


class RigettiSimulator(Simulator):
    def simulate_circuit(self, circuit: QuantumCircuit, noisy_backend: str = None) -> dict[str, int]:
        raise NotImplementedError
