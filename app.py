import streamlit as st
import cv2
import tempfile
import os
import subprocess
from pydub import AudioSegment
from faster_whisper import WhisperModel

from analyzer.scene_detection import detect_scenes
from analyzer.timeline_analysis import analyze_timeline
from analyzer.retention_analysis import analyze_retention
from analyzer.hook_analysis import analyze_hook
from analyzer.story_analysis import analyze_story
from analyzer.visual_analysis import analyze_visuals
from analyzer.title_analysis import analyze_title
from analyzer.thumbnail_analysis import analyze_thumbnail
from analyzer.overall_score import calculate_overall_score
from analyzer.human_virality import calculate_human_virality
# from analyzer.attention_analysis import calculate_attention_analysis
# from analyzer.audience_understanding import analyze_audience_understanding
# from analyzer.trend_analysis import analyze_trends
# from analyzer.viewer_simulator import simulate_viewer_response
# from analyzer.audience_response_score import calculate_audience_response_score
# from analyzer.final_report import generate_final_report
# from analyzer.dataset_manager import (
#     ensure_dataset_exists,
#     load_dataset,
#     get_dataset_summary,
#     validate_dataset
# )
# from analyzer.prediction_analysis import analyze_prediction
# # Audience scoring is kept optional so the app still runs if the
# # audience_score.py file has not yet been updated.
# try:
#     from audience_intelligence.audience_score import calculate_audience_score
# except (ImportError, AttributeError):
#     def calculate_audience_score(
#         curiosity_score=0,
#         emotion_score=0,
#         relatability_score=0,
#         storytelling_score=0,
#         attention_score=0,
#         shareability_score=0,
#         novelty_score=0,
#         promise_match_score=0
#     ):
#         scores = {
#             "curiosity": float(curiosity_score),
#             "emotion": float(emotion_score),
#             "relatability": float(relatability_score),
#             "storytelling": float(storytelling_score),
#             "attention": float(attention_score),
#             "shareability": float(shareability_score),
#             "novelty": float(novelty_score),
#             "promise_match": float(promise_match_score)
#         }

#         scores = {
#             key: max(0.0, min(100.0, value))
#             for key, value in scores.items()
#         }

#         weights = {
#             "curiosity": 0.15,
#             "emotion": 0.10,
#             "relatability": 0.10,
#             "storytelling": 0.15,
#             "attention": 0.15,
#             "shareability": 0.10,
#             "novelty": 0.10,
#             "promise_match": 0.15
#         }

#         audience_score = sum(
#             scores[key] * weights[key]
#             for key in scores
#         )

#         if audience_score >= 80:
#             rating = "Excellent"
#         elif audience_score >= 70:
#             rating = "Strong"
#         elif audience_score >= 60:
#             rating = "Moderate"
#         elif audience_score >= 50:
#             rating = "Weak"
#         else:
#             rating = "Very Weak"

#         strongest = max(scores, key=scores.get)
#         weakest = min(scores, key=scores.get)

#         return {
#             "audience_score": round(audience_score, 1),
#             "component_scores": scores,
#             "weights": weights,
#             "rating": rating,
#             "strongest_area": strongest,
#             "weakest_area": weakest,
#             "status": "Audience scoring engine ready",
#             "confidence": "Initial rule-based estimate"
#         }

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Video Analyzer AI",
    page_icon="🎬",
    layout="wide"
)


# ============================================================
# WHISPER MODEL
# ============================================================

@st.cache_resource
def load_whisper_model():

    return WhisperModel(
        "base",
        device="cpu",
        compute_type="int8"
    )


# ============================================================
# PAGE TITLE
# ============================================================

st.title("🎬 Video Analyzer AI")

st.write(
    "AI-powered pre-publish video analysis and rating system."
)

st.divider()


# ============================================================
# VIDEO UPLOAD
# ============================================================

st.subheader("📤 Upload Your Video")

video = st.file_uploader(
    "Choose a video file",
    type=["mp4", "mov", "avi", "mkv", "webm"]
)


thumbnail_path = None

if video is not None:

    st.success("✅ Video uploaded successfully!")

    st.video(video)

    # ========================================================
    # VIDEO TITLE
    # ========================================================

    st.subheader("📝 Video Title")

    video_title = st.text_input(
        "Enter the title you plan to use on YouTube",
        placeholder="Example: I Tried AI Makeup for 7 Days — Here\'s What Happened"
    )

    st.divider()


    # ========================================================
    # THUMBNAIL UPLOAD
    # ========================================================

    st.subheader("🖼️ YouTube Thumbnail")

    thumbnail = st.file_uploader(
        "Upload the thumbnail you plan to use on YouTube",
        type=["png", "jpg", "jpeg", "webp"],
        key="thumbnail_uploader"
    )

    if thumbnail is not None:
        st.image(
            thumbnail,
            caption="Uploaded YouTube Thumbnail",
            use_container_width=True
        )

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=os.path.splitext(thumbnail.name)[1]
        ) as thumbnail_file:
            thumbnail_file.write(thumbnail.getbuffer())
            thumbnail_path = thumbnail_file.name

        with st.spinner("Analyzing thumbnail..."):
            thumbnail_results = analyze_thumbnail(thumbnail_path)

        st.session_state["thumbnail_results"] = thumbnail_results

        st.subheader("Thumbnail Score")
        st.metric("Thumbnail Score", f"{thumbnail_results['thumbnail_score']}/100")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Dimensions", f"{thumbnail_results['width']} × {thumbnail_results['height']}")
        with col2:
            st.metric("Aspect Ratio", thumbnail_results["aspect_ratio"])
        with col3:
            st.metric("Brightness", thumbnail_results["average_brightness"])
        with col4:
            st.metric("Contrast", thumbnail_results["contrast"])

        st.write(f"**Color Variation:** {thumbnail_results['color_variation']}")
        st.write(f"**Dark Areas:** {thumbnail_results['dark_percentage']}%")
        st.write(f"**Bright Areas:** {thumbnail_results['bright_percentage']}%")
        st.write(f"**Visual Detail:** {thumbnail_results['edge_percentage']}%")

        st.subheader("Assessment")
        st.info(thumbnail_results["assessment"])

        if thumbnail_results["signals"]:
            st.subheader("✅ Positive Signals")
            for signal in thumbnail_results["signals"]:
                st.success(signal)

        if thumbnail_results["warnings"]:
            st.subheader("⚠️ Thumbnail Warnings")
            for warning in thumbnail_results["warnings"]:
                st.warning(warning)

        if thumbnail_results["suggestions"]:
            st.subheader("💡 Improvement Suggestions")
            for suggestion in thumbnail_results["suggestions"]:
                st.info(suggestion)
    else:
        st.info("Upload a thumbnail to generate Thumbnail Analysis.")


    # ========================================================
    # FILE INFORMATION
    # ========================================================

    st.subheader("📋 File Information")

    file_size_mb = video.size / (1024 * 1024)

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            "**Filename:**",
            video.name
        )

    with col2:

        st.write(
            "**File size:**",
            f"{file_size_mb:.2f} MB"
        )


    # ========================================================
    # SAVE VIDEO TEMPORARILY
    # ========================================================

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=os.path.splitext(video.name)[1]
    ) as temp_file:

        temp_file.write(
            video.getbuffer()
        )

        video_path = temp_file.name

    # Save the current temporary video path so analysis sections
    # outside the upload block can use the same video.
    st.session_state["temp_video_path"] = video_path


    # ========================================================
    # OPEN VIDEO
    # ========================================================

    cap = cv2.VideoCapture(video_path)


    if not cap.isOpened():

        st.error(
            "❌ Could not read the video."
        )

    else:

        # ====================================================
        # VIDEO METADATA
        # ====================================================

        fps = cap.get(
            cv2.CAP_PROP_FPS
        )

        frame_count = cap.get(
            cv2.CAP_PROP_FRAME_COUNT
        )

        width = int(
            cap.get(
                cv2.CAP_PROP_FRAME_WIDTH
            )
        )

        height = int(
            cap.get(
                cv2.CAP_PROP_FRAME_HEIGHT
            )
        )


        if fps > 0:

            duration = frame_count / fps

        else:

            duration = 0


        st.divider()

        st.subheader("🎥 Video Information")


        col1, col2, col3, col4 = st.columns(4)


        with col1:

            st.metric(
                "Duration",
                f"{duration:.2f} sec"
            )


        with col2:

            st.metric(
                "Resolution",
                f"{width} × {height}"
            )


        with col3:

            st.metric(
                "FPS",
                f"{fps:.2f}"
            )


        with col4:

            st.metric(
                "Frames",
                f"{int(frame_count):,}"
            )


        # ====================================================
        # FRAME EXTRACTION
        # ====================================================

        st.divider()

        st.subheader("🖼️ Frame Analysis")


        num_frames = st.slider(
            "Number of sample frames",
            min_value=5,
            max_value=30,
            value=12,
            step=1
        )


        if st.button(
            "🔍 Extract Sample Frames"
        ):

            frames_dir = os.path.join(
                os.getcwd(),
                "frames"
            )

            os.makedirs(
                frames_dir,
                exist_ok=True
            )


            # Remove previous frames

            for file in os.listdir(
                frames_dir
            ):

                file_path = os.path.join(
                    frames_dir,
                    file
                )

                if os.path.isfile(
                    file_path
                ):

                    os.remove(
                        file_path
                    )


            # Calculate frame positions

            frame_positions = []

            for i in range(
                num_frames
            ):

                position = int(
                    i * (frame_count - 1)
                    / (num_frames - 1)
                )

                frame_positions.append(
                    position
                )


            extracted_frames = []

            progress = st.progress(0)


            # Extract frames

            for index, frame_number in enumerate(
                frame_positions
            ):

                cap.set(
                    cv2.CAP_PROP_POS_FRAMES,
                    frame_number
                )

                success, frame = cap.read()


                if success:

                    timestamp = (
                        frame_number / fps
                        if fps > 0
                        else 0
                    )


                    filename = (
                        f"frame_{index + 1:02d}_"
                        f"{timestamp:.2f}s.jpg"
                    )


                    frame_path = os.path.join(
                        frames_dir,
                        filename
                    )


                    cv2.imwrite(
                        frame_path,
                        frame
                    )


                    extracted_frames.append(
                        (
                            frame_path,
                            timestamp
                        )
                    )


                progress.progress(
                    (index + 1)
                    / num_frames
                )


            st.success(
                f"✅ Extracted "
                f"{len(extracted_frames)} "
                f"sample frames."
            )


            # =================================================
            # DISPLAY EXTRACTED FRAMES
            # =================================================

            st.subheader(
                "📸 Extracted Frames"
            )


            columns = st.columns(4)


            for index, (
                frame_path,
                timestamp
            ) in enumerate(
                extracted_frames
            ):

                with columns[
                    index % 4
                ]:

                    st.image(
                        frame_path,
                        caption=(
                            f"{timestamp:.2f} seconds"
                        ),
                        use_container_width=True
                    )


        cap.release()


        # ====================================================
        # SCENE DETECTION
        # ====================================================

        st.divider()

        st.subheader(
            "🎞️ Scene Detection"
        )

        st.write(
            "Detecting major visual changes "
            "throughout the video."
        )


        if st.button(
            "🎬 Detect Scene Changes"
        ):

            with st.spinner(
                "Analyzing visual changes..."
            ):

                scenes = detect_scenes(
                    video_path,
                    threshold=30.0,
                    sample_interval=0.5
                )


            st.session_state[
                "scenes"
            ] = scenes


            st.success(
                f"✅ Detected "
                f"{len(scenes)} visual changes."
            )


        # ====================================================
        # GET SAVED SCENE DATA
        # ====================================================

        scenes = st.session_state.get(
            "scenes",
            []
        )


        # ====================================================
        # SCENE RESULTS
        # ====================================================

        if scenes:

            st.subheader(
                "📍 Detected Scene Changes"
            )


            for index, scene in enumerate(
                scenes
            ):

                st.write(
                    f"**Scene Change {index + 1}:** "
                    f"{scene['timestamp']:.2f}s "
                    f"— Change Score: "
                    f"{scene['change_score']}"
                )


        # ====================================================
        # VISUAL TIMELINE
        # ====================================================

        if scenes:

            st.divider()

            st.subheader(
                "📊 Visual Timeline"
            )

            st.write(
                "This timeline shows where major "
                "visual changes occur in the video."
            )


            # Build timeline HTML

            timeline_width = 1000

            timeline_html = f"""
            <div style="
                width: 100%;
                padding: 25px 10px;
                background-color: #111827;
                border-radius: 12px;
                box-sizing: border-box;
            ">

                <div style="
                    position: relative;
                    height: 120px;
                    margin: 0 20px;
                ">

                    <!-- Timeline line -->

                    <div style="
                        position: absolute;
                        top: 50px;
                        left: 0;
                        right: 0;
                        height: 6px;
                        background-color: #6b7280;
                        border-radius: 5px;
                    ">
                    </div>

            """


            # Start marker

            timeline_html += f"""
                    <div style="
                        position: absolute;
                        left: 0%;
                        top: 35px;
                        text-align: center;
                    ">

                        <div style="
                            width: 28px;
                            height: 28px;
                            background-color: #22c55e;
                            border-radius: 50%;
                            border: 3px solid white;
                            margin: auto;
                        ">
                        </div>

                        <div style="
                            color: white;
                            font-size: 12px;
                            margin-top: 8px;
                        ">
                            0s
                        </div>

                    </div>
            """


            # Scene markers

            for index, scene in enumerate(
                scenes
            ):

                timestamp = scene[
                    "timestamp"
                ]

                if duration > 0:

                    percentage = (
                        timestamp
                        / duration
                        * 100
                    )

                else:

                    percentage = 0


                # Keep marker inside timeline

                percentage = max(
                    0,
                    min(
                        percentage,
                        100
                    )
                )


                timeline_html += f"""
                    <div style="
                        position: absolute;
                        left: {percentage}%;
                        top: 27px;
                        transform: translateX(-50%);
                        text-align: center;
                    ">

                        <div style="
                            width: 18px;
                            height: 18px;
                            background-color: #ef4444;
                            border-radius: 50%;
                            border: 2px solid white;
                            margin: auto;
                        ">
                        </div>

                        <div style="
                            color: white;
                            font-size: 11px;
                            margin-top: 10px;
                            white-space: nowrap;
                        ">
                            {timestamp:.1f}s
                        </div>

                    </div>
                """


            # End marker

            timeline_html += f"""
                    <div style="
                        position: absolute;
                        right: 0%;
                        top: 35px;
                        text-align: center;
                    ">

                        <div style="
                            width: 28px;
                            height: 28px;
                            background-color: #3b82f6;
                            border-radius: 50%;
                            border: 3px solid white;
                            margin: auto;
                        ">
                        </div>

                        <div style="
                            color: white;
                            font-size: 12px;
                            margin-top: 8px;
                        ">
                            {duration:.1f}s
                        </div>

                    </div>

                </div>

                <div style="
                    text-align: center;
                    color: #d1d5db;
                    font-size: 13px;
                ">
                    🟢 Start &nbsp;&nbsp;
                    🔴 Scene Change &nbsp;&nbsp;
                    🔵 End
                </div>

            </div>
            """


            st.components.v1.html(
                timeline_html,
                height=190
            )


            # =================================================
            # SCENE CHANGE TABLE
            # =================================================

            st.subheader(
                "📋 Scene Change Timeline"
            )


            for index, scene in enumerate(
                scenes
            ):

                timestamp = scene[
                    "timestamp"
                ]

                change_score = scene[
                    "change_score"
                ]


                if duration > 0:

                    percentage = (
                        timestamp
                        / duration
                        * 100
                    )

                else:

                    percentage = 0


                st.progress(
                    min(
                        percentage / 100,
                        1.0
                    )
                )


                col1, col2, col3 = st.columns(
                    [1, 2, 2]
                )


                with col1:

                    st.write(
                        f"**#{index + 1}**"
                    )


                with col2:

                    st.write(
                        f"⏱️ {timestamp:.2f}s"
                    )


                with col3:

                    st.write(
                        f"Change score: "
                        f"{change_score}"
                    )


    # ========================================================
    # AUDIO EXTRACTION
    # ========================================================

    st.divider()

    st.subheader(
        "🔊 Audio Analysis"
    )


    audio_path = os.path.join(
        os.getcwd(),
        "audio.wav"
    )


    try:

        # Extract audio using FFmpeg

        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                video_path,
                "-vn",
                "-acodec",
                "pcm_s16le",
                "-ar",
                "44100",
                "-ac",
                "1",
                audio_path
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )


        # Load audio

        audio = AudioSegment.from_wav(
            audio_path
        )


        duration_seconds = (
            len(audio) / 1000
        )

        average_db = audio.dBFS

        peak_db = audio.max_dBFS


        # ====================================================
        # SILENCE ANALYSIS
        # ====================================================

        silence_threshold = -40

        chunks = []

        chunk_size = 1000


        for start in range(
            0,
            len(audio),
            chunk_size
        ):

            chunk = audio[
                start:start + chunk_size
            ]

            if len(chunk) > 0:

                chunks.append(
                    chunk.dBFS
                )


        silent_chunks = sum(
            1
            for db in chunks
            if db < silence_threshold
        )


        total_chunks = len(chunks)


        if total_chunks > 0:

            silence_percentage = (
                silent_chunks
                / total_chunks
                * 100
            )

        else:

            silence_percentage = 0


        # ====================================================
        # AUDIO METRICS
        # ====================================================

        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "Audio Duration",
                f"{duration_seconds:.2f} sec"
            )


        with col2:

            st.metric(
                "Average Loudness",
                f"{average_db:.2f} dBFS"
            )


        with col3:

            st.metric(
                "Peak Level",
                f"{peak_db:.2f} dBFS"
            )


        st.metric(
            "Approx. Silence",
            f"{silence_percentage:.1f}%"
        )

        # ====================================================
        # STANDARDIZED AUDIO SCORE
        # ====================================================

        audio_score = 100

        if average_db < -35 or average_db > -8:
            audio_score -= 20
        elif average_db < -30 or average_db > -10:
            audio_score -= 10

        if peak_db > -0.5:
            audio_score -= 15
        elif peak_db > -1:
            audio_score -= 5

        if silence_percentage >= 30:
            audio_score -= 20
        elif silence_percentage >= 20:
            audio_score -= 10

        audio_score = max(
            0,
            min(
                audio_score,
                100
            )
        )

        st.session_state["audio_score"] = audio_score

        st.metric(
            "Audio Score",
            f"{audio_score}/100"
        )


        st.success(
            "✅ Audio extracted and analyzed."
        )


        # ====================================================
        # SPEECH TRANSCRIPTION
        # ====================================================

        st.divider()

        st.subheader(
            "📝 Speech Transcription"
        )


        video_signature = (
            f"{video.name}:{video.size}"
        )

        if (
            st.session_state.get(
                "transcription_signature"
            ) != video_signature
        ):

            with st.spinner(
                "Transcribing video speech..."
            ):

                model = load_whisper_model()

                segments, info = model.transcribe(
                    audio_path,
                    beam_size=1,
                    vad_filter=True
                )

                transcript_segments = []

                for segment in segments:

                    transcript_segments.append(
                        {
                            "start": segment.start,
                            "end": segment.end,
                            "text": segment.text.strip()
                        }
                    )

                st.session_state[
                    "transcript_segments"
                ] = transcript_segments

                st.session_state[
                    "transcription_info"
                ] = {
                    "language": info.language,
                    "language_probability": info.language_probability
                }

                st.session_state[
                    "transcription_signature"
                ] = video_signature

        else:

            transcript_segments = st.session_state.get(
                "transcript_segments",
                []
            )


        # Save transcript for timeline

        st.session_state[
            "transcript_segments"
        ] = transcript_segments


        if transcript_segments:

            st.success(
                f"✅ Transcription complete "
                f"({len(transcript_segments)} "
                f"speech segments)"
            )

            transcription_info = st.session_state.get(
                "transcription_info",
                {}
            )

            st.write(
                "**Detected language:**",
                transcription_info.get(
                    "language",
                    "Unknown"
                )
            )

            st.write(
                "**Language confidence:**",
                f"{transcription_info.get('language_probability', 0):.2f}"
            )


            st.subheader(
                "🕐 Timestamped Transcript"
            )


            for segment in transcript_segments:

                start = segment[
                    "start"
                ]

                end = segment[
                    "end"
                ]

                text = segment[
                    "text"
                ]


                st.markdown(
                    f"**[{start:.2f}s → "
                    f"{end:.2f}s]** "
                    f"{text}"
                )


        else:

            st.info(
                "No speech was detected "
                "in this video."
            )


    except subprocess.CalledProcessError:

        st.warning(
            "⚠️ This video does not appear "
            "to contain an audio track."
        )


    except Exception as e:

        st.error(
            f"❌ Audio analysis failed: {e}"
        )

# ========================================================
# TIMELINE INTELLIGENCE
# ========================================================

scenes = st.session_state.get(
    "scenes",
    []
)

transcript_segments = st.session_state.get(
    "transcript_segments",
    []
)


if scenes or transcript_segments:

    st.divider()

    st.subheader(
        "🧠 Timeline Intelligence"
    )

    with st.spinner(
        "Analyzing video timeline..."
    ):

        timeline_results = analyze_timeline(
            duration=duration,
            scenes=scenes,
            transcript_segments=transcript_segments,
            silence_percentage=silence_percentage
        )


    # Save results

    st.session_state[
        "timeline_results"
    ] = timeline_results


    # ====================================================
    # ACTIVITY SCORE
    # ====================================================

    activity_score = timeline_results[
        "activity_score"
    ]


    st.metric(
        "Timeline Activity Score",
        f"{activity_score}/100"
    )


    # ====================================================
    # METRICS
    # ====================================================

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "Scene Changes",
            timeline_results[
                "scene_changes"
            ]
        )


    with col2:

        st.metric(
            "Changes / Minute",
            timeline_results[
                "scene_changes_per_minute"
            ]
        )


    with col3:

        st.metric(
            "Speech Coverage",
            f"{timeline_results['speech_percentage']:.1f}%"
        )


    with col4:

        st.metric(
            "Silence",
            f"{timeline_results['silence_percentage']:.1f}%"
        )


    # ====================================================
    # HOOK INFORMATION
    # ====================================================

    st.subheader(
        "🎣 Early Video / Hook"
    )


    first_scene_change = timeline_results[
        "first_scene_change"
    ]


    early_scene_changes = timeline_results[
        "early_scene_changes"
    ]


    col1, col2 = st.columns(2)


    with col1:

        if first_scene_change is not None:

            st.metric(
                "First Visual Change",
                f"{first_scene_change:.2f}s"
            )

        else:

            st.metric(
                "First Visual Change",
                "None detected"
            )


    with col2:

        st.metric(
            "Changes in First 30s",
            early_scene_changes
        )


    # ====================================================
    # WARNINGS
    # ====================================================

    warnings = timeline_results[
        "warnings"
    ]


    st.subheader(
        "⚠️ Timeline Warnings"
    )


    if warnings:

        for warning in warnings:

            st.warning(
                warning
            )

    else:

        st.success(
            "✅ No major timeline issues detected."
        )


    # ====================================================
    # LONG VISUAL GAPS
    # ====================================================

    visual_gaps = timeline_results[
        "long_visual_gaps"
    ]


    st.subheader(
        "⏸️ Long Visual Gaps"
    )


    if visual_gaps:

        for gap in visual_gaps:

            st.info(
                f"⏱️ {gap['start']:.2f}s → "
                f"{gap['end']:.2f}s "
                f"({gap['duration']:.2f}s)"
            )

    else:

        st.success(
            "✅ No long visual gaps detected."
        )

        # ========================================================
# RETENTION RISK ANALYSIS
# ========================================================

scenes = st.session_state.get(
    "scenes",
    []
)

transcript_segments = st.session_state.get(
    "transcript_segments",
    []
)


if scenes or transcript_segments:

    st.divider()

    st.subheader(
        "📉 Retention Risk Analysis"
    )

    st.write(
        "This section identifies structural patterns "
        "that may create viewer-retention risks."
    )


    # ====================================================
    # RUN RETENTION ANALYSIS
    # ====================================================

    with st.spinner(
        "Analyzing potential retention risks..."
    ):

        retention_results = analyze_retention(
            duration=duration,
            scenes=scenes,
            transcript_segments=transcript_segments,
            silence_percentage=silence_percentage
        )


    # Save results

    st.session_state[
        "retention_results"
    ] = retention_results


    # ====================================================
    # RETENTION SCORE
    # ====================================================

    retention_score = retention_results[
        "retention_score"
    ]

    risk_score = retention_results[
        "risk_score"
    ]

    risk_count = retention_results[
        "risk_count"
    ]


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Retention Score",
            f"{retention_score}/100"
        )


    with col2:

        st.metric(
            "Risk Score",
            f"{risk_score}/100"
        )


    with col3:

        st.metric(
            "Detected Risks",
            risk_count
        )


    # ====================================================
    # SCORE INTERPRETATION
    # ====================================================

    if retention_score >= 80:

        st.success(
            f"🟢 {retention_results['assessment']}"
        )

    elif retention_score >= 60:

        st.warning(
            f"🟡 {retention_results['assessment']}"
        )

    else:

        st.error(
            f"🔴 {retention_results['assessment']}"
        )


    # ====================================================
    # RETENTION RISKS
    # ====================================================

    risks = retention_results[
        "risks"
    ]


    st.subheader(
        "⚠️ Potential Retention Risks"
    )


    if risks:

        for index, risk in enumerate(
            risks
        ):

            timestamp = risk[
                "timestamp"
            ]

            severity = risk[
                "severity"
            ]

            risk_type = risk[
                "type"
            ]

            reason = risk[
                "reason"
            ]


            if severity == "High":

                st.error(
                    f"🔴 {timestamp:.2f}s — "
                    f"**{risk_type}**\n\n"
                    f"{reason}"
                )

            elif severity == "Medium":

                st.warning(
                    f"🟡 {timestamp:.2f}s — "
                    f"**{risk_type}**\n\n"
                    f"{reason}"
                )

            else:

                st.info(
                    f"🔵 {timestamp:.2f}s — "
                    f"**{risk_type}**\n\n"
                    f"{reason}"
                )

    else:

        st.success(
            "✅ No significant retention risks "
            "were detected by the current rules."
        )


    # ====================================================
    # RETENTION RISK TIMELINE
    # ====================================================

    if risks and duration > 0:

        st.subheader(
            "📍 Retention Risk Timeline"
        )

        st.write(
            "Potential risk points across the video."
        )


        timeline_html = """
        <div style="
            width: 100%;
            padding: 25px 10px;
            background-color: #111827;
            border-radius: 12px;
            box-sizing: border-box;
        ">

            <div style="
                position: relative;
                height: 110px;
                margin: 0 25px;
            ">

                <div style="
                    position: absolute;
                    top: 45px;
                    left: 0;
                    right: 0;
                    height: 7px;
                    background-color: #6b7280;
                    border-radius: 5px;
                ">
                </div>

        """


        # Start marker

        timeline_html += """
                <div style="
                    position: absolute;
                    left: 0%;
                    top: 30px;
                    text-align: center;
                ">

                    <div style="
                        width: 28px;
                        height: 28px;
                        background-color: #22c55e;
                        border-radius: 50%;
                        border: 3px solid white;
                    ">
                    </div>

                    <div style="
                        color: white;
                        font-size: 12px;
                        margin-top: 8px;
                    ">
                        0s
                    </div>

                </div>
        """


        # Risk markers

        for risk in risks:

            timestamp = risk[
                "timestamp"
            ]

            severity = risk[
                "severity"
            ]


            percentage = (
                timestamp
                / duration
                * 100
            )


            percentage = max(
                0,
                min(
                    percentage,
                    100
                )
            )


            if severity == "High":

                marker_size = 22

            else:

                marker_size = 17


            timeline_html += f"""
                <div title="
                    {risk['type']} at {timestamp:.2f}s
                "
                style="
                    position: absolute;
                    left: {percentage}%;
                    top: 33px;
                    transform: translateX(-50%);
                    text-align: center;
                ">

                    <div style="
                        width: {marker_size}px;
                        height: {marker_size}px;
                        background-color: #ef4444;
                        border-radius: 50%;
                        border: 2px solid white;
                    ">
                    </div>

                    <div style="
                        color: white;
                        font-size: 10px;
                        margin-top: 7px;
                        white-space: nowrap;
                    ">
                        {timestamp:.1f}s
                    </div>

                </div>
            """


        # End marker

        timeline_html += f"""
                <div style="
                    position: absolute;
                    right: 0%;
                    top: 30px;
                    text-align: center;
                ">

                    <div style="
                        width: 28px;
                        height: 28px;
                        background-color: #3b82f6;
                        border-radius: 50%;
                        border: 3px solid white;
                    ">
                    </div>

                    <div style="
                        color: white;
                        font-size: 12px;
                        margin-top: 8px;
                    ">
                        {duration:.1f}s
                    </div>

                </div>

            </div>

            <div style="
                text-align: center;
                color: #d1d5db;
                font-size: 13px;
            ">
                🟢 Start
                &nbsp;&nbsp;
                🔴 Potential Risk
                &nbsp;&nbsp;
                🔵 End
            </div>

        </div>
        """


        st.components.v1.html(
            timeline_html,
            height=180
        )

        # ============================================================
# HOOK ANALYSIS
# ============================================================

st.header("🎯 Hook Analysis")

if (
    "scenes" in st.session_state
    and "transcript_segments" in st.session_state
):

    hook_results = analyze_hook(
        duration,
        st.session_state["scenes"],
        st.session_state["transcript_segments"]
    )

    st.session_state["hook_results"] = hook_results

    # --------------------------------------------------------
    # SCORE
    # --------------------------------------------------------

    st.subheader("Hook Score")

    st.metric(
        "Hook Score",
        f"{hook_results['hook_score']}/100"
    )

    # --------------------------------------------------------
    # KEY METRICS
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "First Speech",
            (
                f"{hook_results['first_speech_start']:.1f}s"
                if hook_results["first_speech_start"] is not None
                else "None"
            )
        )

    with col2:
        st.metric(
            "First Visual Change",
            (
                f"{hook_results['first_visual_change']:.1f}s"
                if hook_results["first_visual_change"] is not None
                else "None"
            )
        )

    with col3:
        st.metric(
            "Speech Coverage",
            f"{hook_results['hook_speech_coverage']}%"
        )

    # --------------------------------------------------------
    # OPENING SILENCE
    # --------------------------------------------------------

    st.write(
        f"**Opening Silence:** "
        f"{hook_results['opening_silence']} seconds"
    )

    st.write(
        f"**Early Visual Changes:** "
        f"{hook_results['early_scene_changes']}"
    )

    # --------------------------------------------------------
    # FIRST SPEECH
    # --------------------------------------------------------

    if hook_results["first_speech_text"]:

        st.subheader("🗣️ First Spoken Line")

        st.info(
            hook_results["first_speech_text"]
        )

    # --------------------------------------------------------
    # ASSESSMENT
    # --------------------------------------------------------

    st.subheader("Assessment")

    st.write(
        hook_results["assessment"]
    )

    # --------------------------------------------------------
    # POSITIVE SIGNALS
    # --------------------------------------------------------

    if hook_results["signals"]:

        st.subheader("✅ Positive Signals")

        for signal in hook_results["signals"]:
            st.success(signal)

    # --------------------------------------------------------
    # WARNINGS
    # --------------------------------------------------------

    if hook_results["warnings"]:

        st.subheader("⚠️ Hook Warnings")

        for warning in hook_results["warnings"]:
            st.warning(warning)

else:

    st.info(
        "Run scene detection and transcription first "
        "to generate hook analysis."
    )


    # ============================================================
# STORY & CONTENT ANALYSIS
# ============================================================

st.header("📖 Story & Content Analysis")

if "transcript_segments" in st.session_state:

    story_results = analyze_story(
        duration,
        st.session_state["transcript_segments"]
    )

    st.session_state["story_results"] = story_results

    # --------------------------------------------------------
    # SCORE
    # --------------------------------------------------------

    st.subheader("Story / Content Score")

    st.metric(
        "Story Score",
        f"{story_results['story_score']}/100"
    )

    # --------------------------------------------------------
    # KEY METRICS
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Speech Coverage",
            f"{story_results['speech_coverage']}%"
        )

    with col2:
        st.metric(
            "Content Segments",
            story_results["total_segments"]
        )

    with col3:
        st.metric(
            "Avg Segment Length",
            f"{story_results['average_segment_length']}s"
        )

    # --------------------------------------------------------
    # CONTENT STRUCTURE
    # --------------------------------------------------------

    st.subheader("Content Structure")

    with st.expander("Beginning"):
        if story_results["beginning_content"]:
            st.write(
                story_results["beginning_content"]
            )
        else:
            st.warning(
                "No identifiable beginning content."
            )

    with st.expander("Middle"):
        if story_results["middle_content"]:
            st.write(
                story_results["middle_content"]
            )
        else:
            st.warning(
                "No identifiable middle content."
            )

    with st.expander("Ending"):
        if story_results["ending_content"]:
            st.write(
                story_results["ending_content"]
            )
        else:
            st.warning(
                "No identifiable ending content."
            )

    # --------------------------------------------------------
    # ASSESSMENT
    # --------------------------------------------------------

    st.subheader("Assessment")

    st.info(
        story_results["assessment"]
    )

    # --------------------------------------------------------
    # POSITIVE SIGNALS
    # --------------------------------------------------------

    if story_results["signals"]:

        st.subheader("✅ Positive Signals")

        for signal in story_results["signals"]:
            st.success(signal)

    # --------------------------------------------------------
    # WARNINGS
    # --------------------------------------------------------

    if story_results["warnings"]:

        st.subheader("⚠️ Content Warnings")

        for warning in story_results["warnings"]:
            st.warning(warning)

else:

    st.info(
        "Run transcription first to generate "
        "Story & Content Analysis."
    )

# ============================================================
# VISUAL ANALYSIS
# ============================================================

st.header("🖼️ Visual Analysis")

if "temp_video_path" in st.session_state:

    visual_results = analyze_visuals(
        st.session_state["temp_video_path"],
        sample_interval=2.0
    )

    st.session_state["visual_results"] = visual_results

    # --------------------------------------------------------
    # SCORE
    # --------------------------------------------------------

    st.subheader("Visual Quality Score")

    st.metric(
        "Visual Score",
        f"{visual_results['visual_score']}/100"
    )

    # --------------------------------------------------------
    # KEY METRICS
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Frames Analyzed",
            visual_results["frames_analyzed"]
        )

    with col2:
        st.metric(
            "Avg Brightness",
            visual_results["average_brightness"]
        )

    with col3:
        st.metric(
            "Dark Frames",
            f"{visual_results['dark_percentage']}%"
        )

    with col4:
        st.metric(
            "Bright Frames",
            f"{visual_results['bright_percentage']}%"
        )

    st.metric(
        "Repeated Frames",
        f"{visual_results['repeated_percentage']}%"
    )

    # --------------------------------------------------------
    # ASSESSMENT
    # --------------------------------------------------------

    st.subheader("Assessment")

    st.info(
        visual_results["assessment"]
    )

    # --------------------------------------------------------
    # POSITIVE SIGNALS
    # --------------------------------------------------------

    if visual_results["signals"]:

        st.subheader("✅ Positive Signals")

        for signal in visual_results["signals"]:
            st.success(signal)

    # --------------------------------------------------------
    # WARNINGS
    # --------------------------------------------------------

    if visual_results["warnings"]:

        st.subheader("⚠️ Visual Warnings")

        for warning in visual_results["warnings"]:
            st.warning(warning)

    # ========================================================
    # TITLE ANALYSIS
    # ========================================================

    st.header("📝 Title Analysis")

    if video_title.strip():

        with st.spinner("Analyzing video title..."):
            title_results = analyze_title(
                video_title
            )

        st.session_state["title_results"] = title_results

        # --------------------------------------------------------
        # SCORE
        # --------------------------------------------------------

        st.subheader("Title Score")

        st.metric(
            "Title Score",
            f"{title_results['title_score']}/100"
        )

        # --------------------------------------------------------
        # KEY METRICS
        # --------------------------------------------------------

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Characters",
                title_results["character_count"]
            )

        with col2:
            st.metric(
                "Words",
                title_results["word_count"]
            )

        with col3:
            st.metric(
                "Uppercase",
                f"{title_results['uppercase_percentage']}%"
            )

        # --------------------------------------------------------
        # ASSESSMENT
        # --------------------------------------------------------

        st.subheader("Assessment")

        st.info(
            title_results["assessment"]
        )

        # --------------------------------------------------------
        # POSITIVE SIGNALS
        # --------------------------------------------------------

        if title_results["signals"]:
            st.subheader("✅ Positive Signals")

            for signal in title_results["signals"]:
                st.success(signal)

        # --------------------------------------------------------
        # WARNINGS
        # --------------------------------------------------------

        if title_results["warnings"]:
            st.subheader("⚠️ Title Warnings")

            for warning in title_results["warnings"]:
                st.warning(warning)

        # --------------------------------------------------------
        # SUGGESTIONS
        # --------------------------------------------------------

        if title_results["suggestions"]:
            st.subheader("💡 Improvement Suggestions")

            for suggestion in title_results["suggestions"]:
                st.info(suggestion)

    else:
        st.info(
            "Enter a video title above to generate "
            "Title Analysis."
        )


    # ========================================================
    # OVERALL PRE-PUBLISH SCORE
    # ========================================================

    st.divider()

    st.header("🏆 Overall Pre-Publish Score")

    st.write(
        "This score combines the individual analysis modules "
        "into one overall pre-publish assessment. It does not "
        "predict actual YouTube performance or virality."
    )

    hook_results = st.session_state.get(
        "hook_results"
    )

    story_results = st.session_state.get(
        "story_results"
    )

    retention_results = st.session_state.get(
        "retention_results"
    )

    visual_results = st.session_state.get(
        "visual_results"
    )

    title_results = st.session_state.get(
        "title_results"
    )

    thumbnail_results = st.session_state.get(
        "thumbnail_results"
    )

    audio_score = st.session_state.get(
        "audio_score"
    )

    required_scores_available = all(
        result is not None
        for result in [
            hook_results,
            story_results,
            retention_results,
            visual_results,
            title_results,
            thumbnail_results
        ]
    ) and audio_score is not None

    required_scores_available = all([
    st.session_state.get("hook_results") is not None,
    st.session_state.get("story_results") is not None,
    st.session_state.get("retention_results") is not None,
    st.session_state.get("title_results") is not None,
    st.session_state.get("thumbnail_results") is not None
    ])
    if required_scores_available:

        with st.spinner(
            "Calculating overall pre-publish score..."
        ):

            overall_results = calculate_overall_score(
                hook_score=hook_results["hook_score"],
                story_score=story_results["story_score"],
                retention_score=retention_results["retention_score"],
                visual_score=visual_results["visual_score"],
                audio_score=audio_score,
                title_score=title_results["title_score"],
                thumbnail_score=thumbnail_results["thumbnail_score"]
            )

        st.session_state[
            "overall_results"
        ] = overall_results

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Overall Score",
                f"{overall_results['overall_score']}/100"
            )

        with col2:

            st.metric(
                "Rating",
                overall_results["rating"]
            )

        with col3:

            st.metric(
                "Strongest Area",
                overall_results["strongest_areas"][0][0].title()
            )

        st.subheader("Assessment")

        st.info(
            overall_results["assessment"]
        )

        st.subheader("Component Scores")

        component_scores = overall_results[
            "component_scores"
        ]

        for name, score in component_scores.items():

            st.progress(
                score / 100
            )

            st.write(
                f"**{name.title()}:** {score}/100"
            )

        st.subheader("💪 Strongest Areas")

        for name, score in overall_results["strongest_areas"]:

            st.success(
                f"{name.title()}: {score}/100"
            )

        st.subheader("⚠️ Areas Needing Improvement")

        for name, score in overall_results["weakest_areas"]:

            st.warning(
                f"{name.title()}: {score}/100"
            )

    else:

        st.info(
            "Complete the video, title, thumbnail, audio, "
            "hook, story, retention, and visual analyses "
            "to generate the overall pre-publish score."
        )

# ========================================================
# HUMAN VIRALITY ANALYSIS
# ========================================================

st.divider()

st.header("🔥 Human Virality Analysis")

st.write(
    "This score evaluates human-oriented engagement signals "
    "such as hook strength, pacing, content structure, "
    "visual variation, title and thumbnail quality. "
    "It does not predict actual views or guarantee virality."
)

hook_results = st.session_state.get("hook_results")
story_results = st.session_state.get("story_results")
retention_results = st.session_state.get("retention_results")
visual_results = st.session_state.get("visual_results")
title_results = st.session_state.get("title_results")
thumbnail_results = st.session_state.get("thumbnail_results")
timeline_results = st.session_state.get("timeline_results")

if all([
    hook_results,
    story_results,
    retention_results,
    visual_results,
    title_results,
    thumbnail_results,
    timeline_results
]):

    human_virality_results = calculate_human_virality(
        hook_score=hook_results["hook_score"],
        story_score=story_results["story_score"],
        retention_score=retention_results["retention_score"],
        visual_score=visual_results["visual_score"],
        audio_score=st.session_state.get("audio_score", 0),
        title_score=title_results["title_score"],
        thumbnail_score=thumbnail_results["thumbnail_score"],
        speech_coverage=story_results["speech_coverage"],
        scene_changes_per_minute=timeline_results[
            "scene_changes_per_minute"
        ],
        opening_silence=hook_results["opening_silence"],
        first_visual_change=hook_results[
            "first_visual_change"
        ]
    )

    st.session_state[
        "human_virality_results"
    ] = human_virality_results

    st.metric(
        "🔥 Human Virality Score",
        f"{human_virality_results['human_virality_score']}/100"
    )

    st.subheader("Assessment")

    st.info(
        human_virality_results["assessment"]
    )

    if human_virality_results["signals"]:

        st.subheader("✅ Positive Signals")

        for signal in human_virality_results["signals"]:
            st.success(signal)

    if human_virality_results["warnings"]:

        st.subheader("⚠️ Potential Weaknesses")

        for warning in human_virality_results["warnings"]:
            st.warning(warning)

else:

    st.info(
        "Complete the main analysis modules first "
        "to generate the Human Virality Score."
    )   

# # ========================================================
# # ESTIMATED ATTENTION ANALYSIS
# # ========================================================

# st.divider()

# st.header("👁️ Estimated Attention Analysis")

# st.write(
#     "This module estimates where viewer attention may "
#     "strengthen or weaken using existing video-analysis "
#     "signals. It is a rule-based estimate and does not "
#     "represent measured viewer behavior."
# )

# hook_results = st.session_state.get("hook_results")
# retention_results = st.session_state.get("retention_results")
# visual_results = st.session_state.get("visual_results")
# timeline_results = st.session_state.get("timeline_results")
# story_results = st.session_state.get("story_results")
# scenes = st.session_state.get("scenes", [])

# if all([
#     hook_results,
#     retention_results,
#     visual_results,
#     timeline_results,
#     story_results
# ]):

#     with st.spinner(
#         "Estimating attention pattern..."
#     ):

#         attention_results = calculate_attention_analysis(
#             duration=duration,
#             scenes=scenes,
#             retention_results=retention_results,
#             hook_results=hook_results,
#             visual_results=visual_results,
#             timeline_results=timeline_results,
#             story_results=story_results
#         )

#     st.session_state[
#         "attention_results"
#     ] = attention_results

#     # ----------------------------------------------------
#     # SCORE
#     # ----------------------------------------------------

#     st.subheader("Estimated Attention Score")

#     st.metric(
#         "Attention Score",
#         f"{attention_results['attention_score']}/100"
#     )

#     # ----------------------------------------------------
#     # KEY INFORMATION
#     # ----------------------------------------------------

#     col1, col2, col3 = st.columns(3)

#     with col1:

#         st.metric(
#             "Attention Risks",
#             len(
#                 attention_results[
#                     "attention_risks"
#                 ]
#             )
#         )

#     with col2:

#         st.metric(
#             "Recovery Points",
#             len(
#                 attention_results[
#                     "attention_recoveries"
#                 ]
#             )
#         )

#     with col3:

#         st.metric(
#             "Confidence",
#             attention_results[
#                 "confidence"
#             ]
#         )

#     # ----------------------------------------------------
#     # ATTENTION CURVE
#     # ----------------------------------------------------

#     st.subheader(
#         "📈 Estimated Attention Curve"
#     )

#     curve = attention_results[
#         "attention_curve"
#     ]

#     if curve:

#         curve_data = {
#             point["timestamp"]: point["attention"]
#             for point in curve
#         }

#         st.line_chart(
#             curve_data,
#             x_label="Time (seconds)",
#             y_label="Estimated Attention"
#         )

#     # ----------------------------------------------------
#     # ASSESSMENT
#     # ----------------------------------------------------

#     st.subheader("Assessment")

#     st.info(
#         attention_results[
#             "assessment"
#         ]
#     )

#     # ----------------------------------------------------
#     # ATTENTION RISKS
#     # ----------------------------------------------------

#     risks = attention_results[
#         "attention_risks"
#     ]

#     if risks:

#         st.subheader(
#             "⚠️ Estimated Attention Drops"
#         )

#         for risk in risks:

#             if risk["severity"] == "High":

#                 st.error(
#                     f"🔴 {risk['timestamp']:.2f}s — "
#                     f"Attention drop: "
#                     f"{risk['drop']:.1f} points\n\n"
#                     f"{risk['reason']}"
#                 )

#             else:

#                 st.warning(
#                     f"🟡 {risk['timestamp']:.2f}s — "
#                     f"Attention drop: "
#                     f"{risk['drop']:.1f} points\n\n"
#                     f"{risk['reason']}"
#                 )

#     else:

#         st.success(
#             "✅ No major estimated attention drops detected."
#         )

#     # ----------------------------------------------------
#     # RECOVERY POINTS
#     # ----------------------------------------------------

#     recoveries = attention_results[
#         "attention_recoveries"
#     ]

#     if recoveries:

#         st.subheader(
#             "🔄 Estimated Attention Recovery Points"
#         )

#         for recovery in recoveries:

#             st.success(
#                 f"📈 {recovery['timestamp']:.2f}s — "
#                 f"Estimated increase: "
#                 f"{recovery['increase']:.1f} points"
#             )

# else:

#     st.info(
#         "Complete the main analysis modules first "
#         "to generate Estimated Attention Analysis."
#     )

# # ========================================================
# # AUDIENCE UNDERSTANDING & PROMISE MATCHING
# # ========================================================

# st.divider()

# st.header("🎯 Audience Understanding & Promise Matching")

# st.write(
#     "This module analyzes the available title, transcript, "
#     "story and thumbnail signals to estimate audience intent "
#     "and determine how closely the content matches its promise."
# )

# hook_results = st.session_state.get(
#     "hook_results"
# )

# story_results = st.session_state.get(
#     "story_results"
# )

# thumbnail_results = st.session_state.get(
#     "thumbnail_results"
# )

# transcript_segments = st.session_state.get(
#     "transcript_segments",
#     []
# )

# if hook_results and story_results:

#     with st.spinner(
#         "Analyzing audience understanding and content promise..."
#     ):

#         audience_understanding_results = (
#             analyze_audience_understanding(
#                 title=video_title,
#                 transcript_segments=transcript_segments,
#                 story_results=story_results,
#                 hook_results=hook_results,
#                 thumbnail_results=thumbnail_results
#             )
#         )

#     st.session_state[
#         "audience_understanding_results"
#     ] = audience_understanding_results

#     # ----------------------------------------------------
#     # MAIN SCORE
#     # ----------------------------------------------------

#     st.subheader(
#         "Audience Understanding Score"
#     )

#     st.metric(
#         "Audience Understanding",
#         f"{audience_understanding_results['audience_understanding_score']}/100"
#     )

#     # ----------------------------------------------------
#     # CORE SIGNALS
#     # ----------------------------------------------------

#     col1, col2, col3, col4 = st.columns(4)

#     with col1:

#         st.metric(
#             "Curiosity",
#             f"{audience_understanding_results['curiosity_score']}/100"
#         )

#     with col2:

#         st.metric(
#             "Emotion",
#             f"{audience_understanding_results['emotion_score']}/100"
#         )

#     with col3:

#         st.metric(
#             "Relatability",
#             f"{audience_understanding_results['relatability_score']}/100"
#         )

#     with col4:

#         st.metric(
#             "Novelty",
#             f"{audience_understanding_results['novelty_score']}/100"
#         )

#     # ----------------------------------------------------
#     # PROMISE MATCHING
#     # ----------------------------------------------------

#     st.subheader(
#         "🔗 Content Promise Matching"
#     )

#     col1, col2, col3 = st.columns(3)

#     with col1:

#         st.metric(
#             "Title ↔ Content",
#             f"{audience_understanding_results['title_content_promise_score']}/100"
#         )

#     with col2:

#         st.metric(
#             "Title Clarity",
#             f"{audience_understanding_results['title_clarity_score']}/100"
#         )

#     with col3:

#         st.metric(
#             "Promise Match",
#             f"{audience_understanding_results['promise_match_score']}/100"
#         )

#     if thumbnail_results:

#         st.metric(
#             "Thumbnail Consistency",
#             f"{audience_understanding_results['thumbnail_consistency_score']}/100"
#         )

#     # ----------------------------------------------------
#     # AUDIENCE CLUES
#     # ----------------------------------------------------

#     st.subheader(
#         "👥 Detected Audience Clues"
#     )

#     for clue in audience_understanding_results[
#         "audience_clues"
#     ]:

#         st.info(
#             clue
#         )

#     # ----------------------------------------------------
#     # POSITIVE SIGNALS
#     # ----------------------------------------------------

#     if audience_understanding_results[
#         "signals"
#     ]:

#         st.subheader(
#             "✅ Audience Positive Signals"
#         )

#         for signal in audience_understanding_results[
#             "signals"
#         ]:

#             st.success(
#                 signal
#             )

#     # ----------------------------------------------------
#     # WARNINGS
#     # ----------------------------------------------------

#     if audience_understanding_results[
#         "warnings"
#     ]:

#         st.subheader(
#             "⚠️ Audience / Promise Warnings"
#         )

#         for warning in audience_understanding_results[
#             "warnings"
#         ]:

#             st.warning(
#                 warning
#             )

#     # ----------------------------------------------------
#     # ASSESSMENT
#     # ----------------------------------------------------

#     st.subheader(
#         "Assessment"
#     )

#     st.info(
#         audience_understanding_results[
#             "assessment"
#         ]
#     )

#     st.caption(
#         "Confidence: "
#         + audience_understanding_results[
#             "confidence"
#         ]
#     )

# else:

#     st.info(
#         "Complete the title, transcription, hook and story "
#         "analysis first."
#     )

#     # ========================================================
#     # AUDIENCE POTENTIAL SCORE
#     # ========================================================

#     st.divider()

#     st.header("👥 Audience Potential Score")

#     st.write(
#         "This is an initial rule-based estimate of audience response "
#         "potential. It uses signals already available in the analyzer. "
#         "Emotion, relatability, novelty, and shareability will be "
#         "expanded in later audience-intelligence modules."
#     )

#     required_scores_available = all([
#     st.session_state.get("hook_results") is not None,
#     st.session_state.get("story_results") is not None,
#     st.session_state.get("retention_results") is not None,
#     st.session_state.get("title_results") is not None,
#     st.session_state.get("thumbnail_results") is not None
#     ])

#     if required_scores_available:

#         # Existing analyzer scores are used as initial proxies.
#         # These are deliberately transparent and will be replaced/
#         # enriched by dedicated audience modules later.
#         audience_results = calculate_audience_score(
#             curiosity_score=hook_results["hook_score"],
#             emotion_score=0,
#             relatability_score=0,
#             storytelling_score=story_results["story_score"],
#             attention_score=retention_results["retention_score"],
#             shareability_score=0,
#             novelty_score=0,
#             promise_match_score=(
#                 title_results["title_score"] +
#                 thumbnail_results["thumbnail_score"]
#             ) / 2
#         )

#         st.session_state["audience_results"] = audience_results

#         col1, col2, col3 = st.columns(3)

#         with col1:
#             st.metric(
#                 "Audience Score",
#                 f"{audience_results['audience_score']}/100"
#             )

#         with col2:
#             st.metric(
#                 "Rating",
#                 audience_results["rating"]
#             )

#         with col3:
#             st.metric(
#                 "Confidence",
#                 audience_results["confidence"]
#             )

#         st.subheader("Audience Signals")

#         for name, score in audience_results["component_scores"].items():
#             st.progress(score / 100)
#             st.write(
#                 f"**{name.replace('_', ' ').title()}:** {score}/100"
#             )

#         st.subheader("Current Audience Assessment")

#         st.info(
#             f"Strongest current signal: "
#             f"{audience_results['strongest_area'].replace('_', ' ').title()} "
#             f"({audience_results['component_scores'][audience_results['strongest_area']]:.1f}/100). "
#             f"Weakest current signal: "
#             f"{audience_results['weakest_area'].replace('_', ' ').title()} "
#             f"({audience_results['component_scores'][audience_results['weakest_area']]:.1f}/100)."
#         )

#     else:

#         st.info(
#             "Complete the existing video analyses first to generate "
#             "the initial audience potential score."
#         )


# # ========================================================
# # TREND ANALYSIS & VIRAL-PATTERN COMPARISON
# # ========================================================

# st.divider()

# st.header("📈 Trend Analysis & Viral-Pattern Comparison")

# st.write(
#     "This module compares the video's existing signals "
#     "with generalized high-engagement content patterns. "
#     "It does not predict actual views or guarantee virality."
# )

# hook_results = st.session_state.get(
#     "hook_results"
# )

# story_results = st.session_state.get(
#     "story_results"
# )

# retention_results = st.session_state.get(
#     "retention_results"
# )

# visual_results = st.session_state.get(
#     "visual_results"
# )

# timeline_results = st.session_state.get(
#     "timeline_results"
# )

# title_results = st.session_state.get(
#     "title_results"
# )

# thumbnail_results = st.session_state.get(
#     "thumbnail_results"
# )

# attention_results = st.session_state.get(
#     "attention_results"
# )

# audience_understanding_results = (
#     st.session_state.get(
#         "audience_understanding_results"
#     )
# )

# if all([
#     hook_results,
#     story_results,
#     retention_results,
#     visual_results,
#     timeline_results,
#     title_results,
#     thumbnail_results,
#     attention_results,
#     audience_understanding_results
# ]):

#     with st.spinner(
#         "Comparing video against generalized engagement patterns..."
#     ):

#         trend_results = analyze_trends(
#             duration=duration,
#             hook_results=hook_results,
#             story_results=story_results,
#             retention_results=retention_results,
#             visual_results=visual_results,
#             timeline_results=timeline_results,
#             title_results=title_results,
#             thumbnail_results=thumbnail_results,
#             attention_results=attention_results,
#             audience_understanding_results=(
#                 audience_understanding_results
#             )
#         )

#     st.session_state[
#         "trend_results"
#     ] = trend_results

#     # ----------------------------------------------------
#     # MAIN SCORE
#     # ----------------------------------------------------

#     st.subheader(
#         "Trend Pattern Score"
#     )

#     st.metric(
#         "Trend / Pattern Score",
#         f"{trend_results['trend_score']}/100"
#     )

#     # ----------------------------------------------------
#     # KEY METRICS
#     # ----------------------------------------------------

#     col1, col2, col3 = st.columns(3)

#     with col1:

#         st.metric(
#             "Pattern Matches",
#             len(
#                 trend_results[
#                     "pattern_matches"
#                 ]
#             )
#         )

#     with col2:

#         st.metric(
#             "Pattern Warnings",
#             len(
#                 trend_results[
#                     "pattern_warnings"
#                 ]
#             )
#         )

#     with col3:

#         st.metric(
#             "Confidence",
#             trend_results[
#                 "confidence"
#             ]
#         )

#     # ----------------------------------------------------
#     # CONTENT STYLE
#     # ----------------------------------------------------

#     st.subheader(
#         "🎥 Detected Content Style"
#     )

#     st.info(
#         trend_results["style"]
#     )

#     # ----------------------------------------------------
#     # ASSESSMENT
#     # ----------------------------------------------------

#     st.subheader(
#         "Assessment"
#     )

#     st.info(
#         trend_results["assessment"]
#     )

#     # ----------------------------------------------------
#     # PATTERN MATCHES
#     # ----------------------------------------------------

#     if trend_results[
#         "pattern_matches"
#     ]:

#         st.subheader(
#             "✅ Detected Engagement Patterns"
#         )

#         for pattern in trend_results[
#             "pattern_matches"
#         ]:

#             st.success(
#                 pattern
#             )

#     # ----------------------------------------------------
#     # PATTERN WARNINGS
#     # ----------------------------------------------------

#     if trend_results[
#         "pattern_warnings"
#     ]:

#         st.subheader(
#             "⚠️ Pattern Gaps"
#         )

#         for warning in trend_results[
#             "pattern_warnings"
#         ]:

#             st.warning(
#                 warning
#             )

#     # ----------------------------------------------------
#     # RECOMMENDATIONS
#     # ----------------------------------------------------

#     st.subheader(
#         "💡 Trend-Based Improvements"
#     )

#     for recommendation in trend_results[
#         "recommendations"
#     ]:

#         st.info(
#             recommendation
#         )

# else:

#     st.info(
#         "Complete the main analysis modules, attention "
#         "analysis and audience understanding analysis "
#         "first to generate Trend Analysis."
#     )

# # ========================================================
# # PHASE 28 — HUMAN VIEWER EVALUATION SIMULATOR
# # ========================================================

# st.divider()

# st.header("🧑‍💻 Human Viewer Evaluation Simulator")

# st.write(
#     "This module estimates how a typical viewer may respond "
#     "to the video using the analyzer's existing attention, "
#     "curiosity, emotional, storytelling and engagement signals."
# )

# st.caption(
#     "This is a simulated evaluation, not a substitute for "
#     "real human viewer testing."
# )

# hook_results = st.session_state.get(
#     "hook_results"
# )

# story_results = st.session_state.get(
#     "story_results"
# )

# retention_results = st.session_state.get(
#     "retention_results"
# )

# visual_results = st.session_state.get(
#     "visual_results"
# )

# attention_results = st.session_state.get(
#     "attention_results"
# )

# audience_understanding_results = (
#     st.session_state.get(
#         "audience_understanding_results"
#     )
# )

# trend_results = st.session_state.get(
#     "trend_results"
# )

# if all([
#     hook_results,
#     story_results,
#     retention_results,
#     visual_results,
#     attention_results,
#     audience_understanding_results,
#     trend_results
# ]):

#     with st.spinner(
#         "Simulating likely viewer responses..."
#     ):

#         viewer_results = simulate_viewer_response(
#             hook_results=hook_results,
#             story_results=story_results,
#             retention_results=retention_results,
#             visual_results=visual_results,
#             attention_results=attention_results,
#             audience_understanding_results=(
#                 audience_understanding_results
#             ),
#             trend_results=trend_results
#         )

#     st.session_state[
#         "viewer_simulation_results"
#     ] = viewer_results

#     # --------------------------------------------------
#     # MAIN SCORE
#     # --------------------------------------------------

#     st.subheader(
#         "🎯 Human Viewer Response Score"
#     )

#     st.metric(
#         "Estimated Viewer Response",
#         f"{viewer_results['viewer_response_score']}/100"
#     )

#     # --------------------------------------------------
#     # RESPONSE DIMENSIONS
#     # --------------------------------------------------

#     st.subheader(
#         "📊 Viewer Response Dimensions"
#     )

#     col1, col2, col3, col4 = st.columns(4)

#     with col1:
#         st.metric(
#             "Attention",
#             f"{viewer_results['attention_response']}/100"
#         )

#     with col2:
#         st.metric(
#             "Curiosity",
#             f"{viewer_results['curiosity_response']}/100"
#         )

#     with col3:
#         st.metric(
#             "Emotion",
#             f"{viewer_results['emotional_response']}/100"
#         )

#     with col4:
#         st.metric(
#             "Connection",
#             f"{viewer_results['connection_response']}/100"
#         )

#     col1, col2, col3, col4 = st.columns(4)

#     with col1:
#         st.metric(
#             "Novelty",
#             f"{viewer_results['novelty_response']}/100"
#         )

#     with col2:
#         st.metric(
#             "Story Engagement",
#             f"{viewer_results['story_engagement']}/100"
#         )

#     with col3:
#         st.metric(
#             "Clarity",
#             f"{viewer_results['clarity_response']}/100"
#         )

#     with col4:
#         st.metric(
#             "Shareability",
#             f"{viewer_results['shareability_response']}/100"
#         )

#     # --------------------------------------------------
#     # VIEWER BEHAVIOR
#     # --------------------------------------------------

#     st.subheader(
#         "👀 Estimated Viewer Behavior"
#     )

#     for behavior in viewer_results[
#         "viewer_behavior"
#     ]:
#         st.info(behavior)

#     # --------------------------------------------------
#     # POSITIVE REACTIONS
#     # --------------------------------------------------

#     if viewer_results[
#         "positive_reactions"
#     ]:

#         st.subheader(
#             "❤️ Possible Positive Viewer Reactions"
#         )

#         for reaction in viewer_results[
#             "positive_reactions"
#         ]:
#             st.success(reaction)

#     # --------------------------------------------------
#     # VIEWER RISKS
#     # --------------------------------------------------

#     if viewer_results[
#         "viewer_risks"
#     ]:

#         st.subheader(
#             "⚠️ Possible Viewer Friction"
#         )

#         for risk in viewer_results[
#             "viewer_risks"
#         ]:
#             st.warning(risk)

#     # --------------------------------------------------
#     # ASSESSMENT
#     # --------------------------------------------------

#     st.subheader(
#         "🧠 Simulated Viewer Assessment"
#     )

#     st.info(
#         viewer_results[
#             "assessment"
#         ]
#     )

#     # --------------------------------------------------
#     # CONFIDENCE
#     # --------------------------------------------------

#     st.subheader(
#         "Confidence"
#     )

#     st.metric(
#         "Simulation Confidence",
#         viewer_results[
#             "confidence"
#         ]
#     )

# else:

#     st.info(
#         "Complete Trend Analysis and the other main "
#         "analysis modules first to generate the "
#         "Human Viewer Evaluation."
#     )

# # ========================================================
# # PHASE 29 — AUDIENCE-RESPONSE SCORING ENGINE
# # ========================================================

# st.divider()

# st.header("🎯 Audience-Response Scoring Engine")

# st.write(
#     "This engine consolidates the audience-understanding, "
#     "viewer-simulation, attention and trend signals into "
#     "one structured audience-response score."
# )

# st.caption(
#     "This is an analytical estimate based on the available "
#     "video signals and is not a substitute for real viewer testing."
# )

# audience_understanding_results = (
#     st.session_state.get(
#         "audience_understanding_results"
#     )
# )

# viewer_simulation_results = (
#     st.session_state.get(
#         "viewer_simulation_results"
#     )
# )

# trend_results = st.session_state.get(
#     "trend_results"
# )

# attention_results = st.session_state.get(
#     "attention_results"
# )

# hook_results = st.session_state.get(
#     "hook_results"
# )

# story_results = st.session_state.get(
#     "story_results"
# )

# retention_results = st.session_state.get(
#     "retention_results"
# )

# if all([
#     audience_understanding_results,
#     viewer_simulation_results,
#     trend_results,
#     attention_results,
#     hook_results,
#     story_results,
#     retention_results
# ]):

#     with st.spinner(
#         "Calculating consolidated audience-response score..."
#     ):

#         audience_response_results = (
#             calculate_audience_response_score(
#                 audience_understanding_results=(
#                     audience_understanding_results
#                 ),
#                 viewer_simulation_results=(
#                     viewer_simulation_results
#                 ),
#                 trend_results=trend_results,
#                 attention_results=attention_results,
#                 hook_results=hook_results,
#                 story_results=story_results,
#                 retention_results=retention_results
#             )
#         )

#     st.session_state[
#         "audience_response_results"
#     ] = audience_response_results

#     # ==================================================
#     # MAIN SCORE
#     # ==================================================

#     st.subheader(
#         "🎯 Overall Audience-Response Score"
#     )

#     st.metric(
#         "Audience Response",
#         f"{audience_response_results['audience_response_score']}/100"
#     )

#     st.info(
#         f"Audience Potential: "
#         f"{audience_response_results['audience_potential']}"
#     )

#     # ==================================================
#     # DIMENSIONS
#     # ==================================================

#     st.subheader(
#         "📊 Audience Response Dimensions"
#     )

#     col1, col2, col3, col4 = st.columns(4)

#     with col1:
#         st.metric(
#             "Attention",
#             f"{audience_response_results['attention_score']}/100"
#         )

#     with col2:
#         st.metric(
#             "Curiosity",
#             f"{audience_response_results['curiosity_score']}/100"
#         )

#     with col3:
#         st.metric(
#             "Emotion",
#             f"{audience_response_results['emotion_score']}/100"
#         )

#     with col4:
#         st.metric(
#             "Relatability",
#             f"{audience_response_results['relatability_score']}/100"
#         )

#     col1, col2, col3, col4 = st.columns(4)

#     with col1:
#         st.metric(
#             "Novelty",
#             f"{audience_response_results['novelty_score']}/100"
#         )

#     with col2:
#         st.metric(
#             "Story Engagement",
#             f"{audience_response_results['story_engagement_score']}/100"
#         )

#     with col3:
#         st.metric(
#             "Clarity",
#             f"{audience_response_results['clarity_score']}/100"
#         )

#     with col4:
#         st.metric(
#             "Shareability",
#             f"{audience_response_results['shareability_score']}/100"
#         )

#     # ==================================================
#     # STRONGEST AREAS
#     # ==================================================

#     st.subheader(
#         "💪 Strongest Audience Areas"
#     )

#     for item in audience_response_results[
#         "strongest_areas"
#     ]:

#         st.success(
#             f"{item['area']}: "
#             f"{item['score']}/100"
#         )

#     # ==================================================
#     # WEAKEST AREAS
#     # ==================================================

#     st.subheader(
#         "⚠️ Areas Requiring Attention"
#     )

#     for item in audience_response_results[
#         "weakest_areas"
#     ]:

#         st.warning(
#             f"{item['area']}: "
#             f"{item['score']}/100"
#         )

#     # ==================================================
#     # IMPROVEMENTS
#     # ==================================================

#     st.subheader(
#         "💡 Priority Audience Improvements"
#     )

#     for improvement in audience_response_results[
#         "improvements"
#     ]:

#         st.info(improvement)

#     # ==================================================
#     # ASSESSMENT
#     # ==================================================

#     st.subheader(
#         "🧠 Audience Assessment"
#     )

#     st.info(
#         audience_response_results[
#             "assessment"
#         ]
#     )

#     # ==================================================
#     # CONFIDENCE
#     # ==================================================

#     st.subheader(
#         "Confidence"
#     )

#     st.metric(
#         "Scoring Confidence",
#         audience_response_results[
#             "confidence"
#         ]
#     )

# else:

#     st.info(
#         "Complete Audience Understanding, Trend Analysis "
#         "and Human Viewer Evaluation first to generate "
#         "the consolidated Audience-Response Score."
#     )

# # ========================================================
# # PHASE 30 — FINAL REPORT & DASHBOARD
# # ========================================================

# st.divider()

# st.header("📋 Final Video Analysis Report")

# st.write(
#     "This dashboard consolidates the technical, audience, "
#     "attention and trend analysis into one final report."
# )

# # --------------------------------------------------------
# # GET RESULTS
# # --------------------------------------------------------

# overall_score_results = st.session_state.get(
#     "overall_score_results"
# )

# audience_response_results = st.session_state.get(
#     "audience_response_results"
# )

# viewer_simulation_results = st.session_state.get(
#     "viewer_simulation_results"
# )

# trend_results = st.session_state.get(
#     "trend_results"
# )

# attention_results = st.session_state.get(
#     "attention_results"
# )

# hook_results = st.session_state.get(
#     "hook_results"
# )

# story_results = st.session_state.get(
#     "story_results"
# )

# retention_results = st.session_state.get(
#     "retention_results"
# )

# visual_results = st.session_state.get(
#     "visual_results"
# )

# title_results = st.session_state.get(
#     "title_results"
# )

# thumbnail_results = st.session_state.get(
#     "thumbnail_results"
# )

# # --------------------------------------------------------
# # GENERATE REPORT
# # --------------------------------------------------------

# if all([
#     audience_response_results,
#     viewer_simulation_results,
#     trend_results,
#     attention_results,
#     hook_results,
#     story_results,
#     retention_results,
#     visual_results,
#     title_results,
#     thumbnail_results
# ]):

#     with st.spinner(
#         "Generating final video report..."
#     ):

#         final_report = generate_final_report(
#             overall_score_results=(
#                 overall_score_results
#             ),

#             audience_response_results=(
#                 audience_response_results
#             ),

#             viewer_simulation_results=(
#                 viewer_simulation_results
#             ),

#             trend_results=trend_results,

#             attention_results=attention_results,

#             hook_results=hook_results,

#             story_results=story_results,

#             retention_results=retention_results,

#             visual_results=visual_results,

#             title_results=title_results,

#             thumbnail_results=thumbnail_results
#         )

#     st.session_state[
#         "final_report"
#     ] = final_report

#     # ====================================================
#     # FINAL SCORE
#     # ====================================================

#     st.subheader(
#         "🏆 Overall Video Score"
#     )

#     col1, col2, col3 = st.columns(3)

#     with col1:

#         st.metric(
#             "Final Score",
#             f"{final_report['final_score']}/100"
#         )

#     with col2:

#         st.metric(
#             "Category",
#             final_report[
#                 "score_category"
#             ]
#         )

#     with col3:

#         st.metric(
#             "Confidence",
#             final_report[
#                 "confidence"
#             ]
#         )

#     # ====================================================
#     # MAIN SCORE BREAKDOWN
#     # ====================================================

#     st.subheader(
#         "📊 Score Breakdown"
#     )

#     col1, col2, col3, col4 = st.columns(4)

#     with col1:

#         st.metric(
#             "Technical",
#             f"{final_report['technical_score']}/100"
#         )

#     with col2:

#         st.metric(
#             "Audience",
#             f"{final_report['audience_score']}/100"
#         )

#     with col3:

#         st.metric(
#             "Trends",
#             f"{final_report['trend_score']}/100"
#         )

#     with col4:

#         st.metric(
#             "Attention",
#             f"{final_report['attention_score']}/100"
#         )

#     # ====================================================
#     # COMPONENT SCORES
#     # ====================================================

#     st.subheader(
#         "🔍 Complete Component Scores"
#     )

#     component_scores = (
#         final_report[
#             "component_scores"
#         ]
#     )

#     for component, score in component_scores.items():

#         st.progress(
#             int(score),
#             text=f"{component}: {score}/100"
#         )

#     # ====================================================
#     # ASSESSMENT
#     # ====================================================

#     st.subheader(
#         "🧠 Final Assessment"
#     )

#     st.info(
#         final_report[
#             "assessment"
#         ]
#     )

#     # ====================================================
#     # STRONGEST AREAS
#     # ====================================================

#     st.subheader(
#         "💪 Strongest Areas"
#     )

#     for item in final_report[
#         "strongest_areas"
#     ]:

#         st.success(
#             f"{item['area']}: "
#             f"{item['score']}/100"
#         )

#     # ====================================================
#     # WEAKEST AREAS
#     # ====================================================

#     st.subheader(
#         "⚠️ Weakest Areas"
#     )

#     for item in final_report[
#         "weakest_areas"
#     ]:

#         st.warning(
#             f"{item['area']}: "
#             f"{item['score']}/100"
#         )

#     # ====================================================
#     # PRIORITY IMPROVEMENTS
#     # ====================================================

#     st.subheader(
#         "🚀 Priority Improvements"
#     )

#     for improvement in final_report[
#         "priority_improvements"
#     ]:

#         st.info(
#             improvement
#         )

#     # ====================================================
#     # AUDIENCE SUMMARY
#     # ====================================================

#     st.subheader(
#         "👥 Audience Summary"
#     )

#     st.write(
#         f"**Audience Potential:** "
#         f"{final_report['audience_potential']}"
#     )

#     if final_report[
#         "audience_strongest"
#     ]:

#         st.write(
#             "**Strongest audience signals:**"
#         )

#         for item in final_report[
#             "audience_strongest"
#         ]:

#             st.success(
#                 f"{item['area']}: "
#                 f"{item['score']}/100"
#             )

#     if final_report[
#         "audience_weakest"
#     ]:

#         st.write(
#             "**Weakest audience signals:**"
#         )

#         for item in final_report[
#             "audience_weakest"
#         ]:

#             st.warning(
#                 f"{item['area']}: "
#                 f"{item['score']}/100"
#             )

#     # ====================================================
#     # TREND SUMMARY
#     # ====================================================

#     st.subheader(
#         "📈 Trend & Pattern Summary"
#     )

#     if final_report[
#         "pattern_matches"
#     ]:

#         st.write(
#             "**Detected patterns:**"
#         )

#         for pattern in final_report[
#             "pattern_matches"
#         ]:

#             st.success(
#                 pattern
#             )

#     if final_report[
#         "pattern_warnings"
#     ]:

#         st.write(
#             "**Pattern gaps:**"
#         )

#         for warning in final_report[
#             "pattern_warnings"
#         ]:

#             st.warning(
#                 warning
#             )

#     # ====================================================
#     # ATTENTION SUMMARY
#     # ====================================================

#     st.subheader(
#         "👀 Attention Summary"
#     )

#     if final_report[
#         "attention_risks"
#     ]:

#         st.write(
#             "**Attention risks:**"
#         )

#         for risk in final_report[
#             "attention_risks"
#         ]:

#             st.warning(
#                 risk
#             )

#     if final_report[
#         "attention_recoveries"
#     ]:

#         st.write(
#             "**Potential recovery points:**"
#         )

#         for recovery in final_report[
#             "attention_recoveries"
#         ]:

#             st.success(
#                 recovery
#             )

#     # ====================================================
#     # REPORT STATUS
#     # ====================================================

#     st.success(
#         "Complete video analysis report generated successfully."
#     )

# else:

#     st.info(
#         "Complete all major analysis modules, including "
#         "Audience Response, Trend Analysis and Human Viewer "
#         "Simulation, before generating the final report."
#     )

# # ========================================================
# # PHASE 31 — HISTORICAL PERFORMANCE DATASET
# # ========================================================

# st.divider()

# st.header(
#     "🗃️ Historical Video Performance Dataset"
# )

# st.write(
#     "This section manages the historical video-performance "
#     "dataset that will later be used for channel-specific "
#     "performance prediction."
# )

# # --------------------------------------------------------
# # INITIALIZE DATASET
# # --------------------------------------------------------

# ensure_dataset_exists()

# dataset_summary = (
#     get_dataset_summary()
# )

# dataset_validation = (
#     validate_dataset()
# )

# # --------------------------------------------------------
# # DATASET STATUS
# # --------------------------------------------------------

# st.subheader(
#     "📊 Dataset Status"
# )

# col1, col2, col3, col4 = st.columns(4)

# with col1:

#     st.metric(
#         "Historical Videos",
#         dataset_summary[
#             "total_videos"
#         ]
#     )

# with col2:

#     st.metric(
#         "Channels",
#         dataset_summary[
#             "total_channels"
#         ]
#     )

# with col3:

#     st.metric(
#         "High Performance",
#         dataset_summary[
#             "high_performance_videos"
#         ]
#     )

# with col4:

#     st.metric(
#         "Medium Performance",
#         dataset_summary[
#             "medium_performance_videos"
#         ]
#     )

# # --------------------------------------------------------
# # VALIDATION
# # --------------------------------------------------------

# if dataset_validation[
#     "valid"
# ]:

#     st.success(
#         "Dataset structure is valid."
#     )

# else:

#     st.error(
#         "Dataset validation found problems."
#     )

#     for error in dataset_validation[
#         "errors"
#     ]:

#         st.warning(
#             error
#         )

# # --------------------------------------------------------
# # DATASET INFORMATION
# # --------------------------------------------------------

# st.subheader(
#     "📁 Dataset Information"
# )

# st.info(
#     "The dataset stores historical video metadata "
#     "and normalized engagement metrics. Phase 32 "
#     "will use this data to train the prediction model."
# )

# st.write(
#     f"**Records currently available:** "
#     f"{dataset_summary['total_videos']}"
# )

# st.write(
#     f"**Low-performance records:** "
#     f"{dataset_summary['low_performance_videos']}"
# )

# st.write(
#     f"**Medium-performance records:** "
#     f"{dataset_summary['medium_performance_videos']}"
# )

# st.write(
#     f"**High-performance records:** "
#     f"{dataset_summary['high_performance_videos']}"
# )

# # --------------------------------------------------------
# # DATASET PREVIEW
# # --------------------------------------------------------

# records = load_dataset()

# if records:

#     st.subheader(
#         "📋 Dataset Preview"
#     )

#     st.dataframe(
#         records,
#         width="stretch"
#     )

# else:

#     st.warning(
#         "The dataset is currently empty. "
#         "Add historical video records before "
#         "training the Phase 32 prediction model."
#     )

# # --------------------------------------------------------
# # REQUIRED DATA FIELDS
# # --------------------------------------------------------

# st.subheader(
#     "🧩 Required Historical Data"
# )

# st.write(
#     "Each historical video should ideally provide:"
# )

# required_fields = [
#     "Video ID",
#     "Title",
#     "Channel",
#     "Category",
#     "Upload date",
#     "Duration",
#     "Views",
#     "Likes",
#     "Comments",
#     "Subscriber count"
# ]

# for field in required_fields:

#     st.write(
#         f"• {field}"
#     )

# # --------------------------------------------------------
# # PHASE 31 DATASET TARGET
# # --------------------------------------------------------

# st.subheader(
#     "🎯 Phase 31 Dataset Target"
# )

# st.info(
#     "For meaningful channel-specific modeling, collect "
#     "a sufficiently large historical set from the target "
#     "channel or comparable channel data. Phase 32 should "
#     "only train when the dataset contains enough records "
#     "and meaningful variation in performance."
# )

# # ============================================================
# # PHASE 32 — CHANNEL-SPECIFIC PERFORMANCE PREDICTION
# # ============================================================

# st.divider()

# st.header(
#     "🔮 Phase 32 — Channel Performance Prediction"
# )

# st.write(
#     "Predict the expected performance category of "
#     "the current video using historical YouTube "
#     "performance data."
# )


# # ------------------------------------------------------------
# # LOAD HISTORICAL DATA
# # ------------------------------------------------------------

# try:

#     historical_records = load_dataset()

# except Exception:

#     historical_records = []


# # ------------------------------------------------------------
# # GET EXISTING ANALYSIS RESULTS
# # ------------------------------------------------------------

# title_results = st.session_state.get(
#     "title_results",
#     {}
# )

# thumbnail_results = st.session_state.get(
#     "thumbnail_results",
#     {}
# )

# hook_results = st.session_state.get(
#     "hook_results",
#     {}
# )

# story_results = st.session_state.get(
#     "story_results",
#     {}
# )

# retention_results = st.session_state.get(
#     "retention_results",
#     {}
# )

# audience_results = st.session_state.get(
#     "audience_response_results",
#     {}
# )

# attention_results = st.session_state.get(
#     "attention_results",
#     {}
# )


# # ------------------------------------------------------------
# # SAFE SCORE EXTRACTION
# # ------------------------------------------------------------

# def get_result_score(result, default=50):

#     if not isinstance(result, dict):

#         return default

#     possible_keys = [
#         "score",
#         "title_score",
#         "thumbnail_score",
#         "hook_score",
#         "story_score",
#         "retention_score",
#         "audience_score",
#         "attention_score",
#         "overall_score"
#     ]

#     for key in possible_keys:

#         value = result.get(key)

#         if isinstance(
#             value,
#             (int, float)
#         ):

#             return float(value)

#     return default


# title_score = get_result_score(
#     title_results
# )

# thumbnail_score = get_result_score(
#     thumbnail_results
# )

# hook_score = get_result_score(
#     hook_results
# )

# story_score = get_result_score(
#     story_results
# )

# retention_score = get_result_score(
#     retention_results
# )

# audience_score = get_result_score(
#     audience_results
# )

# attention_score = get_result_score(
#     attention_results
# )


# # ------------------------------------------------------------
# # CURRENT VIDEO DURATION
# # ------------------------------------------------------------

# current_duration = 0

# try:

#     current_duration = float(
#         duration
#     )

# except:

#     current_duration = 0


# # ------------------------------------------------------------
# # DATASET STATUS
# # ------------------------------------------------------------

# if not historical_records:

#     st.warning(
#         "No historical dataset records are available. "
#         "Complete Phase 31 dataset setup first."
#     )

# else:

#     st.success(
#         f"✅ {len(historical_records)} "
#         "historical video records available."
#     )


# # ------------------------------------------------------------
# # PREDICTION BUTTON
# # ------------------------------------------------------------

# if st.button(
#     "🔮 Predict Channel Performance",
#     type="primary"
# ):

#     if len(historical_records) < 5:

#         st.error(
#             "At least 5 historical videos are "
#             "required before prediction."
#         )

#     else:

#         with st.spinner(
#             "Comparing the current video "
#             "with historical channel performance..."
#         ):

#             prediction_results = analyze_prediction(

#                 records=historical_records,

#                 duration=current_duration,

#                 title_score=title_score,

#                 thumbnail_score=thumbnail_score,

#                 hook_score=hook_score,

#                 story_score=story_score,

#                 retention_score=retention_score,

#                 audience_score=audience_score,

#                 attention_score=attention_score
#             )


#         st.session_state[
#             "prediction_results"
#         ] = prediction_results


# # ------------------------------------------------------------
# # DISPLAY RESULTS
# # ------------------------------------------------------------

# prediction_results = st.session_state.get(
#     "prediction_results"
# )


# if prediction_results:

#     st.divider()

#     st.subheader(
#         "📈 Channel Prediction"
#     )

#     prediction = prediction_results[
#         "prediction"
#     ]

#     confidence = prediction_results[
#         "confidence"
#     ]

#     probabilities = prediction_results[
#         "probabilities"
#     ]


#     # --------------------------------------------------------
#     # MAIN METRICS
#     # --------------------------------------------------------

#     col1, col2, col3, col4 = st.columns(4)

#     with col1:

#         st.metric(
#             "Predicted Performance",
#             prediction.upper()
#         )

#     with col2:

#         st.metric(
#             "Confidence",
#             f"{confidence:.1f}%"
#         )

#     with col3:

#         st.metric(
#             "Historical Videos",
#             prediction_results[
#                 "training_records"
#             ]
#         )

#     with col4:

#         st.metric(
#             "Prediction Status",
#             "Ready"
#         )


#     # --------------------------------------------------------
#     # PROBABILITIES
#     # --------------------------------------------------------

#     st.subheader(
#         "📊 Performance Probability"
#     )

#     probability_data = {

#         "Low":
#             probabilities.get(
#                 "low",
#                 0
#             ),

#         "Medium":
#             probabilities.get(
#                 "medium",
#                 0
#             ),

#         "High":
#             probabilities.get(
#                 "high",
#                 0
#             )
#     }

#     st.bar_chart(
#         probability_data
#     )


#     # --------------------------------------------------------
#     # EXPLANATION
#     # --------------------------------------------------------

#     st.subheader(
#         "🧠 Prediction Explanation"
#     )

#     for reason in prediction_results[
#         "explanation"
#     ]:

#         st.info(
#             reason
#         )


#     # --------------------------------------------------------
#     # SIMILAR HISTORICAL VIDEOS
#     # --------------------------------------------------------

#     st.subheader(
#         "🔎 Most Similar Historical Videos"
#     )

#     similar_videos = prediction_results[
#         "similar_videos"
#     ]

#     if similar_videos:

#         st.dataframe(
#             similar_videos,
#             width="stretch"
#         )

#     else:

#         st.info(
#             "No similar historical videos found."
#         )


#     # --------------------------------------------------------
#     # ANALYSIS INPUTS
#     # --------------------------------------------------------

#     st.subheader(
#         "⚙️ Prediction Inputs"
#     )

#     input_data = {

#         "Title Score":
#             round(
#                 title_score,
#                 1
#             ),

#         "Thumbnail Score":
#             round(
#                 thumbnail_score,
#                 1
#             ),

#         "Hook Score":
#             round(
#                 hook_score,
#                 1
#             ),

#         "Story Score":
#             round(
#                 story_score,
#                 1
#             ),

#         "Retention Score":
#             round(
#                 retention_score,
#                 1
#             ),

#         "Audience Score":
#             round(
#                 audience_score,
#                 1
#             ),

#         "Attention Score":
#             round(
#                 attention_score,
#                 1
#             ),

#         "Duration":
#             round(
#                 current_duration,
#                 1
#             )
#     }

#     st.dataframe(
#         input_data,
#         width="stretch"
#     )


#     st.success(
#         "✅ Phase 32 channel-specific "
#         "prediction engine completed."
#     )

#     # ========================================================
#     # COMBINED ANALYSIS TIMELINE
#     # ========================================================

# scenes = st.session_state.get(
#         "scenes",
#         []
#     )

# transcript_segments = st.session_state.get(
#         "transcript_segments",
#         []
#     )


# if scenes or transcript_segments:

#         st.divider()

#         st.subheader(
#             "🧠 Combined Video Timeline"
#         )

#         st.write(
#             "This is the foundation of the AI "
#             "analysis pipeline. It combines "
#             "visual scene changes and spoken "
#             "content according to their timestamps."
#         )


#         # ====================================================
#         # TIMELINE EVENTS
#         # ====================================================

#         timeline_events = []


#         # Add scene events

#         for scene in scenes:

#             timeline_events.append(
#                 {
#                     "time": scene["timestamp"],
#                     "type": "🎬 Scene Change",
#                     "description": (
#                         f"Visual change score: "
#                         f"{scene['change_score']}"
#                     )
#                 }
#             )


#         # Add transcript events

#         for segment in transcript_segments:

#             timeline_events.append(
#                 {
#                     "time": segment["start"],
#                     "type": "🗣️ Speech",
#                     "description": segment["text"]
#                 }
#             )


#         # Sort by timestamp

#         timeline_events.sort(
#             key=lambda x: x["time"]
#         )


#         # ====================================================
#         # DISPLAY EVENTS
#         # ====================================================

#         for event in timeline_events:

#             event_time = event["time"]

#             event_type = event["type"]

#             description = event["description"]


#             if duration > 0:

#                 progress_value = (
#                     event_time / duration
#                 )

#             else:

#                 progress_value = 0


#             progress_value = max(
#                 0,
#                 min(
#                     progress_value,
#                     1
#                 )
#             )


#             st.progress(
#                 progress_value
#             )


#             col1, col2, col3 = st.columns(
#                 [1, 1.5, 5]
#             )


#             with col1:

#                 st.write(
#                     f"**{event_time:.2f}s**"
#                 )


#             with col2:

#                 st.write(
#                     f"**{event_type}**"
#                 )


#             with col3:

#                 st.write(
#                     description
#                 )


#     # ========================================================
#     # CLEANUP
#     # ========================================================

# try:

#         os.remove(
#             video_path
#         )

# except:

#         pass


# if thumbnail_path is not None:
#         try:
#             os.remove(thumbnail_path)
#         except:
#             pass    

