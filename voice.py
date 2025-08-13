import whisper, pyttsx3
import sounddevice as sd
import numpy as np
import warnings

# Suppress the FP16 warning
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

model = whisper.load_model("tiny")  # 1GB RAM usage
engine = pyttsx3.init()

# Configure JARVIS voice settings for natural male voice
def configure_jarvis_voice():
    """Configure JARVIS to have a natural male voice"""
    voices = engine.getProperty('voices')
    
    # Set speech rate (slower for more natural speech)
    engine.setProperty('rate', 140)  # Even slower, more conversational pace
    
    # Set volume
    engine.setProperty('volume', 0.9)
    
    # Preferred male voices in order of preference
    preferred_male_voices = [
        'Alex',           # Classic Mac male voice
        'Daniel',         # British male voice
        'Fred',           # US male voice
        'Thomas',         # French male voice
        'Rishi',          # Indian male voice
        'Majed',          # Arabic male voice
        'Xander'          # Dutch male voice
    ]
    
    # Try to find a preferred male voice
    male_voice = None
    if voices:
        # First, try to find Alex (best quality male voice on Mac)
        for voice in voices:
            if voice.name == 'Alex':
                male_voice = voice
                break
        
        # If Alex not found, try other preferred male voices
        if not male_voice:
            for preferred in preferred_male_voices:
                for voice in voices:
                    if preferred.lower() in voice.name.lower():
                        male_voice = voice
                        break
                if male_voice:
                    break
        
        # If we found a male voice, use it
        if male_voice:
            engine.setProperty('voice', male_voice.id)
            print(f"🗣️ JARVIS voice configured: {male_voice.name}")
        else:
            # Use the first available voice if no male voice found
            if len(voices) > 0:
                engine.setProperty('voice', voices[0].id)
                print(f"🗣️ JARVIS voice configured: {voices[0].name}")

# Configure the voice when module loads
configure_jarvis_voice()

SAMPLE_RATE = 16000

def listen():
    print("👂 Listening...")
    audio = sd.rec(int(5 * SAMPLE_RATE),
                  samplerate=SAMPLE_RATE,
                  channels=1,
                  dtype='float32')
    sd.wait()
    audio = audio.flatten()
    
    # Suppress whisper warnings during transcription
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        result = model.transcribe(audio.astype(np.float32))
    
    return result["text"]

def speak(text):
    """Make JARVIS speak with natural human-like speech"""
    # Process text to make it more natural
    natural_text = make_speech_natural(text)
    
    print(f"🗣️ JARVIS: {natural_text}")
    engine.say(natural_text)
    engine.runAndWait()

def make_speech_natural(text):
    """Process text to make JARVIS sound more natural and human-like"""
    # Remove overly robotic phrases and make more conversational
    natural_replacements = {
        "I am JARVIS": "I'm JARVIS",
        "I will": "I'll",
        "I have": "I've", 
        "I would": "I'd",
        "cannot": "can't",
        "do not": "don't",
        "will not": "won't",
        "should not": "shouldn't",
        "could not": "couldn't",
        "would not": "wouldn't",
        "Supreme Being AI": "your AI assistant",
        "unlimited capabilities": "advanced capabilities",
        "transcendent": "advanced",
        "Supreme Being": "advanced AI",
        "at your service": "here to help",
        "How may I assist you": "How can I help you",
        "I shall": "I'll",
        "processing your request": "working on that",
        "executing command": "got it",
        "affirmative": "yes",
        "negative": "no",
        "acknowledged": "understood",
        "initiating": "starting",
        "terminating": "stopping",
        "optimal": "best",
        "facilitate": "help with",
        "endeavor": "try",
        "commence": "start",
        "utilize": "use",
        "implement": "do",
        "execute": "run"
    }
    
    # Apply natural replacements
    natural_text = text
    for robotic, natural in natural_replacements.items():
        natural_text = natural_text.replace(robotic, natural)
    
    # Add natural speech patterns
    if natural_text.startswith("I can"):
        natural_text = natural_text.replace("I can", "I can definitely", 1)
    
    # Add casual connectors for longer responses
    if len(natural_text) > 100:
        natural_text = natural_text.replace(". ", ". So, ", 1)
    
    return natural_text

def get_voice_info():
    """Get information about available voices"""
    voices = engine.getProperty('voices')
    voice_info = []
    
    if voices:
        for i, voice in enumerate(voices):
            voice_info.append({
                'id': i,
                'name': voice.name,
                'languages': getattr(voice, 'languages', []),
                'gender': getattr(voice, 'gender', 'Unknown')
            })
    
    return voice_info

def set_voice_by_name(voice_name):
    """Set voice by name"""
    voices = engine.getProperty('voices')
    if voices:
        for voice in voices:
            if voice_name.lower() in voice.name.lower():
                engine.setProperty('voice', voice.id)
                print(f"🗣️ Voice changed to: {voice.name}")
                return True
    return False