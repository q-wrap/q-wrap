from flask import redirect, Flask

from .select import SelectView
from .simulate import SimulateView


def index():
    return redirect("/docs/")


def apidocs():
    return redirect("/docs/")


def register_routes(app: Flask):
    app.add_url_rule("/", view_func=index)
    app.add_url_rule("/apidocs/", view_func=apidocs)

    app.add_url_rule("/select", view_func=SelectView.as_view("select"))
    app.add_url_rule("/simulate", view_func=SimulateView.as_view("simulate"))
