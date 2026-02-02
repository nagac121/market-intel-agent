import streamlit as st
from graph import graph
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig

st.set_page_config(page_title="Deep Market Intel", page_icon="🕵️‍♂️")
st.title("🕵️‍♂️ Deep Market Intelligence Agent")

# Initialize Session State for Threading
if "thread_id" not in st.session_state:
    st.session_state.thread_id = "1"

config: RunnableConfig = {"configurable": {"thread_id": str(st.session_state.thread_id)}}

query = st.text_input("What industry/company should I research?")

if st.button("Start Research"):
    # Initial trigger
    input_message = HumanMessage(content=query)
    for event in graph.stream({"messages": [input_message]}, config, stream_mode="values"):
        last_message = event["messages"][-1]
        st.write(f"**Agent:** {last_message.content}")

# --- HUMAN IN THE LOOP UI ---
# Check if the graph is currently paused
state = graph.get_state(config)
if state.next: # If there is a next step (meaning it's interrupted)
    st.warning("⚠️ Researcher has finished. Review the results above.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Approve & Analyze"):
            # Resume the graph with NO changes
            for event in graph.stream(None, config, stream_mode="values"):
                st.write(event["messages"][-1].content)
    with col2:
        if st.button("❌ Stop"):
            st.write("Research cancelled.")
