from http import HTTPStatus

from flask import abort


def print_error(error: Exception):
    print(f"{type(error).__name__}: {str(error)}")


def post_only():
    abort(HTTPStatus.NOT_IMPLEMENTED, "This endpoint only supports POST requests.")
