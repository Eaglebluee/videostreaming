import cv2
import streamlit as st
import numpy as np
from moviepy.editor import VideoFileClip
import tempfile
import os

# Helper function to apply filters to video frames
def apply_filter(frame, filter_type):
    if filter_type == "Grayscale":
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    elif filter_type == "Canny Edge Detection":
        return cv2.Canny(frame, 100, 200)
    # Add more filter options here

    # If no filter selected or unknown filter type, return original frame
    return frame

# Streamlit app
def main():
    st.title("Video Filter App")
    
    # Upload video file
    video_file = st.file_uploader("Upload a video", type=["mp4", "avi"])
    if video_file is not None:
        # Save the uploaded file to a temporary location
        temp_file_path = os.path.join(tempfile.gettempdir(), "uploaded_video.mp4")
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(video_file.read())
        
        clip = VideoFileClip(temp_file_path)
        duration = clip.duration

        # Limit video duration to 10 seconds
        if duration > 10.0:
            st.warning("Video duration exceeds the maximum allowed duration (10 seconds). Please upload a shorter video.")
        else:
            # Display video player
            st.video(video_file)

            # Select filter option
            filter_type = st.selectbox("Select filter", ["None", "Grayscale", "Canny Edge Detection"])

            # Process video frames and display the filtered result
            for frame in clip.iter_frames():
                filtered_frame = apply_filter(frame, filter_type)
                st.image(filtered_frame)

# Run the Streamlit app
if __name__ == "__main__":
    main()
