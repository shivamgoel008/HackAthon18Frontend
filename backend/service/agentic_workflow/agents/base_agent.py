import operator
from typing import Annotated, Sequence
from langchain_core.messages import (
    BaseMessage,
)
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    sender: str


class BaseAgent:
    def __init__(self, nodes=None, conditional_edges=None, start_node=None) -> None:
        if conditional_edges is None:
            conditional_edges = []
        if nodes is None:
            nodes = []
        workflow = StateGraph(AgentState)
        for node in nodes:
            workflow.add_node(node['name'], node['value'])

        for edge in conditional_edges:
            if 'conditions' in edge:
                workflow.add_conditional_edges(edge['source'], edge['target'], edge['conditions'])
            else:
                workflow.add_edge(edge['source'], edge['target'])

        workflow.add_edge(START, start_node)
        workflow.add_edge(start_node, END)
        self.graph = workflow.compile()
