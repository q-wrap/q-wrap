from typing import Any

from qiskit import QuantumCircuit


class Selector:
    def select_device(self, circuit: QuantumCircuit) -> tuple[QuantumCircuit, list[str], Any]:
        raise NotImplementedError
