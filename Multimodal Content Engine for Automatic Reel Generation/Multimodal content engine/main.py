"""
============================================================
 MULTIMODAL CONTENT ENGINE — main.py
============================================================
 Run the ENTIRE pipeline in one command:
   python main.py

 Or run steps individually:
   python steps/step1_transcribe.py
   python steps/step2_find_segments.py
   python steps/step3_generate_content.py
   python steps/step4_cut_clips.py
   python steps/step5_generate_broll.py
   python steps/step6_generate_report.py
============================================================
"""

import os
import sys
import time
from dotenv import load_dotenv

load_dotenv()

# Add steps folder to path so imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "steps"))


def print_banner():
    print("=" * 60)
    print("  🎬 MULTIMODAL CONTENT ENGINE")
    print("  Turn a 10-min video into 5 viral Reels — FREE")
    print("=" * 60)
    print()


def check_env():
    """Check that required environment variables are set."""
    errors = []

    groq_key = os.getenv("GROQ_API_KEY", "")
    if not groq_key or groq_key == "your_groq_api_key_here":
        errors.append("GROQ_API_KEY is not set in your .env file")

    hf_key = os.getenv("HF_API_KEY", "")
    if not hf_key or hf_key == "your_huggingface_token_here":
        errors.append("HF_API_KEY is not set in your .env file")

    video = os.getenv("VIDEO_FILE", "my_video.mp4")
    if not os.path.exists(video):
        errors.append(
            f"Video file not found: '{video}'\n"
            f"   → Place your video in this folder and set VIDEO_FILE in .env"
        )

    if errors:
        print("[ERROR] Fix these problems before running:\n")
        for i, err in enumerate(errors, 1):
            print(f"  {i}. {err}")
        print()
        print("  See README.md for setup instructions.")
        sys.exit(1)

    print(f"[✓] Video    : {video}")
    print(f"[✓] Groq key : {groq_key[:8]}...")
    print(f"[✓] HF key   : {hf_key[:8]}...")
    print()


def run_step(name: str, func):
    """Run a pipeline step with timing and error handling."""
    print(f"\n{'─'*60}")
    print(f"  RUNNING: {name}")
    print(f"{'─'*60}")
    t0 = time.time()
    try:
        func()
        elapsed = time.time() - t0
        print(f"\n[✓] {name} finished in {elapsed:.1f}s")
    except SystemExit:
        raise
    except Exception as e:
        print(f"\n[ERROR] {name} failed: {e}")
        print("        Fix the error above and re-run this step directly.")
        raise


def main():
    print_banner()
    check_env()

    # Import step modules
    from step1_transcribe     import main as step1
    from step2_find_segments  import main as step2
    from step3_generate_content import main as step3
    from step4_cut_clips      import main as step4
    from step5_generate_broll import main as step5
    from step6_generate_report import main as step6

    pipeline = [
        ("Step 1: Transcribe video with Whisper",          step1),
        ("Step 2: Find viral segments with Llama 3",       step2),
        ("Step 3: Generate captions & headlines",          step3),
        ("Step 4: Cut video clips with MoviePy",           step4),
        ("Step 5: Generate B-roll images (Hugging Face)",  step5),
        ("Step 6: Generate final report",                  step6),
    ]

    total_start = time.time()

    for name, func in pipeline:
        run_step(name, func)

    total = time.time() - total_start
    print(f"\n{'='*60}")
    print(f"  PIPELINE COMPLETE in {total/60:.1f} minutes!")
    print(f"  Check the output/ folder for your 5 Reels.")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
