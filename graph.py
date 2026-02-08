from typing import TypedDict, Annotated, List
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from models import groq_model, groq_with_tools
from langchain_core.messages import HumanMessage, AIMessage

# 1. Define the State (what the agents remember)
class AgentState(TypedDict):
    messages: Annotated[List, add_messages]

# 2. Define the Nodes (the workers)
def researcher_node(state: AgentState):
    """Gemini + tools does the initial research via Tavily, etc."""
    response = groq_with_tools.invoke(state["messages"])
    return {"messages": [response]}

def analyst_node(state: AgentState):
    """Groq takes the research and writes a final report."""
    # take all previous research and ask Groq for a summary
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
