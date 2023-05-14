import pytest
from diff_analysis import DiffAnalysis


@pytest.fixture
def diff():
    return """
diff --git a/tests/test_pull_request.py b/tests/test_pull_request.py
new file mode 100644
index 0000000..a57410c
--- /dev/null
+++ b/tests/test_pull_request.py
@@ -0,0 +1,18 @@
+from uuid import uuid4
+import pytest
+from pull_request import PullRequest
+
+
+def test_update_auto_body_preservers_custom_text():
+    custom_text = "Some Custom Text
+That I want to preserve"
+
+    pr_body = f"{custom_text}\n{PullRequest.DELIMITER}\nPr Auto Body"
+    pr = PullRequest(str(uuid4()), pr_body)
+
+    new_auto_body = "New auto body"
+    print(pr.body)
+    pr.update_auto_body(new_auto_body)
+    print(pr.body)
+    assert new_auto_body in pr.body
+    assert pr.body.startswith(custom_text)
"""


def test_diff_analysis_constructor_produce_a_valid_analysis(diff):
    test_diff_analysis = DiffAnalysis(diff=diff)

    assert test_diff_analysis.result == ""
    assert test_diff_analysis.id == hash(diff)
    assert test_diff_analysis.state == DiffAnalysis.State.NOT_STARTED
    assert test_diff_analysis.completion_history == []


def test_diff_analysis_identity_uses_diff_hash(diff):
    test_diff_analysis_1 = DiffAnalysis(diff=diff)
    test_diff_analysis_2 = DiffAnalysis(diff=diff)
    assert test_diff_analysis_1 == test_diff_analysis_2


def test_diff_analysis_switch_states_when_executing(diff):
    test_diff_analysis_1 = DiffAnalysis(diff=diff)
    test_diff_analysis_1.exec()
    assert test_diff_analysis_1.state == DiffAnalysis.State.FINISHED


# def test_diff_analysis_saves_completions_used_to_produce_results():
#     test_diff_analysis_1 = DiffAnalysis(diff=diff)
#     test_diff_analysis_1.exec()
