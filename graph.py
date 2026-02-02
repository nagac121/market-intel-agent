from typing import TypedDict, Annotated, List
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from models import model_with_tools, groq_model
from langchain_core.messages import HumanMessage, AIMessage
from models import groq_model # Ensure this is imported

# 1. Define the State (what the agents remember)
class AgentState(TypedDict):
    messages: Annotated[List, add_messages]

# 2. Define the Nodes (the workers)
def researcher_node(state: AgentState):
    # Groq is much faster and less likely to hit 429 errors on start
    # We use the groq_model which you already initialized in models.py
    response = groq_model.invoke(state["messages"])
    return {"messages": [response]}

def analyst_node(state: AgentState):
    """Groq takes the research and writes a final report."""
    # We take all previous research and ask Groq for a summary
    summary_prompt = "Based on the research above, provide a SWOT analysis and strategic recommendation."
    messages = state["messages"] + [HumanMessage(content=summary_prompt)]
    response = groq_model.invoke(messages)
    return {"messages": [response]}

# 3. Build the Graph
workflow = StateGraph(AgentState)

workflow.add_node("researcher", researcher_node)
workflow.add_node("analyst", analyst_node)

workflow.add_edge(START, "researcher")
workflow.add_edge("researcher", "analyst")
workflow.add_edge("analyst", END)

# 4. Compile with Memory (Required for Human-in-the-Loop)
memory = MemorySaver()
# This 'interrupt' stops the agent before it moves to the analyst node
graph = workflow.compile(checkpointer=memory, interrupt_before=["analyst"])
