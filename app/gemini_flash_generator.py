"""Gemini Flash - quick nutrition / recovery tips."""
from app.config import FLASH_MODEL_NAME, client


def generate_nutrition_tip_with_flash(goal: str) -> str:
    """
    Generate a nutrition or recovery tip using Gemini Flash based on the user's fitness goal.

    Args:
        goal (str): User's fitness goal - "weight loss", "muscle gain", or "general fitness".

    Returns:
        str: Generated tip.
    """
    prompt = (
        f"Give one clear, helpful nutrition or recovery tip for someone focused on '{goal}'. "
        "The tip should be practical, friendly, and easy to understand."
    )
    try:
        response = client.models.generate_content(model=FLASH_MODEL_NAME, contents=prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating tip: {str(e)}"
