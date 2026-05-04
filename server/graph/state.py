from typing import TypedDict , Annotated , Sequence , List
import operator
from langchain_core.messages import BaseMessage

# Defining the state that will be used in langgraph
class AuditState(TypedDict):
    
    # For conversational history 
    messages:Annotated[Sequence[BaseMessage],operator.add]
    
    # For audit
    code_path:str
    current_code:str
    mapping_report:str
    
    vulnerabilities_logs:Annotated[List[str],operator.add]
    verification_logs:str
    
    # Routing Logic / control
    next_step:str
    iter_count:int
    