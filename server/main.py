import os 
import sys

import certifi
certifi.where()
import json

from pydantic import BaseModel

from server.logging.logger import logging
from server.graph.graph import graph_builder
from langchain_core.messages import HumanMessage

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI,File,UploadFile,Request
from uvicorn import run as app_run
from fastapi.responses import Response,RedirectResponse , JSONResponse
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory='./templates')

# Setting Up FastAPI APP
app = FastAPI()
origins=['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=True,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

# Initialize the graph ONCE at startup
try:
    logging.info("Initializing LangGraph workflow...")
    graph = graph_builder()
except Exception as e:
    logging.error(f"Failed to build graph: {str(e)}")
    raise e


@app.get('/',tags=['authentication'])
async def index():
    
    return RedirectResponse(url='/docs')

# Getting Structured output in body

# Defining Schema for the incoming request
class AI(BaseModel):
    query:str
    
# Main Conversational Route
app.post('/agent',tags=['Generate_Audit_Report'])
async def agent_call(request_data:AI):
    try:
        # Create graph if does not exist
        if not graph:
            graph=graph_builder()
        
        
        # Getting query from the user 
        query = request_data.query
        
        # Encapsulating Client query inside human message
        query_message = HumanMessage(content=query)
        
        # Invoking graph to get response
        response = graph.invoke({'messages':[query_message]})

        # Getting AI Response based on type of chat
        if response.get('next_step')=='AUDIT':
            return JSONResponse(
                content={'app_response':response.get('aligner_audit_report')},
                status_code=200
            )
        elif response.get('next_step')=='CHAT':
            return JSONResponse(
                content = {'app_response':response.get('messages')[-1].content},
                status_code=200,
            )
        else:
            return JSONResponse(
                content={'error':'Error while generating AI response . Please try again'},
                status_code=400
            )
    # Using except to return internal server error
    except Exception as e:
        return JSONResponse(
            content={'error':str(e)},
            status_code=500
        )

if __name__=='__main__':
    app_run(app,host='0.0.0.0',port=8080)