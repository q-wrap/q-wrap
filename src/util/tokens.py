import json
from typing import AnyStr


def get_token(token_name: str, error_message: str) -> AnyStr:
    try:
        with open("../data/secrets/tokens.json", "r") as file:
            json_data = json.load(file)
            if token_name in json_data:
                token = json_data[token_name]
            else:
                raise PermissionError(error_message)
    except FileNotFoundError:
        raise PermissionError("Missing file with API keys.")

    return token
