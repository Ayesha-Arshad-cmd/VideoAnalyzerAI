from analyzer.overall_score import calculate_overall_score


result = calculate_overall_score(
    hook_score=80,
    story_score=75,
    retention_score=70,
    visual_score=85,
    audio_score=90,
    title_score=78,
    thumbnail_score=88
)


print("\nOVERALL VIDEO SCORE")
print("-------------------------")

print(
    "Overall Score:",
    f"{result['overall_score']}/100"
)

print(
    "Rating:",
    result["rating"]
)

print(
    "\nAssessment:"
)

print(
    result["assessment"]
)


print(
    "\nComponent Scores:"
)

for name, score in result["component_scores"].items():

    print(
        f"- {name.title()}: {score}/100"
    )


print(
    "\nStrongest Areas:"
)

for name, score in result["strongest_areas"]:

    print(
        f"- {name.title()}: {score}/100"
    )


print(
    "\nWeakest Areas:"
)

for name, score in result["weakest_areas"]:

    print(
        f"- {name.title()}: {score}/100"
    )