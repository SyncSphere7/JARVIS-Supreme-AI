import whisper, pyttsx3
import sounddevice as sd
import numpy as np

model = whisper.load_model("tiny")  # 1GB RAM usage
engine = pyttsx3.init()

SAMPLE_RATE = 16000

def listen():
    print("Recording 5s...")
    audio = sd.rec(int(5 * SAMPLE_RATE),
                  samplerate=SAMPLE_RATE,
                  channels=1,
                  dtype='float32')
    sd.wait()
    audio = audio.flatten()
    return model.transcribe(audio.astype(np.float32))["text"]

def speak(text):
    engine.say(text)
    engine.runAndWait()