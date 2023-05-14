from prompt import Prompt
from diff_analysis import DiffAnalysis
import logging
import inspect


class PromptsAreNotEmpty(Exception):
    pass


class DiffAnalyzerService:
    def __init__(self, diff_file: str, openai_client):
        self.diff_file = diff_file
        self.openai_client = openai_client

    def analyse_diff(self):
        with open(self.diff_file, "r") as f:
            diff_text = f.read()
            diff_analysis = DiffAnalysis(diff_text, self.openai_client)
            diff_analysis.exec()
            logging.info(f"analysis-{diff_analysis.id} - Analysis finished")
            logging.info(f"analysis-{diff_analysis.id} - Analysed {diff_text}")
            logging.info(
                f"analysis-{diff_analysis.id} - Result:  {diff_analysis.result}"
            )
            logging.info(
                f"analysis-{diff_analysis.id} - Completion used:  {diff_analysis.completion_history}"
            )
            return diff_analysis.result
