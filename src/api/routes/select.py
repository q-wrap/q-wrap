from http import HTTPStatus

from flask import abort
from flask.views import MethodView


class SelectView(MethodView):
    def get(self):
        return "Hello, world!"

    def post(self):
        abort(HTTPStatus.NOT_IMPLEMENTED)
