import cv2
import streamlit as st

def main():
    st.title("Live Video Stream")
    video_capture = cv2.VideoCapture(0)

    if not video_capture.isOpened():
        st.error("Unable to open the camera.")
        return

    while True:
        ret, frame = video_capture.read()
        if not ret:
            st.error("Failed to capture frame from camera.")
            break

        # Resize frame to fit the Streamlit app
        resized_frame = cv2.resize(frame, (640, 480))

        # Display the frame in Streamlit
        st.image(resized_frame, channels="BGR")

    video_capture.release()

if __name__ == "__main__":
    main()
