def analyze_timeline(
    duration,
    scenes,
    transcript_segments,
    silence_percentage
):
    """
    Analyze the overall structure and activity
    of a video timeline.
    """

    results = {}

    # ========================================================
    # BASIC INFORMATION
    # ========================================================

    results["duration"] = round(
        duration,
        2
    )

    results["scene_changes"] = len(
        scenes
    )


    # ========================================================
    # SCENE CHANGE FREQUENCY
    # ========================================================

    if duration > 0:

        scene_changes_per_minute = (
            len(scenes)
            / duration
            * 60
        )

    else:

        scene_changes_per_minute = 0


    results[
        "scene_changes_per_minute"
    ] = round(
        scene_changes_per_minute,
        2
    )


    # ========================================================
    # FIRST SCENE CHANGE
    # ========================================================

    if scenes:

        first_scene_change = scenes[0][
            "timestamp"
        ]

    else:

        first_scene_change = None


    results[
        "first_scene_change"
    ] = first_scene_change


    # ========================================================
    # HOOK ANALYSIS
    # ========================================================

    # We consider the first 30 seconds
    # especially important.

    hook_window = min(
        30,
        duration
    )


    early_scenes = [
        scene
        for scene in scenes
        if scene["timestamp"] <= hook_window
    ]


    results[
        "early_scene_changes"
    ] = len(
        early_scenes
    )


    # ========================================================
    # SPEECH COVERAGE
    # ========================================================

    total_speech_duration = 0


    for segment in transcript_segments:

        start = segment["start"]

        end = segment["end"]

        segment_duration = max(
            0,
            end - start
        )

        total_speech_duration += (
            segment_duration
        )


    if duration > 0:

        speech_percentage = (
            total_speech_duration
            / duration
            * 100
        )

    else:

        speech_percentage = 0


    results[
        "speech_percentage"
    ] = round(
        min(
            speech_percentage,
            100
        ),
        2
    )


    # ========================================================
    # SILENCE
    # ========================================================

    results[
        "silence_percentage"
    ] = round(
        silence_percentage,
        2
    )


    # ========================================================
    # LONG VISUAL GAPS
    # ========================================================

    visual_gaps = []


    if scenes:

        previous_time = 0


        for scene in scenes:

            current_time = scene[
                "timestamp"
            ]

            gap = (
                current_time
                - previous_time
            )


            if gap >= 5:

                visual_gaps.append(
                    {
                        "start": round(
                            previous_time,
                            2
                        ),
                        "end": round(
                            current_time,
                            2
                        ),
                        "duration": round(
                            gap,
                            2
                        )
                    }
                )


            previous_time = current_time


        # Check final section

        final_gap = (
            duration
            - previous_time
        )


        if final_gap >= 5:

            visual_gaps.append(
                {
                    "start": round(
                        previous_time,
                        2
                    ),
                    "end": round(
                        duration,
                        2
                    ),
                    "duration": round(
                        final_gap,
                        2
                    )
                }
            )


    else:

        if duration >= 5:

            visual_gaps.append(
                {
                    "start": 0,
                    "end": round(
                        duration,
                        2
                    ),
                    "duration": round(
                        duration,
                        2
                    )
                }
            )


    results[
        "long_visual_gaps"
    ] = visual_gaps


    # ========================================================
    # HOOK WARNING
    # ========================================================

    warnings = []


    if duration > 0:

        if (
            first_scene_change is None
            or first_scene_change > 10
        ):

            warnings.append(
                "The video has limited visual activity "
                "during the first 10 seconds."
            )


    # ========================================================
    # SPEECH WARNING
    # ========================================================

    if (
        duration > 30
        and speech_percentage < 20
    ):

        warnings.append(
            "Speech coverage is relatively low "
            "for this video."
        )


    # ========================================================
    # SILENCE WARNING
    # ========================================================

    if silence_percentage >= 20:

        warnings.append(
            "A significant portion of the audio "
            "contains low-volume or silent sections."
        )


    # ========================================================
    # STATIC VISUAL WARNING
    # ========================================================

    if scene_changes_per_minute < 2:

        warnings.append(
            "The video has a low visual change rate."
        )


    results[
        "warnings"
    ] = warnings


    # ========================================================
    # OVERALL ACTIVITY LEVEL
    # ========================================================

    activity_score = 50


    if scene_changes_per_minute >= 8:

        activity_score += 20

    elif scene_changes_per_minute >= 4:

        activity_score += 10

    elif scene_changes_per_minute < 2:

        activity_score -= 15


    if speech_percentage >= 50:

        activity_score += 10

    elif speech_percentage < 20:

        activity_score -= 10


    if silence_percentage >= 30:

        activity_score -= 15

    elif silence_percentage <= 10:

        activity_score += 5


    activity_score = max(
        0,
        min(
            activity_score,
            100
        )
    )


    results[
        "activity_score"
    ] = activity_score


    return results