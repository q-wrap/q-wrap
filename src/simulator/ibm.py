from qiskit import QuantumCircuit, transpile
from qiskit.circuit import Measure
from qiskit_aer import AerSimulator

from simulator import Simulator


class IbmSimulator(Simulator):
    def simulate_circuit(self, circuit: QuantumCircuit):
        aer_simulator = AerSimulator()
        transpiled_circuit = transpile(circuit, aer_simulator)
        result = aer_simulator.run(transpiled_circuit).result()

        if transpiled_circuit.count_ops().get(Measure().name, 0) > 0:  # circuit with measurements
            return result.get_counts(transpiled_circuit)
        else:  # circuit without measurements
            return result.get_statevector(transpiled_circuit)
