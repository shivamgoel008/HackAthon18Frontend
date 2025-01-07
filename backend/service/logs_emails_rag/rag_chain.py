from elastic_search import LogsManager
from langchain_core.prompts import PromptTemplate
import os,sys
sys.path.append(os.path.abspath(os.path.join('..', "..")))
from utils import get_llm
# Logs RAG Chain

# Retrieval
query = "How many logs have thread count equal to 54?"
logs_retriever = LogsManager()

retrieved_docs = logs_retriever.query_logs(query)
print(retrieved_docs)

# Augmentation
base_prompt = PromptTemplate.from_template("""
    <===Instructions Start===>
    You are a smart Log analyzer for support and Site reliability engineering team.
    You have been tasked with analyzing the logs and providing insights.
    The query has been provided and the relevant logs have also been provided.
    Using the given information identify the root cause of the issue and provide a detailed analysis.
    Suggest any remediation steps if necessary.
    <===Instructions End===>
    <===Examples Start===>
    Example:
    Query: At what time were the Logs having DEBUG log level generated?
    Logs:
    1. Timestamp: 2022-01-01T00:00:00 | URL: https://example.com | Domain: example.com | Host: host 1 | Activity: GET /index.html | Threads Used: 5 | Log level: DEBUG
    Output:
    Root Cause: The logs having DEBUG log level were generated at 2022-01-01T00:00:00
    Analysis: The logs were generated at the start of the day.
    Remediation: No action required.
    <===Examples End===>   
    <===Inputs Start===>
    Query: {query}
    Logs: {logs}
    
""")

augmented_prompt = base_prompt.format_prompt(query=query, logs=retrieved_docs)

# Generation
llm = get_llm()
generated_text = llm.invoke(augmented_prompt)
print(generated_text)