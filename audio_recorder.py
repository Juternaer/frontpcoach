import os
import streamlit as st
from datetime import datetime

def save_audio_recording(audio_data):
    """
    Save audio recording to the recordings folder
    """
    # Create recordings directory if it doesn't exist
    RECORDINGS_DIR = "recordings"
    if not os.path.exists(RECORDINGS_DIR):
        os.makedirs(RECORDINGS_DIR)

    # Generate unique filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"recording_{timestamp}.wav"
    filepath = os.path.join(RECORDINGS_DIR, filename)

    try:
        # Save the audio file
        with open(filepath, "wb") as f:
            f.write(audio_data.getvalue())
        return True, filename
    except Exception as e:
        return False, str(e)

# Streamlit UI
st.title("Audio Recorder")

# Audio input widget
audio_data = st.audio_input("Record your voice", key="audio_input")
if audio_data:
    st.button("Play Recording")


print(audio_data)


if audio_data is not None and st.button("Save Recording"):
    success, result = save_audio_recording(audio_data)
    if success:
        st.success(f"Recording saved as: {result}")
    else:
        st.error(f"Error saving recording: {result}")

#post audiofile send to backend... (post request with fastapi..)
#integration langchain
