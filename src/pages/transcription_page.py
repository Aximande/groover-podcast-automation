"""
Transcription Page
Streamlit interface for transcribing processed audio files
"""

import streamlit as st
from src.transcription import get_transcription_service


def render_transcription_page():
    """Render the transcription page"""

    st.header("🎤 Transcribe Audio")

    # Check if audio files are processed
    if 'processed_audio' not in st.session_state or not st.session_state.processed_audio:
        st.warning("⚠️ No processed audio files found. Please upload and process audio files first.")
        st.info("👈 Go to 'Upload & Process' page to get started")
        return

    processed_files = st.session_state.processed_audio

    st.success(f"✅ Ready to transcribe {len(processed_files)} file(s)")

    # Language selection
    st.subheader("🌐 Language Settings")

    col1, col2 = st.columns([2, 1])

    with col1:
        auto_detect = st.checkbox(
            "Auto-detect language",
            value=True,
            help="Let Whisper automatically detect the language"
        )

    with col2:
        if not auto_detect:
            language = st.selectbox(
                "Select language",
                options=['en', 'fr', 'es', 'de', 'it', 'pt', 'nl', 'pl', 'ru', 'ja', 'ko', 'zh'],
                format_func=lambda x: {
                    'en': 'English',
                    'fr': 'French',
                    'es': 'Spanish',
                    'de': 'German',
                    'it': 'Italian',
                    'pt': 'Portuguese',
                    'nl': 'Dutch',
                    'pl': 'Polish',
                    'ru': 'Russian',
                    'ja': 'Japanese',
                    'ko': 'Korean',
                    'zh': 'Chinese'
                }[x]
            )
        else:
            language = None

    # Files to transcribe
    st.subheader("📁 Select Files to Transcribe")

    files_to_transcribe = []

    for i, file_data in enumerate(processed_files):
        col1, col2, col3 = st.columns([3, 2, 1])

        with col1:
            selected = st.checkbox(
                f"{file_data['filename']}",
                value=True,
                key=f"select_{i}"
            )
            if selected:
                files_to_transcribe.append(file_data)

        with col2:
            st.caption(f"Duration: {file_data['info']['duration_minutes']:.2f} min")

        with col3:
            st.caption(f"{len(file_data['chunk_paths'])} chunk(s)")

    # Transcribe button
    if files_to_transcribe:
        st.markdown("---")

        col1, col2, col3 = st.columns([1, 2, 1])

        with col1:
            transcribe_button = st.button(
                f"🚀 Transcribe {len(files_to_transcribe)} file(s)",
                type="primary",
                use_container_width=True
            )

        if transcribe_button:
            # Initialize transcription service
            try:
                transcription_service = get_transcription_service()
            except ValueError as e:
                st.error(f"❌ {str(e)}")
                st.info("💡 Please add your OPENAI_API_KEY to the .env file")
                return

            # Initialize session state for transcriptions
            if 'transcriptions' not in st.session_state:
                st.session_state.transcriptions = []

            # Process each file
            for i, file_data in enumerate(files_to_transcribe):
                st.subheader(f"📄 Transcribing: {file_data['filename']}")

                progress_bar = st.progress(0)
                status_text = st.empty()

                def progress_callback(progress, message):
                    progress_bar.progress(progress)
                    status_text.text(message)

                try:
                    # Transcribe
                    result = transcription_service.transcribe_file(
                        file_data['chunk_paths'],
                        language=language,
                        progress_callback=progress_callback
                    )

                    # Clear progress indicators
                    progress_bar.empty()
                    status_text.empty()

                    if result['success']:
                        st.success(f"✅ Transcription complete!")

                        # Store result
                        transcription_data = {
                            'filename': file_data['filename'],
                            'text': result['text'],
                            'language': result.get('language', 'unknown'),
                            'duration': result.get('total_duration', 0),
                            'segments': result.get('segments', []),
                            'chunks_info': {
                                'total': result.get('total_chunks', 1),
                                'successful': result.get('successful_chunks', 1),
                                'failed': result.get('failed_chunks', 0)
                            }
                        }

                        st.session_state.transcriptions.append(transcription_data)

                        # Display transcription preview
                        with st.expander("📝 Transcription Preview", expanded=True):
                            st.text_area(
                                "Transcript",
                                value=result['text'][:500] + "..." if len(result['text']) > 500 else result['text'],
                                height=150,
                                disabled=True
                            )

                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Language", result.get('language', 'unknown').upper())
                            with col2:
                                st.metric("Words", len(result['text'].split()))
                            with col3:
                                duration = result.get('total_duration') or 0
                                st.metric("Duration", f"{duration:.1f}s")

                    else:
                        st.error(f"❌ Transcription failed: {result.get('error', 'Unknown error')}")

                except Exception as e:
                    progress_bar.empty()
                    status_text.empty()
                    st.error(f"❌ Error: {str(e)}")

            # Show next steps
            if st.session_state.transcriptions:
                st.markdown("---")
                st.success(f"🎉 Successfully transcribed {len(st.session_state.transcriptions)} file(s)!")
                st.info("👉 Go to 'Generate Content' page to create articles from your transcriptions")

    else:
        st.info("👆 Select at least one file to transcribe")

    # Display existing transcriptions
    if 'transcriptions' in st.session_state and st.session_state.transcriptions:
        st.markdown("---")
        st.subheader("📚 Existing Transcriptions")

        for i, trans in enumerate(st.session_state.transcriptions):
            with st.expander(f"📄 {trans['filename']}", expanded=False):
                st.text_area(
                    "Full Transcript",
                    value=trans['text'],
                    height=200,
                    key=f"trans_{i}"
                )

                col1, col2, col3 = st.columns(3)
                with col1:
                    language = trans.get('language') or 'unknown'
                    st.metric("Language", language.upper())
                with col2:
                    st.metric("Words", len(trans['text'].split()))
                with col3:
                    st.metric("Segments", len(trans.get('segments', [])))

                # Download options
                col1, col2 = st.columns(2)

                with col1:
                    st.download_button(
                        label="📥 Download Raw Transcript (TXT)",
                        data=trans['text'],
                        file_name=f"{trans['filename']}_transcript.txt",
                        mime="text/plain",
                        key=f"download_{i}"
                    )

                with col2:
                    # Create formatted transcript with metadata
                    from datetime import datetime
                    language = trans.get('language') or 'unknown'
                    formatted_transcript = f"""TRANSCRIPT BACKUP
{'=' * 60}

Source File: {trans['filename']}
Language: {language.upper()}
Total Words: {len(trans['text'].split())}
Total Segments: {len(trans.get('segments', []))}
Total Chunks: {trans.get('chunks_info', {}).get('total', 'N/A')}
Successful Chunks: {trans.get('chunks_info', {}).get('successful', 'N/A')}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{'=' * 60}

{trans['text']}
"""
                    st.download_button(
                        label="📥 Download Formatted Backup (TXT)",
                        data=formatted_transcript,
                        file_name=f"{trans['filename']}_transcript_backup.txt",
                        mime="text/plain",
                        key=f"download_formatted_{i}"
                    )
