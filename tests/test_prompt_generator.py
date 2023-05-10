import pytest
from nltk.tokenize import word_tokenize
from prompt_generator import PromptGenerator


def test_generate_prompts_respect_the_max_tokens_limit():
    generator = PromptGenerator("tests/lorem_ipsum.txt")
    generator.generate_prompts()

    for prompt in generator.prompts:
        words = word_tokenize(prompt)
        assert len(words) <= PromptGenerator.MAX_TOKENS
