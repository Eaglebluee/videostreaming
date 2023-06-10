import streamlit as st
import cv2
import numpy as np

def pencil_sketch(video_frame):
    gray_frame = cv2.cvtColor(video_frame, cv2.COLOR_BGR2GRAY)
    inverted_frame = cv2.bitwise_not(gray_frame)
    blurred_frame = cv2.GaussianBlur(inverted_frame, (111, 111), 0)
    inverted_blurred_frame = cv2.bitwise_not(blurred_frame)
    sketch_frame = cv2.divide(gray_frame, inverted_blurred_frame, scale=256.0)
    return cv2.cvtColor(sketch_frame, cv2.COLOR_GRAY2BGR)

def main():
    st.title("Video Filters")

    uploaded_file = st.file_uploader("Upload a video", type=['mp4', 'mov'])

    if uploaded_file is not None:
        # Read the video file
        try:
            video_bytes = uploaded_file.read()
            video_nparray = np.frombuffer(video_bytes, np.uint8)
            video_capture = cv2.imdecode(video_nparray, cv2.IMREAD_UNCHANGED)

            if video_capture is not None:
                # Display the original video
                st.video(video_capture)

                # Dropdown menu for filters
                filter_option = st.selectbox("Filters", ["None", "Pencil Sketch"])

                # Apply selected filter to the video
                if filter_option == "Pencil Sketch":
                    sketch_video = pencil_sketch(video_capture)
                    st.video(sketch_video)
                else:
                    st.warning("Please select a valid filter option.")
            else:
                st.error("Failed to read the video file.")
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
