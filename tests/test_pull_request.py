from uuid import uuid4
import pytest
from pull_request import PullRequest


def test_update_auto_body_preservers_custom_text():
    custom_text = """Some Custom Text
That I want to preserve"""

    pr_body = f"{custom_text}\n{PullRequest.DELIMITER}\nPr Auto Body"
    pr = PullRequest(str(uuid4()), pr_body)

    new_auto_body = "New auto body"
    print(pr.body)
    pr.update_auto_body(new_auto_body)
    print(pr.body)
    assert new_auto_body in pr.body
    assert pr.body.startswith(custom_text)


def test_update_auto_body_works_if_pr_is_empty():
    pr_body = ""
    pr = PullRequest(str(uuid4()), pr_body)

    new_auto_body = "New auto body"
    print(pr.body)
    pr.update_auto_body(new_auto_body)
    print(pr.body)
    assert new_auto_body in pr.body
    assert pr.body == f"{PullRequest.DELIMITER}\n\nNew auto body"
