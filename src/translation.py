"""
Multi-Language Translation Pipeline
Translates content to 6+ languages using Claude API with SEO and cultural context preservation
"""

import os
from typing import Dict, List, Optional
from anthropic import Anthropic
from dotenv import load_dotenv
from langdetect import detect
from concurrent.futures import ThreadPoolExecutor, as_completed

load_dotenv()


class TranslationService:
    """Handles multi-language translation with SEO optimization"""

    # Supported languages
    LANGUAGES = {
        'en': 'English',
        'fr': 'French',
        'es': 'Spanish',
        'de': 'German',
        'it': 'Italian',
        'pt': 'Portuguese',
        'nl': 'Dutch',
        'ja': 'Japanese',
        'ko': 'Korean',
        'zh': 'Chinese (Simplified)'
    }

    def __init__(self, model: str = "claude-sonnet-4-5-20250929"):
        self.client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        self.model = model

    def detect_language(self, text: str) -> str:
        """
        Detect language of text

        Args:
            text: Text to analyze

        Returns:
            Language code
        """
        try:
            return detect(text)
        except:
            return 'unknown'

    def translate_content(
        self,
        content: str,
        target_language: str,
        seo_keywords: Optional[List[str]] = None,
        preserve_formatting: bool = True
    ) -> Dict:
        """
        Translate content to target language with SEO optimization

        Args:
            content: Content to translate
            target_language: Target language code (e.g., 'fr', 'es')
            seo_keywords: Optional SEO keywords to preserve
            preserve_formatting: Whether to preserve markdown formatting

        Returns:
            Translation result dictionary
        """
        # Get target language name
        target_lang_name = self.LANGUAGES.get(target_language, target_language)

        # Build translation prompt
        system_prompt = f"""You are an expert translator specializing in music industry content.
Translate the following content to {target_lang_name}, maintaining:
1. The original tone and style (casual, musician-friendly)
2. Cultural appropriateness and context
3. Industry-specific terminology
4. SEO optimization
5. Markdown formatting (headers, lists, emphasis)

IMPORTANT RULES:
- Preserve emojis exactly as they are
- Maintain markdown formatting (# ## ### * ** etc.)
- Keep technical terms and product names in their original form when appropriate
- Adapt idioms and cultural references to make sense in the target language
- Preserve URLs and links exactly
- Keep the same structure and flow"""

        user_prompt = f"""Translate this music industry article to {target_lang_name}.

{"SEO KEYWORDS TO PRESERVE: " + ", ".join(seo_keywords) if seo_keywords else ""}

CONTENT TO TRANSLATE:
{content}

Provide ONLY the translated content, maintaining all formatting."""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=8000,
                temperature=0.3,  # Lower for more consistent translation
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )

            translated_content = message.content[0].text

            return {
                'success': True,
                'original': content,
                'translated': translated_content,
                'source_language': self.detect_language(content),
                'target_language': target_language,
                'target_language_name': target_lang_name,
                'preserved_keywords': seo_keywords or []
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'target_language': target_language
            }

    def translate_with_cultural_adaptation(
        self,
        content: str,
        target_language: str,
        seo_keywords: Optional[List[str]] = None
    ) -> Dict:
        """
        Advanced translation with cultural adaptation

        Args:
            content: Content to translate
            target_language: Target language code
            seo_keywords: Optional SEO keywords

        Returns:
            Translation result with cultural notes
        """
        target_lang_name = self.LANGUAGES.get(target_language, target_language)

        system_prompt = f"""You are an expert translator and cultural consultant for music industry content.

Your task:
1. Translate to {target_lang_name} maintaining tone and meaning
2. Adapt cultural references and idioms for the target audience
3. Preserve SEO value while adapting keywords culturally
4. Keep music industry terminology accurate
5. Note any cultural adaptations made

Provide:
- The translated content
- A brief note on cultural adaptations (if any)"""

        user_prompt = f"""Translate and culturally adapt this music industry content to {target_lang_name}.

{"KEY TERMS/KEYWORDS: " + ", ".join(seo_keywords) if seo_keywords else ""}

CONTENT:
{content}

Format your response as:
TRANSLATION:
[translated content]

CULTURAL NOTES:
[brief notes on adaptations made, if any]"""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=10000,
                temperature=0.4,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )

            response_text = message.content[0].text

            # Parse response
            parts = response_text.split('CULTURAL NOTES:')
            translated = parts[0].replace('TRANSLATION:', '').strip()
            cultural_notes = parts[1].strip() if len(parts) > 1 else "No special adaptations needed"

            return {
                'success': True,
                'original': content,
                'translated': translated,
                'source_language': self.detect_language(content),
                'target_language': target_language,
                'target_language_name': target_lang_name,
                'cultural_notes': cultural_notes,
                'preserved_keywords': seo_keywords or []
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'target_language': target_language
            }

    def translate_parallel(
        self,
        content: str,
        target_languages: List[str],
        seo_keywords: Optional[List[str]] = None,
        max_workers: int = 3
    ) -> List[Dict]:
        """
        Translate content to multiple languages in parallel

        Args:
            content: Content to translate
            target_languages: List of target language codes
            seo_keywords: Optional SEO keywords
            max_workers: Maximum parallel workers

        Returns:
            List of translation results
        """
        results = []

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_lang = {
                executor.submit(
                    self.translate_content,
                    content,
                    lang,
                    seo_keywords
                ): lang for lang in target_languages
            }

            for future in as_completed(future_to_lang):
                lang = future_to_lang[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    results.append({
                        'success': False,
                        'error': str(e),
                        'target_language': lang
                    })

        # Sort by language code
        results.sort(key=lambda x: x.get('target_language', ''))
        return results

    def translate_seo_metadata(
        self,
        title: str,
        meta_description: str,
        keywords: List[str],
        target_language: str
    ) -> Dict:
        """
        Translate SEO metadata while maintaining optimization

        Args:
            title: SEO title
            meta_description: Meta description
            keywords: List of keywords
            target_language: Target language code

        Returns:
            Translated SEO metadata
        """
        target_lang_name = self.LANGUAGES.get(target_language, target_language)

        prompt = f"""Translate these SEO elements to {target_lang_name}, maintaining:
- Character limits (title: 60 chars, description: 160 chars)
- SEO optimization and keyword relevance
- Call-to-action appeal

TITLE: {title}
META DESCRIPTION: {meta_description}
KEYWORDS: {', '.join(keywords)}

Provide translations in this format:
TITLE: [translated title]
DESCRIPTION: [translated description]
KEYWORDS: [translated keywords, comma-separated]"""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=500,
                temperature=0.3,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            response = message.content[0].text

            # Parse response
            lines = response.strip().split('\n')
            metadata = {}

            for line in lines:
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip().lower()
                    metadata[key] = value.strip()

            return {
                'success': True,
                'title': metadata.get('title', title),
                'description': metadata.get('description', meta_description),
                'keywords': [k.strip() for k in metadata.get('keywords', '').split(',')],
                'target_language': target_language
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'target_language': target_language
            }


def get_translation_service(model: str = "claude-sonnet-4-5-20250929") -> TranslationService:
    """Factory function to get translation service instance"""
    if not os.getenv('ANTHROPIC_API_KEY'):
        raise ValueError("ANTHROPIC_API_KEY not found in environment variables")

    return TranslationService(model)
