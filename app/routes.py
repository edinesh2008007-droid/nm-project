"""All FastAPI routes: HTML pages + JSON API endpoints."""
import os

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError

from app.database import (
    delete_user,
    get_all_users_with_plans,
    get_latest_plan,
    get_original_plan,
    get_user,
    save_plan,
    save_user,
    update_plan,
)
from app.gemini_flash_generator import generate_nutrition_tip_with_flash
from app.gemini_generator import generate_workout_gemini
from app.nutrition import get_fallback_tip
from app.schemas import FeedbackRequest, UserInput, WorkoutRequest
from app.updated_plan import update_workout_plan

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
templates = Jinja2Templates(directory=TEMPLATE_DIR)


def get_tip(goal: str) -> str:
    tip = generate_nutrition_tip_with_flash(goal)
    return get_fallback_tip(goal) if tip.startswith("Error") else tip


# ---------------------------------------------------------------- Web pages
@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request, "index.html", {"error": None})


@router.post("/generate-workout", response_class=HTMLResponse)
def generate_workout(
    request: Request,
    username: str = Form(...),
    user_id: int = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
):
    try:
        data = UserInput(username=username, user_id=user_id, age=age,
                         weight=weight, goal=goal, intensity=intensity)
    except ValidationError as e:
        msg = "; ".join(f"{err['loc'][-1]}: {err['msg']}" for err in e.errors())
        return templates.TemplateResponse(request, "index.html", {"error": msg})

    plan = generate_workout_gemini({
        "goal": data.goal, "intensity": data.intensity,
        "age": data.age, "weight": data.weight,
    })
    if plan.startswith("Error"):
        return templates.TemplateResponse(request, "index.html", {"error": plan})

    tip = get_tip(data.goal)

    save_user(user_id=data.user_id, name=data.username, age=data.age,
              weight=data.weight, goal=data.goal, intensity=data.intensity)
    save_plan(data.user_id, plan)

    return templates.TemplateResponse(request, "result.html", {
        "username": data.username,
        "user_id": data.user_id,
        "age": data.age,
        "weight": data.weight,
        "goal": data.goal,
        "intensity": data.intensity,
        "workout_plan": plan,
        "nutrition_tip": tip,
        "message": None,
        "error": None,
    })


@router.post("/submit-feedback", response_class=HTMLResponse)
def submit_feedback(request: Request, user_id: int = Form(...), feedback: str = Form(...)):
    user = get_user(user_id)
    current_plan = get_latest_plan(user_id)
    if not user or not current_plan:
        return templates.TemplateResponse(request, "index.html", {
            "error": f"No plan found for User ID {user_id}. Generate a plan first."})

    updated = update_workout_plan(current_plan, feedback)
    if updated.startswith("Error"):
        return templates.TemplateResponse(request, "result.html", {
            "username": user.name, "user_id": user.id, "age": user.age,
            "weight": user.weight, "goal": user.goal, "intensity": user.intensity,
            "workout_plan": current_plan, "nutrition_tip": get_fallback_tip(user.goal),
            "message": None, "error": updated,
        })

    update_plan(user_id, updated)
    return templates.TemplateResponse(request, "result.html", {
        "username": user.name,
        "user_id": user.id,
        "age": user.age,
        "weight": user.weight,
        "goal": user.goal,
        "intensity": user.intensity,
        "workout_plan": updated,
        "nutrition_tip": get_tip(user.goal),
        "message": "Your plan has been updated based on your feedback!",
        "error": None,
    })


@router.get("/view-all-users", response_class=HTMLResponse)
def view_all_users(request: Request):
    return templates.TemplateResponse(request, "all_users.html",
                                      {"users": get_all_users_with_plans()})


@router.post("/delete-user/{user_id}")
def remove_user(user_id: int):
    delete_user(user_id)
    return RedirectResponse(url="/view-all-users", status_code=303)


# ------------------------------------------------------------ JSON API routes
# 1. Generate workout using Gemini Pro
@router.post("/generate-workout/gemini")
def generate_gemini_workout(request: WorkoutRequest):
    try:
        result = generate_workout_gemini({"goal": request.goal, "intensity": request.intensity})
        return {"model": "gemini-pro", "workout_plan": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 2. Generate nutrition tip using Gemini Flash
@router.get("/nutrition-tip")
def get_flash_tip(goal: str):
    return {"goal": goal, "nutrition_tip": generate_nutrition_tip_with_flash(goal)}


# 3. Save user info & generate plan
@router.post("/generate-plan")
def generate_plan(user_data: UserInput):
    try:
        save_user(
            user_id=user_data.user_id,
            name=user_data.username,
            age=user_data.age,
            weight=user_data.weight,
            goal=user_data.goal,
            intensity=user_data.intensity,
        )
        plan = generate_workout_gemini({
            "goal": user_data.goal,
            "intensity": user_data.intensity,
            "age": user_data.age,
            "weight": user_data.weight,
        })
        save_plan(user_data.user_id, plan)
        return {"message": "Workout plan generated and saved successfully!", "workout_plan": plan}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {str(e)}")


# 4. Update workout plan based on user feedback
@router.post("/update-plan/{user_id}", response_model=dict)
def update_user_plan(user_id: int, data: FeedbackRequest):
    original = get_original_plan(user_id)
    if not original:
        return {"error": "Original plan not found for this user."}
    updated = update_workout_plan(get_latest_plan(user_id) or original, data.feedback)
    update_plan(user_id, updated)
    return {"updated_plan": updated}
