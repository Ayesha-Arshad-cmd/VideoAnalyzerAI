import cv2
import os


VIDEO_PATH = r"C:\Users\Admin\Desktop\VideoAnalyzerAI\sample.mp4"
OUTPUT_DIR = r"C:\Users\Admin\Desktop\VideoAnalyzerAI\frames"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "test.jpg")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    video = cv2.VideoCapture(VIDEO_PATH)

    if not video.isOpened():
        raise ValueError("Could not open the video file.")

    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    if total_frames <= 0:
        video.release()
        raise ValueError("The video contains no readable frames.")

    # Select a frame near the middle of the video
    middle_frame = total_frames // 2
    video.set(cv2.CAP_PROP_POS_FRAMES, middle_frame)

    success, frame = video.read()
    video.release()

    if not success:
        raise ValueError("Could not read the selected video frame.")

    cv2.imwrite(OUTPUT_PATH, frame)

    print("Test frame created successfully:")
    print(OUTPUT_PATH)


if __name__ == "__main__":
    main()
    