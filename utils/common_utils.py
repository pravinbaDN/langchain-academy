from dotenv import load_dotenv
import os

class ConfProps:
    openai_api_key = None
    langchain_api_key = None
    tavily_api_key = None
    
    @staticmethod
    def load_config():
      # Load environment variables from .env file
        load_dotenv()
      # Access the config properties
        ConfProps.openai_api_key = os.getenv('OPENAI_API_KEY') 
        ConfProps.langchain_api_key = os.getenv('LANGCHAIN_API_KEY') 
        ConfProps.tavily_api_key = os.getenv('TAVILY_API_KEY') 
        