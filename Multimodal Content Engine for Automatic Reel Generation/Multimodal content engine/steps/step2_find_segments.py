"""
============================================================
 STEP 2 — Find the 5 Most Viral Segments Using Groq + Llama 3
============================================================
 Tool   : Groq API (Free tier) with Llama 3.3 70B model
 Cost   : FREE — 14,400 requests/day on free plan
 Input  : output/transcript.txt
 Output : output/viral_segments.json
============================================================
"""

import os
import json
import sys
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


def load_transcript(path: str = "output/transcript.txt") -> str:
    """Load the transcript text from file."""
    if not os.path.exists(path):
        print(f"[ERROR] Transcript not found: {path}")
        print("        Run step1_transcribe.py first!")
        sys.exit(1)

    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def find_viral_segments(transcript: str) -> list:
    """
    Sends the transcript to Groq + Llama 3 and gets back
    the 5 most viral segments with timestamps.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "your_groq_api_key_here":
        print("[ERROR] GROQ_API_KEY not set in your .env file.")
        print("        Sign up free at https://console.groq.com")
        sys.exit(1)

    client = Groq(api_key=api_key)

    print("[INFO]  Sending transcript to Groq (Llama 3.3 70B)...")
    print("[INFO]  Identifying the 5 most viral segments...")

    system_prompt = """You are an expert viral content strategist with 10 years of 
experience turning long-form videos into viral short-form content.
You always respond with valid JSON only — no markdown, no extra text, no backticks."""

    user_prompt = f"""Analyze this video transcript and identify the 5 most engaging 
moments that would make great standalone 30-60 second Reels or TikTok videos.

Look for:
- Surprising facts or statistics
- Emotional or relatable moments  
- Actionable tips or advice
- Controversial or bold opinions
- Funny or entertaining moments
- Story climaxes or reveals

For each segment, return a JSON array with EXACTLY these fields:
- "segment_number": integer 1 to 5
- "start_time": number in seconds (estimate based on position in transcript)
- "end_time": number in seconds (start_time + 30 to 60 seconds)
- "segment_text": the exact words from that moment (copy directly)
- "why_viral": one sentence explaining why this works as a Reel
- "hook_line": the single most attention-grabbing sentence from this segment
- "emotion": the primary emotion this triggers (e.g. "curiosity", "surprise", "inspiration")
- "viral_score": a score from 1-10 rating viral potential

VIDEO TRANSCRIPT:
{transcript}

Return ONLY a valid JSON array. Start your response with [ and end with ]"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=3000
        )

        raw = response.choices[0].message.content.strip()

        # Clean up in case model adds backticks
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        raw = raw.strip()

        segments = json.loads(raw)
        return segments

    except json.JSONDecodeError as e:
        print(f"[ERROR] Groq returned invalid JSON: {e}")
        print(f"[DEBUG] Raw response:\n{raw}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Groq API call failed: {e}")
        sys.exit(1)


def save_segments(segments: list, output_dir: str = "output") -> None:
    """Save viral segments to JSON file."""
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "viral_segments.json")

    with open(path, "w", encoding="utf-8") as f:
        json.dump(segments, f, indent=2, ensure_ascii=False)

    print(f"\n[DONE]  Viral segments saved → {path}")
    print("\n--- FOUND SEGMENTS ---")
    for seg in segments:
        score = seg.get("viral_score", "?")
        start = seg.get("start_time", 0)
        end   = seg.get("end_time", 0)
        emotion = seg.get("emotion", "")
        print(f"  #{seg['segment_number']} [{start:.0f}s-{end:.0f}s] "
              f"Score: {score}/10  Emotion: {emotion}")
        print(f"     Hook: {seg.get('hook_line', '')[:80]}...")
        print()


def main():
    transcript = load_transcript()
    segments = find_viral_segments(transcript)
    save_segments(segments)
    print("[✓] Step 2 complete. Run step3_generate_content.py next.")


if __name__ == "__main__":
    main()
