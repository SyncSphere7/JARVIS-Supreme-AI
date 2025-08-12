import os
from pathlib import Path

def setup_jarvis():
    # Create directory structure
    os.makedirs("core/voice", exist_ok=True)
    
    # 1. Create wakeword.py
    wakeword_code = """import numpy as np
from core.voice.listen import record_audio, transcribe_audio

def detect_wake_word(confidence=0.85):
    \"\"\"Detects 'Jarvis' wake word\"\"\"
    try:
        audio = record_audio(2)
        text = transcribe_audio(audio).strip().lower()
        triggers = ["jarvis", "hey jarvis", "ok jarvis"]
        return any(trigger in text for trigger in triggers)
    except Exception as e:
        print(f"Wake word error: {str(e)}")
        return False
"""
    Path("core/voice/wakeword.py").write_text(wakeword_code)

    # 2. Create listen.py
    listen_code = """import sounddevice as sd
import numpy as np
import whisper

SAMPLE_RATE = 16000

def record_audio(duration=3):
    print(f"Recording {duration}s...")
    audio = sd.rec(int(duration * SAMPLE_RATE),
                  samplerate=SAMPLE_RATE,
                  channels=1,
                  dtype='float32')
    sd.wait()
    return audio.flatten()

def transcribe_audio(audio=None):
    model = whisper.load_model("tiny.en")
    result = model.transcribe(audio if audio else record_audio())
    return result["text"].strip()
"""
    Path("core/voice/listen.py").write_text(listen_code)

    # 3. Create test script
    test_code = """from core.voice.wakeword import detect_wake_word

print("Say 'Jarvis' when prompted...")
if detect_wake_word():
    print("Wake word detected!")
else:
    print("Not detected")
"""
    Path("test_jarvis.py").write_text(test_code)

    # 4. Create requirements
    Path("requirements.txt").write_text("""numpy==1.26.4
sounddevice==0.4.6
whisper==1.1.10
scipy==1.11.4
torch==2.2.1
""")

    print("Setup complete! Run:")
    print("1. pip install -r requirements.txt")
    print("2. python test_jarvis.py")

if __name__ == "__main__":
    setup_jarvis()
