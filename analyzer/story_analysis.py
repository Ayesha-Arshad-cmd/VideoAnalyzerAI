def analyze_story(
    duration,
    transcript_segments
):
    """
    Analyze the structure and focus of a video
    using its transcript.

    V1 is rule-based.
    It does not claim to understand the video
    like a human or predict audience behavior.
    """

    results = {}

    # ========================================================
    # BASIC INFORMATION
    # ========================================================

    total_segments = len(transcript_segments)

    results["total_segments"] = total_segments

    # ========================================================
    # TRANSCRIPT COVERAGE
    # ========================================================

    total_speech_duration = 0

    for segment in transcript_segments:

        start = segment["start"]
        end = segment["end"]

        total_speech_duration += max(
            0,
            end - start
        )

    if duration > 0:
        speech_coverage = (
            total_speech_duration
            / duration
            * 100
        )
    else:
        speech_coverage = 0

    results["speech_coverage"] = round(
        min(speech_coverage, 100),
        2
    )

    # ========================================================
    # EARLY TOPIC INTRODUCTION
    # ========================================================

    early_text = ""

    for segment in transcript_segments:

        if segment["start"] <= min(30, duration):

            early_text += (
                segment["text"] + " "
            )

    early_text = early_text.strip()

    results["early_content"] = early_text

    # ========================================================
    # BEGINNING / MIDDLE / END
    # ========================================================

    beginning_text = ""
    middle_text = ""
    ending_text = ""

    for segment in transcript_segments:

        midpoint = duration / 2

        if segment["start"] <= min(30, duration):
            beginning_text += segment["text"] + " "

        elif segment["start"] < midpoint:
            middle_text += segment["text"] + " "

        else:
            ending_text += segment["text"] + " "

    results["beginning_content"] = beginning_text.strip()
    results["middle_content"] = middle_text.strip()
    results["ending_content"] = ending_text.strip()

    # ========================================================
    # STRUCTURE SIGNALS
    # ========================================================

    signals = []
    warnings = []

    # Beginning
    if beginning_text.strip():

        signals.append(
            "The video contains identifiable "
            "opening content."
        )

    else:

        warnings.append(
            "Little or no spoken content was "
            "detected in the opening."
        )

    # Middle
    if middle_text.strip():

        signals.append(
            "The video contains a middle section "
            "with continued content."
        )

    else:

        warnings.append(
            "A clear middle section could not "
            "be detected."
        )

    # Ending
    if ending_text.strip():

        signals.append(
            "The video contains content near "
            "the ending."
        )

    else:

        warnings.append(
            "Little or no spoken content was "
            "detected near the ending."
        )

    # ========================================================
    # CONTENT LENGTH
    # ========================================================

    if total_segments == 0:

        warnings.append(
            "No transcript content was detected."
        )

    elif total_segments < 5:

        warnings.append(
            "The transcript contains very few "
            "content segments."
        )

    elif total_segments >= 15:

        signals.append(
            "The video contains substantial "
            "spoken content."
        )

    # ========================================================
    # FOCUS CHECK
    # ========================================================

    # V1 uses segment distribution as a simple
    # consistency signal.

    if total_segments > 0:

        average_segment_length = (
            total_speech_duration
            / total_segments
        )

    else:

        average_segment_length = 0

    results["average_segment_length"] = round(
        average_segment_length,
        2
    )

    if average_segment_length < 1:

        warnings.append(
            "Speech is divided into very short "
            "segments, which may indicate fragmented content."
        )

    elif average_segment_length >= 2:

        signals.append(
            "Speech segments generally contain "
            "continuous content."
        )

    # ========================================================
    # STORY SCORE
    # ========================================================

    score = 50

    # Speech coverage
    if speech_coverage >= 60:
        score += 15
    elif speech_coverage >= 30:
        score += 8
    elif speech_coverage < 15:
        score -= 15

    # Beginning
    if beginning_text.strip():
        score += 10
    else:
        score -= 10

    # Middle
    if middle_text.strip():
        score += 10
    else:
        score -= 10

    # Ending
    if ending_text.strip():
        score += 10
    else:
        score -= 10

    # Content quantity
    if total_segments >= 15:
        score += 5
    elif total_segments < 5:
        score -= 5

    score = max(
        0,
        min(
            score,
            100
        )
    )

    results["story_score"] = score

    # ========================================================
    # ASSESSMENT
    # ========================================================

    if score >= 80:

        assessment = (
            "Strong content structure detected. "
            "The video contains substantial content "
            "across its timeline."
        )

    elif score >= 60:

        assessment = (
            "Moderate content structure. "
            "The video has a recognizable structure, "
            "but some areas could be strengthened."
        )

    elif score >= 40:

        assessment = (
            "The video shows several potential "
            "content-structure weaknesses."
        )

    else:

        assessment = (
            "The video shows significant potential "
            "story and content-structure weaknesses."
        )

    results["signals"] = signals
    results["warnings"] = warnings
    results["assessment"] = assessment

    return results