"""Download a Dolphin GGUF model from Hugging Face using huggingface_hub.
Usage (example):
    python -m Jarvis.tools.download_dolphin --repo TheBloke/dolphin-2_7b-mistral-GGUF --filename dolphin-2_7b-mistral.Q4_K_M.gguf --out ./models
"""
from __future__ import annotations

import argparse
import os
from huggingface_hub import hf_hub_download


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--repo", required=True, help="HuggingFace repo id")
    p.add_argument("--filename", required=True, help="GGUF filename in the repo")
    p.add_argument("--out", default="./models", help="Output directory")
    args = p.parse_args()

    os.makedirs(args.out, exist_ok=True)
    path = hf_hub_download(repo_id=args.repo, filename=args.filename, local_dir=args.out)
    print(f"Downloaded to: {path}")


if __name__ == "__main__":
    main()

