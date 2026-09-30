"""Loads the API key and creates the Gemini API client."""
import os

from google import genai
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
PRO_MODEL_NAME = os.getenv("GEMINI_PRO_MODEL", "gemini-3.1-pro-preview")
FLASH_MODEL_NAME = os.getenv("GEMINI_FLASH_MODEL", "gemini-3.5-flash")

client = genai.Client(api_key=API_KEY)