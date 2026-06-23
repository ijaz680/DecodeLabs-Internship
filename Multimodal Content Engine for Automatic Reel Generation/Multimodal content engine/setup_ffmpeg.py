#!/usr/bin/env python3
"""
Setup script to add FFmpeg to system PATH permanently
Run this once to configure FFmpeg for Whisper
"""

import os
import sys
import subprocess
from pathlib import Path

def add_ffmpeg_to_path():
    """Add local FFmpeg installation to system PATH"""
    
    # Get the project directory
    project_dir = Path(__file__).parent
    ffmpeg_bin = project_dir / "ffmpeg-master-latest-win64-gpl" / "bin"
    
    if not ffmpeg_bin.exists():
        print("❌ FFmpeg directory not found!")
        print(f"   Expected: {ffmpeg_bin}")
        return False
    
    print(f"✅ Found FFmpeg at: {ffmpeg_bin}")
    
    # Add to current environment
    os.environ['PATH'] = f"{ffmpeg_bin};{os.environ['PATH']}"
    
    # Verify it works
    try:
        result = subprocess.run(["ffmpeg", "-version"], 
                              capture_output=True, 
                              text=True,
                              timeout=5)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"✅ FFmpeg is working: {version_line}")
            return True
        else:
            print(f"❌ FFmpeg returned error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Could not verify FFmpeg: {e}")
        return False

if __name__ == "__main__":
    if add_ffmpeg_to_path():
        print("\n✅ FFmpeg setup complete!")
        print("   You can now run: streamlit run streamlit_app.py")
        sys.exit(0)
    else:
        print("\n❌ FFmpeg setup failed!")
        sys.exit(1)
