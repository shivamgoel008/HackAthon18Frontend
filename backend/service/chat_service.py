from .agentic_workflow import TriageAssistant


class ChatService:
    def __init__(self):
        self.assistant = TriageAssistant()

    def query(self, query: str):
        return self.assistant.query(query)
