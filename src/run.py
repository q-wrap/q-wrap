from flasgger import Swagger

from api import create_app
from selector import MqtPredictor

app = create_app()

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'docs',
            "route": '/openapi.json',
        }
    ],
    "static_url_path": "/docs",
    "specs_route": "/docs/",
    "title": "Wrapper",
}
swagger_template = {
    "info": {
        "title": "Wrapper",
        "description": "This API provides a wrapper for the MQT Predictor as selector and for multiple simulators, "
                       "allowing users to select suitable quantum computers for OpenQASM circuits and to simulate "
                       "them with or without noise models of actual quantum computers.",
    },
}
Swagger(app, config=swagger_config, template=swagger_template)

MqtPredictor.set_model_path(r"..\..\training_env\mqt-predictor\src")

if __name__ == '__main__':
    app.run(debug=True)
