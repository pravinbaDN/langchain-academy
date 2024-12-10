from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

class OverallState(TypedDict):
    foo: int

class PrivateState(TypedDict):
    baz: int

# Define node 1
def node_1(state: OverallState) -> PrivateState:
    print("---Node 1---")
    print(f"Input OverallState: {state}")
    output_state = {"baz": state['foo'] + 1}
    print(f"Output PrivateState: {output_state}")
    return output_state

# Define node 2
def node_2(state: PrivateState) -> OverallState:
    print("---Node 2---")
    print(f"Input PrivateState: {state}")
    output_state = {"foo": state['baz'] + 1}
    print(f"Output OverallState: {output_state}")
    return output_state


# Build graph
builder = StateGraph(OverallState)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)

# Logic
builder.add_edge(START, "node_1")
builder.add_edge("node_1", "node_2")
builder.add_edge("node_2", END)

# Add
graph = builder.compile()

# View
# Save the image to a file 
with open("graph_multiple_schema_1.png", "wb") as f: 
    f.write(graph.get_graph().draw_mermaid_png()) 
    print("Graph saved as graph_multiple_schema_1.png")

messages = graph.invoke({"foo" : 1})
print(messages)
