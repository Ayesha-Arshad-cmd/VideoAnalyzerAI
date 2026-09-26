def calculate_overall_score(
    hook_score,
    story_score,
    retention_score,
    visual_score,
    audio_score,
    title_score,
    thumbnail_score
):
    """
    Calculate the overall pre-publish video score.

    V1 uses weighted measurable module scores.
    It does NOT claim to predict actual YouTube
    performance or virality.
    """

    weights = {
        "hook": 0.20,
        "story": 0.15,
        "retention": 0.20,
        "visual": 0.10,
        "audio": 0.10,
        "title": 0.10,
        "thumbnail": 0.15
    }

    scores = {
        "hook": hook_score,
        "story": story_score,
        "retention": retention_score,
        "visual": visual_score,
        "audio": audio_score,
        "title": title_score,
        "thumbnail": thumbnail_score
    }

    overall_score = (
        scores["hook"] * weights["hook"]
        + scores["story"] * weights["story"]
        + scores["retention"] * weights["retention"]
        + scores["visual"] * weights["visual"]
        + scores["audio"] * weights["audio"]
        + scores["title"] * weights["title"]
        + scores["thumbnail"] * weights["thumbnail"]
    )

    overall_score = round(
        max(0, min(overall_score, 100)),
        1
    )

    if overall_score >= 90:
        rating = "Excellent"
        assessment = (
            "The video shows strong overall pre-publish "
            "characteristics across the analyzed areas."
        )

    elif overall_score >= 80:
        rating = "Strong"
        assessment = (
            "The video is well prepared overall, "
            "with some areas that could still be improved."
        )

    elif overall_score >= 70:
        rating = "Good"
        assessment = (
            "The video has a reasonable overall structure, "
            "but several improvements may strengthen it."
        )

    elif overall_score >= 60:
        rating = "Needs Improvement"
        assessment = (
            "The video has several areas that should "
            "be improved before publishing."
        )

    else:
        rating = "Weak"
        assessment = (
            "The analysis detected significant areas "
            "that should be improved before publishing."
        )

    # Find strongest and weakest areas

    sorted_scores = sorted(
        scores.items(),
        key=lambda item: item[1]
    )

    weakest_areas = sorted_scores[:3]
    strongest_areas = sorted_scores[-3:][::-1]

    return {
        "overall_score": overall_score,
        "rating": rating,
        "assessment": assessment,
        "component_scores": scores,
        "weights": weights,
        "weakest_areas": weakest_areas,
        "strongest_areas": strongest_areas
    }