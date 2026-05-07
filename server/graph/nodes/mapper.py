from server.graph.state import AuditState
from typing import Literal
from server.logger.logger import logging
from server.exception.exception import CustomException
from langchain_core.prompts import ChatPromptTemplate
from server.core.prompts import MAPPER_PROMPT
import sys
from langchain_core.output_parsers import StrOutputParser
from server.tools.github_repo_loader import get_codebase_from_github

# Main mapper node
def mapper(state:AuditState,llm):
    """analyze the current_code and identify the specific "Sinks" (vulnerable functions) and "Sources" to guide the Attacker."""
    try:
        # Retrieving last user query
        logging.info('Entered Mapper and started Mapping')
        
        # retrieving last user query
        user_input = state['messages'][-1].content
        
        # Creating url retriever prompt for mapper
        url_prompt = """
        You are expert at determining and finding links from an input message from user . Provided an input query from the user you have to analyze the input and strictly retrieve github repository url from the input . 
        
        **IMPORTANT INSTRUCTIONS**
        1.You strictly have to just return the associated github repository url with the query , No commas , no seperators , no formatting just pure url string nothing else .
        2.If a user input does not have a github url , Strictly return 'Provided input does not have a github url . Please provide github url'
        
        Input query: {input}
        """
        
        # Creating url retriever chain
        url_retriever_chain = ChatPromptTemplate.from_template(url_prompt) | llm | StrOutputParser()
        
        # Getting response from the repository link retriever
        url_retriever_response = url_retriever_chain.invoke({'input':user_input})
        
        # Check if response contains a github url or not
        if ("https://github.com/" in url_retriever_response):
            logging.info('Retrieved URL for mapping successfully')
            # Retrieving codebase from the url , branch is default main
            current_code = get_codebase_from_github(url_retriever_response)
            
            # Defining chat prompt template for mapper
            prompt_template = ChatPromptTemplate.from_template(MAPPER_PROMPT)
            
            # defining mapper chain
            mapper_chain = prompt_template | llm  | StrOutputParser()
            
            # Retrieving mapper response 
            mapper_response = mapper_chain.invoke({'current_code':current_code}).strip()
            logging.info('Mapping report generated successfully')
            return {'mapping_report':mapper_response , 'current_code':current_code}
        # Else return error and donot change or return state   
        else:
            raise CustomException('No github URL found in input .',sys)
    except Exception as e:
        logging.error(f'Exception occured while mapping codebase : {str(e)}')
        raise CustomException(e,sys)
