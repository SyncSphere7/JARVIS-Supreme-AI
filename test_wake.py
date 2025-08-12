from jarvis_voice import JarvisVoice
from core.brain.command_manager import CommandManager

print("== Wake Word Test ==")
print("Say 'Jarvis' or 'Hey Jarvis' when prompted")

voice = JarvisVoice(CommandManager())

try:
    while True:
        input("Press Enter to test (Ctrl+C to quit)...")
        if voice.detect_wake_word(debug=True):
            print(">> Wake word DETECTED")
        else:
            print(">> No wake word")
except KeyboardInterrupt:
    print("\nExiting.")
