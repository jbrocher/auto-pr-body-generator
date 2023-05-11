from prompt import Prompt
import logging


class PrBodyGenerator:
    MAX_SUMMARY_DEPTH = 3

    def __init__(self, openai_client, prompts: list[str]):
        self.openai_client = openai_client
        self.prompts = prompts
        self.body = ""

    def _complete_prompt(self, prompt):
        response = self.openai_client.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
        )
        return response.choices[0].text

    def generate_body(self):
        print(f"generating response for {len(self.prompts)} prompts...")
        for i, prompt in enumerate(self.prompts):
            segment_text = self._complete_prompt(prompt)
            self.body += segment_text
            print(f"Generated prompt for segment {i+1} continuing ...")
        logging.info("Initial body")
        logging.info(self.body)
        self.body = str(self.summarize(Prompt(self.body)))

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
            return self._complete_prompt(str(complete_prompt))

        split_prompts = Prompt(self.body).split()
        print(f"Too big to summarize, splitted in {len(split_prompts)} prompts")
        summary = Prompt("")
        for split_prompt in split_prompts:
            summary = summary.concat(self.summarize(split_prompt, next_depth))
        return self.summarize(summary, next_depth)

    def dummy_function_that_does_nothtin(self):
        pass
