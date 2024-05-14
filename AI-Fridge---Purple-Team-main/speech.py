import streamlit as st
from st_audiorec import st_audiorec
from openai import OpenAI
from pathlib import Path
import io
import tempfile
import os
from pydub import AudioSegment

client = OpenAI(api_key="OPEN_API_KEY") 


speech_file_path = Path(__file__).parent / "newfile.mp3"
# DESIGN implement changes to the standard streamlit UI/UX
# --> optional, not relevant for the functionality of the component!
st.set_page_config(page_title="Fridge Support")
# Design move app further up and remove top padding
st.markdown('''<style>.css-1egvi7u {margin-top: -3rem;}</style>''',
            unsafe_allow_html=True)
# Design change st.Audio to fixed height of 45 pixels
st.markdown('''<style>.stAudio {height: 45px;}</style>''',
            unsafe_allow_html=True)
# Design change hyperlink href link color
st.markdown('''<style>.css-v37k9u a {color: #ff4c4b;}</style>''',
            unsafe_allow_html=True)  # darkmode
st.markdown('''<style>.css-nlntq9 a {color: #ff4c4b;}</style>''',
            unsafe_allow_html=True)  # lightmode

def text_to_speech(text,path):
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=text
    )
    response.stream_to_file(speech_file_path)

def get_completion(prompt, model="gpt-3.5-turbo"):
   completion = client.chat.completions.create(
        model=model,
        messages=[
        {"role":"system",
         "content": "Your job is to help keep track of and give suggestions/recommendations based on user input/data."},
        {"role": "user",
         "content": prompt},
        ]
    )
   return completion.choices[0].message.content

def transcribe_audio(audio_data):
    # Convert audio data to WAV format using pydub
    audio_segment = AudioSegment(data=audio_data)
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
        temp_wav_path = temp_wav.name
        audio_segment.export(temp_wav_path, format="wav")

    # Open the temporary WAV file and send it to the OpenAI API
    with open(temp_wav_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )

    # Remove the temporary WAV file
    os.remove(temp_wav_path)

    return transcription.text

# Define Streamlit app function
def audiorec_demo_app():
    # Title and creator information
    st.title('Fridge Recommendation')
    st.write('\n\n')
    
    # Recording audio
    wav_audio_data = st_audiorec()
    
    # Display recorded audio
    if wav_audio_data is not None:
        st.audio(wav_audio_data, format='audio/wav')

    if st.button('Support'):
        if wav_audio_data is not None:
            transcription = transcribe_audio(wav_audio_data)
            #st.write(transcription)
            st.write(get_completion(transcription))
            st.write(text_to_speech(get_completion(transcription), speech_file_path))
            audio_file = open(speech_file_path, 'rb')
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format='audio/mp3')
    
if __name__ == '__main__':
    # call main function
    audiorec_demo_app()
