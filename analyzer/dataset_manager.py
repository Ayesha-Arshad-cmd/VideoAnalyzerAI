import csv
import os
from datetime import datetime


DATASET_PATH = os.path.join(
    "data",
    "video_dataset.csv"
)


DATASET_COLUMNS = [
    "video_id",
    "title",
    "channel",
    "category",
    "upload_date",
    "duration_seconds",
    "views",
    "likes",
    "comments",
    "subscribers",
    "views_per_subscriber",
    "like_rate",
    "comment_rate",
    "engagement_rate",
    "performance_label"
]


def ensure_dataset_exists():
    """
    Creates the local video dataset if it does not exist.
    """

    directory = os.path.dirname(
        DATASET_PATH
    )

    if directory:
        os.makedirs(
            directory,
            exist_ok=True
        )

    if not os.path.exists(
        DATASET_PATH
    ):

        with open(
            DATASET_PATH,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=DATASET_COLUMNS
            )

            writer.writeheader()


def safe_float(value):
    try:
        return float(value)
    except (
        TypeError,
        ValueError
    ):
        return 0.0


def calculate_video_metrics(
    views,
    likes,
    comments,
    subscribers
):
    """
    Calculates normalized performance metrics.
    """

    views = safe_float(views)
    likes = safe_float(likes)
    comments = safe_float(comments)
    subscribers = safe_float(subscribers)

    if subscribers > 0:

        views_per_subscriber = (
            views / subscribers
        )

    else:

        views_per_subscriber = 0.0

    if views > 0:

        like_rate = (
            likes / views
        ) * 100

        comment_rate = (
            comments / views
        ) * 100

        engagement_rate = (
            (likes + comments)
            / views
        ) * 100

    else:

        like_rate = 0.0
        comment_rate = 0.0
        engagement_rate = 0.0

    return {
        "views_per_subscriber":
            round(
                views_per_subscriber,
                4
            ),

        "like_rate":
            round(
                like_rate,
                4
            ),

        "comment_rate":
            round(
                comment_rate,
                4
            ),

        "engagement_rate":
            round(
                engagement_rate,
                4
            )
    }


def determine_performance_label(
    views_per_subscriber,
    engagement_rate
):
    """
    Creates a simple relative performance label.

    This is only a preliminary labeling system.
    Phase 32 will use a more robust target strategy.
    """

    views_per_subscriber = safe_float(
        views_per_subscriber
    )

    engagement_rate = safe_float(
        engagement_rate
    )

    if (
        views_per_subscriber >= 5
        and engagement_rate >= 5
    ):

        return "high"

    if (
        views_per_subscriber >= 2
        or engagement_rate >= 3
    ):

        return "medium"

    return "low"


def add_video_record(
    video_id,
    title,
    channel,
    category,
    upload_date,
    duration_seconds,
    views,
    likes,
    comments,
    subscribers
):
    """
    Adds one historical video record to the dataset.
    """

    ensure_dataset_exists()

    metrics = calculate_video_metrics(
        views=views,
        likes=likes,
        comments=comments,
        subscribers=subscribers
    )

    performance_label = (
        determine_performance_label(
            metrics[
                "views_per_subscriber"
            ],
            metrics[
                "engagement_rate"
            ]
        )
    )

    record = {
        "video_id": str(
            video_id
        ),

        "title": str(
            title
        ),

        "channel": str(
            channel
        ),

        "category": str(
            category
        ),

        "upload_date": str(
            upload_date
        ),

        "duration_seconds": (
            safe_float(
                duration_seconds
            )
        ),

        "views": safe_float(
            views
        ),

        "likes": safe_float(
            likes
        ),

        "comments": safe_float(
            comments
        ),

        "subscribers": safe_float(
            subscribers
        ),

        "views_per_subscriber":
            metrics[
                "views_per_subscriber"
            ],

        "like_rate":
            metrics[
                "like_rate"
            ],

        "comment_rate":
            metrics[
                "comment_rate"
            ],

        "engagement_rate":
            metrics[
                "engagement_rate"
            ],

        "performance_label":
            performance_label
    }

    with open(
        DATASET_PATH,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=DATASET_COLUMNS
        )

        writer.writerow(
            record
        )

    return record


def load_dataset():
    """
    Loads all historical video records.
    """

    ensure_dataset_exists()

    with open(
        DATASET_PATH,
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(
            file
        )

        return list(
            reader
        )


def get_dataset_summary():
    """
    Returns basic dataset statistics.
    """

    records = load_dataset()

    total_videos = len(
        records
    )

    channels = set()

    high_count = 0
    medium_count = 0
    low_count = 0

    for record in records:

        channel = record.get(
            "channel",
            ""
        )

        if channel:
            channels.add(
                channel
            )

        label = record.get(
            "performance_label",
            ""
        ).lower()

        if label == "high":
            high_count += 1

        elif label == "medium":
            medium_count += 1

        elif label == "low":
            low_count += 1

    return {
        "total_videos":
            total_videos,

        "total_channels":
            len(channels),

        "high_performance_videos":
            high_count,

        "medium_performance_videos":
            medium_count,

        "low_performance_videos":
            low_count,

        "dataset_path":
            DATASET_PATH
    }


def validate_dataset():
    """
    Checks whether the dataset contains the
    required columns and valid records.
    """

    ensure_dataset_exists()

    records = load_dataset()

    errors = []

    for index, record in enumerate(
        records,
        start=1
    ):

        for column in DATASET_COLUMNS:

            if column not in record:

                errors.append(
                    f"Row {index}: missing column "
                    f"{column}"
                )

        numeric_columns = [
            "duration_seconds",
            "views",
            "likes",
            "comments",
            "subscribers",
            "views_per_subscriber",
            "like_rate",
            "comment_rate",
            "engagement_rate"
        ]

        for column in numeric_columns:

            try:

                float(
                    record.get(
                        column,
                        0
                    )
                )

            except (
                TypeError,
                ValueError
            ):

                errors.append(
                    f"Row {index}: invalid numeric "
                    f"value in {column}"
                )

    return {
        "valid":
            len(errors) == 0,

        "errors":
            errors,

        "records":
            len(records)
    }