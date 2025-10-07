"""
Groover Podcast-to-Article Automation Platform
Main Streamlit application entry point
"""

import streamlit as st
from src.pages.upload_page import render_upload_page
from src.pages.transcription_page import render_transcription_page
from src.pages.content_page import render_content_page
from src.pages.translation_page import render_translation_page
from src.pages.export_page import render_export_page


def main():
    """Main application entry point"""
    st.set_page_config(
        page_title="Groover Podcast Automation",
        page_icon="🎙️",
        layout="wide"
    )

    # Header with Groover logo
    col1, col2 = st.columns([1, 5])
    with col1:
        st.image("Logo_GROOVER.png", width=120)
    with col2:
        st.title("🎙️ Groover Podcast-to-Article Automation Platform")
        st.markdown("""
        Transform your podcast audio files into engaging, multilingual blog articles
        optimized for Groover's content strategy.
        """)

    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Choose a page:",
        ["Upload & Process", "Transcribe", "Generate Content", "Translate", "Export"]
    )

    # Show progress indicators in sidebar
    if 'processed_audio' in st.session_state and st.session_state.processed_audio:
        st.sidebar.success(f"✅ {len(st.session_state.processed_audio)} file(s) processed")

    if 'transcriptions' in st.session_state and st.session_state.transcriptions:
        st.sidebar.success(f"✅ {len(st.session_state.transcriptions)} transcription(s) ready")

    if 'generated_articles' in st.session_state and st.session_state.generated_articles:
        st.sidebar.success(f"✅ {len(st.session_state.generated_articles)} article(s) generated")

    # Page routing
    if page == "Upload & Process":
        render_upload_page()

    elif page == "Transcribe":
        render_transcription_page()

    elif page == "Generate Content":
        render_content_page()

    elif page == "Translate":
        render_translation_page()

    elif page == "Export":
        render_export_page()


if __name__ == "__main__":
    main()
