from prompt import Prompt
import logging
import inspect


class PromptsAreNotEmpty(Exception):
    pass


class DiffAnalyzerService:
    DEFAULT_PROMPT = Prompt(
        inspect.cleandoc(
            """ 
            Act like a very senior software developer caring for his coworkers. Summarize the changes introduced by the pull request whose diff is provided below. Each change should be described with a bullet point. Suggest refactoring and modifications to improve the code. 


            Here is the pull request diff:
            """
        )
    )

    def __init__(self, diff_file: str, openai_client):
        self.diff_file = diff_file
        self.openai_client = openai_client

    def _complete_prompt(self, prompt: str) -> str:
        response = self.openai_client.Completion.create(
            model="text-davinci-003", prompt=prompt, max_tokens=1024
        )
        return response.choices[0].text

    def analyse_diff(self):
        # The default prompt is included in the max token limit
        max_tokens = self.DEFAULT_PROMPT.remaining_length

        with open(self.diff_file, "r") as f:
            diff_text = f.read()

        diff_prompt = Prompt(diff_text, max_tokens)
        splitted_diff_prompts = diff_prompt.split()

        print(f"generating response for {len(splitted_diff_prompts)} prompts...")
        diff_analysis = ""
        for i, prompt in enumerate(splitted_diff_prompts):
            logging.info(f"Prompt {i}: {prompt}")
            segment_text = self._complete_prompt(
                str(self.DEFAULT_PROMPT.concat(prompt.wrap("###")))
            )
            logging.info(f"Reponse {i}: {segment_text}")

            diff_analysis += segment_text
            print(f"Generated prompt for segment {i+1} continuing ...")
        print(f"generated {len(splitted_diff_prompts)}, staring body generation...")
        return diff_analysis
