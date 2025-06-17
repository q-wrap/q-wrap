TRAINED_MODEL_LOCATION = r"..\..\..\training_env\mqt-predictor\src"

import sys

sys.path.insert(0, TRAINED_MODEL_LOCATION)

import mqt.predictor
import mqt.bench
import qiskit.qasm3

from selectors import Selector


class MqtPredictor(Selector): ...
