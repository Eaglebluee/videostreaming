import cv2
import numpy as np
import streamlit as st
from streamlit_webrtc import VideoTransformerBase, webrtc_streamer, WebRtcMode

class PencilSketchTransformer(VideoTransformerBase):
    def __init__(self):
        self.canvas = None

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")

        # Apply pencil sketch effect
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred_img = cv2.GaussianBlur(gray_img, (21, 21), 0, 0)
        inverted_img = cv2.bitwise_not(blurred_img)
        img_sketch = cv2.divide(gray_img, inverted_img, scale=256.0)

        if self.canvas is None:
            self.canvas = np.zeros_like(img_sketch)

        img_blend = cv2.multiply(img_sketch, self.canvas, scale=1 / 256.0)
        img_blend = cv2.cvtColor(img_blend, cv2.COLOR_GRAY2BGR)

        self.canvas = cv2.add(img_blend, img, dtype=cv2.CV_8UC3)
        return self.canvas

def main():
    st.title("Real-Time Pencil Sketch")

    webrtc_ctx = webrtc_streamer(
        key="example",
        mode=WebRtcMode.SENDRECV,
        video_transformer_factory=PencilSketchTransformer,
        async_transform=True,
    )

    if webrtc_ctx.video_transformer:
        st.write("Webcam Video")
        st.video(webrtc_ctx.video_transformer)

if __name__ == "__main__":
    main()
