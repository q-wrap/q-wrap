# q-wrap

> A wrapper for **Automated Quantum Backend Selection** and **Quantum Circuit Simulation**

This API provides a wrapper for the [MQT Predictor](https://github.com/munich-quantum-toolkit/predictor) as selector
and for multiple simulators, allowing users to select suitable quantum computers for OpenQASM circuits and to simulate
them with or without noise models of actual quantum computers.

q-wrap supports the following quantum computers:

| Quantum computer | Number of qubits | Selection | Simulation |
|------------------|-----------------:|:---------:|:----------:|
| IBM Montreal     |               27 |     ✅     |     ✅      |
| IBM Washington   |              127 |     ✅     |     ✅      |
| IonQ Aria 1      |               25 |     ✅     |     ✅*     |
| IonQ Harmony     |               11 |     ✅     |     ❓*     |
| IQM Apollo       |               20 |     ✅     |     ✅      |
| Quantinuum H2    |               32 |     ✅     |     ❌*     |
| Rigetti Aspen-M3 |               79 |     ✅     |     ❌*     |

\* requires an API token, see [API tokens](#api-tokens) below.

Simulation on IonQ Harmony may be unavailable due to server-side failure of the IonQ simulator for this noise model.
Simulation on Quantinuum H2 and Rigetti Aspen-M3 is not supported because of missing API tokens.

## Installation

Install Python 3.12 on your system. You can download it from the
[official Python website](https://www.python.org/downloads/release/python-31210/).

Clone this repository, where `<path>` is the URL of this repository and `--depth 1` is optional:

```bash
git clone --depth 1 <path>
```

Before you install the required packages, you should create and activate a virtual environment. However, this is
optional, and you are free to use another package manager like `uv` as well.

```bash
python -m venv venv  # Python 3.12

# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

If you want to get an overview of the packages used by this application, see the `requirements_direct.txt` file,
instead, which only contains directly installed or imported packages without their dependencies.

## Trained model

The MQT Predictor needs a trained model which is not included in this repository. You can either create your own
model using [this separate repository](https://github.com/q-wrap/training) or get a pre-trained model.

After training or downloading the model, place the `mqt-predictor/src/` directory inside the `data/model/` directory
of this repository, such that you have `data/model/mqt-predictor/src/`. If you prefer another location on your system,
you can change the `MODEL_PATH` constant in `run.py` to point to your custom location.

## API tokens

For simulation on IonQ, an API token is required as explained [here](https://docs.ionq.com/guides/managing-api-keys).
The token should be pasted in `data/secrets/tokens.json` as follows:

```json
{
  "ionq": "YOUR_IONQ_API_TOKEN"
}
```

Quantinuum and Rigetti require API tokens as well, but simulation isn't supported for them, yet, because we couldn't
obtain API tokens ourselves.

## Running the API

Make sure that your virtual environment is activated if you created one. To run the API, just execute the `run.py`
script in the `src` directory with Python 3.12:

```bash
python src/run.py
```

The API will then be available at http://localhost:5000.

## Documentation

The API is documented using Swagger. You are redirected to the documentation page when you open the API in your browser,
or you can access it directly at http://localhost:5000/docs.
