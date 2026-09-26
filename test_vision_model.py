from semantic_analysis.vision_model import load_vision_model, analyze_frame

IMAGE_PATH = "frames/test.jpg"


def main():

    print("Loading vision model...")
    pipe = load_vision_model()

    print("Vision model loaded.")

    print("\n===== FRAME ANALYSIS =====")

    result = analyze_frame(
        pipe,
        IMAGE_PATH
    )

    print(result)


if __name__ == "__main__":
    main()