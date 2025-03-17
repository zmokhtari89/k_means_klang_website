import streamlit as st
import requests
import io
import numpy as np
import wave
import tempfile

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

# Function to send the audio to the API
def send_audio_to_api(audio_file_path):
    """Function to send recorded audio to the API."""
    with open(audio_file_path, "rb") as f:
        files = {"audio_file": ("audio.wav", f, "audio/wav")}

        response = requests.post(post_api, files=files)

        if response.status_code == 200:
            st.success("Audio successfully sent for analysis!")
            try:
                result = response.json()
                st.write(f"Predicted Cluster: {result.get('predicted_cluster')}")
            except ValueError:
                st.error("Error: Unable to parse response from the API.")
        else:
            st.error(f"Failed to send audio. Status code: {response.status_code} - {response.text}")

# Streamlit UI - Record Audio (Second)
st.markdown('''<br>
            <h4 style="text-align: center;">Record your Voice</h4>''',
            unsafe_allow_html=True)

# Audio input with on_change callback
recording = st.audio_input("Let me hear your voice:", key="recording", on_change=my_callback)

# If audio has been recorded, we process it
if recording:
    st.write("Recording complete. Sending audio to the API...")

    # Convert the UploadedFile to bytes
    if isinstance(recording, st.runtime.uploaded_file_manager.UploadedFile):
        # Get the raw bytes from the UploadedFile object
        recording_data = recording.getvalue()
        st.write("Recording is in bytes format.")

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
                st.write(f"Audio data length: {len(audio_samples)} samples")

                # Save the numpy array as a .wav file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav:
                    with wave.open(temp_wav, 'wb') as wav_out:
                        wav_out.setnchannels(1)  # Mono audio
                        wav_out.setsampwidth(2)  # 16-bit audio
                        wav_out.setframerate(framerate)
                        wav_out.writeframes(audio_samples.tobytes())

                    # Send the temporary .wav file to the API
                    send_audio_to_api(temp_wav.name)

        except Exception as e:
            st.error(f"Error processing audio: {e}")
    else:
        st.error("Error: Recorded audio is not in the expected format.")
