from enum import Enum
from completion import Completion
from prompt import Prompt
import uuid
import inspect


class DiffAnalysis:
    DEFAULT_PROMPT = Prompt(
        inspect.cleandoc(
            """ 
            Act like a very senior software developer caring for his coworkers. Summarize the changes introduced by the pull request whose diff is provided below. Each change should be described with a bullet point. Suggest refactoring and modifications to improve the code. 


            Here is the pull request diff:
            """
        )
    )

    class State(Enum):
        NOT_STARTED = "NOT_STARTED"
        FINISHED = "FINISHED"

    def __init__(self, diff: str, openai_client):
        self.id = f"{hash(diff)}-{uuid.uuid4()}"
        self.openai_client = openai_client
        self.diff = diff
        self.state = self.State.NOT_STARTED
        self.completion_history = []
        self.result = ""

    def exec(self):
        # The default prompt is included in the max token limit
        max_tokens = self.DEFAULT_PROMPT.remaining_length

        diff_prompt = Prompt(self.diff, max_tokens)
        splitted_diff_prompts = diff_prompt.split()

        print(f"generating response for {len(splitted_diff_prompts)} prompts...")
        diff_analysis = ""
        for i, prompt in enumerate(splitted_diff_prompts):
            completion = Completion(
                self.DEFAULT_PROMPT.concat(prompt.wrap("###")), self.openai_client
            )
            completion.complete()
            self.completion_history.append(completion)
            segment_text = completion.result

            diff_analysis += segment_text
            print(f"Generated prompt for segment {i+1} continuing ...")
        print(f"generated {len(splitted_diff_prompts)}")
        self.result = diff_analysis
        self.state = self.State.FINISHED

    def __eq__(self, diff_analysis):
        return self.id == diff_analysis.id
