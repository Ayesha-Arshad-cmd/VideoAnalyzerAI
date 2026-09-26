from analyzer.scene_detection import detect_scenes


video_path = input(
    "Enter video path: "
).strip()


print()
print("Detecting scenes...")
print()


scenes = detect_scenes(
    video_path,
    threshold=30.0,
    sample_interval=0.5
)


print(
    f"Detected {len(scenes)} visual changes."
)


print()
print("===== SCENE CHANGES =====")


for scene in scenes:

    print(
        f"{scene['timestamp']:.2f}s"
        f" | Change score: "
        f"{scene['change_score']}"
    )


print()
print("===== DONE =====")