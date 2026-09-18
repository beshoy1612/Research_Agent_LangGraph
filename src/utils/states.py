from typing_extensions import TypedDict,NotRequired,Annotated
from langgraph.graph import MessagesState
from typing import Optional,List
from .objects import Analyst
import operator
# basic state
class GenerateAnalystState(TypedDict):
    topic: str # research topic 
    max_analysts: int 
    human_analyst_feedback: NotRequired[Optional[str]]
    analyst: NotRequired[List[Analyst]]

class InterviewState(MessagesState):
    max_num_turns: int #number turns of conversation
    context: Annotated[list,operator.add] #source of documentation
    analyst: Analyst # my analyst
    interview: str 
    strsection: list #finalkey we dublicate in outer state for send() api
