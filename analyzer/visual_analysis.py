import cv2


def analyze_visuals(
    video_path,
    sample_interval=2.0
):
    """
    Analyze sampled video frames.

    V1 uses measurable visual properties:
    brightness, darkness, overexposure,
    frame similarity and visual changes.

    It does not claim to understand
    semantic image quality.
    """

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        return {
            "visual_score": 0,
            "frames_analyzed": 0,
            "warnings": [
                "Could not open the video."
            ],
            "signals": []
        }

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = cap.get(
        cv2.CAP_PROP_FRAME_COUNT
    )

    if fps <= 0:
        cap.release()

        return {
            "visual_score": 0,
            "frames_analyzed": 0,
            "warnings": [
                "Could not determine video FPS."
            ],
            "signals": []
        }

    duration = frame_count / fps

    frames_analyzed = 0
    dark_frames = 0
    bright_frames = 0
    repeated_frames = 0

    brightness_values = []

    previous_gray = None
    current_time = 0.0

    while current_time < duration:

        cap.set(
            cv2.CAP_PROP_POS_MSEC,
            current_time * 1000
        )

        success, frame = cap.read()

        if not success:
            break

        # Resize for faster analysis
        frame = cv2.resize(
            frame,
            (320, 180)
        )

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        # ----------------------------------------------------
        # BRIGHTNESS
        # ----------------------------------------------------

        brightness = float(
            gray.mean()
        )

        brightness_values.append(
            brightness
        )

        if brightness < 35:
            dark_frames += 1

        if brightness > 220:
            bright_frames += 1

        # ----------------------------------------------------
        # FRAME SIMILARITY
        # ----------------------------------------------------

        if previous_gray is not None:

            difference = cv2.absdiff(
                previous_gray,
                gray
            )

            change_score = float(
                difference.mean()
            )

            if change_score < 3:
                repeated_frames += 1

        previous_gray = gray

        frames_analyzed += 1

        current_time += sample_interval

    cap.release()

    # ========================================================
    # PERCENTAGES
    # ========================================================

    if frames_analyzed > 0:

        dark_percentage = (
            dark_frames
            / frames_analyzed
            * 100
        )

        bright_percentage = (
            bright_frames
            / frames_analyzed
            * 100
        )

        repeated_percentage = (
            repeated_frames
            / max(frames_analyzed - 1, 1)
            * 100
        )

        average_brightness = (
            sum(brightness_values)
            / len(brightness_values)
        )

    else:

        dark_percentage = 0
        bright_percentage = 0
        repeated_percentage = 0
        average_brightness = 0

    # ========================================================
    # RESULTS
    # ========================================================

    results = {

        "frames_analyzed": frames_analyzed,

        "average_brightness": round(
            average_brightness,
            2
        ),

        "dark_percentage": round(
            dark_percentage,
            2
        ),

        "bright_percentage": round(
            bright_percentage,
            2
        ),

        "repeated_percentage": round(
            repeated_percentage,
            2
        )
    }

    # ========================================================
    # SIGNALS & WARNINGS
    # ========================================================

    signals = []
    warnings = []

    if (
        dark_percentage < 10
        and bright_percentage < 10
    ):
        signals.append(
            "Most sampled frames have "
            "reasonable brightness levels."
        )

    if repeated_percentage < 20:

        signals.append(
            "The sampled frames show "
            "reasonable visual variation."
        )

    if dark_percentage >= 20:

        warnings.append(
            f"{dark_percentage:.1f}% of sampled "
            "frames are very dark."
        )

    if bright_percentage >= 20:

        warnings.append(
            f"{bright_percentage:.1f}% of sampled "
            "frames are highly bright or overexposed."
        )

    if repeated_percentage >= 50:

        warnings.append(
            f"{repeated_percentage:.1f}% of sampled "
            "frames are visually very similar."
        )

    # ========================================================
    # VISUAL SCORE
    # ========================================================

    score = 100

    if dark_percentage >= 20:
        score -= 20
    elif dark_percentage >= 10:
        score -= 10

    if bright_percentage >= 20:
        score -= 20
    elif bright_percentage >= 10:
        score -= 10

    if repeated_percentage >= 50:
        score -= 20
    elif repeated_percentage >= 30:
        score -= 10

    score = max(
        0,
        min(
            score,
            100
        )
    )

    results["visual_score"] = score

    # ========================================================
    # ASSESSMENT
    # ========================================================

    if score >= 80:

        assessment = (
            "The sampled frames show generally "
            "healthy visual characteristics."
        )

    elif score >= 60:

        assessment = (
            "The video has moderate visual quality. "
            "Some visual areas could be improved."
        )

    elif score >= 40:

        assessment = (
            "Several visual quality issues "
            "were detected in the sampled frames."
        )

    else:

        assessment = (
            "Significant visual quality issues "
            "were detected."
        )

    results["signals"] = signals
    results["warnings"] = warnings
    results["assessment"] = assessment

    return results