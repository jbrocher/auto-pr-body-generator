from prompt import Prompt
import logging


class PrBodyGenerator:
    MAX_SUMMARY_DEPTH = 5
    PR_BODY_PROMPT = Prompt(
        """ 
        Generate a body for the github pull request that introduces the changes described below. The PR must contain a quick sumarry of the changes, as well as element the reviewer should pay attention to and refactoring suggesions. 

        Desired Format: Markdown

        Changes introduces by the PR:
        ###
    """
    )

    def __init__(self, openai_client, prompts: list[str]):
        self.openai_client = openai_client
        self.prompts = prompts
        self.body = ""

    def _complete_prompt(self, prompt: str) -> str:
        response = self.openai_client.Completion.create(
            model="text-davinci-003", prompt=prompt, max_tokens=1024
        )
        return response.choices[0].text

    def generate_body(self):
        print(f"generating response for {len(self.prompts)} prompts...")

        for i, prompt in enumerate(self.prompts):
            logging.info(f"Prompt {i}: {prompt}")
            segment_text = self._complete_prompt(prompt)
            logging.info(f"Reponse {i}: {segment_text}")
            self.body += segment_text
            print(f"Generated prompt for segment {i+1} continuing ...")

        logging.info("Initial body")
        logging.info(self.body)

        # Sumarize body
        self.body = str(self.summarize(Prompt(self.body)))
        logging.info("=== summarized body ===")
        logging.info(self.body)

        # Add PR and markdown
        self.body = self._complete_prompt(
            str(self.PR_BODY_PROMPT.concat(Prompt(self.body)))
        )
        logging.info("=== Final Body ===")
        logging.info(self.body)

    def summarize(self, prompt: Prompt, depth=0) -> Prompt:
        print(f"Summarzing at depth {depth}...")
        if depth >= self.MAX_SUMMARY_DEPTH:
            print("Max depth, returning prompt as is")
            return prompt

        next_depth = depth + 1

        summary_prompt = Prompt(
            """ Remove duplicate titles and summarize 
        the following text. The resulting text MUST be shorter
        
        ###
        """
        )
        complete_prompt = summary_prompt.concat(prompt)
        if complete_prompt.is_valid:
            print(f"Finaly summary at depth {depth}, returning prompt")
            return Prompt(self._complete_prompt(str(complete_prompt)))

        split_prompts = Prompt(self.body).split()
        print(f"Too big to summarize, splitted in {len(split_prompts)} prompts")
        summary = Prompt("")
        for split_prompt in split_prompts:
            summary = summary.concat(self.summarize(split_prompt, next_depth))
        return self.summarize(summary, next_depth)

    def dummy_function_that_does_nothtin(self):
        pass
