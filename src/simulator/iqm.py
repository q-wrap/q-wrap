from qiskit import QuantumCircuit

from simulator import Simulator


class IqmSimulator(Simulator):
    def simulate_circuit(self, circuit: QuantumCircuit, noisy_backend: str = None):
        return NotImplementedError
