import requests
import streamlit as st
import os 
from dotenv import load_dotenv
load_dotenv()
BACKEND_URL = os.getenv('BACKEND_URL')

# Function that fetches responses from the backend and return responses to the client

# Creating a single session object
session = requests.Session()

# Function to perform signup authentication
def checkauth_user():
    try:
        response =session.get(
            f'{BACKEND_URL}/isAuthenticated',
            timeout=30
        )
        
        # Return request body even if error occured cause error also in body
        return response
    except Exception as e:
        st.error(f'Connection Failed: {str(e)}')
        return None


# Function to perform signup authentication
def logout_user():
    try:
        response =session.post(
            f'{BACKEND_URL}/logout',
            timeout=30
        )
        
        return response
    except Exception as e:
        st.error(f'Connection Failed: {str(e)}')
        return None

# Function to perform signup authentication
def login_user(user):
    try:
        response =session.post(
            f'{BACKEND_URL}/login',
            json=user,
            timeout=30
        )
        # Return request body even if error occured cause error also in body
        return response
    except Exception as e:
        st.error(f'Connection Failed: {str(e)}')
        return None

# Function to perform signup authentication
def signup_user(user):
    try:
        response =session.post(
            f'{BACKEND_URL}/signup',
            timeout=30,
            json=user
        )
        # Return request body even if error occured cause error also in body
        return response
    except Exception as e:
        st.error(f'Connection Failed: {str(e)}')
        return None

# Requests function to fetch AI response from the client
def fetch_ai_response(query: str):
    try:
        response =session.post(
            f'{BACKEND_URL}/agent', 
            json={"query": query},
            timeout=600  # Longer timeout for deep audits
        )
        if response.status_code == 200:
            return response
        else:
            return response
    except Exception as e:
        st.error(f"Connection failed: {str(e)}")
        return None