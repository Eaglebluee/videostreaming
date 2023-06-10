import streamlit as st
from streamlit_webrtc import webrtc_streamer

st.title("My first Streamlit app")
st.write("Hello, world")

webrtc_streamer(key="example", video=True, audio=False, 
                client_settings={"constraints": {"video": True, "audio": False}})

