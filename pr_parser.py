import json


class PrParser:
    DELIMITER = "### === auto-pr-body ==="

    def __init__(self, pr_data_file_path: str):
        with open(pr_data_file_path, "r") as f:
            self.body = json.load(f)["body"]

    @property
    def prefix(self):
        return self.body.split(self.DELIMITER)[0]
