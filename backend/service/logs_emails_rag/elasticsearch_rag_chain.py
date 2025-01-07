from uuid import uuid4
from langchain_google_genai import GoogleGenerativeAIEmbeddings

import os
from dotenv import load_dotenv
from langchain_elasticsearch import ElasticsearchStore
from langchain_core.documents import Document
from elasticsearch import Elasticsearch
import datetime

load_dotenv()

ELASTIC_SEARCH_URL = os.getenv("ELASTIC_SEARCH_URL")
ELASTIC_SEARCH_USER = os.getenv("ELASTIC_SEARCH_USER")
ELASTIC_SEARCH_PASSWORD = os.getenv("ELASTIC_SEARCH_PASSWORD")
ELASTIC_API_KEY = os.getenv("ELASTIC_SEARCH_API_KEY")
ELASTIC_CERT_PATH = os.getenv("ELASTIC_CERT_PATH")
ELASTIC_SEARCH_HOST = os.getenv("ELASTIC_SEARCH_HOST")
ELASTIC_SEARCH_PORT = os.getenv("ELASTIC_SEARCH_PORT")

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

client = Elasticsearch(
    hosts=f"https://{ELASTIC_SEARCH_USER}:{ELASTIC_SEARCH_PASSWORD}@{ELASTIC_SEARCH_HOST}:{ELASTIC_SEARCH_PORT}",
    ca_certs=ELASTIC_CERT_PATH,
    verify_certs=False,
    basic_auth=("elastic", ELASTIC_SEARCH_PASSWORD)
)
print(client.info())

elastic_vector_store = ElasticsearchStore(
    es_connection=client,
    index_name="langchain_index",
    embedding=embeddings,

)

def add_documents_to_es_store(documents,store):
    uuids = [str(uuid4()) for _ in range(len(documents))]
    elastic_vector_store.add_documents(documents=documents, ids=uuids)

def create_sample_logs(num=10):
    logs = []
    for i in range(num):
        timestamp = datetime.datetime.now().isoformat()
        url = "https://example.com"
        domain = "example.com"
        host = f"host {i}"
        activity = "GET /index.html"
        threads_used = 5
        log_format = Document(
            page_content=f"Timestamp: {timestamp} | URL: {url} | Domain: {domain} | Host: {host} | Activity: {activity} | Threads Used: {threads_used}",
            metadata={"source": "logstash"},
        )
        logs.append(log_format)
    add_documents_to_es_store(logs,elastic_vector_store)


query = "retieve the Logs having DEBUG log level"
query_vector = embeddings.embed_query(query)


res = client.knn_search(index="langchain_index", body=  {
    "knn": {
      "field": "vector",
      "k": 5,
      "num_candidates": 50,
      "query_vector": query_vector
      },
    "_source": ["app_name","time_stamp","thread_count","log_level","log_type","log_format","log_message","log_source"]
  },)

print(res.body.get("hits").get("hits"))

