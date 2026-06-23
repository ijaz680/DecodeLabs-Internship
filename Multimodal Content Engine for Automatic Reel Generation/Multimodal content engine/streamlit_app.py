"""
============================================================
 MULTIMODAL CONTENT ENGINE — Streamlit UI
============================================================
 Run with:  streamlit run streamlit_app.py
============================================================
"""

import streamlit as st
import os, json, time, tempfile, shutil, requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ── Auto-setup FFmpeg ────────────────────────────────────────
# Add local FFmpeg installation to PATH if it exists
ffmpeg_local = Path(__file__).parent / "ffmpeg-master-latest-win64-gpl" / "bin"
if ffmpeg_local.exists() and str(ffmpeg_local) not in os.environ['PATH']:
    os.environ['PATH'] = f"{ffmpeg_local};{os.environ['PATH']}"

# ── Page config ─────────────────────────────────────────────
st.set_page_config(
    page_title="🎬 Content Engine",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ───────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600;700&display=swap');

/* Root theme */
:root {
    --bg: #0a0a0f;
    --surface: #111118;
    --card: #16161f;
    --border: #2a2a3a;
    --accent: #7c3aed;
    --accent2: #06b6d4;
    --green: #10b981;
    --red: #ef4444;
    --yellow: #f59e0b;
    --text: #e2e8f0;
    --muted: #64748b;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

/* Hide streamlit branding */
#MainMenu, footer, header { visibility: hidden; }

/* Main container */
.block-container {
    padding: 2rem 2.5rem !important;
    max-width: 1200px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] * { color: var(--text) !important; }

/* Hero banner */
.hero {
    background: linear-gradient(135deg, #1e1030 0%, #0f1729 50%, #0a1a1a 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 2.5rem 2rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(124,58,237,0.15) 0%, transparent 70%);
    pointer-events: none;
}
.hero h1 {
    font-family: 'Space Mono', monospace !important;
    font-size: 2.4rem !important;
    font-weight: 700 !important;
    background: linear-gradient(90deg, #a78bfa, #06b6d4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem !important;
}
.hero p { color: var(--muted) !important; font-size: 1rem; margin: 0; }

/* Step cards */
.step-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 0.75rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    transition: border-color 0.2s;
}
.step-card.done   { border-left: 3px solid var(--green); }
.step-card.active { border-left: 3px solid var(--accent); }
.step-card.idle   { border-left: 3px solid var(--border); opacity: 0.6; }
.step-num {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    color: var(--muted);
    min-width: 24px;
}
.step-title { font-weight: 600; font-size: 0.95rem; }
.step-sub   { font-size: 0.8rem; color: var(--muted); }

/* Result cards */
.reel-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1.25rem;
}
.reel-num {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    color: var(--accent2);
    text-transform: uppercase;
    letter-spacing: 0.1em;
}
.reel-headline {
    font-size: 1.2rem;
    font-weight: 700;
    margin: 0.4rem 0 1rem;
    color: var(--text);
}
.badge {
    display: inline-block;
    padding: 0.2rem 0.6rem;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 600;
    margin-right: 0.4rem;
    margin-bottom: 0.4rem;
}
.badge-purple { background: rgba(124,58,237,0.2); color: #a78bfa; }
.badge-cyan   { background: rgba(6,182,212,0.15); color: #67e8f9; }
.badge-green  { background: rgba(16,185,129,0.15); color: #6ee7b7; }

/* Caption box */
.caption-box {
    background: #0d0d16;
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1rem;
    font-size: 0.875rem;
    line-height: 1.6;
    margin: 0.5rem 0;
    white-space: pre-wrap;
}

/* Input styling override */
.stTextInput input, .stTextArea textarea {
    background: var(--card) !important;
    border-color: var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
}
.stSelectbox > div > div {
    background: var(--card) !important;
    border-color: var(--border) !important;
}

/* Button */
.stButton > button {
    background: linear-gradient(135deg, var(--accent), #5b21b6) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    padding: 0.6rem 2rem !important;
    width: 100% !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

/* File uploader */
.stFileUploader { 
    background: var(--card) !important;
    border: 2px dashed var(--border) !important;
    border-radius: 12px !important;
}

/* Progress */
.stProgress > div > div { background: var(--accent) !important; }

/* Expander */
.streamlit-expanderHeader {
    background: var(--card) !important;
    border-radius: 8px !important;
}

/* Metric */
[data-testid="metric-container"] {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1rem;
}

/* Score badge */
.score-badge {
    display: inline-block;
    font-family: 'Space Mono', monospace;
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--accent2);
}
</style>
""", unsafe_allow_html=True)

# ── Session state init ────────────────────────────────────────
for key in ["transcript", "segments", "reels", "clips_done", "broll_done", "step"]:
    if key not in st.session_state:
        st.session_state[key] = None if key != "step" else 0

# ── Sidebar — API Keys ────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:1rem 0 0.5rem'>
        <span style='font-family:Space Mono;font-size:1rem;font-weight:700;
        background:linear-gradient(90deg,#a78bfa,#06b6d4);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent'>
        ⚙️ Configuration
        </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**API Keys** *(stored only in your browser session)*")

    groq_key = st.text_input(
        "Groq API Key (FREE)",
        value=os.getenv("GROQ_API_KEY", ""),
        type="password",
        placeholder="gsk_...",
        help="Get free key at console.groq.com"
    )
    st.caption("🔗 [Get free Groq key](https://console.groq.com) — no card needed")

    hf_key = st.text_input(
        "Hugging Face Token (FREE)",
        value=os.getenv("HF_API_KEY", ""),
        type="password",
        placeholder="hf_...",
        help="Get free token at huggingface.co/settings/tokens"
    )
    st.caption("🔗 [Get free HF token](https://huggingface.co/settings/tokens)")

    st.divider()

    whisper_model = st.selectbox(
        "Whisper Model",
        ["tiny", "base", "small", "medium"],
        index=1,
        help="tiny=fastest, medium=most accurate"
    )

    st.markdown("""
    <div style='background:#0d0d16;border:1px solid #2a2a3a;border-radius:8px;
    padding:0.75rem;font-size:0.78rem;color:#64748b;margin-top:1rem'>
    💡 <b style='color:#a78bfa'>All tools are free</b><br>
    Whisper runs offline.<br>
    Groq: 14,400 requests/day.<br>
    Hugging Face: free inference.
    </div>
    """, unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────
st.markdown("""
<div class='hero'>
    <h1>🎬 Multimodal Content Engine</h1>
    <p>Upload a video → Get 5 viral Reels with captions, headlines & B-roll — 100% free</p>
</div>
""", unsafe_allow_html=True)

# ── Pipeline steps indicator ──────────────────────────────────
step = st.session_state.step
steps_info = [
    ("01", "Upload Video",             "Drop your MP4 here"),
    ("02", "Transcribe with Whisper",  "Offline speech-to-text"),
    ("03", "Find Viral Segments",      "Llama 3 via Groq (free)"),
    ("04", "Generate Content",         "Captions · Headlines · B-roll"),
    ("05", "Cut Video Clips",          "MoviePy — free video editor"),
    ("06", "Generate B-roll Images",   "Stable Diffusion on Hugging Face"),
]

cols = st.columns(3)
for i, (num, title, sub) in enumerate(steps_info):
    state = "done" if step > i else ("active" if step == i else "idle")
    icon  = "✅" if step > i else ("⚡" if step == i else "○")
    cols[i % 3].markdown(f"""
    <div class='step-card {state}'>
        <span class='step-num'>{icon}</span>
        <div>
            <div class='step-title'>{num} · {title}</div>
            <div class='step-sub'>{sub}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
#  STEP 0 — Upload Video
# ═══════════════════════════════════════════════════════════════
st.markdown("### 📁 Step 1 — Upload Your Video")
uploaded = st.file_uploader(
    "Drop a video file (MP4, MOV, AVI, MKV)",
    type=["mp4", "mov", "avi", "mkv"],
    label_visibility="collapsed"
)

if uploaded:
    st.success(f"✅ Video loaded: **{uploaded.name}** ({uploaded.size / 1_000_000:.1f} MB)")
    # Save to temp file
    if "video_path" not in st.session_state or st.session_state.get("video_name") != uploaded.name:
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded.name).suffix) as tmp:
            tmp.write(uploaded.read())
            st.session_state.video_path = tmp.name
            st.session_state.video_name = uploaded.name
        st.session_state.step = 1

# ═══════════════════════════════════════════════════════════════
#  STEP 1 — TRANSCRIBE
# ═══════════════════════════════════════════════════════════════
if st.session_state.step >= 1:
    st.divider()
    st.markdown("### 🎙️ Step 2 — Transcribe with Whisper")

    col1, col2 = st.columns([3, 1])
    with col1:
        st.info(f"🔇 Whisper runs **offline on your computer** — no API key needed. "
                f"Model: **{whisper_model}**")
    with col2:
        run_transcribe = st.button("▶ Run Transcription", key="btn_transcribe",
                                   disabled=st.session_state.transcript is not None)

    if run_transcribe:
        with st.spinner("Loading Whisper model (downloads once ~140MB)..."):
            try:
                import whisper
                model = whisper.load_model(whisper_model)
            except ImportError:
                st.error("❌ Whisper not installed. Run: `pip install openai-whisper`")
                st.stop()

        progress = st.progress(0, text="Transcribing audio...")
        with st.spinner("Transcribing... this takes 1-3 mins for a 10-min video"):
            try:
                result = model.transcribe(
                    st.session_state.video_path,
                    verbose=False,
                    language="en"
                )
                st.session_state.transcript = result["text"]
                st.session_state.segments_raw = result["segments"]
                progress.progress(100, text="Transcription complete!")
                st.session_state.step = 2
                st.rerun()
            except FileNotFoundError as e:
                st.error("❌ **FFmpeg not found!** Whisper needs FFmpeg to extract audio from video.")
                st.info("""
                ### How to install FFmpeg on Windows:

                **Option 1: Using Windows Package Manager (Recommended)**
                ```powershell
                winget install FFmpeg
                ```
                Then restart your terminal and Streamlit app.

                **Option 2: Download Manually**
                1. Download from: https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip
                2. Extract to a folder (e.g., `C:\\ffmpeg`)
                3. Add the `bin` folder to your system PATH
                4. Restart your computer or terminal

                **Option 3: Using Chocolatey**
                ```powershell
                choco install ffmpeg
                ```

                After installation, verify with: `ffmpeg -version` in PowerShell
                """)
                st.stop()
            except Exception as e:
                st.error(f"❌ Transcription error: {str(e)}")
                st.stop()

    if st.session_state.transcript:
        with st.expander("📄 View Full Transcript", expanded=False):
            st.text_area("Transcript", st.session_state.transcript,
                         height=200, label_visibility="collapsed")
        st.success(f"✅ Transcript ready — {len(st.session_state.transcript.split())} words")

# ═══════════════════════════════════════════════════════════════
#  STEP 2 — FIND VIRAL SEGMENTS
# ═══════════════════════════════════════════════════════════════
if st.session_state.step >= 2:
    st.divider()
    st.markdown("### 🔥 Step 3 — Find 5 Viral Segments")
    st.info("Using **Llama 3.3 70B** via Groq (free) to identify the best moments")

    run_segments = st.button("▶ Find Viral Segments", key="btn_segments",
                             disabled=st.session_state.segments is not None)

    if run_segments:
        if not groq_key or groq_key == "your_groq_api_key_here":
            st.error("❌ Enter your Groq API key in the sidebar first!")
            st.stop()

        try:
            from groq import Groq
        except ImportError:
            st.error("❌ Groq not installed. Run: `pip install groq`")
            st.stop()

        client = Groq(api_key=groq_key)
        transcript = st.session_state.transcript

        with st.spinner("Llama 3 is analysing your transcript..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "Return only valid JSON. No markdown, no backticks."},
                        {"role": "user", "content": f"""Find the 5 most viral-worthy moments in this transcript.
Return a JSON array with these fields per segment:
- segment_number (1-5)
- start_time (seconds, estimate from position)
- end_time (start_time + 30 to 60)
- segment_text (exact words)
- why_viral (1 sentence)
- hook_line (most grabbing sentence)
- emotion (e.g. curiosity, surprise, inspiration)
- viral_score (1-10)

TRANSCRIPT:
{transcript}

Return ONLY a JSON array starting with [ and ending with ]"""}
                    ],
                    temperature=0.7, max_tokens=3000
                )
                raw = response.choices[0].message.content.strip()
                if raw.startswith("```"):
                    raw = raw.split("```")[1]
                    if raw.startswith("json"): raw = raw[4:]
                raw = raw.strip()
                st.session_state.segments = json.loads(raw)
                st.session_state.step = 3
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error: {e}")

    if st.session_state.segments:
        segs = st.session_state.segments
        st.success(f"✅ Found {len(segs)} viral segments!")

        for seg in segs:
            score = seg.get("viral_score", "?")
            bar_color = "#10b981" if score >= 8 else ("#f59e0b" if score >= 6 else "#ef4444")
            st.markdown(f"""
            <div class='reel-card'>
                <div class='reel-num'>SEGMENT {seg.get('segment_number','?')}</div>
                <div style='display:flex;align-items:center;gap:0.75rem;margin:0.3rem 0'>
                    <span class='score-badge'>{score}/10</span>
                    <span class='badge badge-purple'>{seg.get('emotion','')}</span>
                    <span class='badge badge-cyan'>
                        {seg.get('start_time',0):.0f}s – {seg.get('end_time',0):.0f}s
                    </span>
                </div>
                <div class='reel-headline'>"{seg.get('hook_line','')}"</div>
                <div style='font-size:0.8rem;color:#64748b'>{seg.get('why_viral','')}</div>
            </div>
            """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
#  STEP 3 — GENERATE CONTENT
# ═══════════════════════════════════════════════════════════════
if st.session_state.step >= 3:
    st.divider()
    st.markdown("### ✍️ Step 4 — Generate Captions & Headlines")
    st.info("Generating Instagram captions, TikTok captions, viral headlines & B-roll descriptions")

    run_content = st.button("▶ Generate All Content", key="btn_content",
                            disabled=st.session_state.reels is not None)

    if run_content:
        if not groq_key:
            st.error("❌ Enter your Groq API key in the sidebar!")
            st.stop()

        from groq import Groq
        client = Groq(api_key=groq_key)
        segs = st.session_state.segments
        all_reels = []
        progress = st.progress(0, text="Generating content...")

        for i, seg in enumerate(segs):
            progress.progress((i / len(segs)), text=f"Writing content for segment {i+1}/{len(segs)}...")
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "Return only valid JSON. No markdown, no backticks."},
                        {"role": "user", "content": f"""Create social media content for this video clip.
CLIP TEXT: "{seg.get('segment_text','')}"
HOOK LINE: "{seg.get('hook_line','')}"
EMOTION: {seg.get('emotion','')}

Return a JSON object with:
- viral_headline (punchy title, max 10 words)
- instagram_caption (3-4 sentences + 5 hashtags + emojis)
- tiktok_caption (1-2 sentences + 3 hashtags)
- youtube_title (search-optimised)
- broll_shots (array of 3 detailed AI image generation prompts, each 1-2 sentences)
- text_overlay (3-5 words to show at start of clip)
- thumbnail_idea (what to show in thumbnail)
- best_post_time (e.g. Tuesday 7pm EST)
- target_audience (1 sentence)"""}
                    ],
                    temperature=0.85, max_tokens=1000
                )
                raw = response.choices[0].message.content.strip()
                if raw.startswith("```"):
                    raw = raw.split("```")[1]
                    if raw.startswith("json"): raw = raw[4:]
                raw = raw.strip()
                content = json.loads(raw)
            except Exception as e:
                content = {
                    "viral_headline": seg.get("hook_line","")[:60],
                    "instagram_caption": seg.get("segment_text","")[:200],
                    "tiktok_caption": seg.get("hook_line",""),
                    "broll_shots": ["Speaker on camera", "Topic B-roll", "Outro"],
                    "error": str(e)
                }

            content["segment_number"] = seg.get("segment_number")
            content["timestamps"] = {"start": seg.get("start_time",0), "end": seg.get("end_time",60)}
            content["hook_line"]   = seg.get("hook_line","")
            content["why_viral"]   = seg.get("why_viral","")
            content["viral_score"] = seg.get("viral_score",0)
            all_reels.append(content)
            time.sleep(0.5)

        progress.progress(100, text="Content generated!")
        st.session_state.reels = all_reels
        st.session_state.step = 4
        st.rerun()

    if st.session_state.reels:
        st.success(f"✅ Content ready for all {len(st.session_state.reels)} Reels!")

        for reel in st.session_state.reels:
            num = reel.get("segment_number","?")
            score = reel.get("viral_score", "?")
            start = reel["timestamps"]["start"]
            end   = reel["timestamps"]["end"]

            with st.expander(f"🎬 Reel {num} — {reel.get('viral_headline','')[:60]}", expanded=(num==1)):
                c1, c2 = st.columns(2)

                with c1:
                    st.markdown(f"""
                    <div style='margin-bottom:0.5rem'>
                        <span class='badge badge-purple'>Score: {score}/10</span>
                        <span class='badge badge-cyan'>{start:.0f}s – {end:.0f}s</span>
                        <span class='badge badge-green'>Reel {num}</span>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown("**🎯 Text Overlay (Start of clip)**")
                    st.code(reel.get("text_overlay", "N/A"))

                    st.markdown("**📱 Instagram Caption**")
                    st.markdown(f"""<div class='caption-box'>{reel.get('instagram_caption','')}</div>""",
                                unsafe_allow_html=True)

                    st.markdown("**🎵 TikTok Caption**")
                    st.markdown(f"""<div class='caption-box'>{reel.get('tiktok_caption','')}</div>""",
                                unsafe_allow_html=True)

                with c2:
                    st.markdown("**▶️ YouTube Shorts Title**")
                    st.code(reel.get("youtube_title","N/A"))

                    st.markdown("**🎞️ B-Roll Shot List**")
                    for j, shot in enumerate(reel.get("broll_shots",[]), 1):
                        st.markdown(f"""<div class='caption-box'><b>Shot {j}:</b> {shot}</div>""",
                                    unsafe_allow_html=True)

                    st.markdown("**🖼️ Thumbnail Idea**")
                    st.markdown(f"""<div class='caption-box'>{reel.get('thumbnail_idea','N/A')}</div>""",
                                unsafe_allow_html=True)

                    st.markdown("**📅 Best Post Time**")
                    st.info(reel.get("best_post_time","N/A"))

# ═══════════════════════════════════════════════════════════════
#  STEP 4 — CUT CLIPS
# ═══════════════════════════════════════════════════════════════
if st.session_state.step >= 4:
    st.divider()
    st.markdown("### ✂️ Step 5 — Cut Video Clips")
    st.info("Cutting 5 clips from your video using MoviePy (free)")

    run_clips = st.button("▶ Cut All Clips", key="btn_clips",
                          disabled=st.session_state.clips_done is True)

    if run_clips:
        try:
            from moviepy import VideoFileClip
        except ImportError:
            st.error("❌ MoviePy not installed. Run: `pip install moviepy`")
            st.stop()

        video_path = st.session_state.video_path
        reels = st.session_state.reels
        clip_paths = []
        progress = st.progress(0, text="Starting clip cutting...")

        os.makedirs("output/clips", exist_ok=True)

        try:
            original = VideoFileClip(video_path)
            duration = original.duration

            for i, reel in enumerate(reels):
                num   = reel.get("segment_number", i+1)
                start = max(0, float(reel["timestamps"]["start"]) - 0.5)
                end   = min(duration, float(reel["timestamps"]["end"]) + 0.5)

                if end <= start: end = min(duration, start + 30)

                progress.progress((i+0.5)/len(reels),
                                  text=f"Cutting Reel {num} ({start:.0f}s–{end:.0f}s)...")

                out_path = f"output/clips/reel_{num}.mp4"
                clip = original.subclipped(start, end)
                clip.write_videofile(out_path, codec="libx264",
                                     audio_codec="aac", fps=30,
                                     logger='bar')
                clip.close()
                clip_paths.append(out_path)
                progress.progress((i+1)/len(reels), text=f"✅ Reel {num} saved!")

            original.close()
            st.session_state.clip_paths = clip_paths
            st.session_state.clips_done = True
            st.session_state.step = 5
            st.rerun()

        except Exception as e:
            st.error(f"❌ Error cutting clips: {e}")

    if st.session_state.clips_done:
        st.success("✅ All clips cut successfully!")
        clips = st.session_state.get("clip_paths", [])
        for path in clips:
            if os.path.exists(path):
                size_mb = os.path.getsize(path) / 1_000_000
                col1, col2 = st.columns([4, 1])
                col1.markdown(f"📹 `{path}`")
                col2.markdown(f"`{size_mb:.1f} MB`")
                with open(path, "rb") as f:
                    st.download_button(
                        f"⬇ Download {os.path.basename(path)}",
                        f.read(),
                        file_name=os.path.basename(path),
                        mime="video/mp4",
                        key=f"dl_{path}"
                    )

# ═══════════════════════════════════════════════════════════════
#  STEP 5 — B-ROLL IMAGES
# ═══════════════════════════════════════════════════════════════
if st.session_state.step >= 5:
    st.divider()
    st.markdown("### 🖼️ Step 6 — Generate B-roll Images (Hugging Face)")
    st.info("Using **Stable Diffusion XL** — free on Hugging Face inference API")

    run_broll = st.button("▶ Generate B-roll Images", key="btn_broll",
                          disabled=st.session_state.broll_done is True)

    if run_broll:
        if not hf_key or hf_key == "your_huggingface_token_here":
            st.error("❌ Enter your Hugging Face token in the sidebar!")
            st.stop()

        reels = st.session_state.reels
        HF_URL = ("https://api-inference.huggingface.co/models/"
                  "stabilityai/stable-diffusion-xl-base-1.0")
        headers = {"Authorization": f"Bearer {hf_key}"}
        os.makedirs("output/broll", exist_ok=True)

        total_shots = sum(len(r.get("broll_shots",[])) for r in reels)
        progress = st.progress(0, text="Generating B-roll images...")
        done = 0
        broll_paths = []

        for reel in reels:
            num   = reel.get("segment_number","?")
            shots = reel.get("broll_shots",[])
            for j, shot in enumerate(shots, 1):
                out_path = f"output/broll/reel_{num}_shot_{j}.png"
                enhanced = f"{shot}, professional photography, 4K, cinematic, sharp focus"

                progress.progress(done/total_shots,
                                  text=f"Reel {num} Shot {j}: {shot[:50]}...")

                for attempt in range(3):
                    try:
                        resp = requests.post(
                            HF_URL, headers=headers,
                            json={"inputs": enhanced,
                                  "parameters": {"width":768,"height":1344}},
                            timeout=120
                        )
                        if resp.status_code == 200:
                            with open(out_path, "wb") as f:
                                f.write(resp.content)
                            broll_paths.append(out_path)
                            break
                        elif resp.status_code == 503:
                            time.sleep(20)
                        else:
                            break
                    except Exception:
                        time.sleep(10)

                done += 1
                time.sleep(2)

        progress.progress(1.0, text="All B-roll images generated!")
        st.session_state.broll_paths = broll_paths
        st.session_state.broll_done = True
        st.session_state.step = 6
        st.rerun()

    if st.session_state.broll_done:
        paths = st.session_state.get("broll_paths", [])
        st.success(f"✅ {len(paths)} B-roll images generated!")

        # Show images in a grid
        existing = [p for p in paths if os.path.exists(p)]
        if existing:
            cols = st.columns(3)
            for i, path in enumerate(existing):
                cols[i % 3].image(path, caption=os.path.basename(path), use_container_width=True)

# ═══════════════════════════════════════════════════════════════
#  FINAL — DOWNLOAD EVERYTHING
# ═══════════════════════════════════════════════════════════════
if st.session_state.step >= 4 and st.session_state.reels:
    st.divider()
    st.markdown("### 📦 Download Your Reels Package")

    # Build JSON report
    reels_json = json.dumps(st.session_state.reels, indent=2, ensure_ascii=False)
    st.download_button(
        "⬇ Download reels_content.json",
        reels_json,
        file_name="reels_content.json",
        mime="application/json"
    )

    if st.session_state.transcript:
        st.download_button(
            "⬇ Download transcript.txt",
            st.session_state.transcript,
            file_name="transcript.txt",
            mime="text/plain"
        )

    # Build markdown report
    if st.session_state.reels:
        lines = ["# 🎬 Reels Report\n"]
        for reel in st.session_state.reels:
            num = reel.get("segment_number","?")
            lines.append(f"## Reel {num} — {reel.get('viral_headline','')}\n")
            lines.append(f"**Timestamps:** {reel['timestamps']['start']:.0f}s – {reel['timestamps']['end']:.0f}s\n")
            lines.append(f"**Viral Score:** {reel.get('viral_score','?')}/10\n")
            lines.append(f"**Instagram Caption:**\n{reel.get('instagram_caption','')}\n")
            lines.append(f"**TikTok Caption:**\n{reel.get('tiktok_caption','')}\n")
            lines.append(f"**YouTube Title:** {reel.get('youtube_title','')}\n")
            lines.append("**B-Roll Shots:**\n")
            for j, shot in enumerate(reel.get("broll_shots",[]),1):
                lines.append(f"- Shot {j}: {shot}\n")
            lines.append("\n---\n")

        st.download_button(
            "⬇ Download reels_report.md",
            "\n".join(lines),
            file_name="reels_report.md",
            mime="text/markdown"
        )

    st.markdown("""
    <div style='background:linear-gradient(135deg,#0f1729,#1e1030);
    border:1px solid #2a2a3a;border-radius:12px;padding:1.5rem;margin-top:1rem;text-align:center'>
        <div style='font-size:2rem'>🎉</div>
        <div style='font-family:Space Mono;font-size:1.1rem;font-weight:700;
        background:linear-gradient(90deg,#a78bfa,#06b6d4);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent'>
        Pipeline Complete!
        </div>
        <div style='color:#64748b;margin-top:0.5rem;font-size:0.875rem'>
        Your 5 Reels are ready. Total cost: $0.00
        </div>
    </div>
    """, unsafe_allow_html=True)
