def simulate_viewer_response(
    hook_results=None,
    story_results=None,
    retention_results=None,
    visual_results=None,
    attention_results=None,
    audience_understanding_results=None,
    trend_results=None
):
    """
    Lightweight human viewer response simulator.

    This does not represent real human testing.
    It estimates likely viewer reactions from the
    analyzer's existing signals.
    """

    hook_results = hook_results or {}
    story_results = story_results or {}
    retention_results = retention_results or {}
    visual_results = visual_results or {}
    attention_results = attention_results or {}
    audience_understanding_results = (
        audience_understanding_results or {}
    )
    trend_results = trend_results or {}

    # --------------------------------------------------
    # EXISTING SIGNALS
    # --------------------------------------------------

    hook_score = float(
        hook_results.get("hook_score", 50)
    )

    story_score = float(
        story_results.get("story_score", 50)
    )

    retention_score = float(
        retention_results.get("retention_score", 50)
    )

    visual_score = float(
        visual_results.get("visual_score", 50)
    )

    attention_score = float(
        attention_results.get("attention_score", 50)
    )

    curiosity_score = float(
        audience_understanding_results.get(
            "curiosity_score",
            hook_score
        )
    )

    emotion_score = float(
        audience_understanding_results.get(
            "emotion_score",
            story_score
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

    trend_score = float(
        trend_results.get(
            "trend_score",
            50
        )
    )

    # --------------------------------------------------
    # HUMAN RESPONSE DIMENSIONS
    # --------------------------------------------------

    attention_response = (
        hook_score * 0.35
        + retention_score * 0.30
        + attention_score * 0.35
    )

    curiosity_response = (
        curiosity_score * 0.50
        + hook_score * 0.30
        + title_clarity_score * 0.20
    )

    emotional_response = (
        emotion_score * 0.45
        + story_score * 0.35
        + relatability_score * 0.20
    )

    connection_response = (
        relatability_score * 0.55
        + emotion_score * 0.25
        + story_score * 0.20
    )

    novelty_response = (
        novelty_score * 0.60
        + visual_score * 0.20
        + curiosity_score * 0.20
    )

    story_engagement = (
        story_score * 0.45
        + retention_score * 0.25
        + emotion_score * 0.30
    )

    clarity_response = (
        title_clarity_score * 0.35
        + promise_match_score * 0.35
        + visual_score * 0.15
        + story_score * 0.15
    )

    shareability_response = (
        emotion_score * 0.20
        + novelty_score * 0.20
        + relatability_score * 0.20
        + curiosity_score * 0.15
        + trend_score * 0.25
    )

    viewer_response_score = (
        attention_response * 0.20
        + curiosity_response * 0.15
        + emotional_response * 0.15
        + connection_response * 0.10
        + novelty_response * 0.10
        + story_engagement * 0.10
        + clarity_response * 0.10
        + shareability_response * 0.10
    )

    # Keep scores between 0 and 100
    def clamp(value):
        return round(
            max(0, min(100, value)),
            1
        )

    attention_response = clamp(
        attention_response
    )

    curiosity_response = clamp(
        curiosity_response
    )

    emotional_response = clamp(
        emotional_response
    )

    connection_response = clamp(
        connection_response
    )

    novelty_response = clamp(
        novelty_response
    )

    story_engagement = clamp(
        story_engagement
    )

    clarity_response = clamp(
        clarity_response
    )

    shareability_response = clamp(
        shareability_response
    )

    viewer_response_score = clamp(
        viewer_response_score
    )

    # --------------------------------------------------
    # POSITIVE VIEWER REACTIONS
    # --------------------------------------------------

    positive_reactions = []

    if attention_response >= 75:
        positive_reactions.append(
            "Viewer is likely to remain engaged with the opening."
        )

    if curiosity_response >= 75:
        positive_reactions.append(
            "The content creates a strong reason to keep watching."
        )

    if emotional_response >= 75:
        positive_reactions.append(
            "The video has strong emotional-response signals."
        )

    if connection_response >= 75:
        positive_reactions.append(
            "The content contains relatable or personally relevant signals."
        )

    if novelty_response >= 75:
        positive_reactions.append(
            "The video contains elements that may feel fresh or distinctive."
        )

    if story_engagement >= 75:
        positive_reactions.append(
            "The narrative structure supports continued viewer interest."
        )

    if clarity_response >= 75:
        positive_reactions.append(
            "The viewer can relatively easily understand the content promise."
        )

    if shareability_response >= 75:
        positive_reactions.append(
            "Several signals support potential sharing or recommendation."
        )

    # --------------------------------------------------
    # NEGATIVE / RISK REACTIONS
    # --------------------------------------------------

    viewer_risks = []

    if attention_response < 60:
        viewer_risks.append(
            "Viewer attention may weaken during the viewing experience."
        )

    if curiosity_response < 60:
        viewer_risks.append(
            "The content may not create enough curiosity to continue watching."
        )

    if emotional_response < 60:
        viewer_risks.append(
            "The video may produce a relatively weak emotional response."
        )

    if connection_response < 60:
        viewer_risks.append(
            "The content may feel less personally relevant to some viewers."
        )

    if novelty_response < 60:
        viewer_risks.append(
            "The content may feel familiar or insufficiently distinctive."
        )

    if story_engagement < 60:
        viewer_risks.append(
            "Story progression may not strongly sustain viewer interest."
        )

    if clarity_response < 60:
        viewer_risks.append(
            "Some viewers may have difficulty understanding the content promise."
        )

    if shareability_response < 60:
        viewer_risks.append(
            "The current signals provide limited evidence of strong sharing motivation."
        )

    # --------------------------------------------------
    # ESTIMATED VIEWER BEHAVIOR
    # --------------------------------------------------

    viewer_behavior = []

    if attention_response >= 75:
        viewer_behavior.append(
            "Likely to continue watching"
        )
    elif attention_response >= 55:
        viewer_behavior.append(
            "May continue watching if later sections maintain interest"
        )
    else:
        viewer_behavior.append(
            "Higher risk of early disengagement"
        )

    if curiosity_response >= 75:
        viewer_behavior.append(
            "Likely to seek the next piece of information"
        )
    elif curiosity_response >= 55:
        viewer_behavior.append(
            "Moderate curiosity"
        )
    else:
        viewer_behavior.append(
            "Limited curiosity signal"
        )

    if emotional_response >= 75:
        viewer_behavior.append(
            "Potential emotional investment"
        )
    elif emotional_response >= 55:
        viewer_behavior.append(
            "Moderate emotional response"
        )
    else:
        viewer_behavior.append(
            "Limited emotional involvement"
        )

    if shareability_response >= 75:
        viewer_behavior.append(
            "Higher sharing motivation"
        )
    elif shareability_response >= 55:
        viewer_behavior.append(
            "Possible sharing if topic is personally relevant"
        )
    else:
        viewer_behavior.append(
            "Low sharing motivation signal"
        )

    # --------------------------------------------------
    # OVERALL ASSESSMENT
    # --------------------------------------------------

    if viewer_response_score >= 80:
        assessment = (
            "The analyzer detects a strong combination of "
            "attention, curiosity, emotional, clarity and "
            "engagement signals that could support a positive "
            "viewer response."
        )

    elif viewer_response_score >= 65:
        assessment = (
            "The video shows several positive viewer-response "
            "signals, although some dimensions could be strengthened."
        )

    elif viewer_response_score >= 50:
        assessment = (
            "The video contains mixed viewer-response signals. "
            "Some elements may engage viewers while others create "
            "potential disengagement."
        )

    else:
        assessment = (
            "The current signals indicate several potential "
            "viewer-response weaknesses that should be reviewed."
        )

    # --------------------------------------------------
    # CONFIDENCE
    # --------------------------------------------------

    available_modules = sum([
        bool(hook_results),
        bool(story_results),
        bool(retention_results),
        bool(visual_results),
        bool(attention_results),
        bool(audience_understanding_results),
        bool(trend_results)
    ])

    if available_modules >= 6:
        confidence = "Moderate"
    elif available_modules >= 4:
        confidence = "Low-Moderate"
    else:
        confidence = "Low"

    return {
        "viewer_response_score": viewer_response_score,

        "attention_response": attention_response,
        "curiosity_response": curiosity_response,
        "emotional_response": emotional_response,
        "connection_response": connection_response,
        "novelty_response": novelty_response,
        "story_engagement": story_engagement,
        "clarity_response": clarity_response,
        "shareability_response": shareability_response,

        "positive_reactions": positive_reactions,
        "viewer_risks": viewer_risks,
        "viewer_behavior": viewer_behavior,

        "assessment": assessment,
        "confidence": confidence,

        "status": "Human viewer response simulation complete"
    }