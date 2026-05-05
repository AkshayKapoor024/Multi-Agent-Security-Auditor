from server.graph.state import AuditState
from typing import Literal
from server.logging.logger import logging
from server.exception.exception import CustomException
from langchain_core.prompts import ChatPromptTemplate
from server.core.prompts import REPORTER_PROMPT
import sys
from langchain_core.output_parsers import StrOutputParser

# Main Reporter function
def reporter(state:AuditState ,llm ):
    try:
        """Reporter generates AUDIT report draft based on verificationLogs vulnerability logs and currentcode"""
        logging.info('Entered reporter node and started generating draft audit report')
        # Retrieving verification logs
        verification_logs = state['verification_logs']
        
        # Retrieving vulnerability logs
        vulnerabilities_logs = state['vulnerabilities_logs']
        
        # Retrieving current code
        current_code = state['current_code']
        
        # Defining reporter prompt template
        reporter_prompt = ChatPromptTemplate.from_template(REPORTER_PROMPT)
        
        # Defining reporter_chain
        reporter_chain = reporter_prompt | llm | StrOutputParser()
        
        # Retrieving reporter audit report
        reporter_response = reporter_chain.invoke({'current_code':current_code,'vulnerabilities_logs':vulnerabilities_logs,'verification_logs':verification_logs})
        logging.info('Successfully generated draft audit report')
        
        return {'reporter_audit_report':reporter_response}
    except Exception as e:
        logging.info(f'Error while generating draft report {str(e)}')
        raise CustomException(e,sys)

