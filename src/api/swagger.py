from flasgger import Swagger
from flask import Flask

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


def create_swagger(app: Flask):
    Swagger(app, config=swagger_config, template=swagger_template)
