"""Optional: static fallback tips used if the Gemini Flash call fails."""

FALLBACK_TIPS = {
    "weight loss": "Fill half your plate with vegetables and drink a glass of water before meals to stay full.",
    "muscle gain": "Include a protein source (eggs, chicken, paneer, lentils) in your post-workout meal.",
    "general fitness": "Stay hydrated, eat a balanced plate and get 7-8 hours of sleep for recovery.",
}


def get_fallback_tip(goal: str) -> str:
    g = (goal or "").lower()
    if "loss" in g or "fat" in g:
        return FALLBACK_TIPS["weight loss"]
    if "muscle" in g or "gain" in g:
        return FALLBACK_TIPS["muscle gain"]
    return FALLBACK_TIPS["general fitness"]
