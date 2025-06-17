from .select import SelectView


def register_routes(app):
    app.add_url_rule("/select", view_func=SelectView.as_view("select"))
