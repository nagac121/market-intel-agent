import streamlit as st
import json
import uuid
from tools import tools as available_tools
from graph import graph
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import RunnableConfig

st.set_page_config(page_title="Deep Market Intel", page_icon="🕵️‍♂️")
st.title("🕵️‍♂️ Deep Market Intelligence Agent")


def _format_tavily_sources(tool_result: object) -> str | None:
    """Turn Tavily-style list of {title, url, content} into readable markdown."""
    if isinstance(tool_result, str):
        try:
            tool_result = json.loads(tool_result)
        except Exception:
            return None
    if not isinstance(tool_result, list) or not tool_result:
        return None
    lines = ["**Sources found:**"]
    for i, item in enumerate(tool_result[:10], 1):
        if not isinstance(item, dict):
            continue
        title = item.get("title") or item.get("name") or "Source"
        url = item.get("url") or item.get("link") or ""
        content = item.get("content") or item.get("snippet") or ""
        snippet = (content[:300] + "…") if len(content) > 300 else content
        if url:
            lines.append(f"{i}. [{title}]({url})")
        else:
            lines.append(f"{i}. **{title}**")
        if snippet:
            lines.append(f"   {snippet}")
    return "\n\n".join(lines) if len(lines) > 1 else None


# Initialize Session State for Threading and UI
if "thread_id" not in st.session_state:
    st.session_state.thread_id = "1"
if "research_messages" not in st.session_state:
    st.session_state.research_messages = []
if "is_researching" not in st.session_state:
    st.session_state.is_researching = False

config: RunnableConfig = {
    "configurable": {"thread_id": str(st.session_state.thread_id)}
}

query = st.text_input(
    "What industry/company should I research?",
    autocomplete="on",
)

# Container that always renders the latest research above the HITL section
result_container = st.container()

start_clicked = st.button("Start Research", disabled=st.session_state.is_researching)
if start_clicked:
    if not query.strip():
        st.warning("Please enter a research topic before starting research.")
    else:
        st.session_state.is_researching = True
        st.session_state.research_messages = []
        with result_container:
            with st.spinner("🕵️‍♂️ Agent is researching..."):
                input_message = HumanMessage(content=query)
                for event in graph.stream(
                    {"messages": [input_message]}, config, stream_mode="values"
                ):
                    last_message = event["messages"][-1]
                    if not isinstance(last_message, AIMessage):
                        continue
                    raw_content = (
                        last_message.content if last_message.content is not None else ""
                    )
                    content_text = (
                        raw_content
                        if isinstance(raw_content, str)
                        else (
                            json.dumps(raw_content, ensure_ascii=False, indent=2)
                            if isinstance(raw_content, (dict, list))
                            else str(raw_content)
                        )
                    )

                    if content_text.strip():
                        # Real AI text — show as research result
                        display_msg = content_text
                    else:
                        # Tool-call response: try to show formatted sources
                        tool_calls = (
                            getattr(last_message, "additional_kwargs", None) or {}
                        ).get("tool_calls", [])
                        if not tool_calls:
                            continue
                        tc = tool_calls[-1]
                        func_name = (
                            tc.get("name")
                            or (tc.get("function") or {}).get("name")
                            or ""
                        )
                        func_args_raw = tc.get("args") or (
                            tc.get("function") or {}
                        ).get("arguments")
                        args_dict: str | dict = (
                            func_args_raw if func_args_raw is not None else {}
                        )
                        if isinstance(func_args_raw, str):
                            try:
                                args_dict = json.loads(func_args_raw)
                            except Exception:
                                args_dict = {"query": func_args_raw}
                        if not isinstance(args_dict, dict):
                            args_dict = {"query": str(args_dict)}

                        tool_result = None
                        tool_input: str | dict = (
                            args_dict if isinstance(args_dict, dict) else str(args_dict)
                        )
                        try:
                            for t in available_tools:
                                t_name = getattr(t, "name", None) or ""
                                if (
                                    func_name
                                    and t_name
                                    and func_name.lower() in str(t_name).lower()
                                ):
                                    if hasattr(t, "run"):
                                        tool_result = t.run(tool_input)
                                    elif hasattr(t, "invoke"):
                                        tool_result = t.invoke(tool_input)
                                    break
                        except Exception:
                            pass

                        formatted = _format_tavily_sources(tool_result)
                        if formatted:
                            display_msg = formatted
                        else:
                            query_str = (
                                args_dict.get("query", str(args_dict))
                                if isinstance(args_dict, dict)
                                else str(args_dict)
                            )
                            display_msg = f"**Search:** {query_str}\n\n*(Results will be used by the analyst.)*"
                    st.session_state.research_messages.append(display_msg)
                    st.markdown(display_msg)
        st.session_state.is_researching = False
else:
    with result_container:
        if st.session_state.research_messages:
            st.subheader("📊 Research Results")
            for msg in st.session_state.research_messages:
                st.markdown(msg)

# --- HUMAN IN THE LOOP UI ---
state = graph.get_state(config)

# Show HITL when graph is paused (before analyst) and we have results
if state.next and st.session_state.research_messages:
    st.warning("⚠️ Researcher has finished. Review the results above.")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Approve & Analyze"):
            for event in graph.stream(None, config, stream_mode="values"):
                last_content = event["messages"][-1].content
                if last_content:
                    st.session_state.research_messages.append(last_content)
                    st.markdown(last_content)
    with col2:
        if st.button("❌ Clear Research"):
            st.session_state.research_messages = []
            st.session_state.thread_id = str(uuid.uuid4())
            st.rerun()
# Show Clear only when we have content (including after SWOT is displayed)
elif st.session_state.research_messages:
    if st.button("❌ Clear Research"):
        st.session_state.research_messages = []
        st.session_state.thread_id = str(uuid.uuid4())
        st.rerun()
