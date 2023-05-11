import tiktoken
from typing import Union


class Prompt:
    MAX_TOKENS = 500
    MODEL = "text-davinci-003"

    def __init__(self, text: str, max_tokens: Union[int, None] = None):
        self.max_tokens = max_tokens if max_tokens is not None else self.MAX_TOKENS
        encoding = tiktoken.encoding_for_model(self.MODEL)
        self.encoded_prompt = encoding.encode(text)

    @property
    def is_valid(self):
        return len(self.encoded_prompt) <= self.max_tokens
