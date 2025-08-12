import os
from core.brain.brain import Brain

model_path = "/Users/syncsphere/Jarvis/models/dolphin-2_6-phi-2.Q4_K_M.gguf"

b = Brain(backend="local", local_model_path=model_path, n_ctx=1024)
print("Loaded. Thinking...")
reply = b.think("Reply with exactly the single word: ready", max_tokens=16, temperature=0.1)
print("Model reply:", reply)

