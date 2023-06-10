import cv2
import numpy as np
import streamlit as st
from streamlit_webrtc import VideoTransformerBase, webrtc_streamer, WebRtcMode


class PencilSketchTransformer(VideoTransformerBase):
    def transform(self, frame):
        # Convert the BGR frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Invert the grayscale image
        invert = cv2.bitwise_not(gray)
        # Apply Gaussian blur to the inverted image
        blur = cv2.GaussianBlur(invert, (111, 111), 0)
        # Blend the grayscale image and blurred image using color dodge blend mode
        pencil_sketch = cv2.divide(gray, 255 - blur, scale=256.0)
        # Convert the pencil sketch back to BGR
        sketch_bgr = cv2.cvtColor(pencil_sketch, cv2.COLOR_GRAY2BGR)
        return sketch_bgr


def main():
    st.title("Real-time Pencil Sketch Effect")

    # Create a WebRTC pipeline
    webrtc_ctx = webrtc_streamer(
        key="example",
        mode=WebRtcMode.SENDRECV,
        video_transformer_factory=PencilSketchTransformer,
        async_transform=True,
    )

    # Display the transformed video frames
    if webrtc_ctx.video_transformer:
        st.image(webrtc_ctx.video_transformer)

    st.markdown("---")
    st.markdown("### Instructions")
    st.markdown("1. Click the **Start** button to start the video stream.")
    st.markdown("2. Apply the **Pencil Sketch** effect using the menu on the left.")

if __name__ == "__main__":
    main()
