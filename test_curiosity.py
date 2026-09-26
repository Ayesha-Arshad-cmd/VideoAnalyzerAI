from audience_intelligence.audience_score import calculate_curiosity_score


transcript = """
Have you ever wondered why some videos suddenly become popular?
Here's the surprising reason. Most creators make one big mistake
in the first few seconds, and today you'll see exactly how to avoid it.
But wait, there's another important thing you need to know.
"""


result = calculate_curiosity_score(transcript)

print("\n===== CURIOSITY ANALYSIS =====")
print("Score:", result["score"])
print("Rating:", result["rating"])
print("Word count:", result["word_count"])

print("\nSignals:")

for signal in result["signals"]:
    print("-", signal)