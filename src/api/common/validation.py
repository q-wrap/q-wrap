from http import HTTPStatus

from flask import abort, request
from qiskit import QuantumCircuit

import util
from api.common import error_handling


def get_json() -> dict:
    if not request.is_json:
        abort(HTTPStatus.UNSUPPORTED_MEDIA_TYPE, "Request must be JSON")

    return request.get_json()


def get_circuit(data) -> QuantumCircuit:
    # required parameter
    if "openqasm_circuit" not in data:
        abort(HTTPStatus.BAD_REQUEST, "Parameter 'openqasm_circuit' missing in request data")
    openqasm_circuit = data["openqasm_circuit"]
    if not isinstance(openqasm_circuit, str):
        abort(HTTPStatus.BAD_REQUEST, "Parameter 'openqasm_circuit' in request data must be a string")

    # optional parameter
    if "openqasm_version" in data:
        openqasm_version = data["openqasm_version"]
        if openqasm_version not in (2, 3):
            abort(HTTPStatus.BAD_REQUEST, "Parameter 'openqasm_version' in request data must be 2 or 3")
    else:
        try:
            openqasm_version = util.parse_openqasm_version_or_default(openqasm_circuit)
        except ValueError as error:
            error_handling.print_error(error)
            abort(HTTPStatus.BAD_REQUEST, "Invalid version specification in OpenQASM circuit")
    if openqasm_version == 3:
        print("Warning: OpenQASM 3 is not fully supported yet.")

    try:
        return util.load_openqasm_circuit(openqasm_circuit, openqasm_version)
    except ValueError as error:
        error_handling.print_error(error)
        abort(HTTPStatus.BAD_REQUEST, "Invalid OpenQASM circuit")
