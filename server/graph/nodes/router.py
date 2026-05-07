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
        logging.info('Initiated Routing Query')
        # Taking last user Human Message from message history
        user_query = state['messages'][-1].content
        # Building router prompt
        router_prompt = ChatPromptTemplate.from_template(ROUTER_PROMPT)        
        # Bulding Router chain
        router_chain = router_prompt | llm | StrOutputParser()
        # Feeding user query into input of llm
        raw_response = router_chain.invoke({'input':user_query})
        router_response = raw_response.strip().upper()
        
        logging.info('Router Responded Successfully!')
        # Returning router response as per AUDIT OR CHAT
        return {'next_step':router_response}
    except Exception as e:
        logging.error(f'Error while routing the query: {str(e)}')
        raise CustomException(e,sys)
    
# Helper function to return string routed by the router     
def route_after_router(state:AuditState)->Literal['AUDIT','CHAT']:
    return state['next_step']