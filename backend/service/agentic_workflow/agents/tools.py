from langchain_core.tools import tool


@tool
def helpDocsSearch(query: str):
    """
    This tool is used to perform semantic search on SOP documents, videos, and other resources.
    :param query:
        query (str): user query
    :return:
        response to the query generated through RAG
    """
    pass


@tool
def logsAndEmailSearch(query: str):
    """
        This tool is used to perform semantic search on logs and emails data.
        :param query:
            query (str): user query to check in database
        :return:
            response to the query generated through RAG
    """
    return "crowdstrike is used by system1, system501, system101"


@tool
def logsSearch(query: str):
    """
        This tool is used to perform semantic search on logs data.
        :param query:
            query (str): user query to check in database
        :return:
            response to the query generated through RAG
    """
    return "crowdstrike is used by system1, system501, system102"


@tool
def mailsSearch(query: str):
    """
        This tool is used to perform semantic search on email data.
        :param query:
            query (str): user query to check in database
        :return:
            response to the query generated through RAG
    """
    pass

@tool
def pdfSearch(query: str):
    """
        This tool is used to perform semantic search on pdf data.
        :param query:
            query (str): user query to check in database
        :return:
            response to the query generated through RAG
    """
    pass


@tool
def pptSearch(query: str):
    """
        This tool is used to perform semantic search on ppt data.
        :param query:
            query (str): user query to check in database
        :return:
            response to the query generated through RAG
    """
    pass

@tool
def excelCSVSearch(query: str):
    """
        This tool is used to perform semantic search on excel and csv data.
        :param query:
            query (str): user query to check in database
        :return:
            response to the query generated through RAG
    """
    pass