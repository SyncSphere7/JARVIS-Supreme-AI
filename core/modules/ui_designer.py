"""
UI/UX Designer module for Jarvis.
Creates modern, professional UI designs with best practices.
"""
import os
from pathlib import Path
from typing import Dict, List
from core.utils.log import logger


class UIDesigner:
    def __init__(self, brain):
        self.brain = brain
        self.design_systems = {
            "modern": {
                "colors": ["#2563eb", "#1e40af", "#3b82f6", "#60a5fa", "#93c5fd"],
                "fonts": ["Inter", "Roboto", "Poppins"],
                "spacing": "8px grid system",
                "shadows": "subtle, layered",
                "corners": "8px border radius"
            },
            "minimal": {
                "colors": ["#000000", "#ffffff", "#f8fafc", "#e2e8f0", "#64748b"],
                "fonts": ["SF Pro", "Helvetica", "Arial"],
                "spacing": "16px grid system",
                "shadows": "minimal, clean",
                "corners": "4px border radius"
            },
            "vibrant": {
                "colors": ["#7c3aed", "#a855f7", "#c084fc", "#e879f9", "#f0abfc"],
                "fonts": ["Montserrat", "Open Sans", "Lato"],
                "spacing": "12px grid system",
                "shadows": "colorful, dynamic",
                "corners": "12px border radius"
            },
            "corporate": {
                "colors": ["#1f2937", "#374151", "#6b7280", "#9ca3af", "#d1d5db"],
                "fonts": ["Source Sans Pro", "Roboto", "Lato"],
                "spacing": "16px grid system",
                "shadows": "professional, subtle",
                "corners": "6px border radius"
            }
        }

    def enhance_website_design(self, project_dir: Path, design_style: str = "modern", 
                             requirements: str = "") -> str:
        """Enhance website with professional UI/UX design."""
        try:
            if not project_dir.exists():
                return "❌ Project directory not found."
            
            # Read existing files
            existing_files = self._read_existing_files(project_dir)
            
            # Get design system
            design_system = self.design_systems.get(design_style, self.design_systems["modern"])
            
            # Generate enhanced design
            enhanced_design = self._generate_enhanced_design(
                existing_files, design_system, design_style, requirements
            )
            
            # Apply enhancements
            files_updated = self._apply_design_enhancements(project_dir, enhanced_design)
            
            # Create design documentation
            self._create_design_docs(project_dir, design_system, design_style)
            
            result = f"✅ UI/UX enhanced with {design_style} design!\n"
            result += f"📄 Files updated: {', '.join(files_updated)}\n"
            result += f"🎨 Design system: {design_style.title()}\n"
            result += f"📋 Design guide created: design_guide.md\n"
            result += f"🚀 Ready to view: run dev server"
            
            return result
            
        except Exception as e:
            return f"❌ Error enhancing design: {e}"

    def _read_existing_files(self, project_dir: Path) -> Dict[str, str]:
        """Read existing project files."""
        files = {}
        
        for file_path in project_dir.glob('*.html'):
            with open(file_path, 'r', encoding='utf-8') as f:
                files[file_path.name] = f.read()
        
        for file_path in project_dir.glob('*.css'):
            with open(file_path, 'r', encoding='utf-8') as f:
                files[file_path.name] = f.read()
        
        for file_path in project_dir.glob('*.js'):
            with open(file_path, 'r', encoding='utf-8') as f:
                files[file_path.name] = f.read()
        
        return files

    def _generate_enhanced_design(self, existing_files: Dict[str, str], 
                                design_system: Dict, design_style: str, 
                                requirements: str) -> Dict[str, str]:
        """Generate enhanced design using AI."""
        
        prompt = f"""Enhance this website with EXACT specifications from the user's requirements.

USER REQUIREMENTS: {requirements}

DESIGN SYSTEM (use as base, but prioritize user specifications):
- Colors: {design_system['colors']}
- Fonts: {design_system['fonts']}
- Spacing: {design_system['spacing']}
- Shadows: {design_system['shadows']}
- Corners: {design_system['corners']}

CURRENT FILES:
{self._format_files_for_prompt(existing_files)}

CRITICAL: Follow the user's EXACT specifications. If they mention:
- Specific hex colors (e.g., #FF6B6B, #4ECDC4) - use them precisely
- Specific fonts (e.g., "Poppins", "Inter", "Roboto") - implement exactly
- Specific layouts (e.g., "3-column grid", "hero section with video") - create exactly
- Specific components (e.g., "floating action button", "sticky navbar") - build exactly
- Specific animations (e.g., "fade in on scroll", "hover scale effect") - implement exactly
- Specific spacing (e.g., "20px padding", "2rem margin") - use precisely
- Specific sizes (e.g., "80vh height", "300px width") - apply exactly

Please provide enhanced versions with:

1. **EXACT Implementation:**
   - Use specified colors, fonts, and measurements precisely
   - Implement requested layouts and components exactly
   - Apply specified animations and effects
   - Follow spacing and sizing requirements

2. **Modern CSS with:**
   - CSS Grid and Flexbox layouts
   - CSS Custom Properties for specified colors/fonts
   - Responsive design (mobile-first)
   - Smooth animations and transitions as specified
   - Professional typography with specified fonts
   - Hover effects and micro-interactions as requested

3. **Enhanced HTML structure:**
   - Semantic HTML5 elements
   - Accessibility features (ARIA labels, alt text)
   - SEO-friendly structure
   - Clean, organized markup

4. **Interactive JavaScript:**
   - Smooth scrolling if requested
   - Interactive elements as specified
   - Form validation if forms exist
   - Mobile menu functionality
   - Any specific animations or interactions requested

5. **Google Fonts Integration:**
   - Include Google Fonts link for any specified fonts
   - Apply fonts exactly as requested

Format as separate code blocks with clear file names:

**index.html:**
```html
[Enhanced HTML with exact specifications]
```

**style.css:**
```css
[Enhanced CSS with exact colors, fonts, and styling]
```

**script.js:**
```javascript
[Enhanced JavaScript with requested interactions]
```"""

        return self.brain.think(prompt, max_tokens=3000)

    def _format_files_for_prompt(self, files: Dict[str, str]) -> str:
        """Format files for AI prompt."""
        formatted = ""
        for filename, content in files.items():
            formatted += f"\n{filename}:\n```\n{content[:800]}...\n```\n"
        return formatted

    def _apply_design_enhancements(self, project_dir: Path, enhanced_design: str) -> List[str]:
        """Parse and apply design enhancements."""
        files_updated = []
        current_file = None
        current_content = []
        in_code_block = False
        
        lines = enhanced_design.split('\n')
        
        for line in lines:
            # Detect file names
            line_lower = line.lower()
            if any(ext in line_lower for ext in ['.html', '.css', '.js']):
                if 'index.html' in line_lower or 'html' in line_lower:
                    current_file = 'index.html'
                elif 'style.css' in line_lower or 'css' in line_lower:
                    current_file = 'style.css'
                elif 'script.js' in line_lower or 'javascript' in line_lower:
                    current_file = 'script.js'
                continue
            
            # Detect code blocks
            if line.strip().startswith('```'):
                if in_code_block and current_file and current_content:
                    # Save the enhanced file
                    self._save_enhanced_file(project_dir, current_file, '\n'.join(current_content))
                    files_updated.append(current_file)
                    current_content = []
                in_code_block = not in_code_block
                continue
            
            # Collect content
            if in_code_block and current_file:
                current_content.append(line)
        
        # Save last file if needed
        if current_file and current_content:
            self._save_enhanced_file(project_dir, current_file, '\n'.join(current_content))
            files_updated.append(current_file)
        
        return files_updated

    def _save_enhanced_file(self, project_dir: Path, filename: str, content: str):
        """Save enhanced file."""
        file_path = project_dir / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        logger.info(f"Enhanced: {filename}")

    def _create_design_docs(self, project_dir: Path, design_system: Dict, design_style: str):
        """Create design documentation."""
        design_guide = f"""# {design_style.title()} Design System

## Color Palette
{chr(10).join([f"- {color}" for color in design_system['colors']])}

## Typography
{chr(10).join([f"- {font}" for font in design_system['fonts']])}

## Spacing
- System: {design_system['spacing']}

## Shadows
- Style: {design_system['shadows']}

## Border Radius
- Standard: {design_system['corners']}

## UI Components
- Buttons: Consistent padding, hover effects
- Cards: Subtle shadows, rounded corners
- Navigation: Clear hierarchy, responsive
- Forms: Proper validation, accessibility

## Responsive Breakpoints
- Mobile: 320px - 768px
- Tablet: 768px - 1024px
- Desktop: 1024px+

## Accessibility
- ARIA labels implemented
- Keyboard navigation support
- Color contrast compliance
- Screen reader friendly

## Performance
- Optimized CSS
- Minimal JavaScript
- Fast loading images
- Mobile-first approach
"""
        
        with open(project_dir / 'design_guide.md', 'w', encoding='utf-8') as f:
            f.write(design_guide)

    def create_component_library(self, project_dir: Path) -> str:
        """Create a reusable component library."""
        try:
            components_dir = project_dir / 'components'
            components_dir.mkdir(exist_ok=True)
            
            # Generate component library
            prompt = """Create a modern component library with these reusable components:

1. **Button Component** (primary, secondary, outline variants)
2. **Card Component** (with image, title, description)
3. **Navigation Component** (responsive, mobile menu)
4. **Form Components** (input, textarea, select, checkbox)
5. **Modal Component** (overlay, close button)
6. **Hero Section Component**
7. **Footer Component**

Each component should be:
- Self-contained CSS classes
- Responsive design
- Accessibility features
- Hover/focus states
- Modern styling

Provide as separate CSS files for each component."""
            
            components_css = self.brain.think(prompt, max_tokens=2000)
            
            # Save components
            with open(components_dir / 'components.css', 'w', encoding='utf-8') as f:
                f.write(components_css)
            
            # Create component documentation
            with open(components_dir / 'README.md', 'w', encoding='utf-8') as f:
                f.write("# Component Library\n\nReusable UI components for consistent design.\n\n## Usage\n\nInclude `components.css` in your HTML:\n```html\n<link rel=\"stylesheet\" href=\"components/components.css\">\n```")
            
            return "✅ Component library created in /components folder!"
            
        except Exception as e:
            return f"❌ Error creating component library: {e}"
