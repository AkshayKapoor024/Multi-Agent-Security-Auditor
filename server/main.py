import os 
import sys

import certifi
certifi.where()
import json

from pydantic import BaseModel

from server.logging.logger import logging
from server.graph.graph import graph_builder
from langchain_core.messages import HumanMessage

from server.schemas.user import User
from server.schemas.login_user import LoginUser


from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi import FastAPI,Request
from uvicorn import run as app_run
from fastapi.responses import RedirectResponse , JSONResponse
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory='./templates')
from bson import ObjectId

from server.core.mongo import users , sessions , chat_history
from server.tools.password_hashing import hash_password , verify_password

from dotenv import load_dotenv
load_dotenv()
SESSION_KEY = os.getenv('SESSION_SECRET_KEY')
# Setting Up FastAPI APP
app = FastAPI()

# Adding session middlewares
app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_KEY,
    session_cookie="vantaguard_session",
    max_age=10000
    # https_only=True
    # same_site="lax"
)

# Adding cors middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

# Defining signup logic
@app.post('/signup',tags=['Signup'])
async def signup(request:Request,user:User):
    try:
        # Checking if user already exists
        if users.find_one({'email':user.email}):
            return JSONResponse(content={'error':'User already exists'},status_code=400)
        
        # Hashing user password
        hashed_password = hash_password(password=user.password)

        # Entering user to Mongodb
        users.insert_one({
            'name':user.name,
            'username':user.username,
            'email':user.email,
            'password':hashed_password
        })
        
        # AutoLogin the user after signup
        inserted_user = users.find_one({"email": user.email})
        request.session["user"] = str(inserted_user["_id"])
        
        # Returning JSON response
        return JSONResponse(content={
                'message':'User signup successful',
                "user": {
                "name": inserted_user["name"],
                "email": inserted_user["email"],
                "username": inserted_user["username"]
            }},status_code=200)
    except Exception as e:
        logging.error(f'Error while signing user up : {str(e)}')
        return JSONResponse(content={'error':str(e)} , status_code=500)

# Defining post request route 
@app.post('/login',tags=['Login'])
async def login(request:Request,user:LoginUser):
    try:
        # Retrieving stored user
        db_user = users.find_one({"email":user.email})
        
        # Checking if user doesn't exist or password didnt match
        if not db_user:
            return JSONResponse(content={"error":"User does not exist"},status_code=400)
        elif not verify_password(plain=user.password,hashed=db_user['password']):
            return JSONResponse(content={'error':'Password did\'nt match the original password'},status_code=400)
        else:
            
            # Creating session
            request.session['user']=str(db_user['_id'])
            
            # sessions_data = dict(request.session)
            # Storing sessions inside session collection            
            # sessions.insert_one(
            #     {
            #         'session_id':sessions_data,
            #         'user_id':db_user['_id']
            #     }
            # )
            
            return JSONResponse(content={
                'message':'User login successful',
                "user": {
                "name": db_user["name"],
                "email": db_user["email"],
                "username": db_user["username"]
            }},status_code=200)
    except Exception as e:
        logging.error(f'Error while logging user in : {str(e)}')
        return JSONResponse(content={'error':str(e)},status_code=500)


# Defining Logout route
@app.post('/logout')
async def logout(request:Request):
    try:
        request.session.clear()
        return JSONResponse(content={'message':'User logged out successfully'},status_code=200)
    except Exception as e:
        return JSONResponse(content={'error':str(e)},status_code=500)




@app.get("/isAuthenticated", tags=["Authentication"])
async def get_me(request: Request):

    user_id = request.session.get("user")

    if not user_id:
        return JSONResponse(
            content={"authenticated": False},
            status_code=401
        )

    db_user = users.find_one({"_id": ObjectId(user_id)})

    if not db_user:
        request.session.clear()

        return JSONResponse(
            content={"authenticated": False},
            status_code=401
        )

    return JSONResponse(
        content={
            "authenticated": True,
            "user": {
                "name": db_user["name"],
                "email": db_user["email"],
                "username": db_user["username"]
            }
        },
        status_code=200
    )


# Getting Structured output in body

# Defining Schema for the incoming request
class AI(BaseModel):
    query:str
    
# Main Conversational Route
@app.post('/agent',tags=['Generate_Audit_Report'])
async def agent_call(request_data:AI):
    try:
        # Getting query from the user 
        query = request_data.query
        
        # Encapsulating Client query inside human message
        query_message = HumanMessage(content=query)
        
        # Invoking graph to get response
        response = graph.invoke({'messages':[query_message]})

        # Getting AI Response based on type of chat
        if response.get('next_step')=='AUDIT':
            return JSONResponse(
                content={'message':response.get('aligner_audit_report')},
                status_code=200
            )
        elif response.get('next_step')=='CHAT':
            return JSONResponse(
                content = {'message':response.get('messages')[-1].content},
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