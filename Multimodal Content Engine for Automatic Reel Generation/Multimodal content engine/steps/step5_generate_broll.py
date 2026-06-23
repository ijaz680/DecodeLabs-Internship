"""
============================================================
 STEP 5 — Generate B-roll Images Using Hugging Face (Free)
============================================================
 Tool   : Hugging Face Inference API
          Model: stabilityai/stable-diffusion-xl-base-1.0
 Cost   : FREE (free inference tier)
 Input  : output/reels_content.json
 Output : output/broll/reel_1_shot_1.png ... etc
============================================================
"""

import os
import json
import sys
import time
import requests
from dotenv import load_dotenv

load_dotenv()

# Hugging Face model to use for image generation
HF_MODEL_URL = (
    "https://api-inference.huggingface.co/models/"
    "stabilityai/stable-diffusion-xl-base-1.0"
)


def load_reels_content(path: str = "output/reels_content.json") -> list:
    """Load the generated content from step 3."""
    if not os.path.exists(path):
        print(f"[ERROR] Content file not found: {path}")
        print("        Run step3_generate_content.py first!")
        sys.exit(1)

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_image(prompt: str, output_path: str, hf_token: str) -> bool:
    """
    Calls Hugging Face Inference API to generate one image.
    Returns True on success, False on failure.
    """
    headers = {"Authorization": f"Bearer {hf_token}"}

    # Enhance the prompt for better quality
    enhanced_prompt = (
        f"{prompt}, "
        "professional photography, high quality, 4K, "
        "cinematic lighting, sharp focus, detailed"
    )

    payload = {
        "inputs": enhanced_prompt,
        "parameters": {
            "width":  768,
            "height": 1344,   # Vertical 9:16 ratio for Reels
            "num_inference_steps": 30,
            "guidance_scale": 7.5
        }
    }

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.post(
                HF_MODEL_URL,
                headers=headers,
                json=payload,
                timeout=120
            )

            if response.status_code == 200:
                # Save the image bytes
                with open(output_path, "wb") as f:
                    f.write(response.content)
                return True

            elif response.status_code == 503:
                # Model is loading — wait and retry
                wait = 20 + (attempt * 10)
                print(f"    [WAIT] Model loading... retrying in {wait}s "
                      f"(attempt {attempt+1}/{max_retries})")
                time.sleep(wait)

            elif response.status_code == 429:
                # Rate limited — wait longer
                print(f"    [WAIT] Rate limited... waiting 30s")
                time.sleep(30)

            else:
                print(f"    [ERROR] HTTP {response.status_code}: {response.text[:100]}")
                return False

        except requests.exceptions.Timeout:
            print(f"    [WARN] Request timed out (attempt {attempt+1}/{max_retries})")
            time.sleep(10)
        except Exception as e:
            print(f"    [ERROR] Request failed: {e}")
            return False

    return False


def main():
    hf_token = os.getenv("HF_API_KEY")
    if not hf_token or hf_token == "your_huggingface_token_here":
        print("[ERROR] HF_API_KEY not set in your .env file.")
        print("        Sign up free at https://huggingface.co")
        print("        Then go to Settings → Access Tokens → New Token")
        sys.exit(1)

    reels = load_reels_content()
    os.makedirs("output/broll", exist_ok=True)

    total_shots = sum(len(r.get("broll_shots", [])) for r in reels)
    print(f"[INFO]  Generating {total_shots} B-roll images for {len(reels)} reels")
    print("[INFO]  Each image takes ~20-40 seconds on free tier\n")

    generated = 0

    for reel in reels:
        num   = reel.get("segment_number", "?")
        shots = reel.get("broll_shots", [])

        print(f"  [Reel {num}] {reel.get('viral_headline', '')[:50]}")

        for i, shot_prompt in enumerate(shots, start=1):
            output_path = f"output/broll/reel_{num}_shot_{i}.png"

            # Skip if already generated
            if os.path.exists(output_path):
                print(f"    Shot {i}: Already exists — skipping")
                generated += 1
                continue

            print(f"    Shot {i}: Generating...")
            print(f"    Prompt: {shot_prompt[:70]}...")

            ok = generate_image(shot_prompt, output_path, hf_token)

            if ok:
                size_kb = os.path.getsize(output_path) / 1024
                print(f"    [✓] Saved → {output_path}  ({size_kb:.0f} KB)")
                generated += 1
            else:
                print(f"    [✗] Failed to generate shot {i}")

            # Pause between requests to avoid rate limiting
            time.sleep(3)

        print()

    print(f"[DONE]  {generated}/{total_shots} B-roll images saved to output/broll/")
    print("[✓] Step 5 complete. Run step6_generate_report.py next.")


if __name__ == "__main__":
    main()
