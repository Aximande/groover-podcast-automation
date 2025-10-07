"""
OpenAI Whisper API Integration for Audio Transcription
Handles transcription of audio files with chunking support
Uses whisper-1 (proven, stable model)
"""

import os
from openai import OpenAI
from typing import List, Dict, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class TranscriptionService:
    """Handles audio transcription using OpenAI Whisper API"""

    def __init__(self, model: str = "whisper-1", prompt_context: Optional[str] = None):
        """
        Initialize transcription service

        Args:
            model: Model to use (whisper-1 is most stable)
            prompt_context: Optional context prompt to improve transcription quality
        """
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model = model
        self.prompt_context = prompt_context

    def transcribe_audio(self, audio_file_path: str, language: Optional[str] = None, prompt: Optional[str] = None) -> Dict:
        """
        Transcribe a single audio file using Whisper API
        Simple, direct approach like your working code

        Args:
            audio_file_path: Path to the audio file
            language: Optional language code (e.g., 'en', 'fr', 'es')
            prompt: Optional context prompt for better transcription

        Returns:
            Dictionary with transcription results
        """
        try:
            with open(audio_file_path, 'rb') as audio_file:
                # Simple API call - exactly like your working code
                params = {
                    'model': self.model,
                    'file': audio_file,
                }

                # Add language if specified
                if language:
                    params['language'] = language

                # Add prompt for better accuracy
                effective_prompt = prompt or self.prompt_context
                if effective_prompt:
                    params['prompt'] = effective_prompt

                # Call Whisper API
                response = self.client.audio.transcriptions.create(**params)

                # Extract text from response
                text = response.text if hasattr(response, 'text') else str(response)

                print(f"✅ Successfully transcribed {audio_file_path} ({len(text)} chars)")

                return {
                    'success': True,
                    'text': text,
                    'language': response.language if hasattr(response, 'language') else (language or 'unknown'),
                    'duration': response.duration if hasattr(response, 'duration') else None,
                    'segments': response.segments if hasattr(response, 'segments') else [],
                    'file_path': audio_file_path
                }

        except Exception as e:
            error_msg = str(e)
            print(f"❌ Transcription error for {audio_file_path}: {error_msg}")

            return {
                'success': False,
                'error': f"Error: {error_msg}",
                'file_path': audio_file_path
            }

    def transcribe_chunks_sequential(
        self,
        chunk_paths: List[str],
        language: Optional[str] = None,
        progress_callback=None
    ) -> List[Dict]:
        """
        Transcribe multiple audio chunks sequentially (like your working code)
        More reliable than parallel processing

        Args:
            chunk_paths: List of paths to audio chunks
            language: Optional language code
            progress_callback: Optional callback for progress updates

        Returns:
            List of transcription results
        """
        results = []
        total_chunks = len(chunk_paths)

        for i, chunk_path in enumerate(chunk_paths):
            if progress_callback:
                progress_callback(
                    i / total_chunks,
                    f"Transcribing chunk {i+1}/{total_chunks}..."
                )

            result = self.transcribe_audio(chunk_path, language)
            result['chunk_index'] = i
            results.append(result)

            if progress_callback:
                progress_callback(
                    (i + 1) / total_chunks,
                    f"Transcribed chunk {i+1}/{total_chunks}"
                )

        return results

    def reassemble_transcription(self, chunk_results: List[Dict]) -> Dict:
        """
        Reassemble transcription from multiple chunks

        Args:
            chunk_results: List of transcription results from chunks

        Returns:
            Combined transcription result
        """
        successful_chunks = [r for r in chunk_results if r.get('success', False)]
        failed_chunks = [r for r in chunk_results if not r.get('success', False)]

        if not successful_chunks:
            return {
                'success': False,
                'error': 'All chunks failed to transcribe',
                'failed_chunks': len(failed_chunks),
                'chunk_errors': [{'index': r.get('chunk_index', 'unknown'), 'error': r.get('error', 'unknown error')} for r in failed_chunks]
            }

        # Combine transcription text
        full_text = ' '.join([chunk.get('text', '') for chunk in successful_chunks if chunk.get('text')])

        # Combine segments if available
        all_segments = []
        time_offset = 0

        for chunk in successful_chunks:
            segments = chunk.get('segments', [])
            if segments:  # Only process if segments exist
                for segment in segments:
                    # Adjust segment timestamps for continuity
                    adjusted_segment = segment.copy()
                    adjusted_segment['start'] += time_offset
                    adjusted_segment['end'] += time_offset
                    all_segments.append(adjusted_segment)

                # Update time offset for next chunk
                if chunk.get('duration'):
                    time_offset += chunk['duration']

        return {
            'success': True,
            'text': full_text,
            'segments': all_segments,
            'total_chunks': len(chunk_results),
            'successful_chunks': len(successful_chunks),
            'failed_chunks': len(failed_chunks),
            'language': successful_chunks[0].get('language') if successful_chunks else 'unknown',
            'total_duration': time_offset if time_offset > 0 else None
        }

    def transcribe_file(
        self,
        chunk_paths: List[str],
        language: Optional[str] = None,
        progress_callback=None
    ) -> Dict:
        """
        High-level method to transcribe audio file (handles single or multiple chunks)

        Args:
            chunk_paths: List of paths to audio chunks
            language: Optional language code
            progress_callback: Optional callback for progress updates

        Returns:
            Transcription result
        """
        if not chunk_paths:
            return {
                'success': False,
                'error': 'No audio chunks provided'
            }

        # Single chunk - direct transcription
        if len(chunk_paths) == 1:
            if progress_callback:
                progress_callback(0.5, "Transcribing audio...")

            result = self.transcribe_audio(chunk_paths[0], language)

            if progress_callback:
                progress_callback(1.0, "Transcription complete!")

            return result

        # Multiple chunks - sequential transcription (more reliable)
        if progress_callback:
            progress_callback(0.1, "Starting transcription...")

        chunk_results = self.transcribe_chunks_sequential(
            chunk_paths,
            language,
            progress_callback=progress_callback
        )

        if progress_callback:
            progress_callback(0.9, "Reassembling transcription...")

        final_result = self.reassemble_transcription(chunk_results)

        if progress_callback:
            progress_callback(1.0, "Transcription complete!")

        return final_result


def get_transcription_service() -> TranscriptionService:
    """Factory function to get transcription service instance"""
    if not os.getenv('OPENAI_API_KEY'):
        raise ValueError("OPENAI_API_KEY not found in environment variables")

    return TranscriptionService()
