from audience_intelligence.audience_score import calculate_audience_score


def main():

    result = calculate_audience_score(
        curiosity_score=80,
        emotion_score=65,
        relatability_score=75,
        storytelling_score=78,
        attention_score=70,
        shareability_score=68,
        novelty_score=72,
        promise_match_score=85
    )

    print("\n===== AUDIENCE SCORE TEST =====")

    print("Audience Score:", result["audience_score"])
    print("Rating:", result["rating"])

    print("\nComponent Scores:")

    for name, score in result["component_scores"].items():
        print(f"{name}: {score}")

    print("\nStrongest Area:", result["strongest_area"])
    print("Weakest Area:", result["weakest_area"])
    print("Confidence:", result["confidence"])


if __name__ == "__main__":
    main()