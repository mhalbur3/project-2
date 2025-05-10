from datetime import datetime

class JournalEntry:
    """Represents a journal entry."""
    def __init__(self, title: str, content: str, time: datetime = None) -> None:
        """Initializes the journal entry."""
        self.content = content
        self.title = title
        self.time = time if time else datetime.now()
    def __repr__(self) -> str:
        return f"JournalEntry(title={self.title!r}, time={self.time!r}, content={self.content!r})"
