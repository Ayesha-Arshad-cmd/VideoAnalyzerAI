"""
Channel-Specific Performance Prediction Engine
VideoAnalyzerAI - Phase 32

Uses the historical YouTube channel dataset to estimate
performance based on channel-specific benchmarks.

No external ML model is required.
"""

import os
import pandas as pd
import numpy as np


# ============================================================
# CONFIGURATION
# ============================================================

DATASET_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "video_dataset.csv"
)


# ============================================================
# LOAD DATASET
# ============================================================

def load_channel_dataset():
    """
    Load the historical YouTube channel dataset.
    """

    if not os.path.exists(DATASET_PATH):
        return None

    try:
        df = pd.read_csv(DATASET_PATH)

        if df.empty:
            return None

        return df

    except Exception:
        return None


# ============================================================
# CLEAN NUMERIC DATA
# ============================================================

def prepare_dataset(df):
    """
    Convert important performance columns to numeric values.
    """

    numeric_columns = [
        "duration_seconds",
        "views",
        "likes",
        "comments",
        "subscribers",
        "watch_time",
        "average_view_duration",
        "average_percentage_viewed",
        "impressions",
        "ctr",
        "subscribers_gained",
        "unique_viewers",
        "views_per_subscriber",
        "like_rate",
        "comment_rate",
        "engagement_rate"
    ]

    for column in numeric_columns:

        if column in df.columns:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    return df


# ============================================================
# CHANNEL BENCHMARKS
# ============================================================

def calculate_channel_benchmarks(df):
    """
    Calculate historical channel benchmarks.
    """

    benchmark_columns = [
        "views",
        "likes",
        "comments",
        "watch_time",
        "average_view_duration",
        "average_percentage_viewed",
        "impressions",
        "ctr",
        "subscribers_gained",
        "engagement_rate"
    ]

    benchmarks = {}

    for column in benchmark_columns:

        if column in df.columns:

            values = df[column].dropna()

            values = values[values >= 0]

            if len(values) > 0:

                benchmarks[column] = {
                    "mean": float(values.mean()),
                    "median": float(values.median()),
                    "min": float(values.min()),
                    "max": float(values.max())
                }

    return benchmarks


# ============================================================
# PERFORMANCE DISTRIBUTION
# ============================================================

def get_performance_distribution(df):
    """
    Calculate historical distribution of performance labels.
    """

    if "performance_label" not in df.columns:
        return {}

    labels = (
        df["performance_label"]
        .dropna()
        .astype(str)
        .str.lower()
        .str.strip()
    )

    distribution = labels.value_counts().to_dict()

    return {
        "low": int(distribution.get("low", 0)),
        "medium": int(distribution.get("medium", 0)),
        "high": int(distribution.get("high", 0))
    }


# ============================================================
# NORMALIZE VALUE AGAINST CHANNEL
# ============================================================

def benchmark_score(value, benchmark):
    """
    Compare a value against the channel median.

    Returns approximately 0-100.
    """

    if benchmark is None:
        return 50.0

    median = benchmark.get("median", 0)

    if median <= 0:
        return 50.0

    ratio = value / median

    if ratio >= 2:
        return 100.0

    if ratio <= 0:
        return 0.0

    score = ratio * 50

    return float(max(0, min(100, score)))


# ============================================================
# PREDICTION
# ============================================================

def predict_performance(
    duration_seconds=0,
    average_percentage_viewed=0,
    ctr=0,
    engagement_rate=0,
    subscribers_gained=0,
    title=None
):
    """
    Estimate performance using historical channel benchmarks.

    Parameters are intended to represent measurable information
    available for analysis.
    """

    df = load_channel_dataset()

    if df is None:
        return {
            "success": False,
            "error": "Historical channel dataset could not be loaded."
        }

    df = prepare_dataset(df)

    benchmarks = calculate_channel_benchmarks(df)

    scores = {}
    reasons = []
    improvements = []

    # --------------------------------------------------------
    # RETENTION
    # --------------------------------------------------------

    if "average_percentage_viewed" in benchmarks:

        retention_score = benchmark_score(
            average_percentage_viewed,
            benchmarks["average_percentage_viewed"]
        )

        scores["retention"] = retention_score

        median_retention = benchmarks[
            "average_percentage_viewed"
        ]["median"]

        if average_percentage_viewed >= median_retention:
            reasons.append(
                "Expected retention is at or above the channel's historical median."
            )
        else:
            improvements.append(
                "Improve audience retention by strengthening the opening and reducing early drop-off."
            )

    # --------------------------------------------------------
    # CTR
    # --------------------------------------------------------

    if "ctr" in benchmarks:

        ctr_score = benchmark_score(
            ctr,
            benchmarks["ctr"]
        )

        scores["ctr"] = ctr_score

        median_ctr = benchmarks["ctr"]["median"]

        if ctr >= median_ctr:
            reasons.append(
                "Expected CTR is at or above the channel's historical median."
            )
        else:
            improvements.append(
                "Improve the title and thumbnail combination to increase expected click-through rate."
            )

    # --------------------------------------------------------
    # ENGAGEMENT
    # --------------------------------------------------------

    if "engagement_rate" in benchmarks and engagement_rate > 0:

        engagement_score = benchmark_score(
            engagement_rate,
            benchmarks["engagement_rate"]
        )

        scores["engagement"] = engagement_score

        median_engagement = benchmarks[
            "engagement_rate"
        ]["median"]

        if engagement_rate >= median_engagement:
            reasons.append(
                "Expected engagement is at or above the channel's historical median."
            )
        else:
            improvements.append(
                "Strengthen calls-to-action and audience interaction opportunities."
            )

    # --------------------------------------------------------
    # SUBSCRIBER CONVERSION
    # --------------------------------------------------------

    if "subscribers_gained" in benchmarks and subscribers_gained > 0:

        subscriber_score = benchmark_score(
            subscribers_gained,
            benchmarks["subscribers_gained"]
        )

        scores["subscriber_conversion"] = subscriber_score

    # --------------------------------------------------------
    # DURATION
    # --------------------------------------------------------

    if duration_seconds > 0 and "duration_seconds" in benchmarks:

        median_duration = benchmarks[
            "duration_seconds"
        ]["median"]

        duration_difference = abs(
            duration_seconds - median_duration
        )

        duration_score = max(
            0,
            100 - (
                duration_difference /
                max(median_duration, 1)
                * 100
            )
        )

        scores["duration_fit"] = float(
            min(100, duration_score)
        )

        if duration_score >= 60:

            reasons.append(
                "Video duration is reasonably aligned with the channel's historical video range."
            )

        else:

            improvements.append(
                "Consider whether the planned duration matches the pacing expected by the channel's audience."
            )

    # --------------------------------------------------------
    # FALLBACK
    # --------------------------------------------------------

    if not scores:

        return {
            "success": False,
            "error": "Not enough measurable information was supplied."
        }

    # --------------------------------------------------------
    # FINAL SCORE
    # --------------------------------------------------------

    final_score = float(
        np.mean(list(scores.values()))
    )

    # --------------------------------------------------------
    # PERFORMANCE CLASS
    # --------------------------------------------------------

    if final_score >= 70:

        performance_label = "high"

    elif final_score >= 45:

        performance_label = "medium"

    else:

        performance_label = "low"

    # --------------------------------------------------------
    # CONFIDENCE
    # --------------------------------------------------------

    historical_count = len(df)

    if historical_count >= 100:
        confidence = "High"

    elif historical_count >= 50:
        confidence = "Moderate"

    elif historical_count >= 20:
        confidence = "Limited"

    else:
        confidence = "Very Limited"

    # --------------------------------------------------------
    # DISTRIBUTION
    # --------------------------------------------------------

    distribution = get_performance_distribution(df)

    # --------------------------------------------------------
    # RESULT
    # --------------------------------------------------------

    return {

        "success": True,

        "prediction": performance_label,

        "score": round(final_score, 2),

        "confidence": confidence,

        "historical_videos": historical_count,

        "component_scores": {
            key: round(value, 2)
            for key, value in scores.items()
        },

        "channel_benchmarks": benchmarks,

        "historical_distribution": distribution,

        "reasons": reasons,

        "improvements": improvements
    }


# ============================================================
# DATASET SUMMARY
# ============================================================

def get_prediction_system_summary():

    df = load_channel_dataset()

    if df is None:

        return {
            "success": False,
            "error": "Dataset unavailable."
        }

    df = prepare_dataset(df)

    benchmarks = calculate_channel_benchmarks(df)

    distribution = get_performance_distribution(df)

    return {

        "success": True,

        "channel": (
            str(df["channel"].iloc[0])
            if "channel" in df.columns and len(df) > 0
            else "Unknown"
        ),

        "videos": len(df),

        "benchmarks": benchmarks,

        "performance_distribution": distribution
    }