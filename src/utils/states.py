from typing_extensions import TypedDict,NotRequired
from typing import Optional,List
from .objects import Analyst

# basic state
class GenerateAnalystState(TypedDict):
    topic: str # research topic 
    max_analysts: int 
    human_analyst_feedback: NotRequired[Optional[str]]
    analyst: NotRequired[List[Analyst]]
