# server/core/llms.py

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# =========================
# GOOGLE MODELS (FALLBACK CHAIN)
# =========================
GEMINI_MODELS = [
    "gemini-flash-latest",
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-flash-lite-latest",
    "gemini-pro-latest"
]

def get_gemini_llm(model_name: str):
    return ChatGoogleGenerativeAI(
        google_api_key=GOOGLE_API_KEY,
        model=model_name,
        temperature=0
    )

# =========================
# GROQ MODELS
# =========================
def get_groq_llm(model_name: str):
    return ChatGroq(
        api_key=GROQ_API_KEY,
        model=model_name,
        temperature=0
    )

# =========================
# PREDEFINED INSTANCES
# =========================

# Google fallback chain
gemini_llms = [get_gemini_llm(m) for m in GEMINI_MODELS]

# Groq models
groq_primary = get_groq_llm("llama-3.3-70b-versatile")
groq_backup = get_groq_llm("mixtral-8x7b-32768")