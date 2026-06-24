# Policy Chatbot

An AI-powered corporate assistant built with **FastAPI**, **LangGraph**, and **Azure OpenAI**. This chatbot uses Retrieval-Augmented Generation (RAG) to securely search internal company policies and answer employee questions via a real-time WebSocket connection.

## 🚀 Features

* **Real-time Chat:** Fast, conversational frontend interface using WebSockets.
* **Accurate Retrieval:** Uses **FAISS** and HuggingFace Embeddings (`all-MiniLM-L6-v2`) to perform semantic searches across company documents.
* **Strict AI Guardrails:** LangGraph state management ensures the AI only answers using the provided policy context, preventing hallucinations.
* **Clean Architecture:** Separation of concerns between API routing, AI logic, and data ingestion.

1. Clone the repository

git clone [https://github.com/khushiii277/Policy_Chatbot.git](https://github.com/khushiii277/Policy_Chatbot.git)

cd Policy_Chatbot

2. Set up the virtual environment

# Create the environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate
# Activate it (Git Bash on Windows)
source venv/Scripts/activate
# Activate it (Mac/Linux)
source venv/bin/activate

3. Install dependencies

pip install -r requirements.txt

4. Configure Environment Variables

Rename .env.example to .env (or create a new .env file) and fill in your Azure credentials:

CHAT_DEPLOYMENT_NAME="your_deployment_name"
AZURE_OPENAI_API_VERSION="2024-02-15-preview"
AZURE_OPENAI_API_KEY="your_api_key_here"
AZURE_OPENAI_ENDPOINT="[https://your-resource-name.openai.azure.com/](https://your-resource-name.openai.azure.com/)"

5. Add Data and Build the Index

Place your internal policy PDFs into the data/policies/ folder. Then, run the ingestion script to generate the FAISS vector database:

python -m src.ingest

6. Running the Application

Start the FastAPI server from the root directory:

python -m src.main
