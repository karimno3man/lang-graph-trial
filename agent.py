from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from typing import TypedDict, List, Annotated
from dotenv import load_dotenv
import operator

load_dotenv()

llm = ChatOpenAI(model="gpt-4o", temperature=0.7)

# --- State ---
class State(TypedDict):
    messages: Annotated[List, operator.add]  # memory: messages accumulate
    persona: str

# --- Router ---
def router_node(state: State):
    user_message = state["messages"][-1].content

    prompt = f"""Classify this message into exactly one category:
- "cfo" → finance, budgets, revenue, costs, ROI, cash flow, investments
- "cto" → technology, engineering, architecture, infrastructure, security, software
- "sales" → sales, growth, partnerships, go-to-market, business development, marketing

Message: {user_message}

Reply with ONLY one word: cfo, cto, or sales"""

    result = llm.invoke([HumanMessage(content=prompt)])
    return {"persona": result.content.strip().lower()}

# --- Persona Nodes ---
def cfo_node(state: State):
    system = """You are the CFO of a forward-thinking company.
You are an expert in financial planning, budgeting, revenue strategy, cost optimization, ROI analysis, and cash flow management.
Be direct, data-driven, and strategic. Use financial terminology naturally.
Keep responses concise but insightful. Reference prior conversation context when relevant."""
    response = llm.invoke([SystemMessage(content=system)] + state["messages"])
    return {"messages": [response]}

def cto_node(state: State):
    system = """You are the CTO of a forward-thinking company.
You are an expert in software architecture, engineering decisions, technology strategy, infrastructure, security, and technical roadmaps.
Be clear, technical but accessible, and forward-thinking. Reference prior conversation context when relevant."""
    response = llm.invoke([SystemMessage(content=system)] + state["messages"])
    return {"messages": [response]}

def sales_node(state: State):
    system = """You are a combined Business Developer, GTM (Go-To-Market) Manager, and Sales Manager.
You are an expert in sales strategy, partnership development, go-to-market execution, revenue growth, and customer acquisition.
Be energetic, strategic, and results-focused. Reference prior conversation context when relevant."""
    response = llm.invoke([SystemMessage(content=system)] + state["messages"])
    return {"messages": [response]}

# --- Routing Function ---
def route_to_persona(state: State):
    persona = state["persona"]
    if persona not in ["cfo", "cto", "sales"]:
        return "sales"  # default fallback
    return persona

# --- Build Graph ---
def build_graph():
    graph = StateGraph(State)

    graph.add_node("router", router_node)
    graph.add_node("cfo", cfo_node)
    graph.add_node("cto", cto_node)
    graph.add_node("sales", sales_node)

    graph.set_entry_point("router")

    graph.add_conditional_edges("router", route_to_persona, {
        "cfo": "cfo",
        "cto": "cto",
        "sales": "sales"
    })

    graph.add_edge("cfo", END)
    graph.add_edge("cto", END)
    graph.add_edge("sales", END)

    # Memory: persists messages across turns using thread_id
    memory = MemorySaver()
    return graph.compile(checkpointer=memory)

app = build_graph()
