import json
import re
import time

import google.generativeai as genai

from utils.logging_handler import get_logger

logger = get_logger(__name__)
JSON_FORMAT = re.compile(r"\{.*\}")
JSON_CLEANUP = re.compile(r"\n|\t|\r")

class Gemini:
    _call_datetimes = {}

    def __init__(self, api_key: str, model: str) -> None:
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)

    def text_request(self, text: str) -> str:
        response = self.model.generate_content(text, generation_config={'temperature': 0.9})
        Gemini._update_counter(response.usage_metadata.total_token_count)
        return response.text

    def json_request(self, text: str) -> dict:
        context = "ONLY RESPONSE TO THIS WITH A JSON COMPATIBLE STRING, WITHOUT ANY CONTEXT TEXT:"
        response = self.model.generate_content(context + text, generation_config={'temperature': 0.9})
        Gemini._update_counter(response.usage_metadata.total_token_count)
        return json.loads(JSON_FORMAT.findall(JSON_CLEANUP.sub('',response.text))[0])

    @classmethod
    def _update_counter(cls, tokens: int) -> None:
        actual_time = time.time()
        cls._call_datetimes[actual_time] = tokens
        cls._call_datetimes = {k: v for k, v in Gemini._call_datetimes.items() if (actual_time - k) < 60}
        logger.info("Minute tokens: %s  -  Minute requests: %s", sum(cls._call_datetimes.values()), len(cls._call_datetimes))
