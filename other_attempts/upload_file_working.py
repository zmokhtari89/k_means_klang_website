import streamlit as st
import requests
import io
from pydub import AudioSegment

# API Endpoint
post_api = "https://kmeansklang-364885724897.europe-west1.run.app/predict"  # Replace with your API endpoint

# Website Header
st.markdown("""
    <h1 style="text-align: center; color: #ecd4cf;">K-means-Klang</h1>
    <h4 style="text-align: center; color: #ecd4cf;">
    Welcome to the K-means-Klang Project.
    Give us a song, we'll give you its cluster.
    </h4><br>
""", unsafe_allow_html=True)

# Callback function - gives info when audio is changed
def my_callback():
    st.write("Audio input has changed!")

# Audio File Uploader
audio_file = st.file_uploader("Give me an audio file:",
                              type=["wav", "mp3", "flac"],
                              accept_multiple_files=False,
                              help="The type of the file must be .wav, .mp3, or .flac",
                              on_change=my_callback)

# Function to send the audio to the API
def send_audio_to_api(audio_file_bytes, file_type):
    """Function to send recorded audio to the API."""

    # Convert audio to WAV if it's not already in WAV format
    if file_type != "wav":  # If not WAV, convert to WAV
        audio = AudioSegment.from_file(io.BytesIO(audio_file_bytes), format=file_type)
        audio_bytes = io.BytesIO()
        audio.export(audio_bytes, format="wav")
        audio_bytes.seek(0)
        # Preparing the file for sending with 'audio_file' key
        file = {"audio_file": ("audio.wav", audio_bytes, "audio/wav")}
    else:
        audio_bytes = io.BytesIO(audio_file_bytes)
        audio_bytes.seek(0)
        # Preparing the file for sending with 'audio_file' key
        file = {"audio_file": ("audio.wav", audio_bytes, "audio/wav")}

    # Send the audio file to the API
    response = requests.post(post_api, files=file)

    if response.status_code == 200:
        st.success("Audio successfully sent for analysis!")
        try:
            result = response.json()
            st.write(f"Predicted Cluster : {result.get('predicted_cluster')}")
        except ValueError:
            st.error("Error: Unable to parse response from the API.")
    else:
        st.error(f"Failed to send audio. Status code: {response.status_code} - {response.text}")


# Ensure session state is initialized
if "recording" not in st.session_state:
    st.session_state["recording"] = None

# Callback function to handle audio input change
def process_audio():
    st.session_state["new_audio"] = st.session_state["recording"]

    if st.session_state["new_audio"]:
        st.write("New audio detected! Sending to API...")
        send_audio_to_api(st.session_state["new_audio"], "wav")

# If an audio file is uploaded
if audio_file:
    st.audio(audio_file.getvalue(), format="audio/wav")  # Ensure correct format for playback
    st.write("File uploaded successfully!")

    # Read file as bytes
    audio_file_bytes = audio_file.getvalue()
    st.write(f"File size: {len(audio_file_bytes) / 1024:.2f} KB")

    # Extract file type from extension (either mp3, flac, or wav)
    file_type = audio_file.name.split(".")[-1]

    # Convert and send the audio file to the API
    send_audio_to_api(audio_file_bytes, file_type)
