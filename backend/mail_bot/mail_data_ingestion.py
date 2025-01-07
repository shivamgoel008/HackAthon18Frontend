import win32com.client
import os
import faiss
import zlib
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.docstore import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document
from uuid import uuid4

INDEX_FILE = "alert_mail_index"

def compress_text(text, method="zlib"):
    """Compresses text using zlib."""
    text_bytes = text.encode('utf-8')
    return zlib.compress(text_bytes)

def decompress_text(compressed_data, method="zlib"):
    """Decompresses previously compressed data using zlib."""
    return zlib.decompress(compressed_data).decode('utf-8')

def get_outlook_emails(num_emails=10):
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    inbox = outlook.GetDefaultFolder(6)

    messages = inbox.Items
    messages.Sort("[ReceivedTime]", True)

    email_data = []

    for i in range(min(num_emails, messages.Count)):
        message = messages.Item(i+1)
        try:
            body = message.body
            subject = message.subject
            sender = message.SenderName

            compressed_body = compress_text(body)
            email_data.append({
                "subject": subject,
                "sender": sender,
                "compressed_body": compressed_body
            })
        except Exception as e:
            print(f"Error processing email {i+1}: {e}")
            continue
    return email_data

def create_and_store_embeddings(email_data,dimension):

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001") # Initialize Gemini embeddings
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

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0) # Split text into chunks

    docs = []
    metadatas = []
    
    for email in email_data:
        decompressed_body = decompress_text(email['compressed_body'])
        email_text = f"Subject: {email['subject']}\nSender: {email['sender']}\nBody: {decompressed_body}"
        texts = text_splitter.split_text(email_text)
        for i, text in enumerate(texts):
            metadata = {
                "source": f"email_{email['subject']}",
                "chunk": i
            }
            metadatas.append(metadata)
            docs.append(Document(page_content=text,metadata=metadata))
    uuids = [str(uuid4()) for _ in range(len(docs))]
    vector_store.add_documents(documents=docs,ids=uuids)
    return vector_store, docs, metadatas

if __name__ == "__main__":
    email_data = get_outlook_emails(num_emails=10)

    vector_store, docs, metadatas = create_and_store_embeddings(email_data,dimension=768)
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

    # Example search with score
    similar_docs_with_scores = vector_store.similarity_search_with_score(query)
    print("\nSimilarity Search Results with Scores:")
    for doc, score in similar_docs_with_scores:
        print(f"Document: {doc}")
        print(f"Score: {score}")
        print("Metadata",doc.metadata)