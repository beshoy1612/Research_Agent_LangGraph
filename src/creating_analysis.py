from src.utils.nodes import create_analysts,human_feedback
from langgraph.graph import START,END,StateGraph
from src.utils.states import GenerateAnalystState
from src.utils.edges import create_analysts_human_feedback_edges
from dotenv import load_dotenv

load_dotenv()

#creating our Graph 
#GenerateAnalystState State
# node create_analysts

builder = StateGraph(GenerateAnalystState)
builder.add_node("create_analysts",create_analysts)
builder.add_node("human_feedback",human_feedback)

builder.add_edge(START,"create_analysts")
builder.add_edge("create_analysts","human_feedback")
builder.add_conditional_edges("human_feedback",create_analysts_human_feedback_edges)
builder.add_edge("human_feedback",END)

graph = builder.compile()