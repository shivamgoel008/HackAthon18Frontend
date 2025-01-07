from uuid import uuid4
from langchain_google_genai import GoogleGenerativeAIEmbeddings

import os
from dotenv import load_dotenv
from langchain_elasticsearch import ElasticsearchStore
from langchain_core.documents import Document
from elasticsearch import Elasticsearch
import datetime
import os,sys
# sys.path.append(os.path.join(os.path.dirname(__file__), '..',".."))
sys.path.append(os.path.abspath(os.path.join('..', "..")))
from utils import get_custom_embedding

load_dotenv()

class LogsManager:
    def __init__(self):
        self.ELASTIC_SEARCH_URL = os.getenv("ELASTIC_SEARCH_URL")
        self.ELASTIC_SEARCH_USER = os.getenv("ELASTIC_SEARCH_USERNAME")
        self.ELASTIC_SEARCH_PASSWORD = os.getenv("ELASTIC_SEARCH_PASSWORD")
        self.ELASTIC_API_KEY = os.getenv("ELASTIC_SEARCH_API_KEY")
        self.ELASTIC_CERT_PATH = os.getenv("ELASTIC_CERT_PATH")
        self.ELASTIC_SEARCH_HOST = os.getenv("ELASTIC_SEARCH_HOST")
        self.ELASTIC_SEARCH_PORT = os.getenv("ELASTIC_SEARCH_PORT")
        self.ELASTIC_SEARCH_INDEX = os.getenv("ELASTIC_SEARCH_INDEX")
        self.client = Elasticsearch(
            hosts=f"https://{self.ELASTIC_SEARCH_USER}:{self.ELASTIC_SEARCH_PASSWORD}@{self.ELASTIC_SEARCH_HOST}:{self.ELASTIC_SEARCH_PORT}",
            ca_certs=self.ELASTIC_CERT_PATH,
            verify_certs=False,
            basic_auth=("elastic", self.ELASTIC_SEARCH_PASSWORD),
        )
        self.elastic_vector_store = ElasticsearchStore(
            es_connection=self.client,
            index_name=self.ELASTIC_SEARCH_INDEX,
            embedding=get_custom_embedding("models/embedding-001"),
        )

    def client_info(self):
        return self.client.info()
    
    def add_document_to_es_store(self, document):
        uuid = str(uuid4())
        self.elastic_vector_store.add_documents(documents=[document], ids=[uuid])

    def add_documents_to_es_store(self, documents, store):
        uuids = [str(uuid4()) for _ in range(len(documents))]
        self.elastic_vector_store.add_documents(documents=documents, ids=uuids)
    
    def remove_document_from_es_store(self, document_id):
        self.elastic_vector_store.delete(ids=[document_id])

    def remove_documents_from_es_store(self, document_ids):
        self.elastic_vector_store.delete(ids=document_ids)

    def create_sample_logs(self, num=10):
        """
        Creates sample logs and adds them to the elastic search store
        attributes:
        num: int: number of logs to be created

        """
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
                metadata={"source": "mkthon-log-script"},
            )
            logs.append(log_format)
        self.add_documents_to_es_store(logs, self.elastic_vector_store)

    def query_logs(self, query, k=5, num_candidates=50, field="vector"):
        """
        Query the logs in the elastic search store
        attributes:
        query: str: query to be used to search the logs
        k: int: number of logs to be returned
        num_candidates: int: number of candidates to be considered
        field: str: field to be used for searching the logs

        """
        query_vector = self.elastic_vector_store.embedding.embed_query(query)

        res = self.client.knn_search(
            index=self.ELASTIC_SEARCH_INDEX,
            body={
                "knn": {
                    "field": field,
                    "k": k,
                    "num_candidates": num_candidates,
                    "query_vector": query_vector,
                },
                # "_source": [
                #     "text"
                # ],
                "_source": [
                    "app_name",
                    "time_stamp",
                    "thread_count",
                    "log_level",
                    "log_type",
                    "log_format",
                    "log_message",
                    "log_source",
                ],
            },
        )

        # print(res.body.get("hits").get("hits"))
        return res.body.get("hits").get("hits")
