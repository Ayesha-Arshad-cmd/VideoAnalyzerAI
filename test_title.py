from analyzer.title_analysis import analyze_title


title = "I Tried AI Makeup for 7 Days — Here's What Happened"

result = analyze_title(title)

print("\nTITLE ANALYSIS")
print("-------------------------")

print("Title:", result["title"])
print("Characters:", result["character_count"])
print("Words:", result["word_count"])
print("Score:", result["title_score"])

print("\nSignals:")
for signal in result["signals"]:
    print("-", signal)

print("\nWarnings:")
for warning in result["warnings"]:
    print("-", warning)

print("\nSuggestions:")
for suggestion in result["suggestions"]:
    print("-", suggestion)

print("\nAssessment:")
print(result["assessment"])