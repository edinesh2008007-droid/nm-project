🏋️‍♂️ FitBuddy – AI Fitness Plan Generator
FitBuddy is an AI-powered web application designed to generate personalized 7-day workout plans and tailored nutrition or recovery tips based on individual user fitness goals, age, weight, and preferred exercise intensity.   
PDF

Built with FastAPI, SQLite, and integrated with Google's Gemini 1.5 Pro & Gemini Flash AI models, FitBuddy provides dynamic, goal-oriented fitness guidance that adapts to user feedback over time.   
PDF
+ 3

✨ Features
🏋️ Personalized 7-Day Workout Plans: Generates structured day-by-day routines (including warm-ups, main workouts, and cool-downs) powered by Gemini 1.5 Pro.   
PDF

🥗 Targeted Nutrition & Recovery Tips: Delivers fast, goal-aligned nutrition suggestions using Gemini Flash.   
PDF

🔄 Feedback-Driven Plan Refinement: Allows users to submit feedback (e.g., "add more cardio", "include yoga") to instantly update and regenerate their routine.   
PDF

📊 Admin Dashboard: Enables trainers or administrators to view all registered users alongside their original and updated plans via /view-all-users.   
PDF

💾 Data Persistence: Uses SQLite and SQLAlchemy ORM to save user profiles and workout plan histories securely.   
PDF

🛠️ Tech Stack & Architecture
Backend: FastAPI (Python)   
PDF

Frontend: HTML5, CSS3, Jinja2 Templating   
PDF

Database: SQLite with SQLAlchemy ORM   
PDF

AI Models:

Gemini 1.5 Pro (Detailed workout generation & updates)   
PDF

Gemini Flash (Fast nutrition & recovery tip generation)   
PDF

ASGI Server: Uvicorn   
PDF

📁 Project Structure
Plaintext
fitbuddy/
│
├── requirements.txt           # Project dependencies
├── fitbuddy.db                # SQLite database (auto-generated)
│
├── app/
│   ├── main.py                # FastAPI app entry point
│   ├── routes.py              # Application route handlers
│   ├── database.py            # Database setup & SQLAlchemy models
│   ├── schemas.py             # Pydantic data schemas
│   ├── gemini_generator.py    # Gemini 1.5 Pro workout generator
│   ├── gemini_flash_generator.py # Gemini Flash nutrition tip generator
│   ├── updated_plan.py        # Feedback plan updater
│   └── nutrition.py           # Nutrition logic module
│
├── templates/
│   ├── index.html             # User input form
│   ├── result.html            # Workout plan, tip & feedback form
│   └── all_users.html          # Admin dashboard
│
└── static/
    └── images/
        └── gym-bg.jpg         # App background image
   
PDF

🚀 Getting Started
Prerequisites
Python 3.8+ installed   
PDF

A Google Gemini API Key   
PDF

Installation
Clone the Repository:

Bash
git clone https://github.com/your-username/fitbuddy.git
cd fitbuddy
Create and Activate a Virtual Environment:

Windows:

Bash
python -m venv fitbuddy-env
fitbuddy-env\Scripts\activate
Linux/macOS:

Bash
python3 -m venv fitbuddy-env
source fitbuddy-env/bin/activate
   
PDF

Install Dependencies:

Bash
pip install fastapi uvicorn jinja2 sqlalchemy python-multipart google-generativeai python-dotenv
   
PDF

Set Up Environment Variables:
Create a .env file in the root directory and add your Google Gemini API key:   
PDF

Code snippet
GOOGLE_API_KEY=your_gemini_api_key_here
   
PDF

Run the Application:

Bash
uvicorn app.main:app --reload
   
PDF

Access the App:

Web Interface: Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.   
PDF

Interactive API Docs: Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).   
PDF

Admin Dashboard: Visit [http://127.0.0.1:8000/view-all-users](http://127.0.0.1:8000/view-all-users).   
PDF

Made by Sai Pretesh