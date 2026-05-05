from langgraph.graph import START,END,StateGraph
from server.graph.state import AuditState
from server.graph.nodes.router import router , route_after_router
from server.graph.nodes.mapper import mapper
from server.graph.nodes.attacker import attacker
from server.graph.nodes.verifier import verifier
from server.graph.nodes.reporter import reporter
from server.graph.nodes.aligner import aligner
from server.graph.nodes.assistant import assistant
from server.graph.edges import continue_to_verification
from functools import partial

import os
from dotenv import load_dotenv
load_dotenv()
from server.core.llms import groq_with_fallback

from server.logging.logger import logging
from server.exception.exception import CustomException
import sys

# Main graph builder function
def graph_builder():
    try:
        logging.info('Started Building Graph')
        # Defining  workflow
        workflow = StateGraph(AuditState)

        # Adding nodes
        workflow.add_node('router',partial(router,llm=groq_with_fallback))
        workflow.add_node("mapper", partial(mapper, llm=groq_with_fallback))
        workflow.add_node("attacker", partial(attacker, llm=groq_with_fallback))
        workflow.add_node("verifier", partial(verifier, llm=groq_with_fallback))
        workflow.add_node("reporter", partial(reporter, llm=groq_with_fallback))
        workflow.add_node("aligner", partial(aligner, llm=groq_with_fallback))
        workflow.add_node("assistant", partial(assistant, llm=groq_with_fallback))
        
        logging.info('Added nodes successfully')
        # Defining Edges
        
        workflow.add_edge(START,'router')
        # Adding conditional edge to create audit report or chat 
        workflow.add_conditional_edges('router',route_after_router,{'AUDIT':'mapper','CHAT':'assistant'})
        
        workflow.add_edge('mapper','attacker')
        
        workflow.add_conditional_edges('attacker',continue_to_verification,['verifier','reporter'])
        
        workflow.add_edge('verifier','reporter')
        
        workflow.add_edge('reporter','aligner')
        
        workflow.add_edge('aligner',END)
        
        # 6. CHAT PATH: Assistant responds and ends (or loops back to START)
        workflow.add_edge('assistant', END)
        
        logging.info('Added edges successfully')
        # Compiling graph
        graph = workflow.compile()
        
        logging.info('Graph compiled and returned successfully')
        return graph
    except Exception as e:
        logging.error(f'Exception occured while building graph: {str(e)}')    
        raise CustomException(e,sys)