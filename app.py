import streamlit as st
import requests
import base64
import io
import pydub  # Ensure you have pydub installed for audio conversion
import librosa
import soundfile as sf

# Custom CSS to change the text and background color globally
def apply_custom_styles():
    st.markdown("""
        <style>
        /* Change text color globally */
        * {
            color: #ecd4cf !important;
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
            color: #ecd4cf !important;
            border: 1px solid #ecd4cf !important;
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

# API that posts the audio to our model
post_api = "https://your-api.com/analyze-audio"  # Replace with your API endpoint


# Website Header
st.markdown("""
    <h1 style="text-align: center; color: #ecd4cf;">K-means-Klang</h1>
    <h4 style="text-align: center; color: #ecd4cf;">Welcome to the K-means-Klang Project.
    Give us a song, we'll give you its cluster.</h3>
    <br>
""", unsafe_allow_html=True)


# Callback function - gives info when audio is changed
def my_callback():
    st.write("Audio input has changed!")


# Function to convert and send the audio to your API
def convert_and_send_audio(audio_data):
    # Check if the data is in bytes already (for recording)
    if isinstance(audio_data, bytes):
        audio_bytes = io.BytesIO(audio_data)
    else:
        # For file uploads, extract bytes using .getvalue()
        audio_bytes = io.BytesIO(audio_data.getvalue())

    # Use librosa to load audio from byte data (no need for ffmpeg)
    try:
        y, sr = librosa.load(audio_bytes, sr=None)  # sr=None to keep original sample rate
    except Exception as e:
        st.error(f"Error loading audio with librosa: {e}")
        return

    # Save the audio as a WAV file using soundfile
    output_file = "converted_audio.wav"
    sf.write(output_file, y, sr)

    # Send to your API (you can send the file or the byte data)
    send_audio_to_api(output_file)


# Function to send the audio to the API
def send_audio_to_api(audio_file_path):
    """Function to send recorded audio to the API."""
    if audio_file_path:
        # Read the converted audio file (WAV) and send it to the API
        with open(audio_file_path, "rb") as f:
            files = {"file": ("audio.wav", f, "audio/wav")}

            # Send request to the API
            response = requests.post(post_api, files=files)

            # Display API response
            if response.status_code == 200:
                st.success("Audio successfully sent for analysis!")
                try:
                    # Display the API response (assuming JSON)
                    result = response.json()
                    st.write(result)  # Display the results from the API (cluster or other data)
                except ValueError:
                    st.error("Error: Unable to parse response from the API.")
            else:
                st.error(f"Failed to send audio. Status code: {response.status_code}")


# Callback function to handle audio input change
def process_audio():
    st.session_state["new_audio"] = st.session_state["recording"]

    if st.session_state["new_audio"]:
        st.write("New audio detected! Sending to API...")
        convert_and_send_audio(st.session_state["new_audio"])


# Streamlit UI - Upload Audio (First)
st.markdown('''<br>
            <h4 style="text-align: center;">Upload your Audio</h4>
            ''',
            unsafe_allow_html=True)

# File uploader
audio_file = st.file_uploader("Give me an audio file:",
                              type=["wav", "mp3", "flac"],
                              accept_multiple_files=False,
                              help="The type of the file must be .wav, .mp3 or .flac",
                              on_change=my_callback)

if audio_file:
    st.audio(audio_file)
    st.write("File uploaded successfully!")

    # Read file as bytes
    bytes_data = audio_file.getvalue()
    st.write(f"File size: {len(bytes_data) / 1024:.2f} KB")

    # Convert and send the audio file to the API
    convert_and_send_audio(bytes_data)


# Streamlit UI - Recording Audio (Second)
st.markdown('''<br>
            <h4 style="text-align: center;">Record your Voice</h4>''',
            unsafe_allow_html=True)

# Audio input with an on_change callback
recording = st.audio_input("Let me hear your voice:", key="recording", on_change=process_audio)

# Show a message if audio is updated
if "new_audio" in st.session_state and st.session_state["new_audio"]:
    st.audio(st.session_state["new_audio"])
