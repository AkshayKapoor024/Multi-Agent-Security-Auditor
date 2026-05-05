from server.graph.state import AuditState
from typing import Literal
from server.logging.logger import logging
from server.exception.exception import CustomException
from langchain_core.prompts import ChatPromptTemplate
from server.core.prompts import ATTACKER_PROMPT
import sys
from langchain_core.output_parsers import StrOutputParser
import json
import re

# Main attacker node 
def attacker(state:AuditState , llm ):
    """Main attacker node responsible for finding possible attacks via finding vulnerabilities"""
    
    try:
        # Retrieving current code base
        codebase = state['current_code']
        
        # Retrieving mapping report
        mapping_report = state['mapping_report']
        
        logging.info('Entered Attacker and started attacking process')
        
        # Developing attacker prompt
        attacker_prompt = ChatPromptTemplate.from_template(ATTACKER_PROMPT)
        
        # Defining attacker chain
        attacker_chain = attacker_prompt | llm | StrOutputParser()
        
        # Retrieving attacker llm response
        attacker_response = attacker_chain.invoke({"mapping_report":mapping_report , "current_code":codebase})
        
        # Cleaning/Sanitizing response to get proper JSON format
        clean_json_response = json.loads(re.sub(r",\s*([\]}])", r"\1", attacker_response.strip()))
        
        logging.info(f"Successfully generated {len(clean_json_response)} vulnerabilities using attacker")    
        
        return {'vulnerabilities_logs':clean_json_response}
    except Exception as e:
        logging.error(f'Error while generating vulnerabilty logs using attacker node {str(e)}')
        raise CustomException(e,sys)