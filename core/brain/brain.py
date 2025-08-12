"""
Brain abstraction with pluggable backends (local llama.cpp or cloud).
No guardrails are applied here; prompts are sent as-is to the selected backend.
Configure via environment variables:
- JARVIS_BACKEND: "local" or "cloud" (default: "local")
- JARVIS_LOCAL_MODEL_PATH: path to GGUF model (e.g., Dolphin *.gguf)
- JARVIS_N_THREADS: CPU threads (default: max available - 1)
- JARVIS_N_CTX: context size tokens (default: 1024)
- OPENAI_API_KEY: for cloud backend
"""
from __future__ import annotations

import os
from typing import Optional


from core.utils.config import Config, DEFAULT_PATH

class Brain:
    def __init__(self,
                 backend: Optional[str] = None,
                 local_model_path: Optional[str] = None,
                 n_threads: Optional[int] = None,
                 n_ctx: Optional[int] = None,
                 config: Optional[Config] = None):
        cfg = config or Config.load_default()
        self.backend = (backend or cfg.backend or os.getenv("JARVIS_BACKEND") or "local").lower()
        self.local_model_path = local_model_path or cfg.local_model_path or os.getenv("JARVIS_LOCAL_MODEL_PATH")
        # Sensible defaults for an 8GB Intel Mac
        cpu_count = os.cpu_count() or 2
        self.n_threads = n_threads or cfg.n_threads or int(os.getenv("JARVIS_N_THREADS", str(max(1, cpu_count - 1))))
        self.n_ctx = n_ctx or cfg.n_ctx or int(os.getenv("JARVIS_N_CTX", "1024"))
        self._config = cfg

        self._llama = None
        self._openai = None
        self._gemini = None
        self._cloud_provider = None

        if self.backend == "local":
            self._init_local()
        elif self.backend == "cloud":
            self._init_cloud()
        else:
            raise ValueError(f"Unknown backend: {self.backend}")

    # --- Backends ---
    def _init_local(self) -> None:
        try:
            from llama_cpp import Llama  # type: ignore
        except Exception as e:  # pragma: no cover
            raise RuntimeError(f"llama-cpp-python not available: {e}")

        if not self.local_model_path or not os.path.exists(self.local_model_path):
            raise FileNotFoundError(
                "JARVIS_LOCAL_MODEL_PATH is not set or model file not found."
            )

        # Conservative settings for Intel macOS to avoid segfaults
        safe_threads = min(2, self.n_threads)  # Limit to 2 threads max
        safe_ctx = min(512, self.n_ctx)        # Smaller context window

        try:
            # Initialize llama.cpp LLM with safe parameters
            self._llama = Llama(
                model_path=self.local_model_path,
                n_ctx=safe_ctx,
                n_threads=safe_threads,
                verbose=False,
                use_mlock=False,  # Disable memory locking
                use_mmap=True,    # Use memory mapping
                n_gpu_layers=0,   # Force CPU-only
            )
        except Exception as e:
            # If local fails, log and suggest cloud fallback
            print(f"Local LLM failed to initialize: {e}")
            print("Suggestion: Use 'set backend cloud' and set OPENAI_API_KEY")
            raise RuntimeError(f"Local LLM initialization failed: {e}")

    def _init_cloud(self) -> None:
        # Try Gemini first, fallback to OpenAI
        gemini_key = os.getenv("GEMINI_API_KEY")
        openai_key = os.getenv("OPENAI_API_KEY")

        if gemini_key:
            try:
                import google.generativeai as genai  # type: ignore
                genai.configure(api_key=gemini_key)
                self._gemini = genai.GenerativeModel('gemini-1.5-flash')
                self._cloud_provider = "gemini"
                return
            except Exception as e:
                print(f"Gemini initialization failed: {e}")

        if openai_key:
            try:
                from openai import OpenAI  # type: ignore
                self._openai = OpenAI()
                self._cloud_provider = "openai"
                return
            except Exception as e:
                print(f"OpenAI initialization failed: {e}")

        raise RuntimeError("No cloud provider available. Set GEMINI_API_KEY or OPENAI_API_KEY.")

    # --- API ---
    def set_backend(self, backend: str) -> None:
        backend = backend.lower()
        if backend == self.backend:
            return
        self.backend = backend
        if backend == "local":
            self._init_local()
        elif backend == "cloud":
            self._init_cloud()
        else:
            raise ValueError(f"Unknown backend: {backend}")

    def save_config(self) -> None:
        self._config.backend = self.backend
        self._config.local_model_path = self.local_model_path
        self._config.n_threads = self.n_threads
        self._config.n_ctx = self.n_ctx
        self._config.save()

    def think(self, prompt: str, max_tokens: int = 256, temperature: float = 0.7) -> str:
        if self.backend == "local":
            if self._llama is None:
                self._init_local()
            # Use text completion API for robustness
            result = self._llama.create_completion(
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=0.95,
            )
            text = result.get("choices", [{}])[0].get("text", "")
            return text.strip()
        else:  # cloud
            if self._cloud_provider is None:
                self._init_cloud()

            if self._cloud_provider == "gemini":
                response = self._gemini.generate_content(
                    prompt,
                    generation_config={
                        "max_output_tokens": max_tokens,
                        "temperature": temperature,
                    }
                )
                return response.text.strip()

            elif self._cloud_provider == "openai":
                resp = self._openai.chat.completions.create(
                    model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_tokens,
                    temperature=temperature,
                )
                msg = resp.choices[0].message.content
                return (msg or "").strip()

            else:
                raise RuntimeError("No cloud provider initialized")

