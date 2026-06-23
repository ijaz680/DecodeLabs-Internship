"""
============================================================
 STEP 4 — Cut Video into 5 Reels Using MoviePy
============================================================
 Tool   : MoviePy (100% free, open source)
 Cost   : FREE
 Input  : output/reels_content.json  +  your original video
 Output : output/clips/reel_1.mp4 ... reel_5.mp4
============================================================
"""

import os
import json
import sys
from dotenv import load_dotenv

load_dotenv()


def load_reels_content(path: str = "output/reels_content.json") -> list:
    """Load the generated content from step 3."""
    if not os.path.exists(path):
        print(f"[ERROR] Content file not found: {path}")
        print("        Run step3_generate_content.py first!")
        sys.exit(1)

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def cut_clip(video_path: str, start: float, end: float, output_path: str) -> bool:
    """
    Cuts a clip from the video between start and end seconds.
    Returns True on success, False on failure.
    """
    try:
        from moviepy import VideoFileClip

        with VideoFileClip(video_path) as video:
            duration = video.duration

            # Validate timestamps
            start = max(0.0, float(start))
            end   = min(duration, float(end))

            if start >= end:
                print(f"  [WARN] Invalid timestamps {start}s-{end}s — skipping")
                return False

            if end - start < 5:
                print(f"  [WARN] Clip is very short ({end-start:.1f}s) — extending to 30s")
                end = min(duration, start + 30)

            # Add a small buffer on each side for smooth cuts
            buffered_start = max(0.0, start - 0.5)
            buffered_end   = min(duration, end + 0.5)

            clip = video.subclipped(buffered_start, buffered_end)
            clip.write_videofile(
                output_path,
                codec="libx264",
                audio_codec="aac",
                fps=30,
                logger='bar'
            )
            clip.close()
        return True

    except Exception as e:
        print(f"  [ERROR] Failed to cut clip: {e}")
        return False


def main():
    video_file = os.getenv("VIDEO_FILE", "my_video.mp4")

    if not os.path.exists(video_file):
        print(f"[ERROR] Video file not found: {video_file}")
        print(f"        Make sure '{video_file}' is in the project folder.")
        print("        Or update VIDEO_FILE in your .env file.")
        sys.exit(1)

    reels = load_reels_content()
    os.makedirs("output/clips", exist_ok=True)

    print(f"[INFO]  Cutting {len(reels)} clips from: {video_file}")
    print("[INFO]  This may take a few minutes...\n")

    success_count = 0

    for reel in reels:
        num   = reel.get("segment_number", "?")
        start = reel["timestamps"]["start"]
        end   = reel["timestamps"]["end"]
        title = reel.get("viral_headline", f"Reel {num}")[:40]

        output_path = f"output/clips/reel_{num}.mp4"

        print(f"  [→] Reel {num}: Cutting {start:.0f}s – {end:.0f}s")
        print(f"       Title: {title}")

        ok = cut_clip(video_file, start, end, output_path)

        if ok:
            size_mb = os.path.getsize(output_path) / (1024 * 1024)
            print(f"  [✓] Saved → {output_path}  ({size_mb:.1f} MB)\n")
            success_count += 1
        else:
            print(f"  [✗] Failed to cut Reel {num}\n")

    print(f"[DONE]  {success_count}/{len(reels)} clips saved to output/clips/")
    print("[✓] Step 4 complete. Run step5_generate_broll.py next.")


if __name__ == "__main__":
    main()
