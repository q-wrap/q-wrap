from api import create_app
from selector import MqtPredictor

MODEL_PATH = r"../data/model/mqt-predictor/src"

app = create_app()

MqtPredictor.set_model_path(MODEL_PATH)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, use_evalex=False)
