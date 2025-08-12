#!/usr/bin/env python3
"""
Debug the exact syntax issue.
"""
import ast

def debug_line_126():
    """Debug the exact issue with line 126."""
    try:
        with open("core/autonomous/goal_executor.py", 'rb') as f:
            lines = f.readlines()
        
        # Check lines around 126
        for i in range(123, 130):
            if i < len(lines):
                line_bytes = lines[i]
                line_str = line_bytes.decode('utf-8', errors='replace')
                print(f"Line {i+1}: {repr(line_bytes)}")
                print(f"Decoded: {repr(line_str)}")
                print(f"Visible: {line_str}")
                print("-" * 50)
        
        # Try to parse just that function
        print("\nTrying to parse the problematic function...")
        
        function_code = '''def _execute_plan_autonomously(self, goal_id: str) -> str:
    """Execute plan autonomously without user intervention."""
    goal = self.active_goals[goal_id]
    plan = goal['plan']
    results = []'''
        
        try:
            ast.parse(function_code)
            print("✅ Isolated function parses correctly")
        except SyntaxError as e:
            print(f"❌ Isolated function has syntax error: {e}")
        
        # Try to find the exact problematic character
        with open("core/autonomous/goal_executor.py", 'r', encoding='utf-8') as f:
            content = f.read()
        
        try:
            ast.parse(content)
            print("✅ Full file parses correctly")
        except SyntaxError as e:
            print(f"❌ Full file syntax error: {e}")
            print(f"Error at line {e.lineno}, column {e.offset}")
            
            if e.lineno and e.lineno <= len(content.split('\n')):
                problematic_line = content.split('\n')[e.lineno - 1]
                print(f"Problematic line: {repr(problematic_line)}")
                
                # Show each character with its Unicode code point
                print("Character analysis:")
                for i, char in enumerate(problematic_line):
                    print(f"  {i}: {repr(char)} (U+{ord(char):04X})")
        
    except Exception as e:
        print(f"Debug error: {e}")

if __name__ == "__main__":
    debug_line_126()
