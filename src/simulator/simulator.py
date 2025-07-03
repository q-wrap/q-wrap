from typing import Self

from qiskit import QuantumCircuit


# simulator.ibm.IbmSimulator, simulator.ionq.IonqSimulator, simulator.iqm.IqmSimulator,
# simulator.quantinuum.QuantinuumSimulator, simulator.rigetti.RigettiSimulator
# imported in Simulator.get_simulator() to avoid circular imports

class Simulator:
    @classmethod
    def get_simulator(cls, vendor: str) -> Self:
        match vendor:
            case "ibm":
                from simulator.ibm import IbmSimulator
                return IbmSimulator()
            case "ionq":
                from simulator.ionq import IonqSimulator
                return IonqSimulator()
            case "iqm":
                from simulator.iqm import IqmSimulator
                return IqmSimulator()
            case "quantinuum":
                from simulator.quantinuum import QuantinuumSimulator
                return QuantinuumSimulator()
            case "rigetti":
                from simulator.rigetti import RigettiSimulator
                return RigettiSimulator()
            case _:
                raise ValueError(f"Unknown vendor: {vendor}")

    @classmethod
    def get_all_vendor_names(cls) -> list[str]:
        return ["ibm", "ionq", "iqm", "quantinuum", "rigetti"]

    def simulate_circuit(self, circuit: QuantumCircuit, noisy_backend: str = None) -> dict[str, int]:
        return NotImplementedError
