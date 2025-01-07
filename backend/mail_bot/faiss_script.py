import faiss
import os
from dotenv import load_dotenv
import gzip
from langchain.text_splitter import CharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.schema import Document
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from uuid import uuid4
from bs4 import BeautifulSoup

load_dotenv()
os.environ["GOOGLE_API_KEY"]="AIzaSyCN-rG0OyFty0dEL7YCsa7ONR-jeY79qTs"
# Configuration
INDEX_FILE = "C:\\AlertData\\alert_index.faiss"
DATA_DIRECTORY = "C:\\AlertData\\CompressedMails" # Directory where PowerShell saves compressed data

def extract_from_html(file_path):
    with open(file_path,'r',encoding='utf-8') as file:
        if file_path.endswith(".html"):
            soup = BeautifulSoup(file,'html.parser')
            return soup.get_text(separator=' ').strip()
        else:
            with open(file_path,'r',encoding='utf-8') as file:
                return file.read()

def process_and_add_to_index(data_directory):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001") # Initialize Gemini embeddings
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0) # Split text into chunks
    if os.path.exists(INDEX_FILE):
        vector_store = FAISS.load_local(
            folder_path = INDEX_FILE,
            embeddings = embeddings,
            allow_dangerous_deserialization=True,
        )
        print("Loaded existing FAISS index.")
    else:
        index = faiss.IndexFlatL2(len(embeddings.embed_query("test")))
        vector_store = FAISS(
            embedding_function=embeddings,
            index=index,
            docstore=InMemoryDocstore(),
            index_to_docstore_id={},
        )
        print("Created new FAISS index.")
    
    metadatas = []
    docs = []
    for filename in os.listdir(data_directory):
        if filename.endswith(".txt") or filename.endswith(".html"):
            filepath = os.path.join(data_directory, filename)
            try:
                print("Processing File: ",filename)
                body = extract_from_html(filepath)
                subject = filename.split(".")[0]
                email_text = f"Subject: {subject}\nBody: {body}"
                texts = text_splitter.split_text(email_text)
                for i, text_chunk in enumerate(texts):  # Iterate through the chunks
                    metadata = {
                        "source": f"email_{subject}",
                        "chunk": i,  # Add chunk number for context
                        "total_chunks": len(texts), # Add total chunks for context
                        "subject": subject # Add subject for context
                    }
                    docs.append(Document(page_content=text_chunk, metadata=metadata))
                    metadatas.append(metadata)

                uuids = [str(uuid4()) for _ in range(len(docs))]
                vector_store.add_documents(documents=docs,ids=uuids)
            except Exception as e:
                print(f"Error processing {filename}: {e}")
    return vector_store, docs, metadatas
# Main execution
if __name__ == "__main__":

    vector_store, docs, metadatas = process_and_add_to_index(DATA_DIRECTORY)
    vector_store.save_local(INDEX_FILE)
    print(f"FAISS index created with {vector_store.index.ntotal} vectors.")
    print(f"Number of documents created: {len(docs)}")
    print(f"Number of metadata created: {len(metadatas)}")
    print(f"Index File saved at {INDEX_FILE}")

    # Example similarity search
    query = "What is the email about?"
    similar_docs = vector_store.similarity_search(query)
    print("\nSimilarity Search Results:")
    for doc in similar_docs:
      print(doc)
      print("Metadata:",doc.metadata)
