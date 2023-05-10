class PrBodyGenerator:
    def __init__(self, openai_client, prompts: list[str]):
        self.openai_client = openai_client
        self.prompts = prompts
        self.body = ""

    def _complete_prompt(self, prompt):
        response = self.openai_client.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=1024,
        )
        return response.choices[0].text

    def generate_body(self):
        print(f"generating response for {len(self.prompts)} prompts...")
        for i, prompt in enumerate(self.prompts):
            segment_text = self._complete_prompt(prompt)
            self.body += segment_text
            print(f"Generated prompt for segment {i+1} continuing ...")

    def dummy_function_that_does_nothtin(self):
        pass
