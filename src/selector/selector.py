from qiskit import QuantumCircuit


class Selector:
    def select_device(self, circuit: QuantumCircuit) -> str:
        raise NotImplementedError
