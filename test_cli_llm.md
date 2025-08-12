# Quick test of local LLM via CLI

1. Ensure model exists:
   - `ls -lh models/dolphin-2_6-phi-2.Q4_K_M.gguf`
2. Run CLI:
   - `python main.py --cli`
3. Set backend and model if needed:
   - `set backend local`
   - `set model /Users/syncsphere/Jarvis/models/dolphin-2_6-phi-2.Q4_K_M.gguf`
   - `save config`
4. Inline ask:
   - `ask Reply with exactly the single word: ready`

