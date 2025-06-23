from .select import SelectView
from .simulate import SimulateView


def register_routes(app):
    app.add_url_rule("/select", view_func=SelectView.as_view("select"))
    app.add_url_rule("/simulate", view_func=SimulateView.as_view("simulate"))
