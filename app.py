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

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        blurred_frame = cv2.GaussianBlur(frame, kernel_size, 0)
        writer.write(blurred_frame)
        progress = (video_capture.get(cv2.CAP_PROP_POS_FRAMES) / video_capture.get(cv2.CAP_PROP_FRAME_COUNT)) * 100
        st.progress(progress)

    video_capture.release()
    writer.release()

    st.success("Blur effect applied to the video!")

def main():
    st.title("Python Video Editor")
    st.write("Upload a video file and select the editing option.")

    uploaded_file = st.file_uploader("Upload a video", type=['mp4', 'mov'])

    if uploaded_file is not None:
        selected_option = st.selectbox("Select an editing option", ["Extract Frames", "Add Text Overlay", "Apply Blur Effect"])

        if selected_option == "Extract Frames":
            if st.button("Extract"):
                extract_frames(uploaded_file)
        elif selected_option == "Add Text Overlay":
            if st.button("Add"):
                add_text_overlay(uploaded_file)
        elif selected_option == "Apply Blur Effect":
            if st.button("Apply"):
                apply_blur_effect(uploaded_file)

if __name__ == '__main__':
    main()
