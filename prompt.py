import tiktoken
from typing import Union


class Prompt:
    MAX_TOKENS = 2048
    MODEL = "text-davinci-003"

    def __init__(self, text: str, max_tokens: Union[int, None] = None):
        self.max_tokens = max_tokens if max_tokens is not None else self.MAX_TOKENS
        self.encoding = tiktoken.encoding_for_model(self.MODEL)

        self._text = text
        self._encoded_prompt = self.encoding.encode(text)

    @property
    def length(self):
        return len(self._encoded_prompt)

    @property
    def text(self):
        return self._text

    @property
    def is_valid(self):
        return len(self._encoded_prompt) <= self.max_tokens

    @property
    def remaining_length(self):
        return self.max_tokens - self.length

    def concat(self, prompt: "Prompt"):
        max_tokens = min(self.max_tokens, prompt.max_tokens)
        return Prompt(self.text + " " + prompt.text, max_tokens)

    def split(self):
        if self.is_valid:
            return [Prompt(self.text, self.max_tokens)]

        prompts = []
        for i in range(0, len(self._encoded_prompt), self.max_tokens):
            partial_prompt = Prompt(
                self.encoding.decode(self._encoded_prompt[i : i + self.max_tokens])
            )
            prompts.append(partial_prompt)
        return prompts

    def __repr__(self):
        return self.text
