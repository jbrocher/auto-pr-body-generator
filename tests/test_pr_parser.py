import json
from pr_parser import PrParser
from unittest.mock import mock_open, patch


def test_initializing_the_parser_load_the_pr_body():
    mock_pr_data = json.dumps({"body": "Test pr body"})
    with patch("builtins.open", mock_open(read_data=mock_pr_data)):
        pr_parser = PrParser("pr_data")


def test_get_prefix_returns_the_correct_string():
    mock_pr_data = json.dumps(
        {
            "body": "A prior text \n### === auto-pr-body === \n\n\nThis Pull Request includes the following changes:\n\n- Changed the `on` from `pull_request` to `push`.\n- Added `permissions: write-all` for job definition\n- Added a `f.write(...)` to main.py\n- Added a dummy function `dummy_function_that_does_nothing()` to pr_body_generator.py\n- Adjusted the Generate Prompts text in prompt_generator.py \n\nReviewers should pay special attention to these changes, and ensure that nothing else has been unexpectedly impacted. Additionally, it would be beneficial to check the permissions in the job definition, as too many permissions can be dangerou"
        }
    )

    with patch("builtins.open", mock_open(read_data=mock_pr_data)):
        pr_parser = PrParser("pr_data")
        assert pr_parser.prefix == "A prior text \n"


def test_get_prefix_returns_the_correct_string_for_empty_pr():
    mock_pr_data = json.dumps({"body": ""})

    with patch("builtins.open", mock_open(read_data=mock_pr_data)):
        pr_parser = PrParser("pr_data")
        assert pr_parser.prefix == ""


def test_get_prefix_returns_the_correct_string_if_no_custom_text_exists():
    mock_pr_data = json.dumps(
        {
            "body": "### === auto-pr-body === \n\n\nThis Pull Request includes the following changes:\n\n- Changed the `on` from `pull_request` to `push`.\n- Added `permissions: write-all` for job definition\n- Added a `f.write(...)` to main.py\n- Added a dummy function `dummy_function_that_does_nothing()` to pr_body_generator.py\n- Adjusted the Generate Prompts text in prompt_generator.py \n\nReviewers should pay special attention to these changes, and ensure that nothing else has been unexpectedly impacted. Additionally, it would be beneficial to check the permissions in the job definition, as too many permissions can be dangerous "
        }
    )

    with patch("builtins.open", mock_open(read_data=mock_pr_data)):
        pr_parser = PrParser("pr_data")
        assert pr_parser.prefix == ""
