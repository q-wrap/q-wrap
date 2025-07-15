from typing import Self

from qiskit import QuantumCircuit, transpile
from qiskit.providers import Backend

from selector import MqtPredictor


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

    def simulate_circuit(self, circuit: QuantumCircuit, noisy_backend: str | None = None,
                         compilation: str | None = None) -> dict[str, int]:
        raise NotImplementedError

    @staticmethod
    def compile_circuit(circuit: QuantumCircuit, backend: Backend, device_name: str,
                        compilation: str | None = None) -> QuantumCircuit:
        # Quantinuum circuits are always compiled with qnexus and this method is not used

        match compilation:
            case None | "none":
                return circuit
            case "qiskit":
                return transpile(circuit, backend)
            case "mqt":
                if device_name == "ideal":
                    raise ValueError("MQT Predictor only supports compilation for noisy backends.")

                return MqtPredictor.compile_for_device(circuit, device_name)
            case _:
                raise ValueError(f"Unknown compilation method: {compilation}")
