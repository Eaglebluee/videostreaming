import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, RTCConfiguration

RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

class VideoTransformer(VideoTransformerBase):
    def transform(self, frame):
        # Apply transformations to the frame (optional)
        return frame

st.title("My first Streamlit app")
st.write("Hello, world")

webrtc_streamer(
    key="example",
    mode="video",
    rtc_configuration=RTC_CONFIGURATION,
    video_transformer_factory=VideoTransformer,
)
