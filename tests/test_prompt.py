from prompt import Prompt
import pytest
import random

import tiktoken


@pytest.fixture
def encoding():
    return tiktoken.encoding_for_model("text-davinci-003")


def test_prompt_that_exceed_max_token_are_invalid(encoding):
    encoded_prompt = random.sample(range(1, 50), 40)
    test_prompt_1 = Prompt(encoding.decode(encoded_prompt), 10)
    test_prompt_2 = Prompt(encoding.decode(encoded_prompt), 100)
    assert test_prompt_1.is_valid == False
    assert test_prompt_2.is_valid == True


def test_remaining_length_is_diff_to_max_tokens(encoding):
    encoded_prompt = random.sample(range(1, 50), 40)
    test_prompt = Prompt(encoding.decode(encoded_prompt), 100)
    # encoding and decoding is lossy
    # We ensure it is within reason
    assert test_prompt.remaining_length - 60 <= 10


def test_concat_return_a_new_prompt_with_both_text():
    test_prompt_1 = Prompt("How are you ?")
    test_prompt_2 = Prompt("Fine thank you")
    test_prompt_3 = test_prompt_1.concat(test_prompt_2)
    assert test_prompt_3.text == "How are you ? Fine thank you"

    # Prompts are immutable
    assert test_prompt_1.text == "How are you ?"
    assert test_prompt_2.text == "Fine thank you"


def test_split_returns_list_of_new_prompts_that_respect_max_size():
    test_prompt_1 = Prompt("How are you today ?", 2)
    assert test_prompt_1.is_valid == False
    split_prompts = test_prompt_1.split()
    assert all([prompt.is_valid for prompt in split_prompts])
