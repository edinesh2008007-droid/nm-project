"""Gemini Pro - revise an existing plan using user feedback."""
from app.config import PRO_MODEL_NAME, client


def update_workout_plan(original_plan: str, user_feedback: str) -> str:
    """Use Gemini Pro to update the workout plan based on user feedback."""
    prompt = f"""
You are a professional fitness trainer assistant.

Here's the original 7-day workout plan:
{original_plan}

User Feedback:
"{user_feedback}"

Based on the feedback, revise the relevant parts of the workout plan. Keep the format and rest of the plan unchanged if not needed.
"""
    try:
        response = client.models.generate_content(model=PRO_MODEL_NAME, contents=prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error updating plan: {e}"
