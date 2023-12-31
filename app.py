import streamlit as st
import cv2
import numpy as np
from moviepy.editor import VideoFileClip
import tempfile
import os

def apply_sepia_filter(frame):
    # Apply sepia filter to the frame
    sepia_matrix = np.array([[0.272, 0.534, 0.131],
                             [0.349, 0.686, 0.168],
                             [0.393, 0.769, 0.189]])
    filtered_frame = cv2.transform(frame, sepia_matrix)

    return filtered_frame

def main():
    st.title("Video Editor")

    # Upload video
    video_file = st.file_uploader("Upload a video", type=["mp4"])

    if video_file is not None:
        st.subheader("Original Video")
        st.video(video_file)

        # Save video to a temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(video_file.read())

        # Process video
        cap = cv2.VideoCapture(temp_file.name)
        frames = []

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Apply sepia filter
            filtered_frame = apply_sepia_filter(frame)

            # Add filtered frame to the list
            frames.append(filtered_frame)

        cap.release()

        # Save edited video as a temporary file
        edited_temp_file = tempfile.NamedTemporaryFile(delete=False)
        edited_temp_file.close()

        out = cv2.VideoWriter(edited_temp_file.name, cv2.VideoWriter_fourcc(*"mp4v"), cap.get(cv2.CAP_PROP_FPS),
                              (frames[0].shape[1], frames[0].shape[0]))

        for frame in frames:
            out.write(frame)

        out.release()

        # Display edited video
        st.subheader("Edited Video")
        st.video(edited_temp_file.name)

        # Remove the edited temporary file
        os.remove(edited_temp_file.name)

if __name__ == "__main__":
    main()
