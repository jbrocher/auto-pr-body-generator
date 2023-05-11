from pr_body_generator import PrBodyGenerator
from unittest.mock import MagicMock


def test_generate_body_calls_the_client_for_each_prompt():
    class MockCompletion:
        @staticmethod
        def create(*args, **kwargs):
            mock_choice = MagicMock()
            mock_choice.text = "test"
            mock_response = MagicMock()
            mock_response.choices = [mock_choice]
            return mock_response

    class MockClient:
        Completion = MockCompletion

    generator = PrBodyGenerator(MockClient, "This is a very good pr")
    generator.generate_body()
    assert generator.body == "test"
