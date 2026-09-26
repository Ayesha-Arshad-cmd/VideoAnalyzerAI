from analyzer.visual_analysis import analyze_visuals


video_path = "D:\\all downloads on d\\cat anim.mp4"

results = analyze_visuals(
    video_path,
    sample_interval=2.0
)


print()
print("================================")
print("         VISUAL ANALYSIS")
print("================================")
print()

print(
    "Visual Score:",
    results["visual_score"]
)

print(
    "Frames Analyzed:",
    results["frames_analyzed"]
)

print(
    "Average Brightness:",
    results["average_brightness"]
)

print(
    "Dark Frames:",
    results["dark_percentage"],
    "%"
)

print(
    "Bright Frames:",
    results["bright_percentage"],
    "%"
)

print(
    "Repeated Frames:",
    results["repeated_percentage"],
    "%"
)

print()

print(
    "Assessment:",
    results["assessment"]
)

print()

print("===== POSITIVE SIGNALS =====")

for signal in results["signals"]:
    print("✓", signal)

print()

print("===== WARNINGS =====")

for warning in results["warnings"]:
    print("⚠", warning)

print()
print("================================")
print("              DONE")
print("================================")