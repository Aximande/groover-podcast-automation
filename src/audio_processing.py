"""
Audio File Processing and Chunking Module
Handles MP3 file uploads, validation, and chunking for API consumption
"""

import os
import tempfile
from typing import List, Tuple
from pydub import AudioSegment
import streamlit as st


class AudioProcessor:
    """Handles audio file processing and chunking"""

    # Maximum file size for API calls (25MB in bytes)
    MAX_CHUNK_SIZE = 25 * 1024 * 1024

    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()

    def validate_audio_file(self, file) -> Tuple[bool, str]:
        """
        Validate uploaded audio file

        Args:
            file: Uploaded file object from Streamlit

        Returns:
            Tuple of (is_valid, message)
        """
        if file is None:
            return False, "No file uploaded"

        # Check file extension
        if not file.name.lower().endswith('.mp3'):
            return False, "Only MP3 files are accepted"

        # Check file size (basic check)
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)

        if file_size == 0:
            return False, "File is empty"

        return True, "File is valid"

    def load_audio(self, file) -> AudioSegment:
        """
        Load audio file into AudioSegment

        Args:
            file: Uploaded file object

        Returns:
            AudioSegment object
        """
        # Save to temporary file
        temp_path = os.path.join(self.temp_dir, file.name)
        with open(temp_path, 'wb') as f:
            f.write(file.getvalue())

        # Load audio
        audio = AudioSegment.from_mp3(temp_path)
        return audio

    def get_audio_info(self, audio: AudioSegment) -> dict:
        """
        Get audio file information

        Args:
            audio: AudioSegment object

        Returns:
            Dictionary with audio information
        """
        return {
            'duration_seconds': len(audio) / 1000,
            'duration_minutes': len(audio) / 1000 / 60,
            'channels': audio.channels,
            'sample_width': audio.sample_width,
            'frame_rate': audio.frame_rate,
            'size_bytes': len(audio.raw_data)
        }

    def chunk_audio(self, audio: AudioSegment, chunk_duration_ms: int = 600000) -> List[AudioSegment]:
        """
        Split audio into chunks based on duration (default 10 minutes)

        Args:
            audio: AudioSegment object
            chunk_duration_ms: Duration of each chunk in milliseconds (default 10 min)

        Returns:
            List of AudioSegment chunks
        """
        chunks = []
        audio_length = len(audio)

        for start_ms in range(0, audio_length, chunk_duration_ms):
            end_ms = min(start_ms + chunk_duration_ms, audio_length)
            chunk = audio[start_ms:end_ms]
            chunks.append(chunk)

        return chunks

    def chunk_audio_by_size(self, audio: AudioSegment, max_size_bytes: int = MAX_CHUNK_SIZE) -> List[AudioSegment]:
        """
        Split audio into chunks based on fixed 10-minute duration

        Args:
            audio: AudioSegment object
            max_size_bytes: Maximum size of each chunk in bytes (kept for API compatibility)

        Returns:
            List of AudioSegment chunks
        """
        chunks = []
        audio_length = len(audio)

        # Use fixed 10-minute chunks (600,000 ms) to stay under 25MB limit
        chunk_duration_ms = 600000  # 10 minutes in milliseconds

        for start_ms in range(0, audio_length, chunk_duration_ms):
            end_ms = min(start_ms + chunk_duration_ms, audio_length)
            chunk = audio[start_ms:end_ms]
            chunks.append(chunk)

        return chunks

    def save_chunks(self, chunks: List[AudioSegment], base_filename: str) -> List[str]:
        """
        Save audio chunks to temporary files with bitrate control

        Args:
            chunks: List of AudioSegment chunks
            base_filename: Base filename for chunks

        Returns:
            List of file paths
        """
        chunk_paths = []
        base_name = os.path.splitext(base_filename)[0]

        for i, chunk in enumerate(chunks):
            chunk_filename = f"{base_name}_chunk_{i+1}.mp3"
            chunk_path = os.path.join(self.temp_dir, chunk_filename)
            # Export with bitrate control to ensure file size stays under 25MB
            chunk.export(chunk_path, format="mp3", bitrate="128k")
            chunk_paths.append(chunk_path)

        return chunk_paths

    def process_file(self, file, progress_callback=None) -> Tuple[AudioSegment, List[str], dict]:
        """
        Process uploaded audio file with progress tracking

        Args:
            file: Uploaded file object
            progress_callback: Optional callback function for progress updates

        Returns:
            Tuple of (audio, chunk_paths, audio_info)
        """
        # Validate file
        if progress_callback:
            progress_callback(0.1, "Validating file...")
        is_valid, message = self.validate_audio_file(file)
        if not is_valid:
            raise ValueError(message)

        # Load audio
        if progress_callback:
            progress_callback(0.3, "Loading audio file...")
        audio = self.load_audio(file)

        # Get audio info
        audio_info = self.get_audio_info(audio)

        # Check if chunking is needed
        if progress_callback:
            progress_callback(0.5, "Analyzing audio...")

        chunk_paths = []
        if audio_info['size_bytes'] > self.MAX_CHUNK_SIZE:
            if progress_callback:
                progress_callback(0.6, "Chunking large file...")
            chunks = self.chunk_audio_by_size(audio)
            chunk_paths = self.save_chunks(chunks, file.name)
        else:
            # Save single file
            if progress_callback:
                progress_callback(0.6, "Saving audio...")
            chunk_paths = self.save_chunks([audio], file.name)

        if progress_callback:
            progress_callback(1.0, "Processing complete!")

        return audio, chunk_paths, audio_info

    def cleanup(self):
        """Clean up temporary files"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)


def process_batch_files(files: List, progress_placeholder=None) -> dict:
    """
    Process multiple audio files in batch

    Args:
        files: List of uploaded file objects
        progress_placeholder: Streamlit placeholder for progress updates

    Returns:
        Dictionary with processing results
    """
    processor = AudioProcessor()
    results = {
        'processed': [],
        'failed': [],
        'total_duration': 0
    }

    for i, file in enumerate(files):
        try:
            if progress_placeholder:
                progress_placeholder.progress(
                    (i + 1) / len(files),
                    text=f"Processing {file.name} ({i+1}/{len(files)})"
                )

            audio, chunk_paths, audio_info = processor.process_file(file)

            results['processed'].append({
                'filename': file.name,
                'audio': audio,
                'chunk_paths': chunk_paths,
                'info': audio_info
            })
            results['total_duration'] += audio_info['duration_minutes']

        except Exception as e:
            results['failed'].append({
                'filename': file.name,
                'error': str(e)
            })

    return results
