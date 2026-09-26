import cv2


def analyze_thumbnail(image_path):
    """
    Analyze a YouTube thumbnail image.

    V1 uses measurable visual properties.
    It does not claim to predict CTR or YouTube performance.
    """

    image = cv2.imread(image_path)

    if image is None:
        return {
            "thumbnail_score": 0,
            "width": 0,
            "height": 0,
            "aspect_ratio": 0,
            "average_brightness": 0,
            "contrast": 0,
            "color_variation": 0,
            "warnings": [
                "Could not open the thumbnail image."
            ],
            "signals": [],
            "suggestions": [],
            "assessment": "Thumbnail could not be analyzed."
        }

    # --------------------------------------------------
    # Basic dimensions
    # --------------------------------------------------

    height, width = image.shape[:2]

    aspect_ratio = width / height if height > 0 else 0

    # --------------------------------------------------
    # Convert to grayscale
    # --------------------------------------------------

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    # --------------------------------------------------
    # Brightness
    # --------------------------------------------------

    average_brightness = float(
        gray.mean()
    )

    # --------------------------------------------------
    # Contrast
    # --------------------------------------------------

    contrast = float(
        gray.std()
    )

    # --------------------------------------------------
    # Color variation
    # --------------------------------------------------

    hsv = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2HSV
    )

    saturation = hsv[:, :, 1]

    color_variation = float(
        saturation.std()
    )

    # --------------------------------------------------
    # Very dark / very bright areas
    # --------------------------------------------------

    dark_pixels = (
        gray < 35
    ).sum()

    bright_pixels = (
        gray > 220
    ).sum()

    total_pixels = gray.size

    dark_percentage = (
        dark_pixels
        / total_pixels
        * 100
    )

    bright_percentage = (
        bright_pixels
        / total_pixels
        * 100
    )

    # --------------------------------------------------
    # Edge / visual detail
    # --------------------------------------------------

    edges = cv2.Canny(
        gray,
        100,
        200
    )

    edge_percentage = (
        (edges > 0).sum()
        / total_pixels
        * 100
    )

    # --------------------------------------------------
    # Results
    # --------------------------------------------------

    results = {
        "width": width,
        "height": height,
        "aspect_ratio": round(
            aspect_ratio,
            2
        ),
        "average_brightness": round(
            average_brightness,
            2
        ),
        "contrast": round(
            contrast,
            2
        ),
        "color_variation": round(
            color_variation,
            2
        ),
        "dark_percentage": round(
            dark_percentage,
            2
        ),
        "bright_percentage": round(
            bright_percentage,
            2
        ),
        "edge_percentage": round(
            edge_percentage,
            2
        )
    }

    warnings = []
    signals = []
    suggestions = []

    # --------------------------------------------------
    # Aspect ratio
    # --------------------------------------------------

    if 1.7 <= aspect_ratio <= 1.8:

        signals.append(
            "The thumbnail has a widescreen aspect ratio "
            "close to the standard YouTube thumbnail format."
        )

    else:

        warnings.append(
            "The thumbnail aspect ratio is not close "
            "to the standard widescreen format."
        )

        suggestions.append(
            "Use a widescreen thumbnail layout "
            "suitable for YouTube."
        )

    # --------------------------------------------------
    # Brightness
    # --------------------------------------------------

    if 60 <= average_brightness <= 190:

        signals.append(
            "The thumbnail has a moderate overall "
            "brightness level."
        )

    elif average_brightness < 60:

        warnings.append(
            "The thumbnail is relatively dark."
        )

        suggestions.append(
            "Increase lighting or brightness "
            "so important visual elements remain clear."
        )

    else:

        warnings.append(
            "The thumbnail is relatively bright."
        )

        suggestions.append(
            "Check highlights and bright areas "
            "to ensure important details remain visible."
        )

    # --------------------------------------------------
    # Contrast
    # --------------------------------------------------

    if contrast >= 45:

        signals.append(
            "The thumbnail has strong grayscale contrast."
        )

    elif contrast < 25:

        warnings.append(
            "The thumbnail has relatively low contrast."
        )

        suggestions.append(
            "Increase separation between important "
            "foreground and background elements."
        )

    # --------------------------------------------------
    # Dark areas
    # --------------------------------------------------

    if dark_percentage >= 40:

        warnings.append(
            f"{dark_percentage:.1f}% of the thumbnail "
            "contains very dark pixels."
        )

        suggestions.append(
            "Check whether important subjects or text "
            "are being lost in dark areas."
        )

    # --------------------------------------------------
    # Bright areas
    # --------------------------------------------------

    if bright_percentage >= 40:

        warnings.append(
            f"{bright_percentage:.1f}% of the thumbnail "
            "contains very bright pixels."
        )

        suggestions.append(
            "Check whether important details are being "
            "lost in bright or overexposed areas."
        )

    # --------------------------------------------------
    # Color variation
    # --------------------------------------------------

    if color_variation >= 35:

        signals.append(
            "The thumbnail contains noticeable "
            "color variation."
        )

    elif color_variation < 15:

        warnings.append(
            "The thumbnail has relatively low "
            "color variation."
        )

        suggestions.append(
            "Consider stronger visual separation "
            "between important elements."
        )

    # --------------------------------------------------
    # Visual detail
    # --------------------------------------------------

    if edge_percentage >= 5:

        signals.append(
            "The thumbnail contains a reasonable "
            "amount of visible visual detail."
        )

    elif edge_percentage < 2:

        warnings.append(
            "The thumbnail contains relatively "
            "little visual detail."
        )

        suggestions.append(
            "Consider using clearer or more visually "
            "distinct elements."
        )

    # --------------------------------------------------
    # Score
    # --------------------------------------------------

    score = 60

    # Aspect ratio
    if 1.7 <= aspect_ratio <= 1.8:
        score += 10
    else:
        score -= 5

    # Brightness
    if 60 <= average_brightness <= 190:
        score += 8
    elif average_brightness < 40 or average_brightness > 220:
        score -= 10

    # Contrast
    if contrast >= 45:
        score += 10
    elif contrast < 25:
        score -= 8

    # Color variation
    if color_variation >= 35:
        score += 5
    elif color_variation < 15:
        score -= 5

    # Dark areas
    if dark_percentage >= 40:
        score -= 8

    # Bright areas
    if bright_percentage >= 40:
        score -= 8

    # Visual detail
    if edge_percentage >= 5:
        score += 5
    elif edge_percentage < 2:
        score -= 5

    score = max(
        0,
        min(
            score,
            100
        )
    )

    # --------------------------------------------------
    # Assessment
    # --------------------------------------------------

    if score >= 80:

        assessment = (
            "The thumbnail shows strong measurable "
            "visual characteristics."
        )

    elif score >= 60:

        assessment = (
            "The thumbnail has reasonable visual "
            "characteristics, but some areas could "
            "be improved."
        )

    elif score >= 40:

        assessment = (
            "The thumbnail has several visual "
            "areas that could be improved."
        )

    else:

        assessment = (
            "The thumbnail has significant visual "
            "quality issues that should be addressed."
        )

    results["thumbnail_score"] = score
    results["signals"] = signals
    results["warnings"] = warnings
    results["suggestions"] = suggestions
    results["assessment"] = assessment

    return results