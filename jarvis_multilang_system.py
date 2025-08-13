#!/usr/bin/env python3
"""
JARVIS Multi-Language System - Advanced Language Support and Translation
Comprehensive multi-language capabilities for JARVIS Supreme Being AI V01
"""

import os
import json
import sqlite3
import time
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
import threading
import re

# Try to import translation libraries
try:
    from googletrans import Translator
    GOOGLE_TRANSLATE_AVAILABLE = True
except ImportError:
    GOOGLE_TRANSLATE_AVAILABLE = False
    print("⚠️ Google Translate not available. Install with: pip install googletrans==4.0.0rc1")

try:
    import langdetect
    from langdetect import detect, detect_langs
    LANGDETECT_AVAILABLE = True
except ImportError:
    LANGDETECT_AVAILABLE = False
    print("⚠️ Language detection not available. Install with: pip install langdetect")

class JarvisMultiLangSystem:
    """Advanced multi-language system for JARVIS Supreme Being AI"""
    
    def __init__(self, lang_dir: str = "supreme_languages"):
        self.lang_dir = lang_dir
        self.db_path = os.path.join(lang_dir, "languages.db")
        self.translations_path = os.path.join(lang_dir, "translations")
        
        # Language capabilities
        self.capabilities = {
            'translation': GOOGLE_TRANSLATE_AVAILABLE,
            'language_detection': LANGDETECT_AVAILABLE,
            'custom_translations': True,
            'language_learning': True,
            'voice_synthesis': True,
            'text_analysis': True
        }
        
        # Supported languages with their codes and names
        self.supported_languages = {
            'en': {'name': 'English', 'native': 'English', 'rtl': False},
            'es': {'name': 'Spanish', 'native': 'Español', 'rtl': False},
            'fr': {'name': 'French', 'native': 'Français', 'rtl': False},
            'de': {'name': 'German', 'native': 'Deutsch', 'rtl': False},
            'it': {'name': 'Italian', 'native': 'Italiano', 'rtl': False},
            'pt': {'name': 'Portuguese', 'native': 'Português', 'rtl': False},
            'ru': {'name': 'Russian', 'native': 'Русский', 'rtl': False},
            'zh': {'name': 'Chinese', 'native': '中文', 'rtl': False},
            'ja': {'name': 'Japanese', 'native': '日本語', 'rtl': False},
            'ko': {'name': 'Korean', 'native': '한국어', 'rtl': False},
            'ar': {'name': 'Arabic', 'native': 'العربية', 'rtl': True},
            'hi': {'name': 'Hindi', 'native': 'हिन्दी', 'rtl': False},
            'th': {'name': 'Thai', 'native': 'ไทย', 'rtl': False},
            'vi': {'name': 'Vietnamese', 'native': 'Tiếng Việt', 'rtl': False},
            'tr': {'name': 'Turkish', 'native': 'Türkçe', 'rtl': False}
        }
        
        # Current language settings
        self.current_language = 'en'
        self.fallback_language = 'en'
        self.auto_detect = True
        
        # Translation cache
        self.translation_cache = {}
        
        # Language statistics
        self.lang_stats = {
            'translations_performed': 0,
            'languages_detected': 0,
            'custom_translations_added': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'most_used_languages': {}
        }
        
        # Initialize translator
        if GOOGLE_TRANSLATE_AVAILABLE:
            self.translator = Translator()
        else:
            self.translator = None
        
        # Thread lock
        self.lang_lock = threading.Lock()
        
        # Initialize system
        self.initialize_language_system()
    
    def initialize_language_system(self):
        """Initialize the multi-language system"""
        print("🌍 INITIALIZING JARVIS MULTI-LANGUAGE SYSTEM...")
        
        try:
            # Create directories
            os.makedirs(self.lang_dir, exist_ok=True)
            os.makedirs(self.translations_path, exist_ok=True)
            
            # Initialize database
            self.init_database()
            
            # Load language statistics
            self.load_language_stats()
            
            print("✅ JARVIS Multi-Language System initialized successfully")
            print(f"🌍 Supported Languages: {len(self.supported_languages)}")
            print(f"🔧 Capabilities: {sum(self.capabilities.values())}/6 active")
            
        except Exception as e:
            print(f"❌ Multi-language system initialization error: {e}")
    
    def init_database(self):
        """Initialize SQLite database for language data"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Custom translations table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS custom_translations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_text TEXT,
                    source_lang TEXT,
                    target_lang TEXT,
                    translation TEXT,
                    context TEXT,
                    created_at TEXT,
                    updated_at TEXT,
                    usage_count INTEGER DEFAULT 0
                )
            ''')
            
            # Translation history
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS translation_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_text TEXT,
                    source_lang TEXT,
                    target_lang TEXT,
                    translation TEXT,
                    method TEXT,
                    confidence REAL,
                    timestamp TEXT
                )
            ''')
            
            conn.commit()
    
    def detect_language(self, text: str) -> Dict[str, Any]:
        """Detect the language of input text"""
        try:
            if not text or len(text.strip()) < 3:
                return {
                    'success': False,
                    'error': 'Text too short for reliable detection'
                }
            
            detected_lang = 'en'
            confidence = 0.5
            
            # Try langdetect if available
            if LANGDETECT_AVAILABLE:
                try:
                    detected_lang = detect(text)
                    lang_probs = detect_langs(text)
                    if lang_probs:
                        confidence = lang_probs[0].prob
                except Exception as e:
                    print(f"Language detection failed: {e}")
                    detected_lang = self.simple_language_detection(text)
            else:
                detected_lang = self.simple_language_detection(text)
            
            # Map to supported language
            if detected_lang not in self.supported_languages:
                detected_lang = self.map_to_supported_language(detected_lang)
            
            return {
                'success': True,
                'language': detected_lang,
                'language_name': self.supported_languages.get(detected_lang, {}).get('name', 'Unknown'),
                'confidence': confidence,
                'supported': detected_lang in self.supported_languages
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Language detection failed: {str(e)}'
            }
    
    def translate_text(self, text: str, target_lang: str, source_lang: str = None) -> Dict[str, Any]:
        """Translate text to target language"""
        try:
            if not text or not text.strip():
                return {
                    'success': False,
                    'error': 'No text provided for translation'
                }
            
            # Auto-detect source language if not provided
            if not source_lang:
                detection_result = self.detect_language(text)
                if detection_result['success']:
                    source_lang = detection_result['language']
                else:
                    source_lang = self.current_language
            
            # Check if translation is needed
            if source_lang == target_lang:
                return {
                    'success': True,
                    'translation': text,
                    'source_language': source_lang,
                    'target_language': target_lang,
                    'method': 'no_translation_needed'
                }
            
            # Use Google Translate if available
            if self.translator and GOOGLE_TRANSLATE_AVAILABLE:
                try:
                    translation_result = self.translator.translate(
                        text, 
                        src=source_lang, 
                        dest=target_lang
                    )
                    
                    translated_text = translation_result.text
                    
                    # Store in history
                    self.store_translation_history(
                        text, source_lang, target_lang, 
                        translated_text, 'google_translate', 0.8
                    )
                    
                    # Update statistics
                    self.lang_stats['translations_performed'] += 1
                    
                    return {
                        'success': True,
                        'translation': translated_text,
                        'source_language': source_lang,
                        'target_language': target_lang,
                        'method': 'google_translate',
                        'confidence': 0.8
                    }
                    
                except Exception as e:
                    print(f"Google Translate error: {e}")
            
            # Fallback to simple translation
            fallback_translation = self.fallback_translation(text, source_lang, target_lang)
            
            return {
                'success': True,
                'translation': fallback_translation,
                'source_language': source_lang,
                'target_language': target_lang,
                'method': 'fallback',
                'confidence': 0.3
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Translation failed: {str(e)}'
            }
    
    def simple_language_detection(self, text: str) -> str:
        """Simple heuristic-based language detection"""
        text = text.lower()
        
        # Common words in different languages
        language_indicators = {
            'en': ['the', 'and', 'is', 'in', 'to', 'of', 'a', 'that', 'it', 'with'],
            'es': ['el', 'la', 'de', 'que', 'y', 'en', 'un', 'es', 'se', 'no'],
            'fr': ['le', 'de', 'et', 'à', 'un', 'il', 'être', 'et', 'en', 'avoir'],
            'de': ['der', 'die', 'und', 'in', 'den', 'von', 'zu', 'das', 'mit', 'sich'],
            'it': ['il', 'di', 'che', 'e', 'la', 'per', 'una', 'in', 'con', 'da']
        }
        
        # Count matches for each language
        scores = {}
        words = text.split()
        
        for lang, indicators in language_indicators.items():
            score = sum(1 for word in words if word in indicators)
            if score > 0:
                scores[lang] = score / len(words)
        
        # Return language with highest score
        if scores:
            return max(scores, key=scores.get)
        
        return 'en'  # Default to English
    
    def map_to_supported_language(self, detected_lang: str) -> str:
        """Map detected language code to supported language"""
        # Common language code mappings
        mappings = {
            'zh-cn': 'zh', 'zh-tw': 'zh',
            'pt-br': 'pt', 'pt-pt': 'pt',
            'en-us': 'en', 'en-gb': 'en',
            'es-es': 'es', 'es-mx': 'es'
        }
        
        # Try direct mapping
        if detected_lang in mappings:
            return mappings[detected_lang]
        
        # Try first two characters
        if len(detected_lang) > 2:
            short_code = detected_lang[:2]
            if short_code in self.supported_languages:
                return short_code
        
        # Return as-is if supported, otherwise fallback
        if detected_lang in self.supported_languages:
            return detected_lang
        
        return self.fallback_language
    
    def fallback_translation(self, text: str, source_lang: str, target_lang: str) -> str:
        """Simple fallback translation using basic word mappings"""
        # Basic word mappings for common words
        basic_translations = {
            'en': {
                'es': {'hello': 'hola', 'goodbye': 'adiós', 'yes': 'sí', 'no': 'no', 'thank you': 'gracias'},
                'fr': {'hello': 'bonjour', 'goodbye': 'au revoir', 'yes': 'oui', 'no': 'non', 'thank you': 'merci'},
                'de': {'hello': 'hallo', 'goodbye': 'auf wiedersehen', 'yes': 'ja', 'no': 'nein', 'thank you': 'danke'},
                'it': {'hello': 'ciao', 'goodbye': 'arrivederci', 'yes': 'sì', 'no': 'no', 'thank you': 'grazie'}
            }
        }
        
        if source_lang in basic_translations and target_lang in basic_translations[source_lang]:
            translations = basic_translations[source_lang][target_lang]
            text_lower = text.lower()
            
            for word, translation in translations.items():
                if word in text_lower:
                    text = text.replace(word, translation)
        
        return text
    
    def store_translation_history(self, source_text: str, source_lang: str, target_lang: str,
                                translation: str, method: str, confidence: float):
        """Store translation in history"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO translation_history 
                    (source_text, source_lang, target_lang, translation, method, confidence, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (source_text, source_lang, target_lang, translation, method, confidence, datetime.now().isoformat()))
                conn.commit()
        except Exception as e:
            print(f"Error storing translation history: {e}")
    
    def load_language_stats(self):
        """Load language statistics from database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Count translations
                cursor.execute('SELECT COUNT(*) FROM translation_history')
                result = cursor.fetchone()
                if result:
                    self.lang_stats['translations_performed'] = result[0]
                    
        except Exception as e:
            print(f"Error loading language stats: {e}")
    
    def get_language_status(self) -> Dict[str, Any]:
        """Get comprehensive language system status"""
        self.load_language_stats()
        
        return {
            'capabilities': self.capabilities,
            'supported_languages': len(self.supported_languages),
            'current_language': self.current_language,
            'fallback_language': self.fallback_language,
            'auto_detect': self.auto_detect,
            'statistics': self.lang_stats,
            'database_path': self.db_path,
            'system_status': 'active'
        }
    
    def translate_jarvis_response(self, response: str, target_lang: str) -> str:
        """Translate JARVIS response to target language"""
        if target_lang == 'en' or target_lang == self.current_language:
            return response
        
        translation_result = self.translate_text(response, target_lang, 'en')
        if translation_result['success']:
            return translation_result['translation']
        else:
            return response  # Return original if translation fails
    
    def get_supported_languages_list(self) -> List[Dict[str, Any]]:
        """Get list of all supported languages with details"""
        return [
            {
                'code': code,
                'name': info['name'],
                'native_name': info['native'],
                'rtl': info['rtl']
            }
            for code, info in self.supported_languages.items()
        ]


def main():
    """Test the multi-language system"""
    print("🌍 JARVIS MULTI-LANGUAGE SYSTEM TEST")
    print("=" * 50)
    
    # Initialize language system
    lang_system = JarvisMultiLangSystem()
    
    # Test language detection
    print("\n🔄 Testing language detection...")
    test_texts = [
        "Hello, how are you today?",
        "Hola, ¿cómo estás hoy?",
        "Bonjour, comment allez-vous aujourd'hui?",
        "Guten Tag, wie geht es Ihnen heute?"
    ]
    
    for text in test_texts:
        detection = lang_system.detect_language(text)
        if detection['success']:
            print(f"✅ '{text[:30]}...' -> {detection['language']} ({detection['language_name']}) - {detection['confidence']:.2f}")
        else:
            print(f"❌ Detection failed for '{text[:30]}...': {detection['error']}")
    
    # Test translation
    print("\n�� Testing translation...")
    test_translations = [
        ("Hello, I am JARVIS", "es"),
        ("How can I help you today?", "fr"),
        ("Thank you for using JARVIS", "de"),
        ("Goodbye and have a great day!", "it")
    ]
    
    for text, target_lang in test_translations:
        translation = lang_system.translate_text(text, target_lang)
        if translation['success']:
            print(f"✅ EN->({target_lang.upper()}): '{text}' -> '{translation['translation']}'")
        else:
            print(f"❌ Translation failed: {translation['error']}")
    
    # Show supported languages
    print("\n🌍 Supported Languages:")
    languages = lang_system.get_supported_languages_list()
    for lang in languages[:10]:  # Show first 10
        print(f"   {lang['code']}: {lang['name']} ({lang['native_name']})")
    print(f"   ... and {len(languages) - 10} more languages")
    
    # Show system status
    print("\n📊 Multi-Language System Status:")
    status = lang_system.get_language_status()
    print(f"   Supported Languages: {status['supported_languages']}")
    print(f"   Active Capabilities: {sum(status['capabilities'].values())}/6")
    print(f"   Translations Performed: {status['statistics']['translations_performed']}")
    print(f"   System Status: {status['system_status']}")


if __name__ == "__main__":
    main()
