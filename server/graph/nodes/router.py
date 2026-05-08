from server.graph.state import AuditState
from typing import Literal
from server.logger.logger import logging
from server.exception.exception import CustomException
from langchain_core.prompts import ChatPromptTemplate
from server.core.prompts import ROUTER_PROMPT
import sys
from langchain_core.output_parsers import StrOutputParser
# Main router Node 
def router(state:AuditState , llm):
    """Router node to route the user query to either AUDIT or CHAT"""
    try:
        logging.info('Entered router and initiated the routing request')
        user_query = state['messages'][-1].content

        previous_audit = state.get("aligner_audit_report", "")
        current_code = state.get("current_code", "")

        has_existing_audit = bool(previous_audit.strip())
        has_codebase = bool(current_code.strip())

        router_prompt = ChatPromptTemplate.from_template(ROUTER_PROMPT)

        router_chain = router_prompt | llm | StrOutputParser()

        raw_response = router_chain.invoke({
            'input': user_query,
            'has_existing_audit': has_existing_audit,
            'has_codebase': has_codebase,
            'previous_audit': previous_audit[:3000]
        })

        router_response = raw_response.strip().upper()
        
        logging.info('successfully routed to the next step')
        return {'next_step': router_response}
    except Exception as e:
        logging.error(f'Error while routing the query: {str(e)}')
        raise CustomException(e,sys)
    
# Helper function to return string routed by the router     
def route_after_router(state:AuditState)->Literal['AUDIT','CHAT']:
    return state['next_step']