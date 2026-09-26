from semantic_analysis.video_understanding import analyze_video_semantics
from pprint import pprint
VIDEO_PATH = "sample.mp4"

result = analyze_video_semantics(
    transcript="This video explains how to create an AI video analyzer.",
    scene_descriptions=[
        "A person opens a video editing application.",
        "A dashboard showing video analysis results appears."
    ],
    title="How to Build an AI Video Analyzer",
    video_path=VIDEO_PATH
)

pprint(result)