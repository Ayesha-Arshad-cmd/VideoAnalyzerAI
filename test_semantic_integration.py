from semantic_analysis.video_understanding import analyze_video_semantics

VIDEO_PATH = "sample.mp4"


def main():
    transcript = (
        "This video explains how to create an AI video analyzer "
        "using Python and computer vision."
    )

    scene_descriptions = [
        "A video-analysis application is displayed.",
        "A dashboard showing analysis results appears."
    ]

    result = analyze_video_semantics(
        transcript=transcript,
        scene_descriptions=scene_descriptions,
        title="How to Build an AI Video Analyzer",
        video_path=VIDEO_PATH
    )

    print("\n===== SEMANTIC INTEGRATION TEST =====")
    print("Title:", result["title"])
    print("Extracted frames:", result["extracted_frame_count"])
    print("Scene count:", result["scene_count"])
    print("Status:", result["status"])

    print("\n===== SEMANTIC SUMMARY =====")
    print(result["semantic_summary"]["overall_summary"])


if __name__ == "__main__":
    main()