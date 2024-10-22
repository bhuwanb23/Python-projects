import os
import openai
import requests
import json
from moviepy.editor import VideoFileClip, AudioFileClip
import speech_recognition as sr
from gtts import gTTS

# Azure OpenAI connection details (replace with your actual API key and endpoint)
azure_openai_key = "22ec84421ec24230a3638d1b51e3a7dc"
azure_openai_endpoint = "https://internshala.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-08-01-preview"

def transcribe_audio(audio_file):
    """Transcribes audio using SpeechRecognition (Google Web Speech API)."""
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)

    try:
        # Google Web Speech API is used by default
        transcription = recognizer.recognize_google(audio)
        print("Original Transcription: ", transcription)
        return transcription
    except sr.UnknownValueError:
        print("Google Web Speech could not understand the audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Web Speech service; {e}")

    return ""

def correct_transcript_with_gpt4o(transcript):
    """Sends the transcription to Azure OpenAI's GPT-4o model to correct it."""
    headers = {
        "Content-Type": "application/json",
        "api-key": azure_openai_key
    }

    data = {
        "messages": [{"role": "user", "content": transcript}],
        "max_tokens": 1000
    }

    response = requests.post(azure_openai_endpoint, headers=headers, json=data)
    
    if response.status_code == 200:
        result = response.json()
        corrected_text = result["choices"][0]["message"]["content"].strip()
        print("Corrected Transcription: ", corrected_text)
        return corrected_text
    else:
        print(f"Failed to retrieve GPT-4o response: {response.status_code} - {response.text}")
        return None

def text_to_speech(corrected_text):
    """Converts corrected text to speech using gTTS."""
    tts = gTTS(text=corrected_text, lang='en')
    audio_output = 'output_audio.mp3'
    tts.save(audio_output)
    print(f"Generated new audio: {audio_output}")
    return audio_output

def replace_audio_in_video(video_clip, new_audio_file):
    """Replaces the audio in the original video with the AI-generated audio."""
    # Load the new audio file
    new_audio = AudioFileClip(new_audio_file)
    
    # Set the new audio to the video
    final_clip = video_clip.set_audio(new_audio)
    
    # Write the result to a new video file
    output_video_file = "output_video.mp4"
    final_clip.write_videofile(output_video_file, codec="libx264", audio_codec="aac")
    print(f"Video with new audio saved as {output_video_file}")
    return output_video_file

def main():
    # Step 1: Upload a video file
    video_file_path = input("Enter the path to the video file: ")
    
    if not os.path.exists(video_file_path):
        print("Video file not found!")
        return

    # Load video and extract audio
    video_clip = VideoFileClip(video_file_path)
    audio_file_path = "extracted_audio.wav"
    video_clip.audio.write_audiofile(audio_file_path)
    print(f"Extracted audio saved as {audio_file_path}")

    # Step 2: Transcribe the audio
    transcript = transcribe_audio(audio_file_path)

    if transcript:
        # Step 3: Correct transcription using GPT-4o
        corrected_text = correct_transcript_with_gpt4o(transcript)

        if corrected_text:
            # Step 4: Convert corrected text to speech
            new_audio_file = text_to_speech(corrected_text)

            # Step 5: Replace original audio with AI-generated audio in the video
            replace_audio_in_video(video_clip, new_audio_file)

if __name__ == "__main__":
    main()
