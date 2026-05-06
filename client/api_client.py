import requests
import streamlit as st
import os 
from dotenv import load_dotenv
load_dotenv()
BACKEND_URL = os.getenv('BACKEND_URL')

# Function that fetches responses from the backend and return responses to the client
def fetch_audit_response(query: str):
    try:
        response = requests.post(
            BACKEND_URL, 
            json={"query": query},
            timeout=300  # Longer timeout for deep audits
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Connection failed: {str(e)}")
        return None