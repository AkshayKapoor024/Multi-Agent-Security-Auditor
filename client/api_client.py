import requests
import streamlit as st
import os 
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv('BACKEND_URL')

# Creating a single session object
session = requests.Session()


# Function to perform authentication check
def checkauth_user():
    try:
        response = session.get(
            f'{BACKEND_URL}/isAuthenticated',
            timeout=30
        )

        return response

    except Exception as e:
        st.error(f'Connection Failed: {str(e)}')
        return None


# Function to logout user
def logout_user():
    try:
        response = session.post(
            f'{BACKEND_URL}/logout',
            timeout=30
        )

        return response

    except Exception as e:
        st.error(f'Connection Failed: {str(e)}')
        return None


# Function to login user
def login_user(user):
    try:
        response = session.post(
            f'{BACKEND_URL}/login',
            json=user,
            timeout=30
        )

        return response

    except Exception as e:
        st.error(f'Connection Failed: {str(e)}')
        return None


# Function to signup user
def signup_user(user):
    try:
        response = session.post(
            f'{BACKEND_URL}/signup',
            timeout=30,
            json=user
        )

        return response

    except Exception as e:
        st.error(f'Connection Failed: {str(e)}')
        return None


# Function to fetch all user chat histories
def get_full_chat_history():
    try:
        response = session.post(
            f'{BACKEND_URL}/getFullHistory',
            timeout=30
        )

        return response

    except Exception as e:
        st.error(f'Connection Failed: {str(e)}')
        return None


# Function to fetch a particular chat history
def get_chat_history(chat_id: str):
    try:
        response = session.post(
            f'{BACKEND_URL}/getHistory',
            json={
                "chatid": chat_id
            },
            timeout=30
        )

        return response

    except Exception as e:
        st.error(f'Connection Failed: {str(e)}')
        return None


# Requests function to fetch AI response from backend
def fetch_ai_response(query: str, conversational_id=None):
    try:
        response = session.post(
            f'{BACKEND_URL}/agent',
            json={
                "query": query,
                "conversational_id": conversational_id
            },
            timeout=600
        )

        return response

    except Exception as e:
        st.error(f"Connection failed: {str(e)}")
        return None