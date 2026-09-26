def analyze_hook(
    duration,
    scenes,
    transcript_segments
):
    """
    Analyze the opening section of a video.

    V1 focuses on measurable hook signals.
    It does not claim to predict virality.
    """

    hook_duration = min(
        30,
        duration
    )

    results = {}

    # ========================================================
    # EARLIEST SPEECH
    # ========================================================

    first_speech_start = None

    first_speech_text = ""


    for segment in transcript_segments:

        if segment["start"] <= hook_duration:

            first_speech_start = segment["start"]

            first_speech_text = segment["text"]

            break


    results[
        "first_speech_start"
    ] = first_speech_start


    results[
        "first_speech_text"
    ] = first_speech_text


    # ========================================================
    # FIRST VISUAL CHANGE
    # ========================================================

    first_scene_change = None


    if scenes:

        for scene in scenes:

            if scene["timestamp"] <= hook_duration:

                first_scene_change = scene["timestamp"]

                break


    results[
        "first_visual_change"
    ] = first_scene_change


    # ========================================================
    # SPEECH INSIDE HOOK
    # ========================================================

    hook_speech_duration = 0


    hook_segments = []


    for segment in transcript_segments:

        start = segment["start"]

        end = segment["end"]


        if start < hook_duration:

            clipped_end = min(
                end,
                hook_duration
            )

            speech_length = max(
                0,
                clipped_end - start
            )

            hook_speech_duration += (
                speech_length
            )


            hook_segments.append(
                segment
            )


    if hook_duration > 0:

        speech_coverage = (
            hook_speech_duration
            / hook_duration
            * 100
        )

    else:

        speech_coverage = 0


    results[
        "hook_speech_duration"
    ] = round(
        hook_speech_duration,
        2
    )


    results[
        "hook_speech_coverage"
    ] = round(
        min(
            speech_coverage,
            100
        ),
        2
    )


    # ========================================================
    # OPENING SILENCE
    # ========================================================

    if first_speech_start is not None:

        opening_silence = first_speech_start

    else:

        opening_silence = hook_duration


    results[
        "opening_silence"
    ] = round(
        opening_silence,
        2
    )


    # ========================================================
    # EARLY VISUAL ACTIVITY
    # ========================================================

    early_scene_changes = 0


    for scene in scenes:

        if scene["timestamp"] <= 10:

            early_scene_changes += 1


    results[
        "early_scene_changes"
    ] = early_scene_changes


    # ========================================================
    # HOOK SIGNALS
    # ========================================================

    signals = []

    warnings = []


    # --------------------------------------------------------
    # SIGNAL 1 — EARLY SPEECH
    # --------------------------------------------------------

    if first_speech_start is None:

        warnings.append(
            "No speech was detected during "
            "the first 30 seconds."
        )

    elif first_speech_start <= 3:

        signals.append(
            "Speech begins quickly."
        )

    elif first_speech_start <= 7:

        signals.append(
            "Speech begins within the first "
            "several seconds."
        )

    else:

        warnings.append(
            f"Speech begins relatively late "
            f"at {first_speech_start:.1f}s."
        )


    # --------------------------------------------------------
    # SIGNAL 2 — VISUAL CHANGE
    # --------------------------------------------------------

    if first_scene_change is None:

        warnings.append(
            "No major visual change was detected "
            "during the opening."
        )

    elif first_scene_change <= 5:

        signals.append(
            "A visual change occurs early."
        )

    elif first_scene_change <= 10:

        signals.append(
            "A visual change occurs within "
            "the first 10 seconds."
        )

    else:

        warnings.append(
            f"The first major visual change occurs "
            f"at {first_scene_change:.1f}s."
        )


    # --------------------------------------------------------
    # SIGNAL 3 — OPENING SILENCE
    # --------------------------------------------------------

    if opening_silence >= 5:

        warnings.append(
            f"The video has approximately "
            f"{opening_silence:.1f}s before detected speech."
        )


    # --------------------------------------------------------
    # SIGNAL 4 — SPEECH COVERAGE
    # --------------------------------------------------------

    if hook_speech_duration == 0:

        warnings.append(
            "The first 30 seconds contain "
            "no detected speech."
        )

    elif speech_coverage >= 60:

        signals.append(
            "The opening contains substantial "
            "spoken content."
        )

    elif speech_coverage < 25:

        warnings.append(
            "The opening contains relatively "
            "little spoken content."
        )


    # --------------------------------------------------------
    # SIGNAL 5 — VISUAL ACTIVITY
    # --------------------------------------------------------

    if early_scene_changes >= 2:

        signals.append(
            "Multiple visual changes occur "
            "during the first 10 seconds."
        )

    elif early_scene_changes == 0:

        warnings.append(
            "No major visual changes were detected "
            "during the first 10 seconds."
        )


    # ========================================================
    # HOOK SCORE
    # ========================================================

    score = 50


    # Early speech

    if (
        first_speech_start is not None
        and first_speech_start <= 3
    ):

        score += 15

    elif (
        first_speech_start is not None
        and first_speech_start <= 7
    ):

        score += 8

    else:

        score -= 10


    # Early visual change

    if (
        first_scene_change is not None
        and first_scene_change <= 5
    ):

        score += 15

    elif (
        first_scene_change is not None
        and first_scene_change <= 10
    ):

        score += 8

    else:

        score -= 10


    # Speech coverage

    if speech_coverage >= 60:

        score += 10

    elif speech_coverage < 25:

        score -= 8


    # Early visual activity

    if early_scene_changes >= 2:

        score += 10

    elif early_scene_changes == 0:

        score -= 8


    score = max(
        0,
        min(
            score,
            100
        )
    )


    # ========================================================
    # ASSESSMENT
    # ========================================================

    if score >= 80:

        assessment = (
            "Strong opening signals detected. "
            "The video becomes active quickly."
        )

    elif score >= 60:

        assessment = (
            "Moderate opening. "
            "Some hook elements are present, "
            "but the opening could be stronger."
        )

    elif score >= 40:

        assessment = (
            "The opening has several potential "
            "hook weaknesses."
        )

    else:

        assessment = (
            "The opening shows significant "
            "potential hook weaknesses."
        )


    # ========================================================
    # RETURN RESULTS
    # ========================================================

    results[
        "hook_score"
    ] = score

    results[
        "signals"
    ] = signals

    results[
        "warnings"
    ] = warnings

    results[
        "assessment"
    ] = assessment


    return results