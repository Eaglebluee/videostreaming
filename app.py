import streamlit as st
import tempfile
import moviepy.editor as mp
import cv2
import numpy as np

# Set maximum video duration in seconds
MAX_DURATION = 15

def apply_canine_filter(frame):
    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    # Apply the canine filter
    canine_filter = np.zeros_like(frame)
    canine_filter[..., 2] = gray  # Set the red channel to the grayscale image
    canine_filter[..., 1] = gray  # Set the green channel to the grayscale image

    return canine_filter

# Display upload file form
uploaded_file = st.file_uploader("Upload Video", type=["mp4", "mov", "avi"])

# Process uploaded file
if uploaded_file is not None:
    # Create a temporary file to save the uploaded video
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(uploaded_file.read())

    # Get the duration of the video
    video_duration = mp.VideoFileClip(temp_file.name).duration

    # Check if the video duration is within the allowed limit
    if video_duration <= MAX_DURATION:
        # Process the video
        st.success("Video uploaded successfully!")

        # Apply canine filter to the video frames
        video_clip = mp.VideoFileClip(temp_file.name)
        edited_clip = video_clip.fl_image(lambda frame: apply_canine_filter(frame))

        # Save the edited video to a temporary file
        edited_temp_file = tempfile.NamedTemporaryFile(delete=False)
        edited_clip.write_videofile(edited_temp_file.name, codec="libx264")

        # Display the original and edited videos
        col1, col2 = st.beta_columns(2)
        with col1:
            st.subheader("Original Video")
            st.video(temp_file.name)

        with col2:
            st.subheader("Edited Video")
            st.video(edited_temp_file.name)

        # Remove the temporary files
        temp_file.close()
        edited_temp_file.close()
    else:
        # Video duration exceeds the allowed limit
        st.error(f"Video duration should be less than or equal to {MAX_DURATION} seconds.")
