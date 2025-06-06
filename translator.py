import os
import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
from pydub import AudioSegment

# Định nghĩa các thư mục
input_folder = "inputs"
output_folder = "outputs"
temp_folder = "temp"

# Đảm bảo thư mục tồn tại
os.makedirs(temp_folder, exist_ok=True)
os.makedirs(output_folder, exist_ok=True)

# Kiểm tra thư mục đầu vào
if not os.path.exists(input_folder):
    print(f"Thư mục {input_folder} không tồn tại!")
    exit(1)

# Chuyển đổi file MP3 sang WAV và lưu vào thư mục temp
def convert_mp3_to_wav(mp3_path):
    temp_wav = os.path.join(temp_folder, os.path.basename(mp3_path).replace(".mp3", ".wav"))
    audio = AudioSegment.from_file(mp3_path, format="mp3")
    audio.export(temp_wav, format="wav")
    return temp_wav

# Nhận diện giọng nói từ file WAV
def transcribe_audio(file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data, language='en-US') #zh-CN
    return text

# Dịch văn bản sang tiếng Việt
def translate_text(text):
    translator = GoogleTranslator(source='auto', target='vi')
    return translator.translate(text)

# Chuyển đổi văn bản sang giọng nói tiếng Việt
def text_to_speech(text, output_path):
    tts = gTTS(text=text, lang='vi')
    tts.save(output_path)

# Xử lý tất cả các file MP3 trong thư mục inputs
try:
    for filename in os.listdir(input_folder):
        if filename.endswith(".mp3"):
            try:
                input_mp3 = os.path.join(input_folder, filename)
                temp_wav = convert_mp3_to_wav(input_mp3)
                output_mp3 = os.path.join(output_folder, filename)

                text = transcribe_audio(temp_wav)
                translated_text = translate_text(text)
                print(f"{filename}: {translated_text}")

                text_to_speech(translated_text, output_mp3)

                # Xóa file WAV trung gian sau khi hoàn tất
                os.remove(temp_wav)
            except Exception as e:
                print(f"Lỗi khi xử lý {filename}: {e}")
except KeyboardInterrupt:
    print("\nQuá trình bị hủy bởi người dùng.")
