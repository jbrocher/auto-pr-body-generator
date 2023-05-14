import pytest
from unittest.mock import MagicMock
from prompt import Prompt
from completion import Completion


@pytest.fixture
def test_prompt():
    return Prompt("test")


def test_completion_state_is_updated_correctly(test_prompt):
    test_completion = Completion(test_prompt, MagicMock())
    assert test_completion.state == Completion.State.UNCOMPLETE
    test_completion.complete()
    assert test_completion.state == Completion.State.COMPLETED


def test_completion_calls_open_ai_client(test_prompt):
    mock_openai_completion = MagicMock()

    test_completion = Completion(test_prompt, mock_openai_completion)
    test_completion.complete()
    mock_openai_completion.Completion.create.assert_called_once_with(
        model="text-davinci-003", prompt=test_prompt.text, max_tokens=1024
    )


def test_completion_can_be_printed(test_prompt):
    test_completion = Completion(test_prompt, MagicMock())
    test_completion.complete()
    assert (
        str(test_completion)
        == f"{test_completion.id} - {test_completion.state} - result: {test_completion.result}"
    )
