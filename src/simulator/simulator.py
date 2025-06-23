from qiskit import QuantumCircuit


# simulator.ibm.IbmSimulator, simulator.ionq.IonqSimulator, simulator.iqm.IqmSimulator,
# simulator.quantinuum.QuantinuumSimulator, simulator.rigetti.RigettiSimulator
# imported in Simulator.get_simulator() to avoid circular imports

class Simulator:
    @classmethod
    def get_simulator(cls, vendor: str):
        match vendor:
            case "ibm":
                from simulator.ibm import IbmSimulator
                return IbmSimulator()
            case "ionq":
                raise NotImplementedError
            case "iqm":
                raise NotImplementedError
            case "quantinuum":
                raise NotImplementedError
            case "rigetti":
                raise NotImplementedError
            case _:
                raise ValueError(f"Unknown vendor: {vendor}")

    @classmethod
    def get_all_vendor_names(cls):
        return ["ibm", "ionq", "iqm", "quantinuum", "rigetti"]

    def simulate_circuit(self, circuit: QuantumCircuit):
        return NotImplementedError
