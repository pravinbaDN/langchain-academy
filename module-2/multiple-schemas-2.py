from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END


class InputState(TypedDict):
    question: str

class OutputState(TypedDict):
    question: str
    answer: str

class OverallState(TypedDict):
    question: str
    answer: str
    notes: str

def thinking_node(state: InputState):
    return {"answer": "bye", "notes": "... his is name is Lance"}

def answer_node(state: OverallState) -> OutputState:
    return {"answer": "bye Lance"}

graph = StateGraph(OverallState, input=InputState, output=OutputState)
graph.add_node("answer_node", answer_node)
graph.add_node("thinking_node", thinking_node)
graph.add_edge(START, "thinking_node")
graph.add_edge("thinking_node", "answer_node")
graph.add_edge("answer_node", END)

graph = graph.compile()

# View
# Save the image to a file 
with open("graph_multiple_schema_2.png", "wb") as f: 
    f.write(graph.get_graph().draw_mermaid_png()) 
    print("Graph saved as graph_multiple_schema_2.png")

messages = graph.invoke({"question":"hi"})

print(messages)