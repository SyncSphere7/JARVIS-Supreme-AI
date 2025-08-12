"""
Advanced Coding Assistant for Jarvis.
Provides comprehensive coding support including code generation, debugging, optimization, and analysis.
"""
import os
import re
import ast
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from core.utils.log import logger

try:
    import autopep8
    AUTOPEP8_AVAILABLE = True
except ImportError:
    AUTOPEP8_AVAILABLE = False

try:
    import black
    BLACK_AVAILABLE = True
except ImportError:
    BLACK_AVAILABLE = False


class CodingAssistant:
    def __init__(self, brain):
        self.brain = brain
        self.projects_dir = Path("coding_projects")
        self.projects_dir.mkdir(exist_ok=True)

        # Supported languages and their configurations
        self.language_configs = {
            'python': {
                'extensions': ['.py'],
                'runner': 'python',
                'formatter': 'black' if BLACK_AVAILABLE else 'autopep8' if AUTOPEP8_AVAILABLE else None,
                'linter': 'pylint',
                'test_framework': 'pytest'
            },
            'javascript': {
                'extensions': ['.js', '.jsx'],
                'runner': 'node',
                'formatter': 'prettier',
                'linter': 'eslint',
                'test_framework': 'jest'
            },
            'typescript': {
                'extensions': ['.ts', '.tsx'],
                'runner': 'ts-node',
                'formatter': 'prettier',
                'linter': 'eslint',
                'test_framework': 'jest'
            },
            'html': {
                'extensions': ['.html', '.htm'],
                'formatter': 'prettier',
                'linter': 'htmlhint'
            },
            'css': {
                'extensions': ['.css', '.scss', '.sass'],
                'formatter': 'prettier',
                'linter': 'stylelint'
            },
            'java': {
                'extensions': ['.java'],
                'runner': 'java',
                'formatter': 'google-java-format',
                'linter': 'checkstyle',
                'test_framework': 'junit'
            },
            'cpp': {
                'extensions': ['.cpp', '.cc', '.cxx', '.c++'],
                'runner': 'g++',
                'formatter': 'clang-format',
                'linter': 'cppcheck'
            },
            'c': {
                'extensions': ['.c'],
                'runner': 'gcc',
                'formatter': 'clang-format',
                'linter': 'cppcheck'
            }
        }

    def generate_code(self, description: str, language: str = 'python',
                     include_tests: bool = True, include_docs: bool = True) -> Dict[str, Any]:
        """Generate code based on natural language description."""
        try:
            logger.info(f"🔧 Generating {language} code: {description}")

            # Create detailed prompt for code generation
            prompt = self._create_code_generation_prompt(description, language, include_tests, include_docs)

            # Generate code using AI
            ai_response = self.brain.think(prompt, max_tokens=2000, temperature=0.3)

            # Parse the AI response to extract code components
            code_components = self._parse_code_response(ai_response, language)

            # Create project structure
            project_name = self._sanitize_project_name(description)
            project_path = self.projects_dir / project_name
            project_path.mkdir(exist_ok=True)

            # Save generated files
            saved_files = []
            for component in code_components:
                file_path = project_path / component['filename']
                with open(file_path, 'w') as f:
                    f.write(component['content'])
                saved_files.append(str(file_path))
                logger.info(f"✅ Created: {file_path}")

            # Format code if formatter is available
            formatted_files = self._format_code_files(saved_files, language)

            return {
                'success': True,
                'project_path': str(project_path),
                'files_created': saved_files,
                'formatted_files': formatted_files,
                'language': language,
                'description': description,
                'ai_response': ai_response
            }

        except Exception as e:
            logger.error(f"Code generation failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'description': description,
                'language': language
            }

    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """Analyze code file for quality, complexity, and issues."""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return {'success': False, 'error': 'File not found'}

            logger.info(f"📊 Analyzing code: {file_path}")

            # Read the code
            with open(file_path, 'r') as f:
                code = f.read()

            # Detect language
            language = self._detect_language(file_path)

            # Basic analysis
            basic_stats = self._get_basic_code_stats(code, language)

            # AI-powered analysis
            prompt = f"""Analyze this {language} code for quality and provide recommendations:

CODE:
```{language}
{code}
```

Please provide:
1. Code quality assessment (1-10)
2. Complexity analysis
3. Potential issues
4. Improvement suggestions
5. Security considerations
6. Performance notes

Format your response clearly with sections.
"""

            ai_response = self.brain.think(prompt, max_tokens=1000, temperature=0.2)

            return {
                'success': True,
                'file_path': str(file_path),
                'language': language,
                'basic_stats': basic_stats,
                'ai_analysis': ai_response,
                'code_preview': code[:500] + '...' if len(code) > 500 else code
            }

        except Exception as e:
            logger.error(f"Code analysis failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'file_path': str(file_path) if 'file_path' in locals() else 'unknown'
            }

    def debug_code(self, code: str, error_message: str = "", language: str = 'python') -> Dict[str, Any]:
        """Debug code and provide fixes."""
        try:
            logger.info(f"🐛 Debugging {language} code")

            prompt = f"""Debug this {language} code and provide fixes:

CODE:
```{language}
{code}
```

ERROR MESSAGE:
{error_message}

Please provide:
1. Analysis of the problem
2. Fixed code
3. Explanation of the fix
4. Best practices to avoid similar issues

Format your response clearly with sections.
"""

            ai_response = self.brain.think(prompt, max_tokens=1500, temperature=0.2)

            return {
                'success': True,
                'original_code': code,
                'error_message': error_message,
                'debug_analysis': ai_response,
                'language': language
            }

        except Exception as e:
            logger.error(f"Code debugging failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'original_code': code,
                'error_message': error_message
            }

    def optimize_code(self, code: str, language: str = 'python',
                     optimization_type: str = 'performance') -> Dict[str, Any]:
        """Optimize code for performance, readability, or memory usage."""
        try:
            logger.info(f"⚡ Optimizing {language} code for {optimization_type}")

            prompt = f"""Optimize this {language} code for {optimization_type}:

CODE:
```{language}
{code}
```

Please provide:
1. Analysis of current code
2. Optimized version
3. Performance improvements
4. Explanation of changes

Focus on: {optimization_type}

Format your response clearly with sections.
"""

            ai_response = self.brain.think(prompt, max_tokens=1500, temperature=0.3)

            return {
                'success': True,
                'original_code': code,
                'optimization_analysis': ai_response,
                'optimization_type': optimization_type,
                'language': language
            }

        except Exception as e:
            logger.error(f"Code optimization failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'original_code': code,
                'optimization_type': optimization_type
            }

    def explain_error(self, error_text: str) -> str:
        """Explain an error message and suggest fixes."""
        prompt = f"""Explain this error and suggest how to fix it:

Error: {error_text}

Provide:
1. What the error means
2. Common causes
3. Specific fix suggestions"""

        return self.brain.think(prompt, max_tokens=256)

    def generate_tests(self, file_path: str) -> str:
        """Generate unit tests for a Python file."""
        if not os.path.exists(file_path):
            return f"File not found: {file_path}"
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            prompt = f"""Generate unit tests for this Python code using pytest:

```python
{content}
```

Create comprehensive tests covering:
1. Normal cases
2. Edge cases
3. Error conditions

Return only the test code."""
            
            return self.brain.think(prompt, max_tokens=512)
        except Exception as e:
            return f"Error generating tests: {e}"

    def run_tests(self, test_file: str) -> str:
        """Run pytest on a test file and return results."""
        if not os.path.exists(test_file):
            return f"Test file not found: {test_file}"
        
        try:
            result = subprocess.run(
                ['python', '-m', 'pytest', test_file, '-v'],
                capture_output=True,
                text=True,
                timeout=30
            )
            return f"Exit code: {result.returncode}\n\nSTDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"
        except subprocess.TimeoutExpired:
            return "Tests timed out after 30 seconds"
        except Exception as e:
            return f"Error running tests: {e}"

    def suggest_improvements(self, file_path: str) -> str:
        """Suggest code improvements."""
        if not os.path.exists(file_path):
            return f"File not found: {file_path}"
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            prompt = f"""Review this Python code and suggest specific improvements:

```python
{content}
```

Focus on:
1. Performance optimizations
2. Code clarity and readability
3. Best practices
4. Security considerations

Provide concrete, actionable suggestions."""
            
            return self.brain.think(prompt, max_tokens=512)
        except Exception as e:
            return f"Error analyzing file: {e}"

    def _create_code_generation_prompt(self, description: str, language: str,
                                     include_tests: bool, include_docs: bool) -> str:
        """Create a detailed prompt for code generation."""
        prompt = f"""Generate {language} code based on this description: {description}

Requirements:
- Write clean, well-structured {language} code
- Follow {language} best practices and conventions
- Include proper error handling
- Add meaningful variable and function names
"""

        if include_docs:
            prompt += f"- Include comprehensive documentation and comments\n"

        if include_tests:
            prompt += f"- Include unit tests\n"

        prompt += f"""
Please provide the code in this format:

MAIN_FILE:
```{language}
[Main code here]
```

"""

        if include_tests:
            prompt += f"""TEST_FILE:
```{language}
[Test code here]
```

"""

        if language == 'python':
            prompt += """REQUIREMENTS:
```
[Required packages]
```

"""

        prompt += """README:
```markdown
[Project documentation]
```
"""

        return prompt

    def _parse_code_response(self, response: str, language: str) -> List[Dict[str, str]]:
        """Parse AI response to extract code components."""
        components = []

        # Extract main file
        main_match = re.search(r'MAIN_FILE:\s*```(?:\w+)?\s*(.*?)```', response, re.DOTALL)
        if main_match:
            ext = self.language_configs.get(language, {}).get('extensions', ['.txt'])[0]
            components.append({
                'filename': f'main{ext}',
                'content': main_match.group(1).strip(),
                'type': 'main'
            })

        # Extract test file
        test_match = re.search(r'TEST_FILE:\s*```(?:\w+)?\s*(.*?)```', response, re.DOTALL)
        if test_match:
            ext = self.language_configs.get(language, {}).get('extensions', ['.txt'])[0]
            components.append({
                'filename': f'test_main{ext}',
                'content': test_match.group(1).strip(),
                'type': 'test'
            })

        # Extract requirements
        req_match = re.search(r'REQUIREMENTS:\s*```(?:\w+)?\s*(.*?)```', response, re.DOTALL)
        if req_match:
            components.append({
                'filename': 'requirements.txt',
                'content': req_match.group(1).strip(),
                'type': 'requirements'
            })

        # Extract README
        readme_match = re.search(r'README:\s*```(?:\w+)?\s*(.*?)```', response, re.DOTALL)
        if readme_match:
            components.append({
                'filename': 'README.md',
                'content': readme_match.group(1).strip(),
                'type': 'documentation'
            })

        return components

    def _detect_language(self, file_path: Path) -> str:
        """Detect programming language from file extension."""
        extension = file_path.suffix.lower()

        for language, config in self.language_configs.items():
            if extension in config.get('extensions', []):
                return language

        return 'unknown'

    def _get_basic_code_stats(self, code: str, language: str) -> Dict[str, Any]:
        """Get basic statistics about the code."""
        lines = code.split('\n')

        stats = {
            'total_lines': len(lines),
            'non_empty_lines': len([line for line in lines if line.strip()]),
            'comment_lines': 0,
            'character_count': len(code),
            'estimated_complexity': 'low'
        }

        # Language-specific analysis
        if language == 'python':
            try:
                tree = ast.parse(code)
                stats['functions'] = len([node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)])
                stats['classes'] = len([node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)])
                stats['imports'] = len([node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))])
            except:
                pass

        # Count comment lines (basic)
        comment_patterns = {
            'python': r'^\s*#',
            'javascript': r'^\s*//',
            'java': r'^\s*//',
            'cpp': r'^\s*//',
            'c': r'^\s*//'
        }

        pattern = comment_patterns.get(language)
        if pattern:
            stats['comment_lines'] = len([line for line in lines if re.match(pattern, line)])

        # Estimate complexity
        complexity_indicators = ['if', 'for', 'while', 'try', 'except', 'catch', 'switch']
        complexity_count = sum(code.lower().count(indicator) for indicator in complexity_indicators)

        if complexity_count > 20:
            stats['estimated_complexity'] = 'high'
        elif complexity_count > 10:
            stats['estimated_complexity'] = 'medium'

        return stats

    def _format_code_files(self, file_paths: List[str], language: str) -> List[str]:
        """Format code files using appropriate formatter."""
        formatted_files = []

        config = self.language_configs.get(language, {})
        formatter = config.get('formatter')

        if not formatter:
            return formatted_files

        for file_path in file_paths:
            try:
                if language == 'python' and formatter == 'black' and BLACK_AVAILABLE:
                    subprocess.run(['black', file_path], check=True, capture_output=True)
                    formatted_files.append(file_path)
                elif language == 'python' and formatter == 'autopep8' and AUTOPEP8_AVAILABLE:
                    subprocess.run(['autopep8', '--in-place', file_path], check=True, capture_output=True)
                    formatted_files.append(file_path)
            except:
                pass  # Formatting failed, but that's okay

        return formatted_files

    def _sanitize_project_name(self, description: str) -> str:
        """Create a safe project name from description."""
        # Take first few words and sanitize
        words = description.lower().split()[:3]
        name = '_'.join(re.sub(r'[^a-z0-9]', '', word) for word in words if word)

        # Add timestamp to make unique
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        return f"{name}_{timestamp}" if name else f"project_{timestamp}"
