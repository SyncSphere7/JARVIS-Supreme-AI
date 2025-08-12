"""Lightweight JSON config for Jarvis.
Stores backend and local model settings.
"""
from __future__ import annotations

import json
import os
from typing import Optional

DEFAULT_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "jarvis_config.json")


class Config:
    def __init__(self,
                 backend: str = "local",
                 local_model_path: Optional[str] = None,
                 n_threads: Optional[int] = None,
                 n_ctx: Optional[int] = None):
        self.backend = backend
        self.local_model_path = local_model_path
        self.n_threads = n_threads
        self.n_ctx = n_ctx

    @classmethod
    def load(cls, path: str) -> "Config":
        try:
            with open(path, "r") as f:
                data = json.load(f)
            return cls(
                backend=data.get("backend", "local"),
                local_model_path=data.get("local_model_path"),
                n_threads=data.get("n_threads"),
                n_ctx=data.get("n_ctx"),
            )
        except FileNotFoundError:
            return cls()

    @classmethod
    def load_default(cls) -> "Config":
        return cls.load(DEFAULT_PATH)

    def save(self, path: str = DEFAULT_PATH) -> None:
        data = {
            "backend": self.backend,
            "local_model_path": self.local_model_path,
            "n_threads": self.n_threads,
            "n_ctx": self.n_ctx,
        }
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

