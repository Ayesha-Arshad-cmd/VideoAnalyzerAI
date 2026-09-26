from performance_predictor import (
    get_prediction_system_summary,
    predict_performance
)


print("=" * 60)
print("VIDEO ANALYZER AI - PHASE 32 TEST")
print("=" * 60)


# ------------------------------------------------------------
# TEST DATASET
# ------------------------------------------------------------

summary = get_prediction_system_summary()

print("\nDATASET STATUS")
print("-" * 60)

if summary["success"]:

    print("Dataset loaded successfully.")
    print("Channel:", summary["channel"])
    print("Historical videos:", summary["videos"])

else:

    print("Dataset error:", summary["error"])


# ------------------------------------------------------------
# TEST PREDICTION
# ------------------------------------------------------------

print("\nPERFORMANCE PREDICTION")
print("-" * 60)

result = predict_performance(
    duration_seconds=300,
    average_percentage_viewed=45,
    ctr=5.0,
    engagement_rate=2.0,
    subscribers_gained=20
)


if result["success"]:

    print("Prediction:", result["prediction"])
    print("Score:", result["score"])
    print("Confidence:", result["confidence"])

    print("\nComponent Scores:")

    for key, value in result["component_scores"].items():
        print(f"  {key}: {value}")

    print("\nReasons:")

    for reason in result["reasons"]:
        print(" -", reason)

    print("\nImprovements:")

    for improvement in result["improvements"]:
        print(" -", improvement)

else:

    print("Prediction error:", result["error"])


print("\n" + "=" * 60)
print("PHASE 32 TEST COMPLETE")
print("=" * 60)