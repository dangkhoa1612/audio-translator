import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS

from pydub import AudioSegment

def convert_mp3_to_wav(mp3_path, wav_path):
    audio = AudioSegment.from_file(mp3_path, format="mp3")
    audio.export(wav_path, format="wav")

# Nhận diện giọng nói từ file MP3
def transcribe_audio(file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data, language='zh-CN') # hoặc 'en-US'
    return text

# Dịch văn bản sang tiếng Việt
def translate_text(text):
    print(text)
    translator = GoogleTranslator(source='auto', target='vi')
    return translator.translate(text)

# Chuyển đổi văn bản sang giọng nói tiếng Việt
def text_to_speech(text, output_path):
    tts = gTTS(text=text, lang='vi')
    tts.save(output_path)

# Main function
def convert_mp3(input_mp3, output_mp3):
    text = transcribe_audio(input_mp3)
    translated_text = translate_text(text)
    print(translated_text)
    text_to_speech(translated_text, output_mp3)

# Ví dụ sử dụng
mp3_file = "1310.mp3" 
wav_file = "output.wav" 
output_file = "output.mp3" 

convert_mp3_to_wav(mp3_file, wav_file)

convert_mp3(wav_file, output_file)
