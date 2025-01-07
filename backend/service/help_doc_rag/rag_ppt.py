from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.chat_history import BaseChatMessageHistory
from langchain.chains import create_history_aware_retriever
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.documents import Document
from dotenv import load_dotenv
from io import BytesIO
from typing import List
import PyPDF2
import os
import uuid
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from service.blob_storage_service import BlobStorageService
load_dotenv()
 
class ragDocs:

    def token_in_all_context(self,docs):
        d_sorted = sorted(docs, key=lambda x: x.metadata["source"])
        d_reversed = list(reversed(d_sorted))
        concatenated_content = "\n\n\n --- \n\n\n".join(
            [doc.page_content + "\n" + str(doc.metadata) for doc in d_reversed]
        )
        print(
            "Num tokens in all context: %s"
            # % num_tokens_from_string(concatenated_content, "cl100k_base")
        )
        return concatenated_content

    def split_pdf(self, input_pdf_path: str, max_pages: int = 5) -> List[str]:
        """Splits a PDF into smaller PDFs, each containing 'max_pages' pages or fewer."""
        pdf_reader = PyPDF2.PdfReader(input_pdf_path)
        total_pages = len(pdf_reader.pages)
        split_pdfs= []
        
        # Split the PDF into chunks of 'max_pages' pages
        for start_page in range(0, total_pages, max_pages):
            pdf_writer = PyPDF2.PdfWriter()
            for page_num in range(start_page, min(start_page + max_pages, total_pages)):
                pdf_writer.add_page(pdf_reader.pages[page_num])
            
            # # Write the chunk to a new PDF file
            # output_pdf_path = f"{input_pdf_path}_part_{start_page // max_pages + 1}.pdf"
            # with open(output_pdf_path, "wb") as output_pdf:
            #     pdf_writer.write(output_pdf)
            # split_pdf_paths.append(output_pdf_path)
            output_pdf = BytesIO()
            pdf_writer.write(output_pdf)
            output_pdf.seek(0)  # Rewind the file pointer to the beginning
            split_pdfs.append(output_pdf)
        
        return split_pdfs

    def get_pdf_text(self, pdf_docs: List[str]):
        docs = []
        for pdf_path in pdf_docs:
            pdf_reader = PyPDF2.PdfReader(pdf_path)
            total_pages = len(pdf_reader.pages)
            
            if total_pages > 5:
                # Split the PDF if it has more than 5 pages
                split_pdfs = self.split_pdf(pdf_path)
            else:
                # No need to split, process the original PDF
                split_pdfs = [pdf_path]
            
            # Process each split PDF or original PDF
            for pdf_chunk_path in split_pdfs:
                pdf_reader_chunk = PyPDF2.PdfReader(pdf_chunk_path)
                
                # Extract content from each page of the chunk
                for index, page in enumerate(pdf_reader_chunk.pages):
                    content = page.extract_text()
                    
                    # Create a document with metadata
                    doc_page = Document(
                        page_content=content, 
                        metadata={
                            "source": pdf_path,  # The original file path
                            "page": index + 1,
                        }
                    )
                    docs.append(doc_page)
        return docs
    
    def get_text_chunks(self,concatenated_content):  
        print("Generating text splits...")
        chunk_size_tok = 1000
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=chunk_size_tok, chunk_overlap=50
        )
        texts_split = text_splitter.split_text(concatenated_content)
        #
        print(f"Number of text splits generated: {len(texts_split)}")
        return texts_split

    def get_vector_store(self,text_chunks):
        embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
        vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
        vector_store.save_local("faiss_index")
        return vector_store
    
    def get_conversational_chain(self , retriever):
        model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.3)
        contextualize_q_system_prompt = (
            "Given the chat history and the latest user question, "
            "provide a response that directly addresses the user's query based on the provided documents. "
            "Do not rephrase the question or ask follow-up questions."
        )

        contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", contextualize_q_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )
        history_aware_retriever = create_history_aware_retriever(
            model, retriever, contextualize_q_prompt
        )
        system_prompt = """
            You are an intelligent and helpful chatbot specialized in providing descriptive answers from documents. You have access to a comprehensive database of documents containing detailed information about various concepts and terms.
            When a user asks a question, your task is to provide a clear, concise, and accurate response based on the information available in the documents. Always ensure your response is relevant to the user's query and derived from the context of the provided documents.
            Also do not mention sentences like "the document mentions ,  the provided text also contains". Provide information to the user
            without mentioning about the document, the response should be like conversation.
            You should not hallucinate your response and provide information only if it is present in provided documents, your response should
            be context relevant. If user asks query that is not related to provided documents just say "I cannot answer that , as i don't have information about it".
            Do not prompt to select answers or do not formulate a stand alone question. do not ask questions in the response.
            Present your response in bullet points if possible
            Below is the context information:
            {context}
            """        
        
        qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )
        question_answer_chain = create_stuff_documents_chain(model, qa_prompt)
        rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

        store = {}

        def get_session_history(session_id: str) -> BaseChatMessageHistory:
            if (session_id not in store):
                store[session_id] = ChatMessageHistory()
            return store[session_id]

        conversational_rag_chain = RunnableWithMessageHistory(
            rag_chain,
            get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer",
        )

        return conversational_rag_chain
        
    def query(self,user_question):
        session_id = str(uuid.uuid4())
        pdf_files = self.load_data()
        embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
        if pdf_files and not os.path.exists("faiss_index"):
            print("Processing PDF files...")
            docs = self.get_pdf_text(pdf_files)
            concatenated_content = self.token_in_all_context(docs)
            text_chunks = self.get_text_chunks(concatenated_content)
            vector_store = self.get_vector_store(text_chunks)
            retriever = vector_store.as_retriever()
            conversational_chain =self.get_conversational_chain(retriever=retriever)
            response = conversational_chain.invoke({"input": user_question}, config={"configurable": {"session_id": session_id}})
        else:
            new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)        
            conversational_chain = self.get_conversational_chain(new_db.as_retriever())
            response = conversational_chain.invoke({"input": user_question}, config={"configurable": {"session_id": session_id}})
        print("Response fetched", response["answer"])
        return response
    
    def load_data(self,pdf_dir="Rag pdf files"):
        if not os.path.exists(pdf_dir):
            print(f"Directory {pdf_dir} does not exist.")
            pdf_files = []
        else:
            pdf_files = [os.path.join(pdf_dir, f) for f in os.listdir(pdf_dir) if f.endswith('.pdf')]
            if not pdf_files:
                print(f"No PDF files found in directory {pdf_dir}.")
            else:
                print("Pdf files := ", pdf_files)
        return pdf_files
    def download_from_blob(self, blob_service):
        if not os.path.exists("Rag pdf files"):
            message = blob_service.download_folder("Rag pdf files", "")
            print(message)
        else:
            print("Folder already exists, skipping download.")

def rag_pipeline(query):
    rag_sys = ragDocs()
    blob_service = BlobStorageService()
    rag_sys.download_from_blob(blob_service)
    response = rag_sys.query(query)
    print("Response fetched :=", response["answer"])
    return response["answer"]    
if __name__ == "__main__":

    rag_pipeline("What does printf command do in awk?")
    # rag_pipeline("How does using NGINX Plus with FastCGI Process Manager (FPM) PHP engine in the Docker container help improve performance and flexibility for the web app, especially when interacting with microservices via JavaScript?")  
       