from http import HTTPStatus

from flask import abort
from flask.views import MethodView

from api.common import validation, error_handling
from simulator import Simulator


class SimulateView(MethodView):
    def get(self):
        error_handling.post_only()

    def post(self) -> tuple[dict, int]:
        """
        Quantum Circuit Simulation
        ---
        description: |
          Simulate a given OpenQASM circuit with the noise model of a specified quantum computer or without noise.
        tags:
          - core
        parameters:
          - name: openqasm_circuit
            in: body
            type: string
            required: true
            description: OpenQASM circuit to be evaluated
          - name: openqasm_version
            in: body
            type: integer
            enum: [2, 3]
            required: false
            description: |
              Version of OpenQASM used in the circuit (2 or 3, default is 2).

              Warning: OpenQASM 3 is not fully supported yet.
          - name: vendor
            in: body
            type: string
            required: true
            description: |
              Vendor of the quantum computer to be simulated (ibm, ionq, iqm). This value must fit the noisy backend.

              Quantinuum and Rigetti are currently not supported due to missing API keys.
          - name: noisy_backend
            in: body
            type: string
            required: false
            enum: [montreal, washington, aria-1, harmony, apollo, h2, aspen-m3]
            description: |
              Name of the quantum computer whose noise model is used for simulation (montreal, washington, aria-1,
              harmony, apollo). This value must fit the vendor.

              If omitted, noise-free simulation is performed.

              Warning: Simulation on IonQ Harmony currently takes very long.
              Quantinuuum H2 and Rigetti Aspen-M3 are currently not supported due to missing API keys.
          - name: compilation
            in: body
            type: string
            required: false
            enum: [qiskit, mqt, none]
            description: |
              Compilation method to be used for the circuit (qiskit, mqt, or none, default is qiskit).

              Compilation with Qiskit is faster than with MQT Predictor, but may be less optimized. Compilation with
              MQT Predictor is only available for noisy backends.

              If `/select` was called before, the returned compiled circuit should be passed as circuit and this
              parameter should be set to none. If not, the circuit needs to be compiled before simulation using the
              specified compilation method.
        responses:
          200:
            description: Successfully simulated quantum circuit
            schema:
              type: object
              properties:
                counts:
                  description: Measurement count of each bitstring
                  type: object
                  additionalProperties:
                    type: integer
          400:
            description: |
              Bad request: Missing required parameters or invalid parameters, especially invalid OpenQASM circuit
          403:
            description: |
              Forbidden: API key for the specified vendor is required but not provided
          415:
            description: |
              Unsupported media type: Request is not in JSON format
          
        """
        data = validation.get_json()
        loaded_circuit = validation.get_circuit(data)

        # additional required parameter
        if "vendor" not in data:
            abort(HTTPStatus.BAD_REQUEST, "Parameter 'vendor' missing in request data")
        vendor = data["vendor"]
        try:
            simulator = Simulator.get_simulator(vendor)
        except NotImplementedError as error:
            error_handling.print_error(error)
            abort(HTTPStatus.NOT_IMPLEMENTED, f"Simulation for vendor '{vendor}' currently not supported")
        except ValueError as error:
            error_handling.print_error(error)
            abort(HTTPStatus.BAD_REQUEST,
                  f"Parameter 'vendor' must be one of: {", ".join(Simulator.get_all_vendor_names())}")

        # additional optional parameters
        if "noisy_backend" in data:
            noisy_backend = data["noisy_backend"]
        else:
            noisy_backend = None

        if "compilation" in data:
            compilation = data["compilation"]
        else:
            compilation = "qiskit"

        try:
            return {
                "counts": simulator.simulate_circuit(loaded_circuit, noisy_backend, compilation),
            }, HTTPStatus.OK
        except PermissionError as error:
            error_handling.print_error(error)
            abort(HTTPStatus.FORBIDDEN, "API key for this vendor required")
