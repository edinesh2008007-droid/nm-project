"""Gemini Pro - 7-day workout plan generator."""
from app.config import PRO_MODEL_NAME, client
from google.genai.errors import ServerError


def _fallback_workout_plan(intensity: str) -> str:
    effort = {
        "low": "2 rounds at a comfortable pace",
        "medium": "3 rounds, resting as needed",
        "high": "3 controlled rounds, stopping 1-2 reps before failure",
    }.get(intensity.lower(), "2-3 comfortable rounds")
    return f"""Gemini is temporarily unavailable, so this is a basic fallback plan, not a personalized AI plan. Adjust or stop any movement that causes pain.

Day 1 - Lower body
Warm-up: 5 minutes easy walking and leg swings.
Main workout: {effort}: chair squats (8-12 reps), glute bridges (10-15 reps), and calf raises (10-15 reps).
Cooldown: 5 minutes easy walking and gentle leg stretches.

Day 2 - Cardio
Warm-up: 5 minutes easy walking.
Main workout: 20-30 minutes of brisk walking or another comfortable, low-impact activity.
Cooldown: 5 minutes slow walking.

Day 3 - Upper body
Warm-up: 5 minutes easy movement and shoulder circles.
Main workout: {effort}: wall or incline push-ups (6-12 reps), backpack rows (8-12 reps), and bird dogs (8 per side).
Cooldown: 5 minutes of gentle chest and shoulder stretches.

Day 4 - Recovery
Warm-up: 5 minutes easy walking.
Main workout: 15-20 minutes of gentle mobility or relaxed walking.
Cooldown: Slow breathing and comfortable stretching.

Day 5 - Full body
Warm-up: 5 minutes easy walking and arm circles.
Main workout: {effort}: chair squats (8-12 reps), incline push-ups (6-12 reps), and glute bridges (10-15 reps).
Cooldown: 5 minutes easy walking and gentle stretches.

Day 6 - Light cardio
Warm-up: 5 minutes easy walking.
Main workout: 20-30 minutes of comfortable walking or cycling.
Cooldown: 5 minutes slow walking.

Day 7 - Rest
Warm-up: Not needed.
Main workout: Rest, or take a short relaxed walk if you feel good.
Cooldown: Not needed."""


def generate_workout_gemini(user_input: dict) -> str:
    extra = ""
    if user_input.get("age"):
        extra += f" The person is {user_input['age']} years old"
        if user_input.get("weight"):
            extra += f" and weighs {user_input['weight']} kg"
        extra += "."

    prompt = f"""
You are a professional fitness trainer.

Create a personalized, structured 7-day workout plan for someone with the goal of **{user_input['goal']}**, and prefers **{user_input['intensity']}** intensity workouts.{extra}

Each day must include:
- A warm-up (5-10 mins)
- Main workout (targeted exercises, sets & reps)
- Cooldown or recovery tip

Format:
Day 1:
Warm-up: ...
Main Workout: ...
Cooldown: ...
(Repeat for Day 2-7)
"""
    try:
        response = client.models.generate_content(model=PRO_MODEL_NAME, contents=prompt)
        return response.text
    except ServerError as e:
        if e.code == 503:
            return _fallback_workout_plan(user_input.get("intensity", "medium"))
        return f"Error: {e}"
    except Exception as e:
        return f"Error: {e}"
