from http import HTTPStatus

from flask import abort, request
from flask.views import MethodView

import util
from selector import MqtPredictor


class SelectView(MethodView):
    def get(self):
        abort(HTTPStatus.NOT_IMPLEMENTED)

    def post(self):
        if not request.is_json:
            abort(HTTPStatus.UNSUPPORTED_MEDIA_TYPE, "Request must be JSON")

        data = request.get_json()

        # required parameters
        if "openqasm_circuit" not in data:
            abort(HTTPStatus.BAD_REQUEST, "Parameter 'openqasm_circuit' missing in request data")
        openqasm_circuit = data["openqasm_circuit"]
        if not isinstance(openqasm_circuit, str):
            abort(HTTPStatus.BAD_REQUEST, "Parameter 'openqasm_circuit' in request data must be a string")

        # optional parameters
        if "openqasm_version" in data:
            openqasm_version = data["openqasm_version"]
            if openqasm_version not in (2, 3):
                abort(HTTPStatus.BAD_REQUEST, "Parameter 'openqasm_version' in request data must be 2 or 3")
        else:
            openqasm_version = util.parse_openqasm_version_or_default(openqasm_circuit)
        if openqasm_version == 3:
            print("Warning: OpenQASM 3 is not fully supported yet.")

        compiled_circuit, compilation_information, quantum_device = MqtPredictor().select_device(
            openqasm_circuit, openqasm_version)

        return {
            "quantum_device": quantum_device.name,
            "number_of_qubits": quantum_device.num_qubits,
        }, HTTPStatus.OK
