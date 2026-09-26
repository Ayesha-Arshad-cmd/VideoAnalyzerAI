def analyze_retention(
    duration,
    scenes,
    transcript_segments,
    silence_percentage
):
    """
    Estimate potential viewer-retention risks.

    This is a rule-based V1.
    It does NOT predict the actual YouTube
    retention curve.
    """

    risks = []

    # ========================================================
    # 1. OPENING / HOOK RISK
    # ========================================================

    first_scene_change = None

    if scenes:

        first_scene_change = scenes[0]["timestamp"]


    if duration >= 10:

        if (
            first_scene_change is None
            or first_scene_change > 10
        ):

            risks.append({
                "timestamp": 0,
                "severity": "High",
                "type": "Weak Opening",
                "reason": (
                    "Limited visual change detected "
                    "during the first 10 seconds."
                )
            })


    # ========================================================
    # 2. LONG VISUAL GAPS
    # ========================================================

    previous_time = 0


    for scene in scenes:

        current_time = scene["timestamp"]

        gap = current_time - previous_time


        if gap >= 8:

            risks.append({
                "timestamp": previous_time,
                "severity": "Medium",
                "type": "Long Visual Gap",
                "reason": (
                    f"No major visual change detected "
                    f"for approximately {gap:.1f} seconds."
                )
            })


        previous_time = current_time


    # Check final section

    if duration > previous_time:

        final_gap = duration - previous_time


        if final_gap >= 8:

            risks.append({
                "timestamp": previous_time,
                "severity": "Medium",
                "type": "Long Ending Section",
                "reason": (
                    f"No major visual change detected "
                    f"for approximately {final_gap:.1f} seconds."
                )
            })


    # ========================================================
    # 3. SPEECH GAPS
    # ========================================================

    previous_speech_end = 0


    for segment in transcript_segments:

        start = segment["start"]

        gap = start - previous_speech_end


        if gap >= 6:

            risks.append({
                "timestamp": previous_speech_end,
                "severity": "Medium",
                "type": "Speech Gap",
                "reason": (
                    f"No detected speech for "
                    f"approximately {gap:.1f} seconds."
                )
            })


        previous_speech_end = segment["end"]


    # ========================================================
    # 4. SILENCE RISK
    # ========================================================

    if silence_percentage >= 30:

        risks.append({
            "timestamp": 0,
            "severity": "High",
            "type": "High Silence",
            "reason": (
                f"Approximately {silence_percentage:.1f}% "
                "of the audio contains very low-volume "
                "or silent sections."
            )
       } )

    elif silence_percentage >= 20:

        risks.append({
            "timestamp": 0,
            "severity": "Medium",
            "type": "Elevated Silence",
            "reason": (
                f"Approximately {silence_percentage:.1f}% "
                "of the audio contains very low-volume "
                "or silent sections."
            )
        })


    # ========================================================
    # 5. LOW VISUAL ACTIVITY
    # ========================================================

    if duration > 0:

        scene_rate = (
            len(scenes)
            / duration
            * 60
        )

    else:

        scene_rate = 0


    if scene_rate < 2:

        risks.append({
            "timestamp": 0,
            "severity": "Medium",
            "type": "Low Visual Activity",
            "reason": (
                f"Only {scene_rate:.1f} major visual "
                "changes were detected per minute."
            )
        })


    # ========================================================
    # 6. CALCULATE RISK SCORE
    # ========================================================

    risk_points = 0


    for risk in risks:

        if risk["severity"] == "High":

            risk_points += 25

        elif risk["severity"] == "Medium":

            risk_points += 12

        else:

            risk_points += 5


    risk_score = min(
        100,
        risk_points
    )


    # ========================================================
    # 7. RETENTION SCORE
    # ========================================================

    retention_score = max(
        0,
        100 - risk_score
    )


    # ========================================================
    # 8. OVERALL ASSESSMENT
    # ========================================================

    if retention_score >= 80:

        assessment = (
            "Strong timeline structure with "
            "relatively few detected retention risks."
        )

    elif retention_score >= 60:

        assessment = (
            "Moderate retention risk. "
            "Some sections may benefit from stronger pacing."
        )

    elif retention_score >= 40:

        assessment = (
            "Several potential retention issues "
            "were detected."
        )

    else:

        assessment = (
            "High potential retention risk. "
            "The video may need significant pacing improvements."
        )


    return {
        "retention_score": retention_score,
        "risk_score": risk_score,
        "risk_count": len(risks),
        "risks": risks,
        "assessment": assessment
    }