import os
import subprocess

def record_sox(duration=3, filename="recording.wav"):
    try:
        subprocess.run([
            'sox',
            '-d',  # Default audio device
            '-t', 'waveaudio',  # File type
            filename,
            'trim', '0', str(duration)
        ], check=True)
        return True
    except:
        return False
