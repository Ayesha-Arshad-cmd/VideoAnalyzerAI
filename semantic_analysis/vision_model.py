import torch
from PIL import Image
from transformers import pipeline


MODEL_NAME = "Qwen/Qwen2.5-VL-3B-Instruct"


def load_vision_model():
    """
    Load the local Hugging Face vision-language model.
    The model is downloaded once and then cached locally.
    """

    if torch.cuda.is_available():
        device = 0
    else:
        device = -1

    pipe = pipeline(
        "image-text-to-text",
        model=MODEL_NAME,
        device=device
    )

    return pipe


def analyze_image(pipe, image_path, prompt):
    """
    Ask the vision-language model to understand one image.
    """

    image = Image.open(image_path).convert("RGB")

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "image": image
                },
                {
                    "type": "text",
                    "text": prompt
                }
            ]
        }
    ]

    result = pipe(
        text=messages,
        max_new_tokens=150,
        return_full_text=False
    )

    return result[0]["generated_text"]


def analyze_frame(pipe, image_path):
    """
    Generate a structured description of a video frame.
    """

    prompt = """
Analyze this video frame for a video performance analyzer.

Describe:
1. What is visibly happening.
2. Main people, objects, or subjects.
3. Setting/environment.
4. On-screen text or UI elements.
5. Visual composition and framing.
6. Whether the frame appears visually interesting or ordinary.
7. Any obvious visual problem that could hurt viewer attention.

Be factual. Do not invent information that cannot be seen.
Keep the response concise.
"""

    return analyze_image(
        pipe=pipe,
        image_path=image_path,
        prompt=prompt
    )