"""
Smart Correction System for Transcriptions
Uses GPT-4 for post-processing and music industry glossary
Implements best practices from OpenAI Whisper documentation
"""

import json
import os
from typing import Dict, List, Optional
from openai import OpenAI
from dotenv import load_dotenv
# Removed: fuzzywuzzy and spaCy (not needed anymore)

load_dotenv()


class CorrectionService:
    """Handles transcription correction using GPT-4 and custom glossary"""

    def __init__(self, glossary_path: str = "data/music_glossary.json"):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.glossary = self._load_glossary(glossary_path)

    def _load_glossary(self, path: str) -> Dict:
        """Load music industry glossary"""
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
        return {}

    # Removed _load_spacy - not needed anymore

    def get_glossary_terms(self, custom_terms: Optional[List[str]] = None) -> str:
        """
        Get all glossary terms as a formatted string for GPT-4 prompt

        Args:
            custom_terms: Optional list of custom terms to add

        Returns:
            Formatted string of all terms
        """
        all_terms = []

        # Collect all terms from glossary
        for category, terms in self.glossary.items():
            all_terms.extend(terms.keys())

        # Add custom terms
        if custom_terms:
            all_terms.extend(custom_terms)

        # Remove duplicates and join
        unique_terms = list(set(all_terms))
        return ", ".join(unique_terms)

    def correct_with_gpt4(
        self,
        transcript: str,
        custom_terms: Optional[List[str]] = None,
        model: str = "gpt-4o-mini",  # Use gpt-4o-mini (128k context) instead of gpt-4
        temperature: float = 0.3
    ) -> Dict:
        """
        Correct transcription using GPT-4 post-processing
        Implements best practice from Whisper documentation

        Args:
            transcript: Raw transcription text
            custom_terms: Optional custom terms to preserve
            model: GPT model to use
            temperature: Model temperature (lower = more deterministic)

        Returns:
            Dictionary with corrected transcript
        """
        # Build glossary terms string
        glossary_terms = self.get_glossary_terms(custom_terms)

        # System prompt based on Whisper docs best practices
        system_prompt = f"""You are a helpful assistant for Groover, a music industry platform.
Your task is to correct any spelling discrepancies in the transcribed podcast text.

Make sure that the names of the following music industry terms, platforms, and products are spelled correctly:
{glossary_terms}

Important instructions:
1. Only add necessary punctuation such as periods, commas, and capitalization
2. Use only the context provided - do not add new information
3. Preserve the original meaning and flow of the conversation
4. Correct obvious transcription errors
5. Keep the casual, conversational tone appropriate for podcast content
6. For artist names and labels, preserve the exact spelling mentioned
7. Maintain industry-specific terminology and acronyms correctly

Output only the corrected transcript without any explanations or notes."""

        try:
            response = self.client.chat.completions.create(
                model=model,
                temperature=temperature,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": transcript
                    }
                ]
            )

            corrected_text = response.choices[0].message.content

            return {
                'success': True,
                'original': transcript,
                'corrected': corrected_text,
                'model_used': model,
                'custom_terms': custom_terms or []
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'original': transcript
            }

    def fuzzy_match_terms(self, text: str, threshold: int = 90) -> List[Dict]:
        """
        Find potential corrections using fuzzy matching
        DISABLED: This was matching nonsense like "a" → "A&R"
        """
        # DISABLE FUZZY MATCHING - it's broken and matches common words
        return []

        # Original broken code commented out:
        # words = text.split()
        # corrections = []
        # all_terms = {}
        # for category, terms in self.glossary.items():
        #     all_terms.update(terms)
        # for word in words:
        #     match, score = process.extractOne(word, all_terms.keys())
        #     if score >= threshold and word != match:
        #         corrections.append({
        #             'original': word,
        #             'suggestion': match,
        #             'score': score,
        #             'definition': all_terms[match]
        #         })
        # return corrections

    def identify_entities(self, text: str) -> List[Dict]:
        """
        Identify named entities (artists, labels, etc.) using spaCy

        Args:
            text: Text to analyze

        Returns:
            List of identified entities
        """
        # spaCy removed - no longer needed
        return []

    def get_correction_prompt(self, custom_terms: Optional[List[str]] = None) -> str:
        """
        Generate a prompt string for use in Whisper API transcription
        This can be used to improve initial transcription quality

        Args:
            custom_terms: Optional custom terms to include

        Returns:
            Prompt string (limited to 224 tokens as per Whisper constraints)
        """
        terms = self.get_glossary_terms(custom_terms)

        # Limit to most important terms (Whisper only uses first 224 tokens)
        # Focus on commonly misheard terms
        priority_terms = [
            "Groover", "Spotify", "Apple Music", "SoundCloud", "Bandcamp",
            "A&R", "DAW", "VST", "MIDI", "EDM", "R&B", "playlist",
            "curator", "streaming", "mastering", "mixing"
        ]

        if custom_terms:
            priority_terms.extend(custom_terms)

        prompt = "The following is a music industry podcast discussion about " + ", ".join(priority_terms[:30])
        return prompt

    def correct_transcript(
        self,
        transcript: str,
        use_gpt4: bool = True,
        custom_terms: Optional[List[str]] = None,
        max_tokens: int = 100000  # Safety limit for very long transcripts
    ) -> Dict:
        """
        Main correction pipeline

        Args:
            transcript: Raw transcription
            use_gpt4: Whether to use GPT-4 for correction
            custom_terms: Optional custom terms

        Returns:
            Correction result
        """
        result = {
            'original': transcript,
            'corrected': transcript,
            'fuzzy_corrections': [],
            'entities': [],
            'success': True
        }

        # Step 1: Fuzzy matching analysis
        result['fuzzy_corrections'] = self.fuzzy_match_terms(transcript)

        # Step 2: Named entity recognition
        result['entities'] = self.identify_entities(transcript)

        # Step 3: GPT-4 correction (best practice from Whisper docs)
        if use_gpt4:
            # Estimate token count (rough: 1 token ≈ 0.75 words)
            estimated_tokens = len(transcript.split()) * 1.33

            if estimated_tokens > max_tokens:
                # Skip GPT-4 correction for very long transcripts
                result['corrected'] = transcript
                result['model_used'] = 'none (transcript too long)'
                result['skipped_correction'] = True
                result['warning'] = f'Transcript too long ({int(estimated_tokens)} tokens estimated). Skipped GPT-4 correction.'
            else:
                gpt4_result = self.correct_with_gpt4(transcript, custom_terms)
                if gpt4_result['success']:
                    result['corrected'] = gpt4_result['corrected']
                    result['model_used'] = gpt4_result['model_used']
                else:
                    result['success'] = False
                    result['error'] = gpt4_result.get('error')
                    # Fallback to original transcript if correction fails
                    result['corrected'] = transcript

        return result


def get_correction_service(glossary_path: str = "data/music_glossary.json") -> CorrectionService:
    """Factory function to get correction service instance"""
    return CorrectionService(glossary_path)
