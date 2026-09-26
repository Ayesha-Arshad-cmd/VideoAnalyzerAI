def calculate_audience_response_score(
    audience_understanding_results=None,
    viewer_simulation_results=None,
    trend_results=None,
    attention_results=None,
    hook_results=None,
    story_results=None,
    retention_results=None
):
    """
    Consolidated audience-response scoring engine.

    Combines audience understanding, simulated viewer response,
    trend patterns and existing engagement signals.

    This score is an analytical estimate and does not represent
    actual viewer testing or guaranteed performance.
    """

    audience_understanding_results = (
        audience_understanding_results or {}
    )

    viewer_simulation_results = (
        viewer_simulation_results or {}
    )

    trend_results = trend_results or {}
    attention_results = attention_results or {}
    hook_results = hook_results or {}
    story_results = story_results or {}
    retention_results = retention_results or {}

    # ======================================================
    # BASE SIGNALS
    # ======================================================

    audience_understanding_score = float(
        audience_understanding_results.get(
            "audience_understanding_score",
            50
        )
    )

    curiosity_score = float(
        audience_understanding_results.get(
            "curiosity_score",
            50
        )
    )

    emotion_score = float(
        audience_understanding_results.get(
            "emotion_score",
            50
        )
    )

    relatability_score = float(
        audience_understanding_results.get(
            "relatability_score",
            50
        )
    )

    novelty_score = float(
        audience_understanding_results.get(
            "novelty_score",
            50
        )
    )

    title_clarity_score = float(
        audience_understanding_results.get(
            "title_clarity_score",
            50
        )
    )

    promise_match_score = float(
        audience_understanding_results.get(
            "promise_match_score",
            50
        )
    )

    # ======================================================
    # VIEWER SIMULATION SIGNALS
    # ======================================================

    viewer_response_score = float(
        viewer_simulation_results.get(
            "viewer_response_score",
            50
        )
    )

    attention_response = float(
        viewer_simulation_results.get(
            "attention_response",
            attention_results.get(
                "attention_score",
                50
            )
        )
    )

    curiosity_response = float(
        viewer_simulation_results.get(
            "curiosity_response",
            curiosity_score
        )
    )

    emotional_response = float(
        viewer_simulation_results.get(
            "emotional_response",
            emotion_score
        )
    )

    connection_response = float(
        viewer_simulation_results.get(
            "connection_response",
            relatability_score
        )
    )

    novelty_response = float(
        viewer_simulation_results.get(
            "novelty_response",
            novelty_score
        )
    )

    story_engagement = float(
        viewer_simulation_results.get(
            "story_engagement",
            story_results.get(
                "story_score",
                50
            )
        )
    )

    clarity_response = float(
        viewer_simulation_results.get(
            "clarity_response",
            (
                title_clarity_score
                + promise_match_score
            ) / 2
        )
    )

    shareability_response = float(
        viewer_simulation_results.get(
            "shareability_response",
            50
        )
    )

    # ======================================================
    # OTHER EXISTING SIGNALS
    # ======================================================

    trend_score = float(
        trend_results.get(
            "trend_score",
            50
        )
    )

    hook_score = float(
        hook_results.get(
            "hook_score",
            50
        )
    )

    retention_score = float(
        retention_results.get(
            "retention_score",
            50
        )
    )

    # ======================================================
    # AUDIENCE DIMENSION SCORES
    # ======================================================

    attention_dimension = (
        attention_response * 0.60
        + hook_score * 0.20
        + retention_score * 0.20
    )

    curiosity_dimension = (
        curiosity_response * 0.65
        + curiosity_score * 0.35
    )

    emotion_dimension = (
        emotional_response * 0.65
        + emotion_score * 0.35
    )

    relatability_dimension = (
        connection_response * 0.70
        + relatability_score * 0.30
    )

    novelty_dimension = (
        novelty_response * 0.70
        + novelty_score * 0.30
    )

    story_dimension = (
        story_engagement * 0.70
        + story_results.get(
            "story_score",
            50
        ) * 0.30
    )

    clarity_dimension = (
        clarity_response * 0.60
        + title_clarity_score * 0.20
        + promise_match_score * 0.20
    )

    shareability_dimension = (
        shareability_response * 0.70
        + trend_score * 0.30
    )

    # ======================================================
    # CLAMP FUNCTION
    # ======================================================

    def clamp(value):
        return round(
            max(
                0,
                min(
                    100,
                    float(value)
                )
            ),
            1
        )

    attention_dimension = clamp(
        attention_dimension
    )

    curiosity_dimension = clamp(
        curiosity_dimension
    )

    emotion_dimension = clamp(
        emotion_dimension
    )

    relatability_dimension = clamp(
        relatability_dimension
    )

    novelty_dimension = clamp(
        novelty_dimension
    )

    story_dimension = clamp(
        story_dimension
    )

    clarity_dimension = clamp(
        clarity_dimension
    )

    shareability_dimension = clamp(
        shareability_dimension
    )

    # ======================================================
    # FINAL AUDIENCE RESPONSE SCORE
    # ======================================================

    audience_response_score = (
        attention_dimension * 0.18
        + curiosity_dimension * 0.14
        + emotion_dimension * 0.12
        + relatability_dimension * 0.10
        + novelty_dimension * 0.10
        + story_dimension * 0.12
        + clarity_dimension * 0.10
        + shareability_dimension * 0.14
    )

    audience_response_score = clamp(
        audience_response_score
    )

    # ======================================================
    # AUDIENCE POTENTIAL
    # ======================================================

    if audience_response_score >= 80:
        audience_potential = "Very Strong"

    elif audience_response_score >= 70:
        audience_potential = "Strong"

    elif audience_response_score >= 60:
        audience_potential = "Moderate"

    elif audience_response_score >= 50:
        audience_potential = "Limited"

    else:
        audience_potential = "Weak"

    # ======================================================
    # FIND STRONGEST / WEAKEST AREAS
    # ======================================================

    dimensions = {
        "Attention": attention_dimension,
        "Curiosity": curiosity_dimension,
        "Emotional Impact": emotion_dimension,
        "Relatability": relatability_dimension,
        "Novelty": novelty_dimension,
        "Story Engagement": story_dimension,
        "Clarity": clarity_dimension,
        "Shareability": shareability_dimension
    }

    strongest_areas = sorted(
        dimensions.items(),
        key=lambda item: item[1],
        reverse=True
    )[:3]

    weakest_areas = sorted(
        dimensions.items(),
        key=lambda item: item[1]
    )[:3]

    # ======================================================
    # PRIORITY IMPROVEMENTS
    # ======================================================

    improvements = []

    if attention_dimension < 65:
        improvements.append(
            "Strengthen the opening and reduce early attention risks."
        )

    if curiosity_dimension < 65:
        improvements.append(
            "Increase curiosity with a clearer question, hook or information gap."
        )

    if emotion_dimension < 65:
        improvements.append(
            "Add stronger emotional stakes, human relevance or meaningful payoff."
        )

    if relatability_dimension < 65:
        improvements.append(
            "Make the content more relevant to the intended audience's experiences."
        )

    if novelty_dimension < 65:
        improvements.append(
            "Introduce a more distinctive idea, visual treatment or presentation angle."
        )

    if story_dimension < 65:
        improvements.append(
            "Strengthen narrative progression and payoff."
        )

    if clarity_dimension < 65:
        improvements.append(
            "Make the video's promise and central message easier to understand."
        )

    if shareability_dimension < 65:
        improvements.append(
            "Strengthen emotional, useful or surprising elements that may encourage sharing."
        )

    if not improvements:
        improvements.append(
            "No major audience-response weakness was detected by the current signals."
        )

    # ======================================================
    # OVERALL ASSESSMENT
    # ======================================================

    if audience_response_score >= 80:

        assessment = (
            "The video shows a strong combination of audience "
            "engagement, curiosity, emotional response, clarity "
            "and sharing signals."
        )

    elif audience_response_score >= 70:

        assessment = (
            "The video demonstrates several strong audience-"
            "response signals, with some areas that could still "
            "be optimized."
        )

    elif audience_response_score >= 60:

        assessment = (
            "The video has a mixed audience-response profile. "
            "Several elements are promising, while other areas "
            "may limit engagement."
        )

    elif audience_response_score >= 50:

        assessment = (
            "The audience-response signals are moderate and "
            "indicate several areas where viewer engagement "
            "could be improved."
        )

    else:

        assessment = (
            "The current analysis identifies multiple audience-"
            "response weaknesses that should be reviewed."
        )

    # ======================================================
    # CONFIDENCE
    # ======================================================

    available_modules = sum([
        bool(audience_understanding_results),
        bool(viewer_simulation_results),
        bool(trend_results),
        bool(attention_results),
        bool(hook_results),
        bool(story_results),
        bool(retention_results)
    ])

    if available_modules >= 6:
        confidence = "Moderate"

    elif available_modules >= 4:
        confidence = "Low-Moderate"

    else:
        confidence = "Low"

    return {
        "audience_response_score": audience_response_score,

        "audience_potential": audience_potential,

        "attention_score": attention_dimension,
        "curiosity_score": curiosity_dimension,
        "emotion_score": emotion_dimension,
        "relatability_score": relatability_dimension,
        "novelty_score": novelty_dimension,
        "story_engagement_score": story_dimension,
        "clarity_score": clarity_dimension,
        "shareability_score": shareability_dimension,

        "strongest_areas": [
            {
                "area": area,
                "score": score
            }
            for area, score in strongest_areas
        ],

        "weakest_areas": [
            {
                "area": area,
                "score": score
            }
            for area, score in weakest_areas
        ],

        "improvements": improvements,

        "assessment": assessment,

        "confidence": confidence,

        "status": "Audience-response scoring complete"
    }