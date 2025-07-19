import os
import time

import requests
from systems.plugins.index import BaseProvider
from utility.data import ensure_list, load_json


class DeepInfraRequestError(Exception):
    pass


class Provider(BaseProvider("encoder", "deepinfra")):

    def encode(self, text):
        if not text:
            return []

        deepinfra_api_key = os.environ.get("DEEPINFRA_API_KEY", None)
        if not deepinfra_api_key:
            self.command.error(
                "To use the DeepInfra encoder provider you must specify a DEEPINFRA_API_KEY environment variable"
            )
        for retry in range(3):
            try:
                response = requests.post(
                    "https://api.deepinfra.com/v1/openai/embeddings",
                    headers={
                        "Authorization": f"Bearer {deepinfra_api_key}",
                        "Content-Type": "application/json",
                    },
                    timeout=2000,
                    json={
                        "input": ensure_list(text),
                        "dimensions": self.field_dimension,
                        "encoding_format": self.field_format,
                        "model": self.field_model,
                    },
                )
                try:
                    response_data = load_json(response.text)
                    break

                except Exception as e:
                    self.command.warning(f"Invalid JSON returned: {response.text}")

            except requests.exceptions.ConnectionError as e:
                self.command.warning(str(e))

            time.sleep(2)

        if response.status_code == 200 and response_data["data"]:
            return [embedding["embedding"] for embedding in response_data["data"]]
        else:
            raise DeepInfraRequestError(
                f"DeepInfra inference request failed with code {response.status_code}: {response_data}"
            )
