import streamlit as st
import cv2
import numpy as np

def pencil_sketch(video_file):
    video_capture = cv2.VideoCapture(video_file.name)

    while video_capture.isOpened():
        ret, frame = video_capture.read()
        if not ret:
            break
        
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        sketch_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2BGR)

        st.image(sketch_frame, channels="BGR")

if __name__ == "__main__":
    st.title("Video Upload")

    uploaded_file = st.file_uploader("Upload a video", type=['mp4', 'mov'])

    if uploaded_file is not None:
        pencil_sketch(uploaded_file)
