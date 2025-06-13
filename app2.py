import streamlit as st
import requests
import os
from datetime import datetime

# Configure the page
st.set_page_config(
    page_title="Audio Transcription App",
    page_icon="🎙️",
    layout="wide"
)

# API endpoint
API_URL = "http://localhost:8000"

def main():
    st.title("🎙️ Audio Transcription")
    st.write("Upload an audio file to get it transcribed using Whisper AI")

    # File uploader
    uploaded_file = st.file_uploader("Choose an audio file", type=['wav', 'mp3', 'm4a'])

    if uploaded_file is not None:
        # Display audio player
        st.audio(uploaded_file, format='audio/wav')

        # Transcribe button
        if st.button("Transcribe"):
            with st.spinner("Transcribing audio..."):
                try:
                    # Prepare the file for upload
                    files = {"file": (uploaded_file.name, uploaded_file, "audio/wav")}
                    
                    # Send request to API
                    response = requests.post(f"{API_URL}/transcribe", files=files)
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        if result["status"] == "success":
                            # Display transcription
                            st.success("Transcription completed!")
                            st.write("### Transcription:")
                            st.write(result["transcription"])
                            
                            # Display saved file path
                            st.info(f"Transcription saved to: {result['saved_file']}")
                        else:
                            st.error(f"Error: {result['message']}")
                    else:
                        st.error(f"Error: API returned status code {response.status_code}")
                        
                except Exception as e:
                    st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 