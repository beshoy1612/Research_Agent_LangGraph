from src.utils.nodes import create_analysts
from langgraph.graph import START,END,StateGraph
from src.utils.states import GenerateAnalystState

from dotenv import load_dotenv

load_dotenv()

#creating our Graph 
#GenerateAnalystState State
# node create_analysts
# edges no need on this graph

builder = StateGraph(GenerateAnalystState)
builder.add_node("creating_analysts",create_analysts)

builder.add_edge(START,"creating_analysts")
builder.add_edge("creating_analysts",END)

graph = builder.compile()