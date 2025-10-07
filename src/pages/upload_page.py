"""
Audio Upload and Processing Page
Streamlit interface for uploading and processing audio files
"""

import streamlit as st
from src.audio_processing import AudioProcessor, process_batch_files


def render_upload_page():
    """Render the audio upload and processing page"""

    st.header("📤 Upload & Process Audio Files")

    st.markdown("""
    Upload your podcast MP3 files to begin the transcription process.
    - Maximum file size: 500MB per file
    - Supported format: MP3
    - Files larger than 25MB will be automatically chunked
    """)

    # File uploader
    uploaded_files = st.file_uploader(
        "Drag and drop MP3 files here",
        type=['mp3'],
        accept_multiple_files=True,
        help="You can upload multiple files at once"
    )

    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} file(s) uploaded")

        # Display uploaded files
        with st.expander("📁 Uploaded Files", expanded=True):
            for file in uploaded_files:
                file_size_mb = len(file.getvalue()) / (1024 * 1024)
                st.write(f"- **{file.name}** ({file_size_mb:.2f} MB)")

        # Process button
        col1, col2 = st.columns([1, 3])
        with col1:
            process_button = st.button("🚀 Process Files", type="primary", use_container_width=True)

        if process_button:
            # Initialize session state for processed files
            if 'processed_audio' not in st.session_state:
                st.session_state.processed_audio = []

            # Create progress placeholder
            progress_placeholder = st.empty()
            status_placeholder = st.empty()

            try:
                # Process files
                with st.spinner("Processing audio files..."):
                    results = process_batch_files(uploaded_files, progress_placeholder)

                # Clear progress
                progress_placeholder.empty()

                # Display results
                if results['processed']:
                    status_placeholder.success(
                        f"✅ Successfully processed {len(results['processed'])} file(s)!"
                    )

                    # Store in session state
                    st.session_state.processed_audio = results['processed']

                    # Display audio information
                    st.subheader("📊 Audio Information")

                    for item in results['processed']:
                        with st.expander(f"📄 {item['filename']}", expanded=False):
                            col1, col2, col3 = st.columns(3)

                            with col1:
                                st.metric(
                                    "Duration",
                                    f"{item['info']['duration_minutes']:.2f} min"
                                )

                            with col2:
                                st.metric(
                                    "Chunks",
                                    len(item['chunk_paths'])
                                )

                            with col3:
                                st.metric(
                                    "Size",
                                    f"{item['info']['size_bytes'] / (1024*1024):.2f} MB"
                                )

                            # Technical details
                            st.caption("Technical Details:")
                            st.json({
                                'channels': item['info']['channels'],
                                'sample_rate': f"{item['info']['frame_rate']} Hz",
                                'sample_width': f"{item['info']['sample_width']} bytes"
                            })

                    # Summary
                    st.info(
                        f"📈 **Total Duration:** {results['total_duration']:.2f} minutes"
                    )

                    # Next steps
                    st.success("✅ Ready for transcription! Go to the next tab to transcribe.")

                # Display failures
                if results['failed']:
                    st.error(f"❌ Failed to process {len(results['failed'])} file(s)")
                    for item in results['failed']:
                        st.error(f"- {item['filename']}: {item['error']}")

            except Exception as e:
                status_placeholder.error(f"❌ Error processing files: {str(e)}")

    else:
        # Show instructions when no files are uploaded
        st.info("👆 Upload MP3 files to get started")

        # Example audio specifications
        with st.expander("ℹ️ Audio Specifications"):
            st.markdown("""
            **Recommended Audio Settings:**
            - Format: MP3
            - Bitrate: 128 kbps or higher
            - Sample Rate: 44.1 kHz or 48 kHz
            - Channels: Mono or Stereo

            **Processing:**
            - Files larger than 25MB will be automatically split into chunks
            - Each chunk will be processed separately for optimal transcription
            - Chunks will be reassembled after transcription
            """)
