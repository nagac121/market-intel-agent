from models import model_with_tools
from langchain_core.messages import HumanMessage

def call_researcher(state):
    """
    This function takes the current state (the conversation history)
    and asks Gemini to decide if it needs to search the web.
    """
    messages = state['messages']
    # Gemini looks at the user's question and decides which 'tools' to call
    response = model_with_tools.invoke(messages)
    
    # We return the response to be added to our 'state'
    return {"messages": [response]}
