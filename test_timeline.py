from analyzer.timeline_analysis import analyze_timeline


# Example test data

duration = 60

scenes = [
    {
        "timestamp": 4.5,
        "change_score": 42.3
    },
    {
        "timestamp": 9.0,
        "change_score": 51.7
    },
    {
        "timestamp": 17.5,
        "change_score": 37.8
    },
    {
        "timestamp": 29.0,
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
        "start": 5,
        "end": 12,
        "text": "Today we are going to discuss this topic."
    },
    {
        "start": 18,
        "end": 25,
        "text": "Let's look at the first example."
    }
]


silence_percentage = 12


# Run analysis

results = analyze_timeline(
    duration,
    scenes,
    transcript_segments,
    silence_percentage
)


# Display results

print()
print("================================")
print("       TIMELINE ANALYSIS")
print("================================")
print()

for key, value in results.items():

    print(
        f"{key}: {value}"
    )

print()
print("================================")
print("             DONE")
print("================================")