import io
import os
import tempfile
from dataclasses import dataclass, asdict
from typing import List

import numpy as np
import pandas as pd
import streamlit as st
from moviepy.video.io.VideoFileClip import VideoFileClip

st.set_page_config(page_title="Basketball Analyst", layout="wide")

st.title("🏀 Basketball Analyst – No-Code Starter")
st.caption("Upload a game, mark events (shots/possessions), and export highlights + CSV.")

# ---------- Models ----------
@dataclass
class Event:
    label: str
    start_s: float
    end_s: float

# ---------- Helpers ----------
def time_to_seconds(t: str) -> float:
    """Convert mm:ss or hh:mm:ss to seconds (also accepts plain seconds)."""
    parts = [p.strip() for p in t.strip().split(":")]
    if len(parts) == 1:
        return float(parts[0])
    if len(parts) == 2:
        m, s = parts
        return float(m) * 60 + float(s)
    if len(parts) == 3:
        h, m, s = parts
        return float(h) * 3600 + float(m) * 60 + float(s)
    raise ValueError("Use mm:ss or hh:mm:ss")

@st.cache_data(show_spinner=False)
def load_video_bytes(b: bytes) -> str:
    """Persist upload to a temp file and return its path."""
    tmpdir = tempfile.mkdtemp()
    path = os.path.join(tmpdir, "input_video.mp4")
    with open(path, "wb") as f:
        f.write(b)
    return path

def cut_clip(in_path: str, out_path: str, start: float, end: float):
    """Cut a subclip using MoviePy (ffmpeg under the hood)."""
    with VideoFileClip(in_path) as clip:
        start = max(0.0, float(start))
        end = min(float(end), float(clip.duration))
        if end <= start:
            raise ValueError("Clip end must be after start.")
        sub = clip.subclip(start, end)
        sub.write_videofile(
            out_path,
            codec="libx264",
            audio_codec="aac",
            preset="ultrafast",
            bitrate="2000k",
            verbose=False,
            logger=None,
        )

# ---------- State ----------
if "events" not in st.session_state:
    st.session_state.events: List[Event] = []

# ---------- Upload ----------
col_left, col_right = st.columns([2, 1])
with col_left:
    file = st.file_uploader(
        "Upload game video (MP4/MOV)",
        type=["mp4", "mov", "m4v", "avi"],
        accept_multiple_files=False
    )
    if file:
        video_path = load_video_bytes(file.getvalue())
        st.video(file)
    else:
        st.info("Upload a video to begin.")
        st.stop()

with col_right:
    st.subheader("Add Event")
    label = st.selectbox("Type", ["Shot", "Possession", "Foul/TO", "Other"], index=0)
    c1, c2 = st.columns(2)
    with c1:
        start_str = st.text_input("Start (mm:ss)", value="00:00")
    with c2:
        end_str = st.text_input("End (mm:ss)", value="00:05")

    if st.button("➕ Add to List", use_container_width=True):
        try:
            s = time_to_seconds(start_str)
            e = time_to_seconds(end_str)
            if e <= s:
                st.error("End time must be greater than start time.")
            else:
                st.session_state.events.append(Event(label, s, e))
        except Exception as ex:
            st.error(f"Invalid time format: {ex}")

st.divider()

# ---------- Events Table ----------
st.subheader("Events")
if st.session_state.events:
    df = pd.DataFrame([asdict(ev) for ev in st.session_state.events])
    df.index = np.arange(1, len(df) + 1)
    st.dataframe(df, use_container_width=True)

    c3, c4, c5 = st.columns(3)
    with c3:
        if st.button("🗑️ Clear All", type="secondary"):
            st.session_state.events = []
    with c4:
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download CSV", csv, file_name="events.csv", mime="text/csv")
    with c5:
        if st.button("🎬 Export Highlight Clips", type="primary"):
            if not st.session_state.events:
                st.warning("No events to export.")
            else:
                zip_bytes = io.BytesIO()
                with tempfile.TemporaryDirectory() as tmpo:
                    # export each clip
                    for i, ev in enumerate(st.session_state.events, start=1):
                        outp = os.path.join(tmpo, f"clip_{i:03d}_{ev.label}.mp4")
                        cut_clip(video_path, outp, ev.start_s, ev.end_s)
                    # bundle as zip
                    import zipfile
                    with zipfile.ZipFile(zip_bytes, "w", zipfile.ZIP_DEFLATED) as zf:
                        for f in sorted(os.listdir(tmpo)):
                            zf.write(os.path.join(tmpo, f), arcname=f)
                st.download_button(
                    "⬇️ Download Clips (.zip)",
                    data=zip_bytes.getvalue(),
                    file_name="highlights.zip",
                    mime="application/zip",
                )
else:
    st.info("No events yet. Add some in the right panel.")

st.caption("Next step (optional): we can add automatic shot/possession proposals and player tracking.")
