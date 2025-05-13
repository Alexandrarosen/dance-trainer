import streamlit as st
import tempfile
import os
import moviepy.editor as mp
import requests

st.set_page_config(page_title="Dance Video Trainer", layout="centered")
st.title("💃 Dance Video Trainer")

st.markdown("""
Upload a dance video or paste a direct video URL (like an .mp4 file).  
You can flip, slow down, or speed up videos to help with practice.
""")

# --- Video input ---
video_url = st.text_input("Paste a direct video URL (e.g. ends in .mp4)")
uploaded_file = st.file_uploader("Or upload a dance video file", type=["mp4", "mov", "avi"])

video_path = None
is_uploaded = False
is_url = False

# Handle file upload
if uploaded_file:
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    tfile.write(uploaded_file.read())
    video_path = tfile.name
    is_uploaded = True
    st.success("✅ Video uploaded successfully")

# Handle URL
elif video_url:
    try:
        response = requests.get(video_url, stream=True)
        if response.status_code == 200:
            tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
            for chunk in response.iter_content(chunk_size=8192):
                tfile.write(chunk)
            video_path = tfile.name
            is_url = True
            st.success("✅ Video downloaded from URL")
        else:
            st.error("🚫 Could not fetch video from the URL.")
    except Exception as e:
        st.error(f"Error downloading video: {e}")

# --- Effects section ---
if video_path:
    st.video(video_path)

    speed = st.slider("Playback speed", min_value=0.25, max_value=2.0, value=1.0, step=0.25)
    mirror = st.checkbox("Mirror video (flip horizontally)")

    if mirror or speed != 1.0:
        st.info("🔄 Processing video with effects...")

        clip = mp.VideoFileClip(video_path)

        if mirror:
            clip = clip.fx(mp.vfx.mirror_x)
        if speed != 1.0:
            clip = clip.fx(mp.vfx.speedx, factor=speed)

        clip_resized = clip.resize(height=480)
        out_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
        clip_resized.write_videofile(
            out_path,
            codec="libx264",
            audio_codec="aac",
            preset="ultrafast",
            bitrate="500k",
            verbose=False,
            logger=None
        )

        st.success("🎥 Modified video is ready:")
        st.video(out_path)



# --- Save video links in session ---
if "saved_links" not in st.session_state:
    st.session_state.saved_links = []

if video_url and st.button("💾 Save this video link"):
    st.session_state.saved_links.append(video_url)
    st.success("🔖 Saved!")

if st.session_state.saved_links:
    st.markdown("### 🔖 Saved Video Links")
    for link in st.session_state.saved_links:
        st.markdown(f"- [{link}]({link})")

#detta ska vara i powershell: streamlit run "C:\Users\AlexandraRosén\OneDrive - Triathlon Group\Desktop\test.py"
#skriv cd.. om är i allbolah flik tex
#detta ska vara i visual studo terminal streamlit run dance_trainer.py