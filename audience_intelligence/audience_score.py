import re


def calculate_curiosity_score(transcript):
    """
    Estimate how strongly the spoken content creates curiosity.

    This is a rule-based heuristic, not a prediction of viewer behavior.
    """

    if not transcript or not transcript.strip():
        return {
            "score": 0,
            "signals": [],
            "status": "No transcript available"
        }

    text = transcript.strip().lower()

    curiosity_patterns = {
        "questions": r"\b(why|how|what|when|where|who|which|can|could|would|is|are|do|does|did)\b",
        "curiosity_words": r"\b(secret|surprising|unexpected|hidden|mistake|problem|truth|reason|revealed|discover|discovered|imagine|guess|wonder|actually)\b",
        "open_loops": r"\b(but|however|until|before|later|coming up|wait|next|here's what happened|you'll see|find out)\b",
        "strong_hooks": r"\b(the reason|here's why|here's how|the biggest|the most|what nobody|what no one|you need to know)\b"
    }

    signals = []
    points = 0

    # Questions
    question_matches = re.findall(
        curiosity_patterns["questions"],
        text
    )

    if question_matches:
        question_count = len(question_matches)
        points += min(question_count * 2, 20)
        signals.append(
            f"Question-style language detected ({question_count} signals)"
        )

    # Curiosity words
    curiosity_matches = re.findall(
        curiosity_patterns["curiosity_words"],
        text
    )

    if curiosity_matches:
        count = len(curiosity_matches)
        points += min(count * 4, 25)
        signals.append(
            f"Curiosity-triggering language detected ({count} signals)"
        )

    # Open loops
    loop_matches = re.findall(
        curiosity_patterns["open_loops"],
        text
    )

    if loop_matches:
        count = len(loop_matches)
        points += min(count * 5, 30)
        signals.append(
            f"Open-loop language detected ({count} signals)"
        )

    # Strong hook phrases
    hook_matches = re.findall(
        curiosity_patterns["strong_hooks"],
        text
    )

    if hook_matches:
        count = len(hook_matches)
        points += min(count * 6, 25)
        signals.append(
            f"Strong curiosity-hook phrases detected ({count} signals)"
        )

    # Penalize extremely short transcripts.
    word_count = len(text.split())

    if word_count < 20:
        points *= 0.5
        signals.append("Very little spoken content available")

    score = max(0, min(100, round(points)))

    if score >= 80:
        rating = "Very Strong"
    elif score >= 65:
        rating = "Strong"
    elif score >= 50:
        rating = "Moderate"
    elif score >= 30:
        rating = "Weak"
    else:
        rating = "Very Weak"

    return {
        "score": score,
        "rating": rating,
        "signals": signals,
        "word_count": word_count,
        "status": "Curiosity analysis completed"
    }