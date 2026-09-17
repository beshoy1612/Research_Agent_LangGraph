from dotenv import load_dotenv
from .objects import Analyst,Perspective
from .states import GenerateAnalystState
from .models import llm
from langchain.messages import SystemMessage,HumanMessage
from .prompts import analyst_instructions

load_dotenv()

#nodes 
def create_analysts(state:GenerateAnalystState): 
    """Create analysts"""
    
    topic = state["topic"]
    max_analyst = state["max_analysts"]
    # because its optinal we use .get 
    human_analyst_feedback = state.get("human_analyst_feedback", "")

    #enforce structured output
    structyred_llm = llm.with_structured_output(Perspective)

    #System_message
    system_message = analyst_instructions.format(topic=topic,
                                                 max_analyst=max_analyst,
                                                 human_analyst_feedback=human_analyst_feedback)
    # Generate Question
    analyst = structyred_llm.invoke([SystemMessage(content=system_message)]+ [HumanMessage(content="Please Generatethe set of analyst")])
    # its only update this part in GenerateAnalystState and everything will be the same 
    return {"analyst" : analyst.analyst}