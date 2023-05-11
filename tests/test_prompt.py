from prompt import Prompt
import random

import tiktoken


def test_prompt_that_exceed_max_token_are_invalid():
    encoding = tiktoken.encoding_for_model("text-davinci-003")
    encoded_prompt = random.sample(range(1, 50), 40)
    test_prompt_1 = Prompt(encoding.decode(encoded_prompt), 10)
    test_prompt_2 = Prompt(encoding.decode(encoded_prompt), 100)
    assert test_prompt_1.is_valid == False
    assert test_prompt_2.is_valid == True
