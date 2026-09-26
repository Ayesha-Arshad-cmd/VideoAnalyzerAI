from analyzer.retention_analysis import analyze_retention


duration = 60


scenes = [
    {
        "timestamp": 4.5,
        "change_score": 42.3
    },
    {
        "timestamp": 15.0,
        "change_score": 51.7
    },
    {
        "timestamp": 25.0,
        "change_score": 37.8
    },
    {
        "timestamp": 40.0,
        "change_score": 48.2
    }
]


transcript_segments = [
    {
        "start": 0,
        "end": 4,
        "text": "Welcome to the video."
    },
    {
        "start": 6,
        "end": 12,
        "text": "Today we are going to discuss this topic."
    },
    {
        "start": 18,
        "end": 25,
        "text": "Let's look at the first example."
    },
    {
        "start": 42,
        "end": 48,
        "text": "Now let's discuss the final part."
    }
]


silence_percentage = 12


results = analyze_retention(
    duration,
    scenes,
    transcript_segments,
    silence_percentage
)


print()
print("================================")
print("       RETENTION ANALYSIS")
print("================================")
print()

print(
    "Retention Score:",
    results["retention_score"]
)

print(
    "Risk Score:",
    results["risk_score"]
)

print(
    "Risk Count:",
    results["risk_count"]
)

print()

print(
    "Assessment:",
    results["assessment"]
)

print()

print("===== RISKS =====")

for risk in results["risks"]:

    print(
        f"{risk['timestamp']:.2f}s | "
        f"{risk['severity']} | "
        f"{risk['type']} | "
        f"{risk['reason']}"
    )

print()
print("================================")
print("              DONE")
print("================================")