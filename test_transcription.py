#!/usr/bin/env python3
"""
Simple test script to debug transcription issues
Run this directly to see console output
"""

import sys
from src.transcription import get_transcription_service

def test_transcription(chunk_path):
    """Test transcribing a single chunk"""
    print(f"\n{'='*60}")
    print(f"Testing transcription for: {chunk_path}")
    print(f"{'='*60}\n")

    try:
        service = get_transcription_service()
        print(f"✓ Service initialized with model: {service.model}")

        result = service.transcribe_audio(chunk_path, language=None)

        print(f"\n{'='*60}")
        print("RESULT:")
        print(f"{'='*60}")
        print(f"Success: {result.get('success')}")

        if result.get('success'):
            print(f"Text length: {len(result.get('text', ''))} chars")
            print(f"Language: {result.get('language')}")
            print(f"First 200 chars: {result.get('text', '')[:200]}...")
        else:
            print(f"Error: {result.get('error')}")

        return result

    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_transcription.py <path_to_audio_chunk>")
        print("\nExample:")
        print("  python test_transcription.py /tmp/tmpXXXXXX/interview_chunk_1.mp3")
        sys.exit(1)

    chunk_path = sys.argv[1]
    test_transcription(chunk_path)
