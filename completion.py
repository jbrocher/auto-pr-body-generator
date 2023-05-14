from prompt import Prompt
from uuid import uuid4
import logging
from enum import Enum


class Completion:
    class State(Enum):
        UNCOMPLETE = "UNCOMPLETE"
        COMPLETED = "COMPLETED"

    def __init__(self, prompt: Prompt, openai_client):
        self._id = f"hash(prompt)-{uuid4()}"
        self._openai_client = openai_client
        self._prompt = prompt
        self._state = self.State.UNCOMPLETE
        self._result = ""

    @property
    def id(self):
        return self._id

    @property
    def result(self):
        return self._result

    @property
    def state(self):
        return self._state

    def _complete_prompt(self) -> str:
        response = self._openai_client.Completion.create(
            model="text-davinci-003", prompt=self._prompt.text, max_tokens=1024
        )
        return response.choices[0].text

    def complete(self):
        logging.info(f"completion_{self.id} - Completing prompt...")
        logging.info(f"completion_{self.id} - prompt to complete: ")
        logging.info(f"completion_{self.id} - {self._prompt}")
        self._result = self._complete_prompt()
        self._state = self.State.COMPLETED
        logging.info(f"completion_{self.id} - Complete")
        logging.info(f"completion_{self.id} - Result: {self.result}")

    def __eq__(self, completion: "Completion"):
        return self._id == completion._id
