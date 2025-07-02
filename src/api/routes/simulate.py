from http import HTTPStatus

from flask import abort
from flask.views import MethodView

from api.common import validation, error_handling
from simulator import Simulator


class SimulateView(MethodView):
    def get(self):
        error_handling.post_only()

    def post(self):
        data = validation.get_json()
        loaded_circuit = validation.get_circuit(data)

        # additional required parameter
        if "vendor" not in data:
            abort(HTTPStatus.BAD_REQUEST, "Parameter 'vendor' missing in request data")
        vendor = data["vendor"]
        try:
            simulator = Simulator.get_simulator(vendor)
        except ValueError as error:
            error_handling.print_error(error)
            abort(HTTPStatus.BAD_REQUEST,
                  f"Parameter 'vendor' must be one of: {", ".join(Simulator.get_all_vendor_names())}")

        # additional optional parameter
        if "noisy_backend" in data:
            noisy_backend = data["noisy_backend"]
        else:
            noisy_backend = None

        try:
            return simulator.simulate_circuit(loaded_circuit, noisy_backend)
        except PermissionError as error:
            error_handling.print_error(error)
            abort(HTTPStatus.FORBIDDEN, "API key for this vendor required")
