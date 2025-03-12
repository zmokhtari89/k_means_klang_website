# import streamlit as st
# import requests
# import datetime


import streamlit as st
import numpy as np
import pandas as pd
import requests
from io import BytesIO

post_api = "https://your-api.com/analyze-audio"

# st.markdown("""# K-means-Klang
# ### Welcome to the K-means-Klang Project. Give us a song, we'll give you its cluster""")

st.markdown("""
    <h1 style="text-align: center;">K-means-Klang</h1>
    <h3 style="text-align: center;">Welcome to the K-means-Klang Project. Give us a song, we'll give you its cluster.</h3>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
        body {
            background-image: url("https://static.vecteezy.com/system/resources/thumbnails/024/295/098/small_2x/music-notes-background-illustration-ai-generative-free-photo.jpg");
            background-size: cover;
        }
    </style>
""", unsafe_allow_html=True)


def my_callback():
    st.write("Audio input has changed!")

recording = st.audio_input("Let me hear your voice:", on_change=my_callback)

if recording:
    st.audio(recording)



def send_audio_to_api(audio_file):
    """Function to send recorded audio to the API."""
    if audio_file:
        # Prepare file for sending
        files = {"file": ("audio.wav", audio_file, "audio/wav")}

        # Send request to the API
        response = requests.post(post_api, files=files)

        # Display API response
        if response.status_code == 200:
            st.success("Audio successfully sent for analysis!")
            st.write(response.json())  # Display API response (assuming JSON)
        else:
            st.error(f"Failed to send audio. Status code: {response.status_code}")

# Callback function to handle audio input change
def process_audio():
    st.session_state["new_audio"] = st.session_state["recording"]

    if st.session_state["new_audio"]:
        st.write("New audio detected! Sending to API...")
        send_audio_to_api(st.session_state["new_audio"])

# Streamlit UI
st.title("Voice Recorder & Analysis")

# Audio input with an on_change callback
st.audio_input("Record your voice:", key="recording", on_change=process_audio)

# Show a message if audio is updated
if "new_audio" in st.session_state and st.session_state["new_audio"]:
    st.audio(st.session_state["new_audio"])




# df = pd.DataFrame({
#     'first column': list(range(1, 11)),
#     'second column': np.arange(10, 101, 10)
# })

# # this slider allows the user to select a number of lines
# # to display in the dataframe
# # the selected value is returned by st.slider
# line_count = st.slider('Select a line count', 1, 10, 3)

# # and used to select the displayed lines
# head_df = df.head(line_count)

# head_df
