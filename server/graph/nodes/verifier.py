from server.graph.state import AuditState
from typing import Literal
from server.logging.logger import logging
from server.exception.exception import CustomException
from langchain_core.prompts import ChatPromptTemplate
from server.core.prompts import VERIFIER_PROMPT
import sys
from langchain_core.output_parsers import StrOutputParser
from server.tools.code_cleaner import clean_llm_code
from server.tools.code_executor import execute_code_in_sandbox

# Main verifier node 
def verifier(state:AuditState , llm ):
    """Main verifier node that verifies attacker hypothesis by creating possible buggy code running sandbox and then updating logs"""
    try:
        logging.info('Entered verifier node and starting verification process!')
        # Retrieving current code
        current_code = state['current_code']
        
        # Retrieving vulnerability logs
        vulnerability_log = state.get('latest_vulnerability')
        
        if not vulnerability_log:
            logging.warning("No specific vulnerability found in state for this verifier instance.")
            return {"verification_logs": ["No test conducted."]}
        
        # Defining verifier prompt template
        verifier_prompt = ChatPromptTemplate.from_template(VERIFIER_PROMPT)
        
        # Defining verifier chain
        verifier_chain = verifier_prompt | llm | StrOutputParser()
        
        # Retrieving verifier Response
        verifier_response = verifier_chain.invoke({'current_code':current_code,'latest_vulnerability':vulnerability_log})
        logging.info('Successfully got verifier response')
        
        # Cleaning LLM code response using cleaner tool 
        cleaned_verifier_response = clean_llm_code(verifier_response)
        
        # Running code on sandbox and getting report using tool
        verification_report = execute_code_in_sandbox(cleaned_verifier_response)
        logging.info('Successfully got verification report')
        
        # 1. Format the dictionary into a readable block for the LLM
        formatted_report = (
            f"STDOUT:\n{verification_report.get('stdout', 'None')}\n"
            f"STDERR:\n{verification_report.get('stderr', 'None')}\n"
            f"EXIT_CODE: {verification_report.get('exit_code', 'Unknown')}"
        )
        
        # Returning verification report
        return {'verification_logs': [f"--- VERIFICATION LOG FOR: {vulnerability_log[:100]} ---\n{formatted_report}"]}
    except Exception as e:
        logging.info(f'Error while generating verification report : {str(e)}')
        raise CustomException(e,sys)