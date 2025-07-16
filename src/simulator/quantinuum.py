import qnexus
from pytket.extensions.qiskit import qiskit_to_tk
from qiskit import QuantumCircuit
from qnexus import QuantinuumConfig

from simulator import Simulator
from util import tokens


class QuantinuumSimulator(Simulator):
    backend_h2 = None

    @classmethod
    def _get_backend_h2(cls) -> QuantinuumConfig:
        if cls.backend_h2 is None:
            user = tokens.get_token("quantinuum_user", "Missing username for Quantinuum.")
            password = tokens.get_token("quantinuum_password", "Missing password for Quantinuum.")
            qnexus.auth.login_no_interaction(user, password)

            project = qnexus.projects.get_or_create(name="Wrapper")
            qnexus.context.set_active_project(project)

            cls.backend_h2 = qnexus.QuantinuumConfig(device_name="H2-Emulator")

        return cls.backend_h2

    def simulate_circuit(self, circuit: QuantumCircuit, noisy_backend: str | None = None,
                         compilation: str | None = None) -> dict[str, int]:
        if compilation not in (None, "none", "qnexus"):
            raise ValueError("Quantinuum circuits are always compiled with qnexus.")

        pytket_circuit = qiskit_to_tk(circuit)

        match noisy_backend:
            case None:
                raise ValueError("Quantinuum does not support backend-independent noise-free simulation.")
            case "h2":
                backend = self._get_backend_h2()

                if pytket_circuit.n_qubits > 32:
                    raise ValueError("Quantinuum H2 backend supports only up to 32 qubits.")
            case _:
                raise ValueError(f"Unknown Quantinuum backend: {noisy_backend}")

        uploaded_circuit = qnexus.circuits.upload(pytket_circuit)
        compile_job = qnexus.start_compile_job(
            programs=uploaded_circuit,
            backend_config=backend,
            name="compilation",
        )
        qnexus.jobs.wait_for(compile_job)
        compile_job_result = qnexus.jobs.results(compile_job)[0].get_output()
        # Quantinuum circuits are always compiled with qnexus
        circuit_to_run = compile_job_result

        execute_job = qnexus.start_execute_job(
            programs=circuit_to_run,
            backend_config=backend,
            name="execution",
            n_shots=[1000],
        )
        qnexus.jobs.wait_for(execute_job)
        execute_job_result = qnexus.jobs.results(execute_job)[0].download_result()

        return execute_job_result.get_counts()
