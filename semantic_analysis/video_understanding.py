import cv2


def extract_video_frames(video_path, max_frames=5):
    """
    Extract evenly spaced frames from a video.
    """

    video = cv2.VideoCapture(video_path)

    if not video.isOpened():
        raise ValueError("Could not open video.")

    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    if total_frames <= 0:
        video.release()
        return []

    frame_positions = [
        int(i * (total_frames - 1) / max_frames)
        for i in range(max_frames)
    ]

    extracted_frames = []

    for position in frame_positions:
        video.set(cv2.CAP_PROP_POS_FRAMES, position)

        success, frame = video.read()

        if success:
            extracted_frames.append({
                "frame_number": position,
                "frame": frame
            })

    video.release()

    return extracted_frames


def describe_frame(frame):
    """
    Generate basic measurable information about one video frame.
    """

    height, width = frame.shape[:2]

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    average_brightness = float(gray_frame.mean())

    return {
        "width": width,
        "height": height,
        "average_brightness": round(average_brightness, 2),
        "is_dark": average_brightness < 60,
        "is_bright": average_brightness > 190
    }


def generate_semantic_summary(title, transcript, scene_descriptions):
    """
    Generate a basic text summary from available video information.
    """

    scene_count = len(scene_descriptions)

    if transcript.strip():
        transcript_summary = transcript.strip()
    else:
        transcript_summary = "No transcript available."

    if scene_count > 0:
        scene_summary = (
            f"The video contains {scene_count} described scene(s). "
            + " ".join(scene_descriptions)
        )
    else:
        scene_summary = "No scene descriptions available."

    return {
        "title_summary": f"Video title: {title}",
        "transcript_summary": transcript_summary,
        "scene_summary": scene_summary,
        "overall_summary": (
            f"The video is titled '{title}'. "
            f"It contains {scene_count} described scene(s). "
            f"The available narration is: {transcript_summary}"
        )
    }


def analyze_video_semantics(
    transcript="",
    scene_descriptions=None,
    title="",
    video_path=None
):
    """
    Initial semantic-analysis pipeline using actual video frames.
    """

    if scene_descriptions is None:
        scene_descriptions = []

    extracted_frames = []

    if video_path:
        extracted_frames = extract_video_frames(video_path)

    frame_descriptions = [
        {
            "frame_number": item["frame_number"],
            "description": describe_frame(item["frame"])
        }
        for item in extracted_frames
    ]

    semantic_summary = generate_semantic_summary(
        title=title,
        transcript=transcript,
        scene_descriptions=scene_descriptions
    )

    return {
        "title": title,
        "transcript": transcript,
        "scene_count": len(scene_descriptions),
        "scene_descriptions": scene_descriptions,
        "extracted_frame_count": len(extracted_frames),
        "frame_numbers": [
            item["frame_number"] for item in extracted_frames
        ],
        "frame_descriptions": frame_descriptions,
        "semantic_summary": semantic_summary,
        "visual_audio_alignment": None,
        "content_relevance": None,
        "status": "Frames extracted successfully"
        if extracted_frames
        else "No frames extracted"
    }