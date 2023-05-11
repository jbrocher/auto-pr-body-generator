from prompt import Prompt
import inspect


class PromptsAreNotEmpty(Exception):
    pass


class PromptGenerator:
    MAX_TOKENS = 2048
    DEFAULT_PROMPT = Prompt(
        inspect.cleandoc(
            """ 
            Summarize the changes introduced by the git diff below. Changes made to file describing the project dependencies should be ignored. If applicable, suggest a few refactoring target. 

            Expected format: Natural language, limiting code quote to one or two relevant sentences

            diff to summarize:
            """
        )
    )

    def __init__(self, diff_file: str):
        self.diff_file = diff_file
        self._prompts = []

    def clear(self):
        self._prompts = []

    @property
    def prompts(self):
        return self._prompts

    def generate_prompts(self, max_tokens=None, force=False):
        if len(self._prompts) > 0 and not force:
            raise PromptsAreNotEmpty(
                "Prompts have already be generated, call clear() first or sue force=True"
            )
        self.clear()

        # The default prompt is included in the max token limit
        prompt_tokens = self.DEFAULT_PROMPT.length
        max_tokens = (
            self.MAX_TOKENS - prompt_tokens
            if max_tokens is None
            else max_tokens - prompt_tokens
        )

        with open(self.diff_file, "r") as f:
            diff_text = f.read()
            diff_prompt = Prompt(diff_text, max_tokens)
            splitted_diff_prompts = diff_prompt.split()
            return [
                str(self.DEFAULT_PROMPT.concat(partial_diff_prompt))
                for partial_diff_prompt in splitted_diff_prompts
            ]
