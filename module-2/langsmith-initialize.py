import os
#os.environ["LANGCHAIN_API_KEY"] = 
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"]="langchain-academy"
from langsmith import utils
print(utils.tracing_is_enabled())

