from enum import Enum


class DiffAnalysis:
    class State(Enum):
        NOT_STARTED = "NOT_STARTED"
        FINISHED = "FINISHED"

    def __init__(self, diff: str):
        self.id = hash(diff)
        self.diff = diff
        self.state = self.State.NOT_STARTED
        self.completion_history = []
        self.result = ""

    def exec(self):
        self.state = self.State.FINISHED

    def __eq__(self, diff_analysis):
        return self.id == diff_analysis.id
