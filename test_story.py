from analyzer.story_analysis import analyze_story


duration = 60

transcript_segments = [
    {
        "start": 1.0,
        "end": 4.0,
        "text": "Today we are testing three different products."
    },
    {
        "start": 5.0,
        "end": 9.0,
        "text": "First, we will look at the quality and performance."
    },
    {
        "start": 15.0,
        "end": 20.0,
        "text": "The first product performed surprisingly well."
    },
    {
        "start": 25.0,
        "end": 30.0,
        "text": "The second product had some problems."
    },
    {
        "start": 35.0,
        "end": 40.0,
        "text": "Now let's compare the results."
    },
    {
        "start": 45.0,
        "end": 50.0,
        "text": "Overall, the first product was the strongest."
    },
    {
        "start": 53.0,
        "end": 58.0,
        "text": "So these are the results and my final recommendation."
    }
]


results = analyze_story(
    duration,
    transcript_segments
)


print()
print("================================")
print("         STORY ANALYSIS")
print("================================")
print()

print(
    "Story Score:",
    results["story_score"]
)

print(
    "Speech Coverage:",
    results["speech_coverage"],
    "%"
)

print(
    "Total Segments:",
    results["total_segments"]
)

print(
    "Average Segment Length:",
    results["average_segment_length"],
    "seconds"
)

print()

print("===== BEGINNING =====")
print(results["beginning_content"])

print()

print("===== MIDDLE =====")
print(results["middle_content"])

print()

print("===== ENDING =====")
print(results["ending_content"])

print()

print("Assessment:")
print(results["assessment"])

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