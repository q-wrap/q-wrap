from http import HTTPStatus

from flask import abort
from flask.views import MethodView

from api.common import validation
from selector import MqtPredictor


class SelectView(MethodView):
    def get(self):
        abort(HTTPStatus.NOT_IMPLEMENTED)

    def post(self):
        data = validation.get_json()
        loaded_circuit = validation.get_circuit(data)

        compiled_circuit, compilation_information, quantum_device = MqtPredictor().select_device(loaded_circuit)

        return {
            "quantum_device": quantum_device.name,
            "number_of_qubits": quantum_device.num_qubits,
        }, HTTPStatus.OK
