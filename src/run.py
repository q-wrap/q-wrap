from api import create_app
from selector import MqtPredictor

app = create_app()

MqtPredictor.set_model_path(r"..\..\training_env\mqt-predictor\src")

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, use_evalex=False)
