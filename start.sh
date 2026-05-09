#!/bin/bash

# Start FastAPI backend
uvicorn server.main:app --host 0.0.0.0 --port 8080 &

# Start Streamlit frontend
streamlit run client/app.py \
--server.port 8501 \
--server.address 0.0.0.0