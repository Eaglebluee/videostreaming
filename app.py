import streamlit as st
import cv2
from moviepy.editor import *
import numpy as np

def extract_frames(video_file):
    video_capture = cv2.VideoCapture(video_file.name)
    fps = int(video_capture.get(cv2.CAP_PROP_FPS))
    count = 0

    st.text("Extracting frames from the video...")
    st.progress(0)

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        cv2.imwrite(f'frame{count:04d}.png', frame)
        count += 1
        progress = (count / fps) * 100
        st.progress(progress)

    st.success("Frame extraction complete!")

def add_text_overlay(video_file):
    video = VideoFileClip(video_file.name)

    text = TextClip('Hello, world!', fontsize=50, color='white')
    text = text.set_duration(video.duration)

    st.text("Adding text overlay to the video...")
    st.progress(0)

    video = CompositeVideoClip([video, text])
    video.write_videofile('output.mp4')

    st.success("Text overlay added to the video!")

def apply_blur_effect(video_file):
    video_capture = cv2.VideoCapture(video_file.name)
    fps = int(video_capture.get(cv2.CAP_PROP_FPS))
    kernel_size = (15, 15)
    writer = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (640, 360))

    st.text("Applying blur effect to the video...")
    st.progress(0)

def download_video(video_path):
    with open(video_path, "rb") as video_file:
        video_bytes = video_file.read()
        video_base64 = base64.b64encode(video_bytes).decode("utf-8")
        href = f'<a href="data:video/mp4;base64,{video_base64}" download="output.mp4">Download edited video</a>'
        st.markdown(href, unsafe_allow_html=True)

def main():
    st.title("Video Editor")

    # Upload video
    uploaded_file = st.file_uploader("Upload a video", type=['mp4', 'mov'])

    if uploaded_file is not None:
        # Get the file name
        file_name = uploaded_file.name

        # Save the uploaded file
        with open(file_name, "wb") as file:
            file.write(uploaded_file.getbuffer())

        # Video editing options
        options = ["Extract Frames", "Add Text Overlay", "Apply Blur Effect"]
        selected_option = st.selectbox("Select an option", options)

        if selected_option == "Extract Frames":
            extract_frames(file_name)
            st.success("Frames extracted successfully.")

        elif selected_option == "Add Text Overlay":
            add_text_overlay(file_name)
            st.success("Text overlay applied successfully.")

        elif selected_option == "Apply Blur Effect":
            apply_blur_effect(file_name)
            st.success("Blur effect applied successfully.")

        st.video(file_name)

        if st.button("Download"):
            download_video(file_name)

if __name__ == '__main__':
    main()
