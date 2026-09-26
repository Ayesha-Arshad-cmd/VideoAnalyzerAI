import re


def _clean_text(text):
    """Normalize text for lightweight text analysis."""

    if not text:
        return ""

    text = str(text).lower()

    text = re.sub(
        r"[^a-z0-9\s]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def _words(text):
    """Return useful words from text."""

    stop_words = {
        "the", "a", "an", "and", "or", "but",
        "is", "are", "was", "were", "to", "of",
        "in", "on", "for", "with", "this", "that",
        "it", "i", "you", "we", "they", "he", "she",
        "my", "your", "our", "their", "be", "been",
        "have", "has", "had", "do", "does", "did",
        "how", "what", "why", "when", "where",
        "can", "could", "will", "would", "should",
        "from", "as", "at", "by", "about"
    }

    return {
        word
        for word in _clean_text(text).split()
        if len(word) >= 3
        and word not in stop_words
    }


def _keyword_overlap(text_a, text_b):
    """Calculate meaningful keyword overlap."""

    words_a = _words(text_a)
    words_b = _words(text_b)

    if not words_a or not words_b:
        return 0.0

    overlap = words_a.intersection(words_b)

    smaller_set = min(
        len(words_a),
        len(words_b)
    )

    if smaller_set == 0:
        return 0.0

    return min(
        100.0,
        (len(overlap) / smaller_set) * 100
    )


def _count_matches(text, keywords):
    """Count keyword matches."""

    clean = _clean_text(text)

    return sum(
        1
        for keyword in keywords
        if keyword in clean
    )


def analyze_audience_understanding(
    title="",
    transcript_segments=None,
    story_results=None,
    hook_results=None,
    thumbnail_results=None
):
    """
    Lightweight audience-understanding and promise-matching analysis.

    Uses existing title, transcript, hook, story and thumbnail signals.
    No external model or dataset is required.
    """

    transcript_segments = transcript_segments or []
    story_results = story_results or {}
    hook_results = hook_results or {}
    thumbnail_results = thumbnail_results or {}

    transcript = " ".join(
        segment.get("text", "")
        for segment in transcript_segments
        if isinstance(segment, dict)
    )

    title = title or ""

    # ---------------------------------------------------------
    # AUDIENCE-ORIENTED LANGUAGE
    # ---------------------------------------------------------

    curiosity_words = [
        "why",
        "how",
        "secret",
        "truth",
        "actually",
        "really",
        "mistake",
        "mistakes",
        "revealed",
        "hidden",
        "test",
        "tested",
        "challenge",
        "unexpected",
        "surprising",
        "shocking"
    ]

    emotion_words = [
        "love",
        "hate",
        "excited",
        "scared",
        "fear",
        "happy",
        "sad",
        "angry",
        "amazing",
        "terrible",
        "beautiful",
        "crazy",
        "shocking",
        "surprised",
        "worried",
        "hope",
        "fail",
        "failed",
        "success"
    ]

    relatability_words = [
        "you",
        "your",
        "we",
        "us",
        "everyone",
        "people",
        "beginner",
        "student",
        "family",
        "friend",
        "daily",
        "day",
        "life",
        "problem",
        "common",
        "easy",
        "simple"
    ]

    novelty_words = [
        "new",
        "first",
        "different",
        "unique",
        "never",
        "unusual",
        "experiment",
        "tested",
        "challenge",
        "unknown",
        "alternative",
        "unexpected",
        "2026"
    ]

    curiosity_count = (
        _count_matches(title, curiosity_words)
        + _count_matches(transcript, curiosity_words)
    )

    emotion_count = (
        _count_matches(title, emotion_words)
        + _count_matches(transcript, emotion_words)
    )

    relatability_count = (
        _count_matches(title, relatability_words)
        + _count_matches(transcript, relatability_words)
    )

    novelty_count = (
        _count_matches(title, novelty_words)
        + _count_matches(transcript, novelty_words)
    )

    # ---------------------------------------------------------
    # SCORES
    # ---------------------------------------------------------

    curiosity_score = min(
        100,
        45 + curiosity_count * 8
    )

    emotion_score = min(
        100,
        45 + emotion_count * 7
    )

    relatability_score = min(
        100,
        45 + relatability_count * 6
    )

    novelty_score = min(
        100,
        45 + novelty_count * 8
    )

    # Existing hook/stories provide additional evidence.

    hook_score = float(
        hook_results.get(
            "hook_score",
            50
        )
    )

    story_score = float(
        story_results.get(
            "story_score",
            50
        )
    )

    curiosity_score = round(
        curiosity_score * 0.65
        + hook_score * 0.35,
        1
    )

    relatability_score = round(
        relatability_score * 0.75
        + story_score * 0.25,
        1
    )

    # ---------------------------------------------------------
    # TITLE ↔ CONTENT PROMISE
    # ---------------------------------------------------------

    title_transcript_overlap = _keyword_overlap(
        title,
        transcript
    )

    if not transcript.strip():
        title_content_promise_score = 0
    else:
        title_content_promise_score = round(
            title_transcript_overlap,
            1
        )

    # ---------------------------------------------------------
    # TITLE CLARITY
    # ---------------------------------------------------------

    title_words = _words(title)

    title_clarity_score = 50.0

    if 4 <= len(title_words) <= 15:
        title_clarity_score += 20

    if any(
        word in _clean_text(title)
        for word in curiosity_words
    ):
        title_clarity_score += 10

    if any(
        word in _clean_text(title)
        for word in novelty_words
    ):
        title_clarity_score += 10

    if title.strip():
        title_clarity_score += 10

    title_clarity_score = min(
        100,
        title_clarity_score
    )

    # ---------------------------------------------------------
    # THUMBNAIL CONSISTENCY
    # ---------------------------------------------------------

    thumbnail_available = bool(
        thumbnail_results
    )

    if thumbnail_available:

        thumbnail_score = float(
            thumbnail_results.get(
                "thumbnail_score",
                50
            )
        )

        thumbnail_consistency_score = round(
            (
                thumbnail_score
                + title_content_promise_score
            ) / 2,
            1
        )

    else:

        thumbnail_consistency_score = 0

    # ---------------------------------------------------------
    # OVERALL PROMISE MATCH
    # ---------------------------------------------------------

    promise_components = [
        title_content_promise_score,
        title_clarity_score
    ]

    if thumbnail_available:
        promise_components.append(
            thumbnail_consistency_score
        )

    promise_match_score = round(
        sum(promise_components)
        / len(promise_components),
        1
    )

    # ---------------------------------------------------------
    # AUDIENCE UNDERSTANDING
    # ---------------------------------------------------------

    audience_understanding_score = round(
        (
            curiosity_score * 0.25
            + emotion_score * 0.15
            + relatability_score * 0.20
            + novelty_score * 0.15
            + promise_match_score * 0.25
        ),
        1
    )

    # ---------------------------------------------------------
    # TARGET AUDIENCE CLUES
    # ---------------------------------------------------------

    audience_clues = []

    clean_title = _clean_text(title)
    clean_transcript = _clean_text(transcript)

    combined_text = (
        clean_title
        + " "
        + clean_transcript
    )

    if any(
        word in combined_text
        for word in [
            "beginner",
            "easy",
            "simple",
            "learn",
            "tutorial",
            "guide"
        ]
    ):
        audience_clues.append(
            "Likely useful to beginners or learners."
        )

    if any(
        word in combined_text
        for word in [
            "student",
            "university",
            "college",
            "assignment",
            "exam"
        ]
    ):
        audience_clues.append(
            "Content contains signals relevant to students."
        )

    if any(
        word in combined_text
        for word in [
            "review",
            "test",
            "tested",
            "compare",
            "comparison"
        ]
    ):
        audience_clues.append(
            "Likely relevant to viewers researching or comparing options."
        )

    if any(
        word in combined_text
        for word in [
            "how",
            "tutorial",
            "step",
            "guide",
            "build",
            "create"
        ]
    ):
        audience_clues.append(
            "Likely targets viewers looking for practical information."
        )

    if any(
        word in combined_text
        for word in [
            "challenge",
            "experiment",
            "trying",
            "tried",
            "24",
            "7 days",
            "30 days"
        ]
    ):
        audience_clues.append(
            "Likely appeals to viewers interested in experiences or challenges."
        )

    if not audience_clues:
        audience_clues.append(
            "Audience category could not be strongly inferred from the available text."
        )

    # ---------------------------------------------------------
    # WARNINGS
    # ---------------------------------------------------------

    warnings = []

    if title_content_promise_score < 30:
        warnings.append(
            "The title has limited keyword/topic overlap with the spoken content."
        )

    if curiosity_score < 55:
        warnings.append(
            "Limited curiosity signals were detected."
        )

    if emotion_score < 55:
        warnings.append(
            "Limited emotional language was detected."
        )

    if relatability_score < 55:
        warnings.append(
            "Limited audience-relatability signals were detected."
        )

    if novelty_score < 55:
        warnings.append(
            "Limited novelty or differentiation signals were detected."
        )

    # ---------------------------------------------------------
    # POSITIVE SIGNALS
    # ---------------------------------------------------------

    signals = []

    if title_content_promise_score >= 60:
        signals.append(
            "Title and spoken content show strong topical alignment."
        )

    if curiosity_score >= 70:
        signals.append(
            "Strong curiosity-oriented language detected."
        )

    if emotion_score >= 70:
        signals.append(
            "Strong emotional language detected."
        )

    if relatability_score >= 70:
        signals.append(
            "Strong audience-relatability signals detected."
        )

    if novelty_score >= 70:
        signals.append(
            "Strong novelty or differentiation signals detected."
        )

    if not signals:
        signals.append(
            "No dominant audience signal exceeded the current threshold."
        )

    # ---------------------------------------------------------
    # ASSESSMENT
    # ---------------------------------------------------------

    if audience_understanding_score >= 80:

        assessment = (
            "The available signals provide a strong understanding "
            "of the likely audience response drivers and the content promise."
        )

    elif audience_understanding_score >= 65:

        assessment = (
            "The available signals provide a moderate understanding "
            "of the likely audience and content promise."
        )

    elif audience_understanding_score >= 50:

        assessment = (
            "Audience intent is partially identifiable, but several "
            "audience-response signals remain weak."
        )

    else:

        assessment = (
            "The available text provides limited evidence about the "
            "intended audience and content promise."
        )

    # ---------------------------------------------------------
    # CONFIDENCE
    # ---------------------------------------------------------

    if len(transcript.strip()) >= 200:
        confidence = "Moderate"

    elif len(transcript.strip()) >= 50:
        confidence = "Low-Moderate"

    else:
        confidence = "Low"

    return {
        "audience_understanding_score": audience_understanding_score,

        "curiosity_score": curiosity_score,

        "emotion_score": emotion_score,

        "relatability_score": relatability_score,

        "novelty_score": novelty_score,

        "title_clarity_score": round(
            title_clarity_score,
            1
        ),

        "title_content_promise_score":
            title_content_promise_score,

        "thumbnail_consistency_score":
            thumbnail_consistency_score,

        "promise_match_score":
            promise_match_score,

        "audience_clues":
            audience_clues,

        "signals":
            signals,

        "warnings":
            warnings,

        "assessment":
            assessment,

        "confidence":
            confidence,

        "status":
            "Audience understanding analysis complete"
    }