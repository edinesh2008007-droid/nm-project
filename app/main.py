"""FastAPI entry point. Run from the project root:  uvicorn app.main:app --reload"""
import os
from dotenv import load_dotenv

# Load environment variables before importing the router.
load_dotenv()

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes import router

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI(title="FitBuddy - AI Fitness Plan Generator")
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
app.include_router(router)