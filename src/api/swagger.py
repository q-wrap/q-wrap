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
    "title": "q-wrap",
}
swagger_template = {
    "info": {
        "title": "q-wrap",
        "description": "This API provides a wrapper for the MQT Predictor as selector and for multiple simulators, "
                       "allowing users to select suitable quantum computers for OpenQASM circuits and to simulate "
                       "them with or without noise models of actual quantum computers.\n\n"
                       ""
                       "q-wrap supports the following quantum computers:\n\n"
                       ""
                       "- **IBM Montreal** with 27 qubits\n\n"
                       "- **IBM Washington** with 127 qubits\n\n"
                       "- **IonQ Aria 1** with 25 qubits\n\n"
                       "- **IonQ Harmony** with 11 qubits (simulation is slow)\n\n"
                       "- **IQM Apollo** with 20 qubits\n\n"
                       "- **Quantinuum H2** with 32 qubits (selection only, no simulation)\n\n"
                       "- **Rigetti Aspen-M3** with 79 qubits (selection only, no simulation)"
    },
}


def create_swagger(app: Flask):
    Swagger(app, config=swagger_config, template=swagger_template)
