import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Centralize your configuration variables here
CHAT_DEPLOYMENT_NAME = os.getenv("CHAT_DEPLOYMENT_NAME")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")