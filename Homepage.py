import os
# Configure pydub to use system ffmpeg
os.environ["PATH"] += os.pathsep + "/usr/bin/ffmpeg"

import streamlit as st
import requests
import io
import numpy as np
import wave
import tempfile
from pydub import AudioSegment
import base64

# -------------------------------- STYLING -------------------------------------

# Custom CSS to change the text and background color globally
def apply_custom_styles():
    st.markdown("""
        <style>
        /* Change text color globally */
        * {
            color: #e38a78 !important;
        }

        /* Sidebar background and text */
        .stSidebar {
            background-color: #000000 !important;
            color: #e38a78 !important;
        }

        /* Header background and text */
        header {
            background-color: #000000 !important;
            color: #e38a78 !important;
        }

        /* Dark background for file uploader and audio uploader */
        div.stFileUploader, div.stAudio {
            background-color: #2a2a2a !important;
            border-radius: 10px;
            padding: 10px;
        }

        /* Style the buttons inside uploaders */
        div.stFileUploader button, div.stAudio button {
            background-color: #444 !important;
            color: #e38a78 !important;
            border: 1px solid #e38a78 !important;
        }
        </style>
    """, unsafe_allow_html=True)

# Apply the styles
apply_custom_styles()

# Background Image
# Function to encode image to Base64
def get_base64(file_path):
    try:
        with open(file_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        st.error("Background image not found. Make sure the file path is correct.")
        return ""

# Store background in session_state to persist across reruns -> It doesn't need to reload the photo every time
if "base64_bg" not in st.session_state:
    image_path = "images/music-8559592.jpg"
    st.session_state["base64_bg"] = get_base64(image_path)

# Apply CSS background
st.markdown(
    f"""
    <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{st.session_state['base64_bg']}");
            background-size: cover;
        }}
    </style>
    """,
    unsafe_allow_html=True
)


# ------------------------------------ API -------------------------------------


# API Endpoint
post_api = "https://kmeansklang-364885724897.europe-west1.run.app/predict"

# Website Header
st.markdown("""
    <h1 style="text-align: center; color: #ecd4cf;">K-Means-Klang</h1>
    <h4 style="text-align: center; color: #ecd4cf;">
    Welcome to the K-means-Klang Project.
    Give us your favorite song, we'll tell you who you are!
    </h4><br>
""", unsafe_allow_html=True)

def load_image(path):
    with open(path, 'rb') as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    return encoded

animals = ['fierce Falcon', 'groovy Dolphin', 'dreamy Panda', 'jumpy Squirrel', 'chill Coala', 'sophisticated Owl']
description = [
    ['intense', 'rebellious', 'bold'],
    ['rhythmic', 'energetic', 'vibrant'],
    ['subdued', 'soft', 'relaxing'],
    ['upbeat', 'conventional', 'optimistic'],
    ['smooth', 'comforting', 'easygoing'],
    ['reflective', 'sophisticated', 'calming']
]

cluster_chars = [
    ['Metal', 'Disco', 'Rock'],
    ['Pop', 'Disco', 'Rock'],
    ['Reggae', 'Blues', 'Country'],
    ['Pop' ,'Hip Hop', 'Reggae'],
    ['Reggae', 'Country', 'Rock'],
    ['Classical', 'Jazz', 'Blues']
]

# # Function to send the audio to the API
def send_audio_to_api(audio_file_path, file_type):
    """Function to send recorded audio to the API."""
    with open(audio_file_path, "rb") as f:
        if file_type == 'mp3':
            # Send the MP3 file to the API
            files = {"audio_file": ("audio.mp3", f, "audio/mp3")}
        else:
            # If it's a different file type, handle accordingly (e.g., WAV)
            files = {"audio_file": ("audio.wav", f, "audio/wav")}

        response = requests.post(post_api, files=files)

        if response.status_code == 200:
            try:
                result = response.json()
                prediction = result.get('predicted_cluster')
                # st.markdown(f'<h4 style="text-align: center;">Predicted Cluster: {result.get("predicted_cluster")}</h4>', unsafe_allow_html=True)

                st.markdown(f'<h4 style="text-align: center;">Hey there {animals[prediction]}!</h4>', unsafe_allow_html=True )
                # st.markdown(f'<h5 style="text-align: center;">Your music taste tends to be <br>{description[prediction][0]} {description[prediction][1]} {description[prediction][2]}</h5>', unsafe_allow_html=True )
                # st.markdown(f'<h5 style="text-align: center;">The cluster assigned to you is defined by <br>{cluster_chars[prediction][0]} {cluster_chars[prediction][1]} {cluster_chars[prediction][2]}</h5>', unsafe_allow_html=True )
                st.markdown(f'''
                    <p style="text-align: center; font-family: Arial, sans-serif; font-size: 18px; line-height: 1.2;">
                        Your music taste tends to be: <br>
                        <div style="display: flex; justify-content: center; gap: 50px; padding-left: 5vw; padding-right: 5vw; margin-top: -10px;">
                            <span>{description[prediction][0]}</span>
                            <span>{description[prediction][1]}</span>
                            <span>{description[prediction][2]}</span>
                        </div>
                    </p>
                ''', unsafe_allow_html=True)
                cluster_img_path = f"images/cluster_{prediction}.png"
                st.write(f'''
                    <div style="text-align: center;">
                        <img src="data:image/jpg;base64,{load_image(cluster_img_path)}" style="max-width: 500px; width: 100%; height: auto; display: inline-block;">
                    </div>
                ''', unsafe_allow_html=True)
                st.markdown(f'''<br>
                    <p style="text-align: center; font-family: Arial, sans-serif; font-size: 18px; line-height: 1.2;">
                        The most dominant genres describing your song are: <br>
                        <div style="display: flex; justify-content: center; gap: 50px; padding-left: 5vw; padding-right: 5vw; margin-top: -10px;">
                            <span>{cluster_chars[prediction][0]}</span>
                            <span>{cluster_chars[prediction][1]}</span>
                            <span>{cluster_chars[prediction][2]}</span>
                        </div>
                    </p>
                ''', unsafe_allow_html=True)
            except ValueError:
                st.error("Error: Unable to parse response from the API.")
        else:
            st.error(f"Failed to send audio. Status code: {response.status_code} - {response.text}")

# Audio File Uploader
audio_file = st.file_uploader("Give me an audio file:",
                              type=["wav", "mp3", "flac"],
                              accept_multiple_files=False,
                              help="The type of the file must be .wav, .mp3, or .flac"
                              )


# If an audio file is uploaded
if audio_file:
    st.audio(audio_file.getvalue(), format="audio/mp3")  # Display audio in mp3 format

    # Read file as bytes
    audio_file_bytes = audio_file.getvalue()

    # Extract file type from extension (either mp3, flac, or wav)
    file_type = audio_file.name.split(".")[-1]

    if file_type == "mp3":
        # Send the audio file as is (no conversion)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_mp3:
            temp_mp3.write(audio_file_bytes)
            temp_mp3.close()
            send_audio_to_api(temp_mp3.name, file_type)  # Send .mp3 file directly to the API
    else:
        # Handle other file types like WAV, FLAC, etc.
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav:
            temp_wav.write(audio_file_bytes)
            temp_wav.close()
            send_audio_to_api(temp_wav.name, "wav")


# Streamlit UI - Record Audio (Second)
st.markdown('''<br>
            <h4 style="text-align: center;">Record your Voice</h4>''',
            unsafe_allow_html=True)


# Recording input
recording = st.audio_input("Let me hear your voice:", key="recording")

if recording:
    st.write("Recording complete. Sending audio to the API...")

    # Convert the UploadedFile to bytes
    if isinstance(recording, st.runtime.uploaded_file_manager.UploadedFile):
        # Get the raw bytes from the UploadedFile object
        recording_data = recording.getvalue()

        # Get the file type from the recording's MIME type or extension (if applicable)
        file_type = recording.name.split(".")[-1]  # Extract the file extension (e.g., mp3, wav, flac)
        # st.write(f"File Type: {file_type}")  # Display file type

        try:
            # Create a wave file-like object from the byte data
            wav_file = io.BytesIO(recording_data)
            with wave.open(wav_file, 'rb') as wav:
                # Get properties of the audio file
                framerate = wav.getframerate()
                num_frames = wav.getnframes()
                audio_data = wav.readframes(num_frames)

                # Convert the audio byte data into numpy array
                audio_samples = np.frombuffer(audio_data, dtype=np.int16)

                # Ensure we have valid audio samples (must be an array of integers)
                # st.write(f"Audio data length: {len(audio_samples)} samples")

                # Save the numpy array as a .wav file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav:
                    with wave.open(temp_wav, 'wb') as wav_out:
                        wav_out.setnchannels(1)  # Mono audio
                        wav_out.setsampwidth(2)  # 16-bit audio
                        wav_out.setframerate(framerate)
                        wav_out.writeframes(audio_samples.tobytes())

                    # Send the temporary .wav file to the API and pass file_type
                    send_audio_to_api(temp_wav.name, file_type)
        except Exception as e:
            st.error(f"Error processing audio: {e}")
    else:
        st.error("Error: Recorded audio is not in the expected format.")
