from dotenv import load_dotenv
from langchain_tavily import TavilySearch
from .objects import Analyst,Perspective,SearchQuery
from .states import GenerateAnalystState,InterviewState
from .models import llm
from langchain.messages import SystemMessage,HumanMessage
from .prompts import analyst_instructions,question_instructions,search_instructions,answer_instructions,section_writer_instructions
from langgraph.types import interrupt
from langchain_core.messages import get_buffer_string
load_dotenv()

#nodes 
def create_analysts(state: GenerateAnalystState): 
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

def human_feedback(state: GenerateAnalystState):
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

def generate_question(state: InterviewState):

    """node to generate the question"""

    analyst = state["analyst"]

    if isinstance(analyst,dict):
        analyst = Analyst.model_validate(analyst)

    # we need to understand this later something related to reducers
    messages = state["messages"]

    #generate question 
    system_message = question_instructions.format(goals = analyst.persona)
    question = llm.invoke([SystemMessage(content=system_message)] + messages)
    
    return {"messages" : [question]}

def search_web1(state:InterviewState):
    """Reteived docs from the web"""
    
    # SEARCH QUERY
    structed_llm = llm.with_structured_output(SearchQuery)

    tavily_search = TavilySearch(max_result=3)

    #SYSTEM MESSAGE WITH SEARCH INSTRUCTION
    system_message = search_instructions.format()

    search_q = structed_llm.invoke([SystemMessage(content=system_message)] + state["messages"])

    #search 
    data = tavily_search.invoke({"query":search_q.search_query})
    search_docs = data.get("result" , data)

    #format

    formatted_search_docs = "\n\n---\n\n".join(
        [
            f'<Document href="{doc["url"]}"/>\n{doc["content"]}\n</Document>'
            for doc in search_docs
        ]
    )

    return {"context": [formatted_search_docs]}

def search_web2(state:InterviewState):
    """Reteived docs from the web"""
    
    # SEARCH QUERY
    structed_llm = llm.with_structured_output(SearchQuery)

    tavily_search = TavilySearch(max_result=3)

    #SYSTEM MESSAGE WITH SEARCH INSTRUCTION
    system_message = search_instructions.format()

    search_q = structed_llm.invoke([SystemMessage(content=system_message)] + state["messages"])

    #search 
    data = tavily_search.invoke({"query":search_q.search_query})
    search_docs = data.get("result" , data)

    #format

    formatted_search_docs = "\n\n---\n\n".join(
        [
            f'<Document href="{doc["url"]}"/>\n{doc["content"]}\n</Document>'
            for doc in search_docs
        ]
    )

    return {"context": [formatted_search_docs]}

def generate_answer(state:InterviewState):
    """Node to answer a question"""

    analyst = state["analyst"]
    context = state["context"]
    message = state["messages"]

    if isinstance(analyst,dict):
        analyst = Analyst.model_validate(analyst)

    #answer question 

    system_message = answer_instructions.format(goals = analyst.persona , context = context)
    answer = llm.invoke([SystemMessage(content=system_message)] + message)

    #name the message as coming from expert 
    answer.name = "expert"

    #append state 
    return {"message":[answer]}

def save_interview(state:InterviewState):
    """save interviews"""

    message = state["messages"]

    interview =  get_buffer_string(message)

    return {"interview": interview}

def write_section(state:InterviewState):
    """Node to answer a question"""

    interview = state["interview"]
    context = state["context"]
    analyst = state["analyst"]

    if isinstance(analyst,dict):
        analyst = Analyst.model_validate(analyst)

    system_message = section_writer_instructions.format(focus = analyst.description)

    section = llm.invoke([SystemMessage(content=system_message)] +
                          [HumanMessage(content=f"Use This ource To Write Your Section :{context}")])

    return {"sections":section.content}

    