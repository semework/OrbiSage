"""orbisage_router.graph – conditional LangGraph router"""
from typing import TypedDict, List
from langgraph.graph import StateGraph, END

class State(TypedDict):
    user_input: str
    messages:   List[str]

# nodes ------------------------------------------------------------
def greet_node(state: State):
    msg = "Agent: Hello!"
    print(msg)
    return {"messages": state["messages"] + [msg]}

def navigator_node(state: State):
    msg = "Navigator: Office → Elevator → Gym."
    print(msg)
    return {"messages": state["messages"] + [msg]}

def news_node(state: State):
    msg = "News: Latest AI news — LLMs are transforming industries."
    print(msg)
    return {"messages": state["messages"] + [msg]}

def discovery_node(state: State):
    msg = "Discovery: Fun Fact — Honey found in pyramids is still edible!"
    print(msg)
    return {"messages": state["messages"] + [msg]}

def jokes_node(state: State):
    msg = "Joke: Why do programmers prefer dark mode? Because light attracts bugs."
    print(msg)
    return {"messages": state["messages"] + [msg]}

# router -----------------------------------------------------------
def decide_route(state: State) -> str:
    txt = state["user_input"].lower()
    if any(k in txt for k in ("navigate", "gym", "where", "go")): return "navigate"
    if "news" in txt:                                            return "news"
    if any(k in txt for k in ("fact", "science", "discovery")):   return "fact"
    return "joke"

# factory ----------------------------------------------------------
def build_router_graph():
    g = StateGraph(State)
    g.add_node("greet",       greet_node)
    g.add_node("Navigator",   navigator_node)
    g.add_node("News",        news_node)
    g.add_node("Discovery",   discovery_node)
    g.add_node("Jokes",       jokes_node)

    g.set_entry_point("greet")
    g.add_conditional_edges(
        "greet", decide_route,
        {"navigate":"Navigator", "news":"News", "fact":"Discovery", "joke":"Jokes"}
    )
    for leaf in ("Navigator", "News", "Discovery", "Jokes"):
        g.add_edge(leaf, END)
    return g.compile()
