class PullRequest:
    DELIMITER = "### === auto-pr-body ==="

    def __init__(self, id, body):
        self._id = id
        body_chunks = body.split(self.DELIMITER)
        self._custom_text = body.split(self.DELIMITER)[0].strip()
        self._auto_text = (
            body.split(self.DELIMITER)[1].strip() if len(body_chunks) > 1 else ""
        )

    @property
    def id(self):
        return self._id

    @property
    def body(self):
        return (
            f"{self._custom_text}\n\n{self.DELIMITER}\n\n{self._auto_text}"
            if self._custom_text
            else f"{self.DELIMITER}\n\n{self._auto_text}"
        )

    def update_auto_body(self, new_body: str):
        self._auto_text = new_body
