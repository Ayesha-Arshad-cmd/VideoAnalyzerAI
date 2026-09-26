def calculate_human_virality(
    hook_score=0,
    story_score=0,
    retention_score=0,
    visual_score=0,
    audio_score=0,
    title_score=0,
    thumbnail_score=0,
    speech_coverage=0,
    scene_changes_per_minute=0,
    opening_silence=0,
    first_visual_change=None
):
    """
    Estimate human-oriented virality potential using
    measurable signals from the existing analysis modules.

    This is not a prediction of actual views or virality.
    """

    score = 0

    # --------------------------------------------------------
    # CORE CONTENT SIGNALS
    # --------------------------------------------------------

    score += hook_score * 0.20
    score += story_score * 0.15
    score += retention_score * 0.15
    score += visual_score * 0.10
    score += audio_score * 0.05
    score += title_score * 0.10
    score += thumbnail_score * 0.10

    # --------------------------------------------------------
    # SPEECH / CONTENT AVAILABILITY
    # --------------------------------------------------------

    speech_score = min(
        max(speech_coverage, 0),
        100
    )

    score += speech_score * 0.05

    # --------------------------------------------------------
    # VISUAL PACING
    # --------------------------------------------------------

    if scene_changes_per_minute >= 8:
        pacing_score = 100
    elif scene_changes_per_minute >= 5:
        pacing_score = 85
    elif scene_changes_per_minute >= 3:
        pacing_score = 70
    elif scene_changes_per_minute >= 1:
        pacing_score = 50
    else:
        pacing_score = 30

    score += pacing_score * 0.05

    # --------------------------------------------------------
    # OPENING ATTENTION
    # --------------------------------------------------------

    if opening_silence <= 1:
        opening_score = 100
    elif opening_silence <= 2:
        opening_score = 85
    elif opening_silence <= 4:
        opening_score = 65
    else:
        opening_score = 35

    score += opening_score * 0.05

    # --------------------------------------------------------
    # EARLY VISUAL CHANGE
    # --------------------------------------------------------

    if first_visual_change is None:
        visual_change_score = 30
    elif first_visual_change <= 3:
        visual_change_score = 100
    elif first_visual_change <= 5:
        visual_change_score = 85
    elif first_visual_change <= 10:
        visual_change_score = 65
    else:
        visual_change_score = 40

    score += visual_change_score * 0.05

    # --------------------------------------------------------
    # FINAL SCORE
    # --------------------------------------------------------

    virality_score = round(
        max(
            0,
            min(
                score,
                100
            )
        ),
        1
    )

    # --------------------------------------------------------
    # ASSESSMENT
    # --------------------------------------------------------

    if virality_score >= 80:
        assessment = (
            "Strong human-virality signals. "
            "The video has several characteristics "
            "that can support viewer attention and sharing."
        )

    elif virality_score >= 65:
        assessment = (
            "Good human-virality potential, "
            "but some attention and engagement signals "
            "could be improved."
        )

    elif virality_score >= 50:
        assessment = (
            "Moderate human-virality potential. "
            "Several important engagement signals "
            "need improvement."
        )

    else:
        assessment = (
            "Weak human-virality signals. "
            "The opening, pacing, content or presentation "
            "may need significant improvement."
        )

    # --------------------------------------------------------
    # SIGNALS
    # --------------------------------------------------------

    signals = []
    warnings = []

    if hook_score >= 80:
        signals.append(
            "Strong opening hook."
        )

    if retention_score >= 80:
        signals.append(
            "Strong retention structure."
        )

    if visual_score >= 80:
        signals.append(
            "Good visual presentation."
        )

    if title_score >= 80:
        signals.append(
            "Title has strong attention-oriented characteristics."
        )

    if thumbnail_score >= 80:
        signals.append(
            "Thumbnail has strong visual appeal signals."
        )

    if scene_changes_per_minute >= 5:
        signals.append(
            "Good visual pacing and scene variation."
        )

    if opening_silence > 3:
        warnings.append(
            "Opening silence may reduce initial attention."
        )

    if first_visual_change is None or first_visual_change > 10:
        warnings.append(
            "No strong early visual change was detected."
        )

    if hook_score < 60:
        warnings.append(
            "Hook score is relatively weak."
        )

    if retention_score < 60:
        warnings.append(
            "Retention structure may need improvement."
        )

    return {
        "human_virality_score": virality_score,
        "assessment": assessment,
        "signals": signals,
        "warnings": warnings,
        "components": {
            "hook": hook_score,
            "story": story_score,
            "retention": retention_score,
            "visual": visual_score,
            "audio": audio_score,
            "title": title_score,
            "thumbnail": thumbnail_score,
            "speech": round(speech_score, 1),
            "visual_pacing": pacing_score,
            "opening_attention": opening_score,
            "early_visual_change": visual_change_score
        }
    }