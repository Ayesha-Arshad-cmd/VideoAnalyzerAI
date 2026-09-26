import math
from collections import Counter


# ============================================================
# PHASE 32 — CHANNEL PERFORMANCE PREDICTION ENGINE
# ============================================================


FEATURES = [
    "duration_seconds",
    "views",
    "watch_time",
    "average_view_duration",
    "average_percentage_viewed",
    "impressions",
    "ctr",
    "subscribers_gained",
    "views_per_subscriber",
    "like_rate",
    "comment_rate",
    "engagement_rate"
]


# ============================================================
# SAFE NUMBER CONVERSION
# ============================================================

def safe_float(value, default=0.0):

    try:

        if value is None:
            return default

        if isinstance(value, str):

            value = value.strip()

            if value == "":
                return default

        return float(value)

    except:

        return default


# ============================================================
# MIN / MAX NORMALIZATION
# ============================================================

def normalize(value, minimum, maximum):

    if maximum <= minimum:

        return 0.5

    result = (
        (value - minimum)
        / (maximum - minimum)
    )

    return max(
        0.0,
        min(
            1.0,
            result
        )
    )


# ============================================================
# PREPARE DATASET
# ============================================================

def prepare_dataset(records):

    cleaned = []

    for record in records:

        if not isinstance(record, dict):

            continue

        row = {}

        for feature in FEATURES:

            row[feature] = safe_float(
                record.get(feature, 0)
            )

        row["performance_label"] = str(
            record.get(
                "performance_label",
                "unknown"
            )
        ).lower().strip()

        row["title"] = str(
            record.get(
                "title",
                ""
            )
        )

        cleaned.append(row)

    return cleaned


# ============================================================
# DATASET STATISTICS
# ============================================================

def calculate_statistics(records):

    statistics = {}

    for feature in FEATURES:

        values = [
            row[feature]
            for row in records
        ]

        if not values:

            statistics[feature] = {
                "min": 0.0,
                "max": 1.0,
                "mean": 0.0
            }

            continue

        statistics[feature] = {

            "min": min(values),

            "max": max(values),

            "mean": (
                sum(values)
                / len(values)
            )
        }

    return statistics


# ============================================================
# HISTORICAL PERFORMANCE PROFILE
# ============================================================

def build_performance_profile(records):

    labels = [
        row["performance_label"]
        for row in records
        if row["performance_label"]
        != "unknown"
    ]

    counts = Counter(labels)

    total = sum(
        counts.values()
    )

    if total == 0:

        return {
            "low": 0,
            "medium": 0,
            "high": 0
        }

    return {

        "low": round(
            counts.get("low", 0)
            / total
            * 100,
            1
        ),

        "medium": round(
            counts.get("medium", 0)
            / total
            * 100,
            1
        ),

        "high": round(
            counts.get("high", 0)
            / total
            * 100,
            1
        )
    }


# ============================================================
# CURRENT VIDEO FEATURE EXTRACTION
# ============================================================

def build_current_features(
    duration=0,
    title_score=50,
    thumbnail_score=50,
    hook_score=50,
    story_score=50,
    retention_score=50,
    audience_score=50,
    attention_score=50
):

    return {

        "duration_seconds":
            safe_float(duration),

        "views":
            0.0,

        "watch_time":
            retention_score,

        "average_view_duration":
            retention_score,

        "average_percentage_viewed":
            retention_score,

        "impressions":
            audience_score,

        "ctr":
            title_score,

        "subscribers_gained":
            audience_score,

        "views_per_subscriber":
            audience_score,

        "like_rate":
            audience_score,

        "comment_rate":
            audience_score,

        "engagement_rate":
            (
                audience_score
                + attention_score
            ) / 2
    }


# ============================================================
# HISTORICAL SIMILARITY
# ============================================================

def calculate_similarity(
    current,
    historical,
    statistics
):

    differences = []

    important_features = [
        "duration_seconds",
        "average_percentage_viewed",
        "ctr",
        "engagement_rate",
        "watch_time"
    ]

    for feature in important_features:

        current_value = current.get(
            feature,
            0
        )

        historical_value = historical.get(
            feature,
            0
        )

        minimum = statistics[
            feature
        ]["min"]

        maximum = statistics[
            feature
        ]["max"]

        current_normalized = normalize(
            current_value,
            minimum,
            maximum
        )

        historical_normalized = normalize(
            historical_value,
            minimum,
            maximum
        )

        differences.append(
            abs(
                current_normalized
                - historical_normalized
            )
        )

    if not differences:

        return 0.0

    average_difference = (
        sum(differences)
        / len(differences)
    )

    similarity = (
        1.0
        - average_difference
    )

    return max(
        0.0,
        min(
            1.0,
            similarity
        )
    )


# ============================================================
# FIND SIMILAR HISTORICAL VIDEOS
# ============================================================

def find_similar_videos(
    current,
    records,
    statistics,
    limit=5
):

    matches = []

    for record in records:

        similarity = calculate_similarity(
            current,
            record,
            statistics
        )

        matches.append(
            {
                "title":
                    record.get(
                        "title",
                        "Unknown"
                    ),

                "label":
                    record.get(
                        "performance_label",
                        "unknown"
                    ),

                "similarity":
                    round(
                        similarity * 100,
                        1
                    )
            }
        )

    matches.sort(
        key=lambda x:
            x["similarity"],
        reverse=True
    )

    return matches[:limit]


# ============================================================
# WEIGHTED HISTORICAL PREDICTION
# ============================================================

def predict_performance(
    current,
    records,
    statistics
):

    if not records:

        return {
            "prediction":
                "Insufficient Data",

            "confidence":
                0.0,

            "probabilities": {
                "low": 0.0,
                "medium": 0.0,
                "high": 0.0
            }
        }

    weighted_scores = {
        "low": 0.0,
        "medium": 0.0,
        "high": 0.0
    }

    total_weight = 0.0

    for record in records:

        label = record.get(
            "performance_label",
            "unknown"
        )

        if label not in weighted_scores:

            continue

        similarity = calculate_similarity(
            current,
            record,
            statistics
        )

        weight = (
            similarity
            + 0.05
        )

        weighted_scores[
            label
        ] += weight

        total_weight += weight

    if total_weight == 0:

        return {
            "prediction":
                "Insufficient Data",

            "confidence":
                0.0,

            "probabilities": {
                "low": 0.0,
                "medium": 0.0,
                "high": 0.0
            }
        }

    probabilities = {

        label:
            round(
                weighted_scores[label]
                / total_weight
                * 100,
                1
            )

        for label in
        weighted_scores
    }

    prediction = max(
        probabilities,
        key=probabilities.get
    )

    confidence = probabilities[
        prediction
    ]

    return {

        "prediction":
            prediction,

        "confidence":
            round(
                confidence,
                1
            ),

        "probabilities":
            probabilities
    }


# ============================================================
# GENERATE EXPLANATION
# ============================================================

def generate_prediction_explanation(
    prediction,
    probabilities,
    current
):

    explanation = []

    if current.get(
        "average_percentage_viewed",
        0
    ) >= 50:

        explanation.append(
            "Strong predicted retention "
            "relative to the historical range."
        )

    elif current.get(
        "average_percentage_viewed",
        0
    ) < 30:

        explanation.append(
            "Predicted retention is relatively weak."
        )

    if current.get(
        "ctr",
        0
    ) >= 5:

        explanation.append(
            "Title/thumbnail click-through "
            "signal is strong."
        )

    elif current.get(
        "ctr",
        0
    ) < 2:

        explanation.append(
            "Title/thumbnail click-through "
            "signal is relatively weak."
        )

    if current.get(
        "engagement_rate",
        0
    ) >= 5:

        explanation.append(
            "Engagement signals are strong."
        )

    elif current.get(
        "engagement_rate",
        0
    ) < 2:

        explanation.append(
            "Engagement signals are relatively low."
        )

    if not explanation:

        explanation.append(
            "Prediction is primarily based "
            "on similarity to historical videos."
        )

    return explanation


# ============================================================
# COMPLETE PREDICTION PIPELINE
# ============================================================

def analyze_prediction(
    records,
    duration=0,
    title_score=50,
    thumbnail_score=50,
    hook_score=50,
    story_score=50,
    retention_score=50,
    audience_score=50,
    attention_score=50
):

    prepared_records = prepare_dataset(
        records
    )

    if len(prepared_records) < 5:

        return {
            "status":
                "Insufficient historical data",

            "prediction":
                "Insufficient Data",

            "confidence":
                0.0,

            "probabilities": {
                "low": 0.0,
                "medium": 0.0,
                "high": 0.0
            },

            "similar_videos": [],

            "explanation": [
                "At least 5 historical records "
                "are required for the prediction "
                "engine to operate."
            ]
        }

    statistics = calculate_statistics(
        prepared_records
    )

    current = build_current_features(
        duration=duration,
        title_score=title_score,
        thumbnail_score=thumbnail_score,
        hook_score=hook_score,
        story_score=story_score,
        retention_score=retention_score,
        audience_score=audience_score,
        attention_score=attention_score
    )

    prediction = predict_performance(
        current,
        prepared_records,
        statistics
    )

    similar_videos = find_similar_videos(
        current,
        prepared_records,
        statistics
    )

    explanation = generate_prediction_explanation(
        prediction["prediction"],
        prediction["probabilities"],
        current
    )

    return {

        "status":
            "Channel-specific prediction completed",

        "prediction":
            prediction["prediction"],

        "confidence":
            prediction["confidence"],

        "probabilities":
            prediction["probabilities"],

        "similar_videos":
            similar_videos,

        "explanation":
            explanation,

        "training_records":
            len(prepared_records)
    }