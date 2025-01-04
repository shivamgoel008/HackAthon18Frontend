from langchain_google_genai import ChatGoogleGenerativeAI


class LLMSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LLMSingleton, cls).__new__(cls)
            cls._instance.llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.1)
        return cls._instance.llm


def get_llm():
    return LLMSingleton()
