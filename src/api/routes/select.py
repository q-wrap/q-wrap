from http import HTTPStatus

from flask.views import MethodView

from api.common import validation, error_handling
from selector import MqtPredictor


class SelectView(MethodView):
    def get(self):
        error_handling.post_only()

    def post(self):
        """
        Automated Quantum Backend Selection
        ---
        description:
          Select the most suitable quantum computer for a given OpenQASM circuit.
        tags:
          - selection
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
            description: version of OpenQASM used in the circuit (default is 2)
        responses:
          200:
            description: Successfully selected quantum computer
            schema:
              type: object
              properties:
                quantum_device:
                  type: string
                  description: Name of the selected quantum computer
                number_of_qubits:
                  type: integer
                  description: Number of qubits in the selected quantum computer
          400:
            description: Bad request, e.g., missing required parameters or invalid OpenQASM circuit
          415:
            description: Unsupported media type, e.g., if the request is not in JSON format
        """
        data = validation.get_json()
        loaded_circuit = validation.get_circuit(data)

        compiled_circuit, compilation_information, quantum_device = MqtPredictor().select_device(loaded_circuit)

        return {
            "quantum_device": quantum_device.name,
            "number_of_qubits": quantum_device.num_qubits,
        }, HTTPStatus.OK
