"""
JARVIS Voice Interface - Speech Recognition and Text-to-Speech
Advanced voice capabilities for natural interaction with JARVIS
"""

import asyncio
import threading
import time
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import os

try:
    import speech_recognition as sr
    import pyttsx3
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False
    print("⚠️ Voice libraries not installed. Run: pip install SpeechRecognition pyttsx3 pyaudio")

class VoiceInterface:
    """Advanced voice interface for JARVIS"""
    
    def __init__(self):
        self.voice_active = False
        self.listening = False
        self.speaking = False
        
        # Voice settings
        self.voice_settings = {
            'rate': 180,  # Speech rate
            'volume': 0.9,  # Volume level
            'voice_id': 0,  # Voice selection
            'language': 'en-US',  # Language
            'wake_word': 'jarvis',  # Wake word
            'continuous_listening': False
        }
        
        # Voice history
        self.voice_history = []
        self.recognition_accuracy = 0.85
        
        if VOICE_AVAILABLE:
            self.initialize_voice_interface()
        else:
            print("❌ Voice interface unavailable - missing dependencies")
    
    def initialize_voice_interface(self):
        """Initialize voice interface components"""
        print("🎤 INITIALIZING VOICE INTERFACE...")
        print("⚡ Setting up speech recognition")
        print("🔊 Configuring text-to-speech")
        
        try:
            # Initialize speech recognition
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            
            # Initialize text-to-speech
            self.tts_engine = pyttsx3.init()
            self._configure_voice()
            
            # Calibrate microphone
            self._calibrate_microphone()
            
            self.voice_active = True
            print("✅ Voice Interface active - Speech capabilities enabled")
            
        except Exception as e:
            print(f"❌ Voice initialization error: {e}")
            self.voice_active = False
    
    def _configure_voice(self):
        """Configure text-to-speech voice"""
        try:
            # Set voice properties
            self.tts_engine.setProperty('rate', self.voice_settings['rate'])
            self.tts_engine.setProperty('volume', self.voice_settings['volume'])
            
            # Get available voices
            voices = self.tts_engine.getProperty('voices')
            if voices and len(voices) > self.voice_settings['voice_id']:
                self.tts_engine.setProperty('voice', voices[self.voice_settings['voice_id']].id)
                print(f"🔊 Voice configured: {voices[self.voice_settings['voice_id']].name}")
            
        except Exception as e:
            print(f"⚠️ Voice configuration error: {e}")
    
    def _calibrate_microphone(self):
        """Calibrate microphone for ambient noise"""
        try:
            print("🎤 Calibrating microphone for ambient noise...")
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("✅ Microphone calibrated")
            
        except Exception as e:
            print(f"⚠️ Microphone calibration error: {e}")
    
    async def speak(self, text: str, interrupt_current: bool = False) -> bool:
        """Convert text to speech"""
        if not self.voice_active:
            print(f"🔊 [VOICE DISABLED] JARVIS: {text}")
            return False
        
        try:
            if interrupt_current and self.speaking:
                self.tts_engine.stop()
            
            self.speaking = True
            
            # Clean text for speech
            speech_text = self._prepare_text_for_speech(text)
            
            print(f"🔊 JARVIS Speaking: {speech_text}")
            
            # Speak text
            self.tts_engine.say(speech_text)
            self.tts_engine.runAndWait()
            
            self.speaking = False
            
            # Log speech
            self.voice_history.append({
                'type': 'speech',
                'text': speech_text,
                'timestamp': datetime.now().isoformat()
            })
            
            return True
            
        except Exception as e:
            print(f"❌ Speech error: {e}")
            self.speaking = False
            return False
    
    def _prepare_text_for_speech(self, text: str) -> str:
        """Prepare text for natural speech"""
        # Remove markdown and special characters
        speech_text = text.replace('**', '').replace('*', '')
        speech_text = speech_text.replace('🤖', '').replace('⚡', '').replace('🌟', '')
        speech_text = speech_text.replace('💀', '').replace('🔓', '').replace('🌐', '')
        
        # Replace technical terms with pronounceable versions
        replacements = {
            'JARVIS': 'Jarvis',
            'AI': 'A I',
            'API': 'A P I',
            'SQL': 'S Q L',
            'XSS': 'Cross Site Scripting',
            'VPN': 'V P N',
            'Tor': 'Tor',
            'URL': 'U R L',
            'HTTP': 'H T T P',
            'HTTPS': 'H T T P S'
        }
        
        for term, replacement in replacements.items():
            speech_text = speech_text.replace(term, replacement)
        
        # Limit length for natural speech
        if len(speech_text) > 300:
            speech_text = speech_text[:300] + "... and more."
        
        return speech_text
    
    async def listen(self, timeout: float = 5.0, phrase_timeout: float = 1.0) -> Optional[str]:
        """Listen for speech input"""
        if not self.voice_active:
            print("❌ Voice interface not available")
            return None
        
        try:
            self.listening = True
            print("🎤 Listening...")
            
            with self.microphone as source:
                # Listen for audio
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_timeout)
            
            print("🧠 Processing speech...")
            
            # Recognize speech
            text = self.recognizer.recognize_google(audio, language=self.voice_settings['language'])
            
            self.listening = False
            
            print(f"👤 You said: {text}")
            
            # Log recognition
            self.voice_history.append({
                'type': 'recognition',
                'text': text,
                'confidence': self.recognition_accuracy,
                'timestamp': datetime.now().isoformat()
            })
            
            return text
            
        except sr.WaitTimeoutError:
            print("⏰ Listening timeout")
            self.listening = False
            return None
        except sr.UnknownValueError:
            print("❌ Could not understand speech")
            self.listening = False
            return None
        except sr.RequestError as e:
            print(f"❌ Speech recognition error: {e}")
            self.listening = False
            return None
        except Exception as e:
            print(f"❌ Listening error: {e}")
            self.listening = False
            return None
    
    async def voice_conversation_loop(self, response_callback=None):
        """Start continuous voice conversation"""
        if not self.voice_active:
            print("❌ Voice interface not available")
            return
        
        print("🎤 STARTING VOICE CONVERSATION MODE...")
        await self.speak("Voice interface activated. I am listening for your commands.")
        
        conversation_active = True
        
        while conversation_active:
            try:
                # Listen for wake word or direct command
                if self.voice_settings['wake_word']:
                    print(f"🎤 Say '{self.voice_settings['wake_word']}' to activate...")
                
                # Listen for input
                user_input = await self.listen(timeout=10.0)
                
                if user_input:
                    # Check for wake word
                    if self.voice_settings['wake_word'] and self.voice_settings['wake_word'].lower() not in user_input.lower():
                        continue
                    
                    # Remove wake word from input
                    if self.voice_settings['wake_word']:
                        user_input = user_input.lower().replace(self.voice_settings['wake_word'].lower(), '').strip()
                    
                    if not user_input:
                        await self.speak("Yes? How may I assist you?")
                        user_input = await self.listen(timeout=10.0)
                    
                    if user_input:
                        # Check for exit commands
                        if any(word in user_input.lower() for word in ['stop', 'exit', 'quit', 'goodbye']):
                            await self.speak("Voice interface deactivated. Goodbye!")
                            conversation_active = False
                            break
                        
                        # Process command with callback
                        if response_callback:
                            response = await response_callback(user_input)
                            if response:
                                await self.speak(response)
                        else:
                            await self.speak(f"I heard: {user_input}. Voice interface is working correctly.")
                
                # Small delay between listening cycles
                await asyncio.sleep(0.5)
                
            except KeyboardInterrupt:
                await self.speak("Voice conversation stopped.")
                conversation_active = False
                break
            except Exception as e:
                print(f"❌ Voice conversation error: {e}")
                await asyncio.sleep(2)
        
        print("🎤 Voice conversation ended")
    
    def set_voice_settings(self, **settings):
        """Update voice settings"""
        for key, value in settings.items():
            if key in self.voice_settings:
                self.voice_settings[key] = value
                print(f"🔧 Voice setting updated: {key} = {value}")
        
        # Reconfigure if TTS engine exists
        if hasattr(self, 'tts_engine'):
            self._configure_voice()
    
    def get_voice_status(self) -> Dict[str, Any]:
        """Get voice interface status"""
        return {
            'voice_active': self.voice_active,
            'listening': self.listening,
            'speaking': self.speaking,
            'voice_available': VOICE_AVAILABLE,
            'settings': self.voice_settings.copy(),
            'recognition_accuracy': self.recognition_accuracy,
            'voice_history_count': len(self.voice_history),
            'capabilities': [
                'Speech Recognition',
                'Text-to-Speech',
                'Continuous Listening',
                'Wake Word Detection',
                'Voice Conversation Mode',
                'Multi-language Support'
            ] if VOICE_AVAILABLE else ['Voice interface disabled - missing dependencies'],
            'last_updated': datetime.now().isoformat()
        }

# Global voice interface instance
voice_interface = VoiceInterface()