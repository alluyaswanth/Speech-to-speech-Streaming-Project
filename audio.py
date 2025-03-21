import os
import whisper
import langchain
from langchain_community.llms import OpenAI
from deep_translator import GoogleTranslator
from gtts import gTTS
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip

# Load Whisper model
def extract_audio_from_video(video_path, audio_output):
    """Extracts audio from video"""
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_output)

def speech_to_text(audio_path):
    """Convert extracted audio to text using Whisper"""
    model = whisper.load_model("base")
    result = model.transcribe("extracted_audio.wav", language="hi")
    return result["text"]

def translate_text(text, target_lang="hi"):
    """Translate text using Google Translate"""
    return GoogleTranslator(source="auto", target=target_lang).translate(text)

def text_to_speech(text, lang="en", output_audio="translated_audio.mp3"):
    """Convert translated text to speech"""
    tts = gTTS(text, lang=lang)
    tts.save(output_audio)

def merge_audio_with_video(video_path, audio_path, output_video):
    """Merge the translated audio with the original video"""
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)
    final_video = video.with_audio(audio)
    final_video.write_videofile(output_video, codec="libx264", audio_codec="aac")

# Pipeline Execution
video_path = "input_video.mp4"
audio_path = "extracted_audio.wav"
translated_audio_path = "translated_audio.mp3"
output_video_path = "final_video.mp4"

# Step 1: Extract Audio
extract_audio_from_video(video_path, audio_path)

# Step 2: Convert Audio to Text
text = speech_to_text(audio_path)
print("Original Text:", text)

# Step 3: Translate Text
translated_text = translate_text(text, "hi")
print("Translated Text:", translated_text)

# Step 4: Convert Translated Text to Speech
text_to_speech(translated_text, "hi", translated_audio_path)

# Step 5: Merge Audio with Original Video
merge_audio_with_video(video_path, translated_audio_path, output_video_path)

print("Process Complete! Output video saved as:", output_video_path)
