from analyzer.hook_analysis import analyze_hook


duration = 60


scenes = [
    {
        "timestamp": 3.5,
        "change_score": 45.2
    },
    {
        "timestamp": 8.0,
        "change_score": 52.4
    },
    {
        "timestamp": 15.5,
        "change_score": 38.1
    }
]


transcript_segments = [
    {
        "start": 1.2,
        "end": 4.5,
        "text": "You need to see this before you buy anything."
    },
    {
        "start": 5.0,
        "end": 10.0,
        "text": "Today we are testing three different products."
    },
    {
        "start": 11.0,
        "end": 17.0,
        "text": "Let's start with the first one."
    }
]


results = analyze_hook(
    duration,
    scenes,
    transcript_segments
)


print()
print("================================")
print("          HOOK ANALYSIS")
print("================================")
print()

print(
    "Hook Score:",
    results["hook_score"]
)

print(
    "First Speech:",
    results["first_speech_start"]
)

print(
    "First Speech Text:",
    results["first_speech_text"]
)

print(
    "First Visual Change:",
    results["first_visual_change"]
)

print(
    "Opening Silence:",
    results["opening_silence"]
)

print(
    "Hook Speech Coverage:",
    results["hook_speech_coverage"],
    "%"
)

print(
    "Early Scene Changes:",
    results["early_scene_changes"]
)

print()

print(
    "Assessment:",
    results["assessment"]
)

print()

print("===== POSITIVE SIGNALS =====")

for signal in results["signals"]:

    print(
        "✓",
        signal
    )


print()

print("===== WARNINGS =====")

for warning in results["warnings"]:

    print(
        "⚠",
        warning
    )


print()
print("================================")
print("              DONE")
print("================================")