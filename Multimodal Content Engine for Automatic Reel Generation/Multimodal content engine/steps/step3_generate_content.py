"""
============================================================
 STEP 3 — Generate Captions, Headlines & B-roll Descriptions
============================================================
 Tool   : Groq API (Free tier) with Llama 3.3 70B model
 Cost   : FREE
 Input  : output/viral_segments.json
 Output : output/reels_content.json
============================================================
"""

import os
import json
import sys
import time
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


def load_segments(path: str = "output/viral_segments.json") -> list:
    """Load viral segments from file."""
    if not os.path.exists(path):
        print(f"[ERROR] Segments file not found: {path}")
        print("        Run step2_find_segments.py first!")
        sys.exit(1)

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_content_for_segment(client: Groq, segment: dict) -> dict:
    """
    Generates all social media content for one segment.
    Returns a dict with headline, captions, B-roll shots, etc.
    """
    segment_text = segment.get("segment_text", "")
    hook_line    = segment.get("hook_line", "")
    emotion      = segment.get("emotion", "")

    system_prompt = """You are a top-tier social media content creator who has 
helped creators grow from 0 to 1 million followers.
You understand what makes content go viral on Instagram Reels and TikTok.
Always respond with valid JSON only — no markdown, no extra text, no backticks."""

    user_prompt = f"""Create complete social media content for this video clip.

CLIP TEXT: "{segment_text}"
HOOK LINE: "{hook_line}"
PRIMARY EMOTION: {emotion}

Return a JSON object with EXACTLY these fields:

"viral_headline": A punchy title for this Reel (max 10 words, 
  use power words, no boring words like "tips" or "things")

"instagram_caption": A full Instagram caption (3-4 sentences that 
  expand on the hook, tell a mini-story, add value) + line break + 
  5 relevant hashtags + a call to action at the end. Use 2-3 emojis naturally.

"tiktok_caption": Short punchy TikTok caption (max 2 sentences) + 
  3 hashtags. Hook readers in the first 5 words.

"youtube_title": A YouTube Shorts title optimized for search + clicks

"broll_shots": An array of exactly 3 B-roll shot descriptions. 
  Each must be a detailed AI video/image generation prompt, for example:
  "Slow motion close-up of hands typing on a MacBook in a dimly lit cafe, 
  warm bokeh lights in background, cinematic color grade, 4K quality"

"text_overlay": A 3-5 word phrase to show as text overlay at the start 
  of the Reel (like a title card that appears in the first 2 seconds)

"thumbnail_idea": Description of the ideal thumbnail for this Reel 
  (what to show, colors, text overlay, facial expression if person)

"best_post_time": Best time to post this type of content (e.g. "Tuesday 7pm EST")

"target_audience": Who will relate to this content most (1 sentence)"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_prompt}
            ],
            temperature=0.85,
            max_tokens=1200
        )

        raw = response.choices[0].message.content.strip()

        # Clean up in case model adds backticks
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        raw = raw.strip()

        content = json.loads(raw)

        # Add the original segment info to the output
        content["segment_number"]  = segment.get("segment_number")
        content["timestamps"]      = {
            "start": segment.get("start_time", 0),
            "end":   segment.get("end_time", 60)
        }
        content["hook_line"]       = hook_line
        content["why_viral"]       = segment.get("why_viral", "")
        content["viral_score"]     = segment.get("viral_score", 0)
        content["segment_text"]    = segment_text

        return content

    except json.JSONDecodeError as e:
        print(f"  [WARN] JSON parse error for segment {segment.get('segment_number')}: {e}")
        print(f"  [DEBUG] Raw: {raw[:200]}")
        # Return a minimal fallback so the pipeline doesn't crash
        return {
            "segment_number": segment.get("segment_number"),
            "timestamps": {"start": segment.get("start_time", 0), "end": segment.get("end_time", 60)},
            "viral_headline": hook_line[:60],
            "instagram_caption": segment_text[:300],
            "tiktok_caption": hook_line,
            "broll_shots": ["Close-up of speaker talking to camera", "B-roll of topic", "Outro screen"],
            "error": str(e)
        }


def main():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "your_groq_api_key_here":
        print("[ERROR] GROQ_API_KEY not set in your .env file.")
        sys.exit(1)

    client = Groq(api_key=api_key)
    segments = load_segments()

    print(f"[INFO]  Generating content for {len(segments)} segments...")
    print("[INFO]  This makes 5 API calls — takes about 30 seconds\n")

    all_reels = []

    for seg in segments:
        num = seg.get("segment_number", "?")
        print(f"  [→] Segment {num}: Generating content...")

        content = generate_content_for_segment(client, seg)
        all_reels.append(content)

        print(f"  [✓] Segment {num}: Done! Headline: {content.get('viral_headline', '')[:60]}")

        # Small delay to be polite to the free API
        time.sleep(1)

    # Save all content
    os.makedirs("output", exist_ok=True)
    output_path = "output/reels_content.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_reels, f, indent=2, ensure_ascii=False)

    print(f"\n[DONE]  All content saved → {output_path}")
    print("[✓] Step 3 complete. Run step4_cut_clips.py next.")


if __name__ == "__main__":
    main()
