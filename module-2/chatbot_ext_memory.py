from langsmith import utils
from dotenv import load_dotenv
load_dotenv()

import os

os.environ["LANGCHAIN_API_KEY"]=os.getenv('LANGCHAIN_API_KEY')
os.environ["LANGCHAIN_TRACING_V2"]=os.getenv('LANGCHAIN_TRACING_V2')
os.environ["LANGCHAIN_PROJECT"]=os.getenv('LANGCHAIN_PROJECT')
print(utils.tracing_is_enabled())

import sqlite3
# In memory
conn = sqlite3.connect(":memory:", check_same_thread = False)

db_path = "Z:\\Python\\langchain-academy\\module-2\\state_db\example.db"
conn = sqlite3.connect(db_path, check_same_thread=False)
# Here is our checkpointer 
from langgraph.checkpoint.sqlite import SqliteSaver
memory = SqliteSaver(conn)

from langchain_openai import ChatOpenAI
model = ChatOpenAI(model="gpt-4o",temperature=0)

from langgraph.graph import MessagesState
class State(MessagesState):
    summary: str


from langchain_core.messages import SystemMessage, HumanMessage, RemoveMessage

# Define the logic to call the model
def call_model(state: State):
    print(">>> call_model()")
    # Get summary if it exists
    summary = state.get("summary", "")

    # If there is summary, then we add it
    if summary:
        
        # Add summary to system message
        system_message = f"Summary of conversation earlier: {summary}"

        # Append summary to any newer messages
        messages = [SystemMessage(content=system_message)] + state["messages"]
    
    else:
        messages = state["messages"]
    
    response = model.invoke(messages)
    return {"messages": response}


def summarize_conversation(state: State):
    print(">>> summarize_conversation()")
    # First, we get any existing summary
    summary = state.get("summary", "")

    # Create our summarization prompt 
    if summary:
        
        # A summary already exists
        summary_message = (
            f"This is summary of the conversation to date: {summary}\n\n"
            "Extend the summary by taking into account the new messages above:"
        )
        
    else:
        summary_message = "Create a summary of the conversation above:"

    # Add prompt to our history
    messages = state["messages"] + [HumanMessage(content=summary_message)]
    response = model.invoke(messages)
    
    # Delete all but the 2 most recent messages
    delete_messages = [RemoveMessage(id=m.id) for m in state["messages"][:-2]]
    return {"summary": response.content, "messages": delete_messages}

from langgraph.graph import END
# Determine whether to end or summarize the conversation
def should_continue(state: State):
    
    """Return the next node to execute."""
    print(">>> should_continue()")
    messages = state["messages"]
    
    # If there are more than six messages, then we summarize the conversation
    if len(messages) > 6:
        return "summarize_conversation"
    
    # Otherwise we can just end
    return END

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START
# Define a new graph
workflow = StateGraph(State)
workflow.add_node("conversation", call_model)
workflow.add_node(summarize_conversation)

# Set the entrypoint as conversation
workflow.add_edge(START, "conversation")
workflow.add_conditional_edges("conversation", should_continue)
workflow.add_edge("summarize_conversation", END)

# Compile
#memory = MemorySaver()
graph = workflow.compile(checkpointer=memory)

# Create a thread
config = {"configurable": {"thread_id": "1"}}

# Start conversation
input_message = HumanMessage(content="hi! I'm Lance") # 1
print("Conversation #1")
output = graph.invoke({"messages": [input_message]}, config) 
for m in output['messages'][-1:]:
    m.pretty_print()

print("Conversation #2")
input_message = HumanMessage(content="what's my name?") # 2
output = graph.invoke({"messages": [input_message]}, config) 
for m in output['messages'][-1:]:
    m.pretty_print()

print("Conversation #3")
input_message = HumanMessage(content="i like the 49ers!") # 3
output = graph.invoke({"messages": [input_message]}, config) 
for m in output['messages'][-1:]:
    m.pretty_print()

print("Checksummary>>>>")
print(graph.get_state(config).values.get("summary",""))

print("Conversation #4")
input_message = HumanMessage(content="i like Nick Bosa, isn't he the highest paid defensive player?") # 4
output = graph.invoke({"messages": [input_message]}, config) 
for m in output['messages'][-1:]:
    m.pretty_print()

print("Checksummary<<<<<<<")
print(graph.get_state(config).values.get("summary",""))

print("Retrieve from SQLite>>>>")
config = {"configurable": {"thread_id": "1"}}
graph_state = graph.get_state(config)
print(graph_state)