from http import HTTPStatus

from flask import abort, request
from flask.views import MethodView

from selector import MqtPredictor


class SelectView(MethodView):
    def get(self):
        abort(HTTPStatus.NOT_IMPLEMENTED)

    def post(self):
        if not request.is_json:
            abort(HTTPStatus.UNSUPPORTED_MEDIA_TYPE, "Request must be JSON")

        data = request.get_json()

        if "openqasm_circuit" not in data:
            abort(HTTPStatus.BAD_REQUEST, "Parameter 'openqasm_circuit' missing in request data")

        openqasm_circuit = data["openqasm_circuit"]

        if not isinstance(openqasm_circuit, str):
            abort(HTTPStatus.BAD_REQUEST, "Parameter 'openqasm_circuit' in request data must be a string")

        compiled_circuit, compilation_information, quantum_device = MqtPredictor().select_device(openqasm_circuit)

        return {
            "quantum_device": quantum_device.name,
            "number_of_qubits": quantum_device.num_qubits,
        }, HTTPStatus.OK
