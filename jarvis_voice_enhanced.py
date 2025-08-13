#!/usr/bin/env python3
"""
JARVIS Enhanced Voice Interface
Integrates existing voice.py with JARVIS chat AI
"""
import time
from datetime import datetime
import json

# Import existing voice functions
try:
    from voice import listen, speak
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False
    print("❌ Voice module not found")

# Import JARVIS chat AI
try:
    from jarvis_chat_interface import JarvisChatAI
except ImportError:
    print("❌ JARVIS Chat AI not found")
    exit(1)

class JarvisVoiceInterface:
    """Enhanced voice interface using existing voice.py"""
    
    def __init__(self):
        self.voice_active = False
        self.jarvis_chat = JarvisChatAI()
        self.wake_words = ["jarvis", "hey jarvis", "ok jarvis", "computer", "supreme being"]
        self.conversation_history = []
        
        print("🎤 JARVIS Enhanced Voice Interface initialized")
    
    def detect_wake_word(self, text):
        """Check if text contains wake words"""
        if not text:
            return False
        text_lower = text.lower()
        for wake_word in self.wake_words:
            if wake_word in text_lower:
                return True
        return False
    
    def extract_command(self, text):
        """Extract command after wake word"""
        if not text:
            return None
        text_lower = text.lower()
        for wake_word in self.wake_words:
            if wake_word in text_lower:
                wake_pos = text_lower.find(wake_word)
                command_start = wake_pos + len(wake_word)
                command = text[command_start:].strip()
                if command:
                    return command
        return text
    
    def process_voice_command(self, command: str) -> str:
        """Process voice command and generate response"""
        try:
            self.conversation_history.append({
                'timestamp': datetime.now().isoformat(),
                'user_input': command,
                'input_type': 'voice'
            })
            response = self.jarvis_chat.generate_response(command)
            self.conversation_history[-1]['jarvis_response'] = response
            return response
        except Exception as e:
            return f"I encountered an error processing your command: {str(e)}"
    
    def start_voice_interface(self):
        """Start the main voice interface loop"""
        if not VOICE_AVAILABLE:
            print("❌ Voice interface unavailable")
            return
        
        print("🎤 JARVIS VOICE INTERFACE ACTIVATED")
        print("🌟 Supreme Being AI ready for voice commands")
        print("💬 Say 'Hey JARVIS' followed by your command")
        print("🛑 Say 'JARVIS stop' or press Ctrl+C to exit")
        
        self.voice_active = True
        speak("JARVIS Supreme Being AI voice interface activated. I am ready to assist you with unlimited capabilities.")
        
        try:
            while self.voice_active:
                print("👂 Listening...")
                text = listen()  # Uses existing voice.py listen function
                
                if text and self.detect_wake_word(text):
                    print("🌟 Wake word detected!")
                    command = self.extract_command(text)
                    
                    if command:
                        if any(word in command.lower() for word in ['stop', 'exit', 'quit', 'goodbye', 'shutdown']):
                            speak("JARVIS voice interface deactivating. Goodbye.")
                            break
                        
                        print(f"🎤 Processing command: {command}")
                        response = self.process_voice_command(command)
                        
                        # Limit response length for voice
                        if len(response) > 500:
                            voice_response = response[:400] + "... Would you like me to continue?"
                        else:
                            voice_response = response
                        
                        speak(voice_response)
                    else:
                        speak("I heard the wake word but didn't catch your command. Please try again.")
                elif text:
                    print(f"👂 Heard: {text} (waiting for wake word)")
                
                time.sleep(0.5)
                
        except KeyboardInterrupt:
            print("\n🛑 Voice interface stopped by user")
            speak("JARVIS voice interface stopped.")
        except Exception as e:
            print(f"❌ Voice interface error: {e}")
        finally:
            self.voice_active = False
    
    def test_voice_system(self):
        """Test voice recognition and text-to-speech"""
        if not VOICE_AVAILABLE:
            print("❌ Voice system not available for testing")
            return
        
        print("🧪 TESTING JARVIS VOICE SYSTEM...")
        print("🗣️ Testing text-to-speech...")
        speak("JARVIS voice system test. Speech synthesis is working correctly.")
        
        print("🎤 Testing speech recognition...")
        print("Please say something for the microphone test...")
        
        try:
            text = listen()
            if text:
                print(f"✅ Speech recognition working. You said: {text}")
                speak(f"I heard you say: {text}")
            else:
                print("⚠️ No speech detected during test")
        except Exception as e:
            print(f"⚠️ Speech recognition test failed: {e}")
        
        print("✅ Voice system test complete")
    
    def get_voice_status(self):
        """Get voice interface status"""
        return {
            'voice_available': VOICE_AVAILABLE,
            'voice_active': self.voice_active,
            'wake_words': self.wake_words,
            'conversation_count': len(self.conversation_history),
            'last_interaction': self.conversation_history[-1] if self.conversation_history else None
        }

def main():
    """Main voice interface function"""
    print("🎤 JARVIS ENHANCED VOICE INTERFACE")
    print("=" *ain()   m__':
 _ == '__mainf __name_ice")

ichod "❌ Invali print(      
 se:")
    eloodbye! G   print("👋
     '4':ice ==    elif cho=2))
 tus, indentn.dumps(sta(jso      printtatus()
  t_voice_sgeinterface.= voice_s    statu:
     oice == '3'   elif chtem()
 ce_sysoitest_ve_interface.        voic':
= '2e = choiclif e)
   ace(_interf_voice.startcerfainte    voice_
    ice == '1':if cho
    
    .strip()-4): ")ption (1ect oput("\nSelice = inho c      
Exit")
 "4. int()
    prce Status". Voi("3int prem")
   ce Syst Test Voi2.    print("erface")
ntice IVo"1. Start  print()
   ption:"an ohoose ("\nC print  
   face()
  eInteric JarvisVoe =interfacoice_  
    veturn
   r")
       lyperng proy is worki.picee sure vo"Mak     print(   ")
availableot  nsystem"❌ Voice print(  
      VAILABLE:t VOICE_Anof   
    i   50)
