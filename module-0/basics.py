import sys
from pathlib import Path

# Add the langchain-academy directory to the system path
project_home = Path(__file__).resolve().parents[1]
sys.path.append(str(project_home))
print(str(project_home))

from utils.common_utils import ConfProps

ConfProps.load_config()


from langchain_openai import ChatOpenAI
gpt4o_chat = ChatOpenAI(model="gpt-4o", temperature=0)
gpt35_chat = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)

from langchain_core.messages import HumanMessage
msg = HumanMessage(content="Hello world", name="Lance") # Create a message
messages = [msg] # Message list
gpt4o_chat.invoke(messages) # Invoke the model with a list of messages 

from langchain_community.tools.tavily_search import TavilySearchResults
tavily_search = TavilySearchResults(max_results=3)
search_docs = tavily_search.invoke("What is LangGraph?")
print(search_docs)