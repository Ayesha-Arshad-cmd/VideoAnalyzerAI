def calculate_attention_analysis(
    duration,
    scenes=None,
    retention_results=None,
    hook_results=None,
    visual_results=None,
    timeline_results=None,
    story_results=None
):
    """
    Estimate viewer attention risk and an approximate attention curve
    using existing lightweight video-analysis signals.

    This is a rule-based estimate, not measured viewer behavior.
    """

    scenes = scenes or []
    retention_results = retention_results or {}
    hook_results = hook_results or {}
    visual_results = visual_results or {}
    timeline_results = timeline_results or {}
    story_results = story_results or {}

    duration = float(duration or 0)

    if duration <= 0:
        return {
            "attention_score": 0,
            "attention_curve": [],
            "attention_risks": [],
            "attention_recoveries": [],
            "assessment": "Unable to estimate attention without video duration.",
            "status": "Insufficient video data",
            "confidence": "Low"
        }

    # ---------------------------------------------------------
    # BASE ATTENTION
    # ---------------------------------------------------------

    attention = 70.0

    hook_score = float(
        hook_results.get("hook_score", 50)
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

    story_score = float(
        story_results.get("story_score", 50)
    )

    attention += (hook_score - 50) * 0.15
    attention += (retention_score - 50) * 0.20
    attention += (visual_score - 50) * 0.10
    attention += (activity_score - 50) * 0.10
    attention += (story_score - 50) * 0.10

    attention = max(0, min(100, attention))

    # ---------------------------------------------------------
    # BUILD IMPORTANT TIMESTAMPS
    # ---------------------------------------------------------

    timestamps = {0.0, duration}

    for scene in scenes:
        try:
            timestamp = float(scene.get("timestamp", 0))

            if 0 < timestamp < duration:
                timestamps.add(timestamp)
        except (TypeError, ValueError):
            pass

    for risk in retention_results.get("risks", []):
        try:
            timestamp = float(risk.get("timestamp", 0))

            if 0 < timestamp < duration:
                timestamps.add(timestamp)
        except (TypeError, ValueError):
            pass

    timestamps = sorted(timestamps)

    # ---------------------------------------------------------
    # ESTIMATE ATTENTION AT EACH POINT
    # ---------------------------------------------------------

    attention_curve = []

    current_attention = attention

    first_visual_change = hook_results.get(
        "first_visual_change"
    )

    opening_silence = hook_results.get(
        "opening_silence",
        0
    )

    risk_timestamps = []

    for risk in retention_results.get("risks", []):
        try:
            risk_timestamps.append(
                (
                    float(risk.get("timestamp", 0)),
                    risk.get("severity", "Medium")
                )
            )
        except (TypeError, ValueError):
            pass

    for timestamp in timestamps:

        point_attention = current_attention

        # -----------------------------------------------------
        # EARLY HOOK EFFECT
        # -----------------------------------------------------

        if timestamp <= min(30, duration):

            if (
                first_visual_change is not None
                and float(first_visual_change) <= 3
            ):
                point_attention += 8

            elif (
                first_visual_change is not None
                and float(first_visual_change) > 8
            ):
                point_attention -= 10

            if opening_silence and float(opening_silence) > 3:
                point_attention -= 8

        # -----------------------------------------------------
        # SCENE CHANGE = POSSIBLE ATTENTION RECOVERY
        # -----------------------------------------------------

        nearby_scene = False

        for scene in scenes:
            try:
                scene_time = float(
                    scene.get("timestamp", 0)
                )

                if abs(scene_time - timestamp) <= 0.5:
                    nearby_scene = True
                    break

            except (TypeError, ValueError):
                continue

        if nearby_scene:
            point_attention += 5

        # -----------------------------------------------------
        # RETENTION RISK = ATTENTION DROP
        # -----------------------------------------------------

        for risk_time, severity in risk_timestamps:

            if abs(risk_time - timestamp) <= 0.5:

                if severity == "High":
                    point_attention -= 18

                elif severity == "Medium":
                    point_attention -= 10

                else:
                    point_attention -= 5

        # -----------------------------------------------------
        # NATURAL LONG-FORM ATTENTION DECAY
        # -----------------------------------------------------

        if duration > 60:
            decay = (
                timestamp / duration
            ) * 8

            point_attention -= decay

        # -----------------------------------------------------
        # KEEP SCORE VALID
        # -----------------------------------------------------

        point_attention = max(
            0,
            min(
                100,
                point_attention
            )
        )

        current_attention = point_attention

        attention_curve.append(
            {
                "timestamp": round(timestamp, 2),
                "attention": round(
                    point_attention,
                    1
                )
            }
        )

    # ---------------------------------------------------------
    # ADD INTERMEDIATE POINTS
    # ---------------------------------------------------------

    if len(attention_curve) < 5:

        interval = duration / 4

        expanded_curve = []

        for i in range(5):

            timestamp = min(
                duration,
                i * interval
            )

            ratio = (
                timestamp / duration
                if duration > 0
                else 0
            )

            estimated = (
                attention
                - ratio * 8
            )

            estimated = max(
                0,
                min(
                    100,
                    estimated
                )
            )

            expanded_curve.append(
                {
                    "timestamp": round(
                        timestamp,
                        2
                    ),
                    "attention": round(
                        estimated,
                        1
                    )
                }
            )

        attention_curve = expanded_curve

    # ---------------------------------------------------------
    # FIND ATTENTION DROPS
    # ---------------------------------------------------------

    attention_risks = []

    for i in range(1, len(attention_curve)):

        previous = attention_curve[i - 1]
        current = attention_curve[i]

        drop = (
            previous["attention"]
            - current["attention"]
        )

        if drop >= 12:

            attention_risks.append(
                {
                    "timestamp": current["timestamp"],
                    "drop": round(drop, 1),
                    "severity": "High",
                    "reason": (
                        "Estimated attention drops sharply "
                        "at this point."
                    )
                }
            )

        elif drop >= 6:

            attention_risks.append(
                {
                    "timestamp": current["timestamp"],
                    "drop": round(drop, 1),
                    "severity": "Medium",
                    "reason": (
                        "Estimated attention may weaken "
                        "at this point."
                    )
                }
            )

    # ---------------------------------------------------------
    # FIND RECOVERY POINTS
    # ---------------------------------------------------------

    attention_recoveries = []

    for i in range(1, len(attention_curve)):

        previous = attention_curve[i - 1]
        current = attention_curve[i]

        increase = (
            current["attention"]
            - previous["attention"]
        )

        if increase >= 5:

            attention_recoveries.append(
                {
                    "timestamp": current["timestamp"],
                    "increase": round(
                        increase,
                        1
                    ),
                    "reason": (
                        "Visual or structural activity "
                        "may help recover attention."
                    )
                }
            )

    # ---------------------------------------------------------
    # FINAL SCORE
    # ---------------------------------------------------------

    curve_average = (
        sum(
            point["attention"]
            for point in attention_curve
        )
        / len(attention_curve)
    )

    attention_score = round(
        curve_average,
        1
    )

    # ---------------------------------------------------------
    # ASSESSMENT
    # ---------------------------------------------------------

    if attention_score >= 80:

        assessment = (
            "Strong estimated attention pattern with "
            "limited structural attention risks."
        )

    elif attention_score >= 65:

        assessment = (
            "Moderate estimated attention pattern. "
            "Some points may require stronger pacing "
            "or visual variation."
        )

    elif attention_score >= 50:

        assessment = (
            "Attention may weaken at several points. "
            "Review pacing, scene changes and retention risks."
        )

    else:

        assessment = (
            "The current signals indicate significant "
            "estimated attention risk throughout the video."
        )

    # ---------------------------------------------------------
    # CONFIDENCE
    # ---------------------------------------------------------

    available_signals = sum(
        [
            bool(scenes),
            bool(retention_results),
            bool(hook_results),
            bool(visual_results),
            bool(timeline_results),
            bool(story_results)
        ]
    )

    if available_signals >= 5:
        confidence = "Moderate"
    elif available_signals >= 3:
        confidence = "Low-Moderate"
    else:
        confidence = "Low"

    return {
        "attention_score": attention_score,
        "attention_curve": attention_curve,
        "attention_risks": attention_risks,
        "attention_recoveries": attention_recoveries,
        "assessment": assessment,
        "status": "Estimated attention analysis complete",
        "confidence": confidence
    }