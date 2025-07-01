from django.conf import settings

from systems.plugins.index import BaseProvider
from utility.data import load_json

import requests
import time


class DeepInfraRequestError(Exception):
    pass


class Provider(BaseProvider("encoder", "deepinfra")):

    def _run_inference(self, **config):
        wait_sec = 1

        while True:
            try:
                response = requests.post(
                    "https://api.deepinfra.com/v1/inference/sentence-transformers/{}".format(self.field_model),
                    headers={
                        "Authorization": "bearer {}".format(settings.DEEPINFRA_API_KEY),
                        "Content-Type": "application/json",
                    },
                    timeout=2000,
                    json=config,
                )
                try:
                    response_data = load_json(response.text)
                    break

                except Exception as e:
                    self.command.warning("Invalid JSON returned: {}".format(response.text))

            except requests.exceptions.ConnectionError as e:
                self.command.warning(str(e))

            wait_sec = min((wait_sec * 2), 300)
            time.sleep(wait_sec)

        if response.status_code == 200 and response_data["embeddings"]:
            return response_data["embeddings"]
        else:
            raise DeepInfraRequestError(
                "DeepInfra inference request failed with code {}: {}".format(response.status_code, response_data)
            )

    def encode(self, text):
        if not text:
            return []
        return self._run_inference(inputs=ensure_list(text))
