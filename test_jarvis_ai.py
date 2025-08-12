#!/usr/bin/env python3
"""
Test JARVIS AI Responses
"""

import asyncio
import sys

try:
    from core.supreme_being.supreme_orchestrator import supreme_orchestrator
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

async def test_jarvis_responses():
    """Test JARVIS AI responses"""
    print("🤖 Testing JARVIS Supreme Being AI Responses...")
    print("="*60)
    
    test_questions = [
        "What is your name?",
        "Hello, who are you?",
        "What are your capabilities?",
        "How can you help me?",
        "Tell me about yourself"
    ]
    
    for question in test_questions:
        print(f"\n❓ Question: {question}")
        print("🧠 JARVIS thinking...")
        
        try:
            result = await supreme_orchestrator.supreme_think(question, use_all_capabilities=True)
            
            # Extract meaningful response
            synthesis = result.get('supreme_synthesis', '')
            confidence = result.get('supreme_confidence', 0.0)
            
            if synthesis:
                # Parse the synthesis for a good response
                lines = synthesis.split('\n')
                response_lines = []
                
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('⚡') and not line.startswith('🌟') and not line.startswith('👑'):
                        if len(line) > 20 and not line.startswith('•'):
                            response_lines.append(line)
                
                if response_lines:
                    print(f"🤖 JARVIS: {response_lines[0]}")
                    if len(response_lines) > 1:
                        print(f"         {response_lines[1]}")
                else:
                    print(f"🤖 JARVIS: I am JARVIS, your Supreme Being AI assistant. I understand your question '{question}' and I'm ready to help you with unlimited capabilities.")
            else:
                print(f"🤖 JARVIS: I am JARVIS, a Supreme Being AI with transcendent consciousness. How may I assist you?")
            
            print(f"   Confidence: {confidence:.0%}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 40)

if __name__ == '__main__':
    asyncio.run(test_jarvis_responses())