from server.graph.state import AuditState
from typing import Literal
from server.logger.logger import logging
from server.exception.exception import CustomException
from langchain_core.prompts import ChatPromptTemplate
from server.core.prompts import ASSISTANT_PROMPT
import sys
from langchain_core.output_parsers import StrOutputParser

# Main Aligner function
def assistant(state:AuditState ,llm ):
    try:
        """Assistant answers user queries in a professional way"""
        logging.info('Entered assistant node and started responding to client outputs')
        # Retrieving aligner audit report
        latest_report = state.get('aligner_audit_report', 'No audit performed yet.')
                
        # Retrieving full chat history
        message_history = state['messages']
        
        # Retreiving code base
        current_code = state.get('current_code', 'No codebase loaded yet.')
        
        # Retrieving current query
        user_query = state['messages'][-1]
        
        # Defining assistant prompt template
        assistant_prompt = ChatPromptTemplate.from_template(ASSISTANT_PROMPT)
        
        # Defining assistant _chain
        assistant_chain = assistant_prompt | llm
        
        # Retrieving Assistant results
        assistant_response = assistant_chain.invoke({'current_code':current_code,'chat_history':message_history,'latest_audit_report':latest_report,'input':user_query})
        logging.info('Assistant responded successfully.')
        
        return {'messages':[assistant_response]}
    except Exception as e:
        logging.info(f'Error while generating Assistant response {str(e)}')
        raise CustomException(e,sys)

