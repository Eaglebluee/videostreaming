import streamlit as st
import tempfile
import moviepy.editor as mp

# Set maximum video duration in seconds
MAX_DURATION = 15

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
        st.video(temp_file.name)
    else:
        # Video duration exceeds the allowed limit
        st.error(f"Video duration should be less than or equal to {MAX_DURATION} seconds.")

    # Remove the temporary file
    temp_file.close()
