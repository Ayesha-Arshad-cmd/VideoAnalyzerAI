from analyzer.thumbnail_analysis import analyze_thumbnail


thumbnail_path = "thumbnail.jpg"

result = analyze_thumbnail(
    thumbnail_path
)

print("\nTHUMBNAIL ANALYSIS")
print("-------------------------")

print(
    "Dimensions:",
    result["width"],
    "x",
    result["height"]
)

print(
    "Aspect Ratio:",
    result["aspect_ratio"]
)

print(
    "Brightness:",
    result["average_brightness"]
)

print(
    "Contrast:",
    result["contrast"]
)

print(
    "Color Variation:",
    result["color_variation"]
)

print(
    "Dark Areas:",
    f"{result['dark_percentage']}%"
)

print(
    "Bright Areas:",
    f"{result['bright_percentage']}%"
)

print(
    "Visual Detail:",
    f"{result['edge_percentage']}%"
)

print(
    "Thumbnail Score:",
    f"{result['thumbnail_score']}/100"
)

print("\nPositive Signals:")

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