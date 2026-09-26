import re


def analyze_title(title):
    """
    Analyze a YouTube video title.

    V1 uses rule-based signals.
    It does not claim to predict YouTube's algorithm
    or guarantee clicks/views.
    """

    title = title.strip()

    results = {}

    # -----------------------------
    # Basic information
    # -----------------------------

    character_count = len(title)
    word_list = title.split()
    word_count = len(word_list)

    results["title"] = title
    results["character_count"] = character_count
    results["word_count"] = word_count

    # -----------------------------
    # Length analysis
    # -----------------------------

    warnings = []
    signals = []
    suggestions = []

    if character_count == 0:

        warnings.append(
            "No title was provided."
        )

        return {
            "title": title,
            "character_count": 0,
            "word_count": 0,
            "title_score": 0,
            "signals": [],
            "warnings": warnings,
            "suggestions": [
                "Add a clear and specific video title."
            ],
            "assessment": "No title provided."
        }

    if 30 <= character_count <= 70:

        signals.append(
            "The title has a reasonable length."
        )

    elif character_count < 30:

        warnings.append(
            "The title is quite short."
        )

        suggestions.append(
            "Consider adding useful context "
            "without making the title unnecessarily long."
        )

    else:

        warnings.append(
            "The title is relatively long."
        )

        suggestions.append(
            "Consider shortening the title and "
            "keeping the most important words."
        )

    # -----------------------------
    # Question / curiosity signals
    # -----------------------------

    if "?" in title:

        signals.append(
            "The title uses a question format."
        )

    # -----------------------------
    # Numbers
    # -----------------------------

    if re.search(r"\d+", title):

        signals.append(
            "The title contains a number or numerical detail."
        )

    # -----------------------------
    # Specificity
    # -----------------------------

    specific_terms = [
        "how",
        "why",
        "best",
        "worst",
        "guide",
        "tutorial",
        "review",
        "test",
        "comparison",
        "tips",
        "mistakes",
        "steps",
        "before",
        "after",
        "vs",
        "versus"
    ]

    title_lower = title.lower()

    specificity_terms_found = [
        term
        for term in specific_terms
        if term in title_lower
    ]

    if specificity_terms_found:

        signals.append(
            "The title contains terms that provide "
            "some context about the video's topic."
        )

    else:

        warnings.append(
            "The title may not communicate enough "
            "specific context."
        )

        suggestions.append(
            "Make the topic or viewer benefit more specific."
        )

    # -----------------------------
    # Excessive punctuation
    # -----------------------------

    exclamation_count = title.count("!")
    question_count = title.count("?")

    if exclamation_count >= 3:

        warnings.append(
            "The title uses many exclamation marks."
        )

        suggestions.append(
            "Reduce excessive punctuation."
        )

    if question_count >= 3:

        warnings.append(
            "The title uses many question marks."
        )

        suggestions.append(
            "Use punctuation selectively."
        )

    # -----------------------------
    # ALL CAPS detection
    # -----------------------------

    letters = [
        character
        for character in title
        if character.isalpha()
    ]

    if letters:

        uppercase_letters = [
            character
            for character in letters
            if character.isupper()
        ]

        uppercase_percentage = (
            len(uppercase_letters)
            / len(letters)
            * 100
        )

    else:

        uppercase_percentage = 0

    results["uppercase_percentage"] = round(
        uppercase_percentage,
        2
    )

    if uppercase_percentage >= 70:

        warnings.append(
            "A large portion of the title is uppercase."
        )

        suggestions.append(
            "Use capitalization selectively "
            "instead of writing most of the title in uppercase."
        )

    # -----------------------------
    # Repeated words
    # -----------------------------

    normalized_words = [
        word.lower().strip(".,!?;:\"'()[]{}")
        for word in word_list
    ]

    normalized_words = [
        word
        for word in normalized_words
        if word
    ]

    repeated_words = []

    for word in set(normalized_words):

        if normalized_words.count(word) >= 3:

            repeated_words.append(word)

    if repeated_words:

        warnings.append(
            "Some words are repeated multiple times."
        )

        suggestions.append(
            "Remove unnecessary repetition."
        )

    # -----------------------------
    # Potential clickbait wording
    # -----------------------------

    clickbait_terms = [
        "you won't believe",
        "shocking",
        "insane",
        "crazy",
        "secret",
        "this changes everything",
        "gone wrong",
        "must watch",
        "watch before",
        "exposed"
    ]

    detected_clickbait_terms = [
        term
        for term in clickbait_terms
        if term in title_lower
    ]

    if detected_clickbait_terms:

        warnings.append(
            "The title contains wording that may "
            "create a clickbait impression."
        )

        suggestions.append(
            "Make sure the title accurately represents "
            "what viewers will actually see in the video."
        )

    # -----------------------------
    # Generic title detection
    # -----------------------------

    generic_titles = [
        "my video",
        "new video",
        "watch this",
        "check this out",
        "important video",
        "youtube video"
    ]

    if title_lower in generic_titles:

        warnings.append(
            "The title is very generic."
        )

        suggestions.append(
            "Describe the actual topic or value "
            "of the video."
        )

    # -----------------------------
    # Score
    # -----------------------------

    score = 60

    # Length
    if 30 <= character_count <= 70:
        score += 15
    elif character_count < 20:
        score -= 10
    elif character_count > 90:
        score -= 10

    # Specificity
    if specificity_terms_found:
        score += 10
    else:
        score -= 8

    # Numbers
    if re.search(r"\d+", title):
        score += 3

    # Question format
    if "?" in title:
        score += 3

    # Excessive punctuation
    if exclamation_count >= 3:
        score -= 7

    if question_count >= 3:
        score -= 5

    # Excessive uppercase
    if uppercase_percentage >= 70:
        score -= 8

    # Repeated words
    if repeated_words:
        score -= 5

    # Clickbait wording
    if detected_clickbait_terms:
        score -= 8

    # Generic title
    if title_lower in generic_titles:
        score -= 15

    score = max(
        0,
        min(
            score,
            100
        )
    )

    # -----------------------------
    # Assessment
    # -----------------------------

    if score >= 80:

        assessment = (
            "Strong title structure based on "
            "the measurable signals analyzed."
        )

    elif score >= 60:

        assessment = (
            "The title is reasonably structured, "
            "but some elements could be improved."
        )

    elif score >= 40:

        assessment = (
            "The title has several areas "
            "that could be improved."
        )

    else:

        assessment = (
            "The title has significant areas "
            "that should be improved."
        )

    results["title_score"] = score
    results["signals"] = signals
    results["warnings"] = warnings
    results["suggestions"] = suggestions
    results["assessment"] = assessment

    return results