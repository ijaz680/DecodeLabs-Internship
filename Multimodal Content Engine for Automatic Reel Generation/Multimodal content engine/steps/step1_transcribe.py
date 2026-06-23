"""
============================================================
 STEP 1 — Transcribe Video Using Local Whisper
============================================================
 Tool   : OpenAI Whisper (runs 100% offline on your PC)
 Cost   : FREE — no API key needed
 Input  : your video file (mp4, mov, avi, mkv)
 Output : output/transcript.txt
          output/segments.json  (with timestamps)
============================================================
"""

import whisper
import json
import os
import sys
from dotenv import load_dotenv

load_dotenv()


def transcribe_video(video_path: str) -> dict:
    """
    Transcribes a video file using local Whisper.
    Returns the full result dict with text and segments.
    """
    if not os.path.exists(video_path):
        print(f"[ERROR] Video file not found: {video_path}")
        print("        Make sure your video is in the project folder.")
        sys.exit(1)

    print(f"[INFO]  Loading Whisper model (downloads ~140MB on first run)...")
    # Options: 'tiny', 'base', 'small', 'medium', 'large'
    # 'base' = fast + good enough for most videos
    # 'medium' = slower but more accurate (recommended for noisy audio)
    model = whisper.load_model("base")

    print(f"[INFO]  Transcribing: {video_path}")
    print(f"[INFO]  This takes ~1-3 minutes for a 10-minute video...")

    result = model.transcribe(
        video_path,
        verbose=False,          # set True to see live output
        language="en",          # change to your video language if not English
        task="transcribe"
    )

    return result


def save_outputs(result: dict, output_dir: str = "output") -> None:
    """
    Saves the full transcript text and timestamped segments to files.
    """
    os.makedirs(output_dir, exist_ok=True)

    # --- Save plain text transcript ---
    transcript_path = os.path.join(output_dir, "transcript.txt")
    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(result["text"])
    print(f"[DONE]  Transcript saved → {transcript_path}")

    # --- Save segments with timestamps ---
    # Each segment looks like:
    # { "id": 0, "start": 0.0, "end": 4.5, "text": "Hello everyone..." }
    segments_path = os.path.join(output_dir, "segments.json")
    with open(segments_path, "w", encoding="utf-8") as f:
        json.dump(result["segments"], f, indent=2, ensure_ascii=False)
    print(f"[DONE]  Segments saved → {segments_path}")

    # --- Print a preview ---
    print("\n--- TRANSCRIPT PREVIEW (first 500 chars) ---")
    print(result["text"][:500])
    print("...")
    print(f"\n[INFO]  Total segments: {len(result['segments'])}")


def main():
    video_file = os.getenv("VIDEO_FILE", "my_video.mp4")
    result = transcribe_video(video_file)
    save_outputs(result)
    print("\n[✓] Step 1 complete. Run step2_find_segments.py next.")


if __name__ == "__main__":
    main()
