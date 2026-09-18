from dotenv import load_dotenv 
from .states import GenerateAnalystState
from .nodes import create_analysts
from langgraph.graph import END
from typing import Literal
load_dotenv()

#conditional edge
def create_analysts_human_feedback_edges(state:GenerateAnalystState) -> Literal["create_analysts",END]:
    """return the next node to execute"""

    human_analyst_feedback= state.get("human_analyst_feedback",None)

    if human_analyst_feedback:
        return "create_analysts"
    
    return END