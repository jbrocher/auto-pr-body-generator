import tiktoken
from nltk.tokenize import word_tokenize
from prompt_generator import PromptGenerator


def test_generate_prompts_respect_the_max_tokens_limit():
    generator = PromptGenerator("tests/lorem_ipsum.txt")
    generator.generate_prompts()

    for prompt in generator.prompts:
        encoding = tiktoken.encoding_for_model("text-davinci-003")
        tokens = encoding.encode(prompt)
        assert len(tokens) <= PromptGenerator.MAX_TOKENS
