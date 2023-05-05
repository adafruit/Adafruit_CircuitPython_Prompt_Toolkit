class InMemoryHistory:
    def __init__(self):
        self._history = []

    def append_string(self, string: str) -> None:
        self._history.append(string)

    def get_strings(self) -> list[str]:
        return self._history
