from typing import TypedDict , Annotated , List
import operator
from langgraph.graph.message import add_messages

# Defining the state that will be used in langgraph
class AuditState(TypedDict):
    
    # For conversational history 
    messages:Annotated[list,add_messages]
    
    # For audit
    dicovered_files:List[str]
    current_code:str
    mapping_report:str
    
    vulnerabilities_logs:Annotated[List[str],operator.add]
    verification_logs:Annotated[List[str],operator.add]
    reporter_audit_report:str
    aligner_audit_report:str
    # Routing Logic / control
    next_step:str
    iter_count:int
    