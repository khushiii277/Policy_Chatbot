from langchain_openai import AzureChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from src.config import CHAT_DEPLOYMENT_NAME, AZURE_OPENAI_API_VERSION

# Initialize the LLM
llm = AzureChatOpenAI(
    azure_deployment=CHAT_DEPLOYMENT_NAME,
    api_version=AZURE_OPENAI_API_VERSION,
    temperature=0.1, 
)

# Initialize the Embeddings model
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")