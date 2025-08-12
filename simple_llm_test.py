#!/usr/bin/env python3
import requests
import json

def test_ollama_direct():
    """Test Ollama directly"""
    url = "http://localhost:11434/api/generate"
    
    payload = {
        "model": "dolphin-phi",
        "prompt": "Hello, this is a test",
        "stream": False,
        "options": {
            "temperature": 0.8,
            "num_predict": 100
        }
    }
    
    try:
        print("Testing direct Ollama connection...")
        response = requests.post(url, json=payload, timeout=10)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Response: {result.get('response', 'No response')}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_ollama_direct()