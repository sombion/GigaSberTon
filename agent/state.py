from typing import TypedDict, Annotated
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages


class State(TypedDict):
    tg_id: int
    input_messages: str
    templates_data: str
    output_messages: str

graph_builder = StateGraph(State)