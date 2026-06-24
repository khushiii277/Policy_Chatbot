from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from src.llm import llm
from src.retriever import retriever

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    context: str

def retrieve_node(state: AgentState):
    user_query = state["messages"][-1].content
    docs = retriever.invoke(user_query)
    context = "\n\n---\n\n".join([doc.page_content for doc in docs])
    
    # Debugging block to see what FAISS finds
    print("\n" + "="*50)
    print("👀 WHAT FAISS RETRIEVED FOR THIS QUERY:")
    print("="*50)
    print(context)
    print("="*50 + "\n")
    
    return {"context": context}

def generate_node(state: AgentState):
    context = state["context"]
    
    system_prompt = f"""
You are a helpful, conversational HR and IT assistant for the company.
Answer the user's question directly and naturally, using ONLY the policy excerpts provided below.

TONE AND STYLE RULES:
1. Speak like a friendly and professional human colleague.
2. Be concise, clear, and conversational.
3. Answer the user's question directly without unnecessary introductions.
4. NEVER use phrases such as "Based on the policy excerpts..."
5. Do not mention that you are using policy excerpts or company documents.
6. If the answer is available in the provided excerpts, provide it naturally.
7. Do not make assumptions, infer missing information, or use external knowledge.
8. If the answer cannot be found in the provided excerpts, politely acknowledge that the information is unavailable.

POLICY EXCERPTS:
{context}
"""

    formatted_chat_history = [{"role": "system", "content": system_prompt}]
    
    for msg in state["messages"]:
        role = "user" if isinstance(msg, HumanMessage) else "assistant"
        formatted_chat_history.append({"role": role, "content": msg.content})
    
    try:
        response = llm.invoke(formatted_chat_history)
        return {"messages": [response]}
    except Exception as e:
        error_msg = str(e)
        if "content_filter" in error_msg or "ResponsibleAIPolicyViolation" in error_msg:
            print("WARNING: User prompt blocked by Azure Content Filter.")
            warning_reply = AIMessage(content="[System Message] Your request was blocked by corporate security filters. Please revise your prompt and try again.")
            return {"messages": [warning_reply]}
        else:
            raise e
        
workflow = StateGraph(AgentState)
workflow.add_node("retrieve", retrieve_node)
workflow.add_node("generate", generate_node)
workflow.add_edge(START, "retrieve")
workflow.add_edge("retrieve", "generate")
workflow.add_edge("generate", END)

# Export the compiled graph
app_graph = workflow.compile()