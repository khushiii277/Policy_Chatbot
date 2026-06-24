import os
from langchain_community.vectorstores import FAISS
from src.llm import embeddings

# Load the vector store from the correct directory
vectorstore = FAISS.load_local(
    "./vector_store/faiss_policy_index", 
    embeddings, 
    allow_dangerous_deserialization=True 
)

# Remember to use the updated k=10 value we discussed!
retriever = vectorstore.as_retriever(search_kwargs={"k": 10})