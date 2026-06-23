# 🎬 Multimodal Content Engine
### Turn a 10-minute video into 5 viral Reels — 100% FREE

> **Built for students.** No credit card. No paid APIs. Just free tools.

---

## 📋 Table of Contents
1. [What This Does](#what-this-does)
2. [Tools Used (All Free)](#tools-used-all-free)
3. [Folder Structure](#folder-structure)
4. [Setup — Step by Step](#setup--step-by-step)
5. [How to Run](#how-to-run)
6. [Output Files](#output-files)
7. [Troubleshooting](#troubleshooting)

---

## What This Does

You give it a video. It automatically:

1. **Transcribes** the entire video with Whisper (runs offline on your PC)
2. **Finds** the 5 most viral-worthy moments using Llama 3 AI
3. **Generates** Instagram captions, TikTok captions, viral headlines, and B-roll descriptions for each moment
4. **Cuts** 5 short video clips at the right timestamps
5. **Creates** 15 B-roll images using Stable Diffusion (free on Hugging Face)
6. **Produces** a final Markdown report with everything packaged together

---

## Tools Used (All Free)

| Step | Tool | Why Free |
|------|------|----------|
| Transcription | **Whisper** (local) | Open-source, runs on your PC, no internet needed |
| AI Analysis | **Groq + Llama 3.3 70B** | Free tier: 14,400 requests/day |
| Video Editing | **MoviePy** | Open-source Python library |
| B-roll Images | **Hugging Face** Stable Diffusion | Free inference API |
| Report | **Pure Python** | No API at all |

**Total cost: $0**

---

## Folder Structure

After cloning/downloading, your project should look like this:

```
multimodal-content-engine/
│
├── main.py                    ← Run the FULL pipeline (all 6 steps)
├── requirements.txt           ← Python packages to install
├── .env.example               ← Copy this to .env and add your keys
├── README.md                  ← This file
│
├── steps/                     ← Each step as a separate script
│   ├── step1_transcribe.py
│   ├── step2_find_segments.py
│   ├── step3_generate_content.py
│   ├── step4_cut_clips.py
│   ├── step5_generate_broll.py
│   └── step6_generate_report.py
│
└── output/                    ← All generated files appear here
    ├── transcript.txt
    ├── segments.json
    ├── viral_segments.json
    ├── reels_content.json
    ├── clips/
    │   ├── reel_1.mp4
    │   ├── reel_2.mp4
    │   ├── reel_3.mp4
    │   ├── reel_4.mp4
    │   └── reel_5.mp4
    ├── broll/
    │   ├── reel_1_shot_1.png
    │   ├── reel_1_shot_2.png
    │   └── ... (15 images total)
    └── reports/
        └── reels_report.md
```

---

## Setup — Step by Step

### Step A — Get Your Free API Keys

#### 1. Groq API Key (replaces GPT-4o)
1. Go to **[console.groq.com](https://console.groq.com)**
2. Click **Sign Up** (it's free, no credit card)
3. In the dashboard, click **API Keys** in the left sidebar
4. Click **Create API Key**
5. Give it a name like `content-engine`
6. **Copy the key** — you won't see it again!

#### 2. Hugging Face Token (replaces Runway)
1. Go to **[huggingface.co](https://huggingface.co)**
2. Click **Sign Up** (free)
3. Go to **Settings → Access Tokens**
4. Click **New Token**
5. Name it `content-engine`, set role to **Read**
6. **Copy the token**

---

### Step B — Set Up the Project on Your Computer

#### 1. Make sure Python is installed
```bash
python --version
# Should show Python 3.8 or higher
```
If not, download from [python.org](https://python.org)

#### 2. Download/clone this project
```bash
# If you have git:
git clone https://github.com/yourusername/multimodal-content-engine.git
cd multimodal-content-engine

# Or just download the ZIP and extract it, then open a terminal in the folder
```

#### 3. Create a virtual environment (recommended)
```bash
# Create the virtual environment
python -m venv venv

# Activate it:
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

#### 4. Install all dependencies
```bash
pip install -r requirements.txt
```
> ⚠️ This installs PyTorch (~500MB). It will take a few minutes.

#### 5. Create your .env file
```bash
# On Windows:
copy .env.example .env

# On Mac/Linux:
cp .env.example .env
```

Now open `.env` in any text editor (Notepad, VS Code, etc.) and fill in:
```
GROQ_API_KEY=paste_your_groq_key_here
HF_API_KEY=paste_your_huggingface_token_here
VIDEO_FILE=my_video.mp4
```

#### 6. Add your video
- Copy your 10-minute video into the project folder
- Rename it to `my_video.mp4` (or update `VIDEO_FILE` in `.env`)
- Supported formats: `.mp4`, `.mov`, `.avi`, `.mkv`

---

## How to Run

### Option 1: Run everything at once (recommended)
```bash
python main.py
```
This runs all 6 steps automatically. Total time: ~10-20 minutes.

### Option 2: Run steps one by one (for learning/debugging)
```bash
# Run from the project root folder each time:
python steps/step1_transcribe.py
python steps/step2_find_segments.py
python steps/step3_generate_content.py
python steps/step4_cut_clips.py
python steps/step5_generate_broll.py
python steps/step6_generate_report.py
```

Running steps individually is useful when:
- You want to see what each step does
- A step fails and you need to fix and re-run just that step
- You already have a transcript and want to skip step 1

---

## Output Files

After running, check the `output/` folder:

| File | What it contains |
|------|-----------------|
| `transcript.txt` | Full text of your video |
| `segments.json` | Transcript broken into timestamped chunks |
| `viral_segments.json` | The 5 viral moments chosen by Llama 3 |
| `reels_content.json` | All captions, headlines, B-roll for all 5 reels |
| `clips/reel_1.mp4` – `reel_5.mp4` | The actual cut video clips |
| `broll/reel_1_shot_1.png` etc. | AI-generated B-roll images |
| `reports/reels_report.md` | Full human-readable report of everything |

---

## Troubleshooting

**`ModuleNotFoundError: No module named 'whisper'`**
```bash
pip install openai-whisper
```

**`moviepy` errors about ffmpeg**
```bash
pip install imageio imageio-ffmpeg
python -m imageio_ffmpeg.binaries
```

**Groq API error: `401 Unauthorized`**
- Check your `.env` file — make sure `GROQ_API_KEY` is set correctly
- Make sure there are no spaces around the `=` sign

**Hugging Face returns `503 Service Unavailable`**
- The model is loading — the script waits and retries automatically
- If it keeps failing, try again in 5 minutes

**Whisper is slow**
- Use `"tiny"` model for speed: open `steps/step1_transcribe.py` and change `"base"` to `"tiny"`
- `tiny` = 1 min for 10-min video, lower accuracy
- `medium` = 5 mins for 10-min video, best accuracy

**Video clip timestamps are wrong**
- Whisper estimates timestamps based on audio pace
- You can manually fix `start_time` and `end_time` in `output/viral_segments.json`
- Then re-run only step 4: `python steps/step4_cut_clips.py`

---

## Technologies

- **[Whisper](https://github.com/openai/whisper)** — OpenAI's open-source speech recognition
- **[Groq](https://groq.com)** — Ultra-fast LLM inference (free tier)
- **[Llama 3.3 70B](https://ai.meta.com/llama/)** — Meta's open-source language model
- **[MoviePy](https://zulko.github.io/moviepy/)** — Python video editing library
- **[Stable Diffusion XL](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0)** — Image generation model
- **[Hugging Face](https://huggingface.co)** — Free model hosting and inference API

---

*Built as a student project. Total API cost: $0.*
