#!/bin/bash

export PYTHONPATH=$PYTHONPATH:.

PORT=${PORT:-8501}

# Start FastAPI backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 &

# Start Streamlit frontend
streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0