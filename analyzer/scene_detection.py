import cv2


def detect_scenes(
    video_path,
    threshold=30.0,
    sample_interval=0.5
):
    """
    Detect major visual changes in a video.

    Returns a list of scene boundaries.
    """

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        return []

    fps = cap.get(cv2.CAP_PROP_FPS)

    frame_count = cap.get(
        cv2.CAP_PROP_FRAME_COUNT
    )

    if fps <= 0:
        cap.release()
        return []

    duration = frame_count / fps

    scenes = []

    previous_frame = None

    current_time = 0.0

    while current_time < duration:

        cap.set(
            cv2.CAP_PROP_POS_MSEC,
            current_time * 1000
        )

        success, frame = cap.read()

        if not success:
            break

        # Resize frame for faster comparison
        frame = cv2.resize(
            frame,
            (320, 180)
        )

        # Convert to grayscale
        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        if previous_frame is not None:

            difference = cv2.absdiff(
                previous_frame,
                gray
            )

            score = difference.mean()

            if score >= threshold:

                scenes.append({
                    "timestamp": round(
                        current_time,
                        2
                    ),
                    "change_score": round(
                        float(score),
                        2
                    )
                })

        previous_frame = gray

        current_time += sample_interval

    cap.release()

    return scenes