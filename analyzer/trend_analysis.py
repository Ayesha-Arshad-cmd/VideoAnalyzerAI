def analyze_trends(
    duration,
    hook_results=None,
    story_results=None,
    retention_results=None,
    visual_results=None,
    timeline_results=None,
    title_results=None,
    thumbnail_results=None,
    attention_results=None,
    audience_understanding_results=None
):
    """
    Lightweight trend and viral-pattern comparison.

    This module compares existing video-analysis signals
    against generalized high-engagement content patterns.

    It does NOT predict actual views or guarantee virality.
    """

    hook_results = hook_results or {}
    story_results = story_results or {}
    retention_results = retention_results or {}
    visual_results = visual_results or {}
    timeline_results = timeline_results or {}
    title_results = title_results or {}
    thumbnail_results = thumbnail_results or {}
    attention_results = attention_results or {}
    audience_understanding_results = (
        audience_understanding_results or {}
    )

    duration = float(duration or 0)

    if duration <= 0:
        return {
            "trend_score": 0,
            "pattern_matches": [],
            "pattern_warnings": [],
            "style": "Unknown",
            "recommendations": [],
            "confidence": "Low",
            "assessment": "Unable to analyze trends without video duration.",
            "status": "Insufficient video data"
        }

    # ========================================================
    # GET EXISTING SIGNALS
    # ========================================================

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

    activity_score = float(
        timeline_results.get("activity_score", 50)
    )

    title_score = float(
        title_results.get("title_score", 50)
    )

    thumbnail_score = float(
        thumbnail_results.get("thumbnail_score", 50)
    )

    attention_score = float(
        attention_results.get("attention_score", 50)
    )

    audience_score = float(
        audience_understanding_results.get(
            "audience_understanding_score",
            50
        )
    )

    curiosity_score = float(
        audience_understanding_results.get(
            "curiosity_score",
            hook_score
        )
    )

    promise_match_score = float(
        audience_understanding_results.get(
            "promise_match_score",
            (title_score + thumbnail_score) / 2
        )
    )

    scene_changes_per_minute = float(
        timeline_results.get(
            "scene_changes_per_minute",
            0
        )
    )

    early_scene_changes = int(
        timeline_results.get(
            "early_scene_changes",
            0
        )
    )

    speech_coverage = float(
        story_results.get(
            "speech_coverage",
            0
        )
    )

    # ========================================================
    # TREND SCORE
    # ========================================================

    trend_score = 0.0

    # Hook
    trend_score += hook_score * 0.15

    # Retention
    trend_score += retention_score * 0.15

    # Visual quality
    trend_score += visual_score * 0.10

    # Activity / pacing
    trend_score += activity_score * 0.10

    # Story structure
    trend_score += story_score * 0.10

    # Title
    trend_score += title_score * 0.10

    # Thumbnail
    trend_score += thumbnail_score * 0.10

    # Attention
    trend_score += attention_score * 0.10

    # Audience understanding
    trend_score += audience_score * 0.05

    # Promise matching
    trend_score += promise_match_score * 0.05

    trend_score = max(
        0,
        min(
            100,
            round(trend_score, 1)
        )
    )

    # ========================================================
    # PATTERN MATCHES
    # ========================================================

    pattern_matches = []

    # Strong hook
    if hook_score >= 75:
        pattern_matches.append(
            "Strong opening hook pattern detected."
        )

    # Fast opening visual change
    first_visual_change = hook_results.get(
        "first_visual_change"
    )

    if (
        first_visual_change is not None
        and float(first_visual_change) <= 3
    ):
        pattern_matches.append(
            "Early visual change matches a fast-opening content pattern."
        )

    # Early activity
    if early_scene_changes >= 2:
        pattern_matches.append(
            "Multiple visual changes occur during the first 30 seconds."
        )

    # Moderate/high pacing
    if scene_changes_per_minute >= 4:
        pattern_matches.append(
            "Visual pacing is relatively active."
        )

    # Strong speech coverage
    if speech_coverage >= 60:
        pattern_matches.append(
            "Speech coverage supports a consistently narrated format."
        )

    # Strong visual quality
    if visual_score >= 75:
        pattern_matches.append(
            "Visual quality is consistent with polished video content."
        )

    # Strong title
    if title_score >= 75:
        pattern_matches.append(
            "Title contains several strong engagement-oriented signals."
        )

    # Strong thumbnail
    if thumbnail_score >= 75:
        pattern_matches.append(
            "Thumbnail contains strong visual-quality signals."
        )

    # Strong attention
    if attention_score >= 75:
        pattern_matches.append(
            "Estimated attention pattern remains relatively stable."
        )

    # Curiosity
    if curiosity_score >= 75:
        pattern_matches.append(
            "Strong curiosity signal detected in the opening/content promise."
        )

    # Promise match
    if promise_match_score >= 75:
        pattern_matches.append(
            "Title/thumbnail/content promise is relatively consistent."
        )

    # ========================================================
    # PATTERN WARNINGS
    # ========================================================

    pattern_warnings = []

    if hook_score < 60:
        pattern_warnings.append(
            "Opening hook is weaker than the target high-engagement pattern."
        )

    if (
        first_visual_change is None
        or float(first_visual_change) > 8
    ):
        pattern_warnings.append(
            "The first major visual change occurs relatively late."
        )

    if early_scene_changes == 0:
        pattern_warnings.append(
            "Little visual variation is detected during the first 30 seconds."
        )

    if scene_changes_per_minute < 2:
        pattern_warnings.append(
            "Visual pacing is relatively slow."
        )

    if speech_coverage < 25:
        pattern_warnings.append(
            "Low speech coverage may indicate long non-narrated sections."
        )

    if visual_score < 60:
        pattern_warnings.append(
            "Visual quality signals are below the target pattern."
        )

    if title_score < 60:
        pattern_warnings.append(
            "Title signals could be strengthened."
        )

    if thumbnail_score < 60:
        pattern_warnings.append(
            "Thumbnail signals could be strengthened."
        )

    if attention_score < 60:
        pattern_warnings.append(
            "Estimated attention pattern contains meaningful risk."
        )

    if promise_match_score < 60:
        pattern_warnings.append(
            "The title/thumbnail/content promise is not strongly aligned."
        )

    # ========================================================
    # CONTENT STYLE DETECTION
    # ========================================================

    if speech_coverage >= 70 and scene_changes_per_minute >= 4:
        style = "Fast-paced narrated content"

    elif speech_coverage >= 70 and scene_changes_per_minute < 2:
        style = "Narrative / talking-head content"

    elif speech_coverage < 30 and scene_changes_per_minute >= 5:
        style = "Highly visual / montage-style content"

    elif scene_changes_per_minute >= 4:
        style = "Fast visual content"

    elif story_score >= 75:
        style = "Story-driven content"

    else:
        style = "General mixed-format content"

    # ========================================================
    # RECOMMENDATIONS
    # ========================================================

    recommendations = []

    if hook_score < 70:
        recommendations.append(
            "Strengthen the first few seconds with a clearer hook, question, result or immediate value."
        )

    if early_scene_changes < 2:
        recommendations.append(
            "Consider introducing stronger visual variation during the opening."
        )

    if scene_changes_per_minute < 2:
        recommendations.append(
            "Review slow sections and consider tighter visual pacing."
        )

    if speech_coverage < 30:
        recommendations.append(
            "Consider adding narration or clearer on-screen communication where appropriate."
        )

    if title_score < 70:
        recommendations.append(
            "Make the title more specific about the video's central value or curiosity gap."
        )

    if thumbnail_score < 70:
        recommendations.append(
            "Strengthen the thumbnail's visual clarity and focal point."
        )

    if promise_match_score < 70:
        recommendations.append(
            "Ensure the title and thumbnail accurately communicate what the video delivers."
        )

    if attention_score < 70:
        recommendations.append(
            "Review estimated attention-drop points and add stronger transitions or payoff moments."
        )

    if not recommendations:
        recommendations.append(
            "Current signals already match several generalized high-engagement patterns."
        )

    # ========================================================
    # CONFIDENCE
    # ========================================================

    available_signals = sum([
        bool(hook_results),
        bool(story_results),
        bool(retention_results),
        bool(visual_results),
        bool(timeline_results),
        bool(title_results),
        bool(thumbnail_results),
        bool(attention_results),
        bool(audience_understanding_results)
    ])

    if available_signals >= 8:
        confidence = "Moderate"

    elif available_signals >= 5:
        confidence = "Low-Moderate"

    else:
        confidence = "Low"

    # ========================================================
    # ASSESSMENT
    # ========================================================

    if trend_score >= 80:
        assessment = (
            "The video matches many of the generalized "
            "high-engagement patterns measured by this analyzer."
        )

    elif trend_score >= 65:
        assessment = (
            "The video matches several generalized "
            "high-engagement patterns, but some areas "
            "could be strengthened."
        )

    elif trend_score >= 50:
        assessment = (
            "The video shows some useful engagement patterns, "
            "but several signals differ from the target patterns."
        )

    else:
        assessment = (
            "The current signals show substantial differences "
            "from the generalized high-engagement patterns."
        )

    return {
        "trend_score": trend_score,
        "pattern_matches": pattern_matches,
        "pattern_warnings": pattern_warnings,
        "style": style,
        "recommendations": recommendations,
        "confidence": confidence,
        "assessment": assessment,
        "status": "Trend and pattern analysis complete"
    }