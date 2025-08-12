
import numpy as np
import sounddevice as sd
import whisper
import time
from sys import exit

from core.utils.log import logger

class JarvisVoice:
    def __init__(self, command_manager):
        self.command_manager = command_manager
        self.sample_rate = 16000
        self.record_duration = 2
        self.wake_words = ["jarvis", "hey jarvis"]
        self.whisper_model = "tiny.en"
        self.model = whisper.load_model(self.whisper_model)

    def list_devices(self):
        """Show available audio devices"""
        print("\n🔊 Available Audio Devices:")
        devices = sd.query_devices()
        for i, dev in enumerate(devices):
            print(f"{i}: {dev['name']} (Inputs: {dev['max_input_channels']})")

    def record_audio(self, duration, device=None):
        """Record audio with error handling"""
        try:
            logger.info(f"Recording {duration}s...")
            audio = sd.rec(
                int(duration * self.sample_rate),
                samplerate=self.sample_rate,
                channels=1,
                dtype='float32',
                device=device
            )
            sd.wait()  # Wait until recording finishes
            return audio.flatten()
        except Exception as e:
            logger.error(f"Recording Error: {str(e)}")
            return None

    def transcribe_audio(self, audio):
        """Convert speech to text using Whisper"""
        if audio is None or len(audio) == 0:
            return ""
        
        try:
            result = self.model.transcribe(audio.astype(np.float32))
            return result["text"].strip().lower()
        except Exception as e:
            logger.error(f"Transcription Error: {str(e)}")
            return ""

    def detect_wake_word(self, debug=False):
        """Core wake word detection logic"""
        audio = self.record_audio(duration=self.record_duration)
        if audio is None:
            return False
        
        text = self.transcribe_audio(audio)
        if debug:
            logger.info(f"Heard: '{text}'")
        
        return any(trigger in text for trigger in self.wake_words)

    def process_command(self):
        """Records and processes a command after wake word detection."""
        logger.info("Listening for command...")
        command_audio = self.record_audio(duration=5)
        if command_audio is None:
            return

        command_text = self.transcribe_audio(command_audio)
        logger.info(f"Command heard: '{command_text}'")

        self.command_manager.execute_command(command_text)

    def start(self):
        """Main loop for the voice system."""
        logger.info("JARVIS Voice System is running...")
        self.list_devices()
        
        try:
            while True:
                if self.detect_wake_word(debug=True):
                    logger.info("Wake word detected! Ready for commands.")
                    self.process_command()
                    time.sleep(1)
                else:
                    logger.info("No wake word detected. Trying again...")
                    time.sleep(0.5)
                    
        except KeyboardInterrupt:
            logger.info("System stopped by user")
            exit(0)
