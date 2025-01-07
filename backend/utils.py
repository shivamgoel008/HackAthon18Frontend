from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings


class LLMSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LLMSingleton, cls).__new__(cls)
            cls._instance.llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.1)
        return cls._instance.llm


class EmbeddingSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EmbeddingSingleton, cls).__new__(cls)
            cls._instance.embedding = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
        return cls._instance.embedding


def get_llm():
    return LLMSingleton()


def get_embedding():
    return EmbeddingSingleton()

def get_custom_embedding(model):
    return GoogleGenerativeAIEmbeddings(model=model)