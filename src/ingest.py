import os
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from src.llm import embeddings

def main():
    # Looking in the new data folder
    data_path = "./data/policies"
    print(f"Loading PDFs from '{data_path}'...")
    loader = PyPDFDirectoryLoader(data_path)
    docs = loader.load()
    
    if not docs:
        print(f"No PDFs found! Please add some to the '{data_path}' folder.")
        return

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(docs)

    print(f"Embedding {len(chunks)} chunks... this may take a moment.")
    
    # Generate and save the FAISS index to the new vector_store folder
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local("./vector_store/faiss_policy_index")
    print("✅ Ingestion complete. FAISS index saved to './vector_store/faiss_policy_index'.")

if __name__ == "__main__":
    main()