from typing import Self

from qiskit import QuantumCircuit


# simulator.ibm.IbmSimulator, simulator.ionq.IonqSimulator, simulator.iqm.IqmSimulator,
# simulator.quantinuum.QuantinuumSimulator, simulator.rigetti.RigettiSimulator
# imported in Simulator.get_simulator() to avoid circular imports

class Simulator:
    @classmethod
    def get_simulator(cls, vendor: str) -> Self:
        """
        | vendor       | noise-free                      | noisy                             |
        |--------------|---------------------------------|-----------------------------------|
        | ibm          | local                           | local (nonlocal update possible)  |
        | ionq         | nonlocal                        | nonlocal                          |
        | iqm          | -                               | local                             |
        | quantinuum   | - (nonlocal backend-dependent)  | nonlocal                          |
        | rigetti      | nonlocal (local via VM)         | nonlocal                          |
        """
        match vendor:
            case "ibm":
                from simulator.ibm import IbmSimulator
                return IbmSimulator()
            case "ionq":  # requires API key
                from simulator.ionq import IonqSimulator
                return IonqSimulator()
            case "iqm":
                from simulator.iqm import IqmSimulator
                return IqmSimulator()
            case "quantinuum":  # deactivated due to no API key
                raise NotImplementedError
            case "rigetti":  # deactivated due to no API key
                raise NotImplementedError
            case _:
                raise ValueError(f"Unknown vendor: {vendor}")

    @classmethod
    def get_all_vendor_names(cls) -> list[str]:
        return ["ibm", "ionq", "iqm", "quantinuum", "rigetti"]

    def simulate_circuit(self, circuit: QuantumCircuit, noisy_backend: str = None) -> dict[str, int]:
        raise NotImplementedError
