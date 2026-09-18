from dotenv import load_dotenv
from .objects import Analyst,Perspective
from .states import GenerateAnalystState
from .models import llm
from langchain.messages import SystemMessage,HumanMessage
from .prompts import analyst_instructions
from langgraph.types import interrupt

load_dotenv()

#nodes 
def create_analysts(state:GenerateAnalystState): 
    """Create analysts"""
    
    topic = state["topic"]
    max_analysts = state["max_analysts"]
    # because its optinal we use .get 
    human_analyst_feedback = state.get("human_analyst_feedback", "")

    #enforce structured output
    structyred_llm = llm.with_structured_output(Perspective)

    #System_message
    system_message = analyst_instructions.format(topic=topic,
                                                 max_analysts=max_analysts,
                                                 human_analyst_feedback=human_analyst_feedback)
    # Generate Question
    analyst = structyred_llm.invoke([SystemMessage(content=system_message)]+ [HumanMessage(content="Please Generatethe set of analyst")])
    # its only update this part in GenerateAnalystState and everything will be the same 
    return {"analyst" : analyst.analysts}


def human_feedback(state:GenerateAnalystState):
    """this is where human gives feedback about the analysis given"""

    feedback= interrupt({
        "question": "Are this analyst okay for you ?",
        "analysts": [
           i.model_dump() if hasattr(i,"model_dump") else i 
           for i in state.get("analyst",[])          
        ],
        "instrution": "Return feedback to regenerate analyst"
        "or return empty/Perfect/okay/continue to approve and continue the graph "
    })
    if feedback is None:
        return {"human_analyst_feedback":None}
    
    if isinstance(feedback,str) :
        feedback = feedback.strip()
       
        if feedback == "":
            return {"human_analyst_feedback":None}
        
        if feedback.lower() in {"Perfect","okay","yes","continue"}:
            return {"human_analyst_feedback":None}
        
        return {"human_analyst_feedback":feedback}
    
    return {"human_analyst_feedback":None}

