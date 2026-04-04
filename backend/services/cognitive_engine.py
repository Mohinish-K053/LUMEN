import random

def calculate_cognitive_load():
    focus_score = random.randint(50, 95)

    if focus_score > 80:
        load = "Low"
        recommendation = "Continue studying"
    elif focus_score > 60:
        load = "Optimal"
        recommendation = "Maintain focus"
    else:
        load = "High"
        recommendation = "Take a short break"

    return {
        "focusScore": focus_score,
        "cognitiveLoad": load,
        "recommendation": recommendation
    }
