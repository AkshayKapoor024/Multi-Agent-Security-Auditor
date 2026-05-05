from typing import TypedDict , Annotated , Sequence , List
import operator
from langchain_core.messages import BaseMessage

# Defining the state that will be used in langgraph
class AuditState(TypedDict):
    
    # For conversational history 
    messages:Annotated[Sequence[BaseMessage],operator.add]
    
    # For audit
    dicovered_files:List[str]
    current_code:str
    mapping_report:str
    
    vulnerabilities_logs:Annotated[List[str],operator.add]
    verification_logs:Annotated[List[str],operator.add]
    
    # Routing Logic / control
    next_step:str
    iter_count:int
    