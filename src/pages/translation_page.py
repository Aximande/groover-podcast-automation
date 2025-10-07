"""
Translation Page
Streamlit interface for translating articles to multiple languages
"""

import streamlit as st
from src.translation import get_translation_service


def render_translation_page():
    """Render the translation page"""

    st.header("🌍 Translate Articles")

    # Check if articles exist
    if 'generated_articles' not in st.session_state or not st.session_state.generated_articles:
        st.warning("⚠️ No generated articles found. Please generate content first.")
        st.info("👈 Go to 'Generate Content' page to create articles")
        return

    articles = st.session_state.generated_articles

    st.success(f"✅ Ready to translate {len(articles)} article(s)")

    # Select article
    st.subheader("📄 Select Article")

    selected_index = st.selectbox(
        "Choose an article to translate",
        options=range(len(articles)),
        format_func=lambda i: f"{articles[i]['source_filename']} ({articles[i]['word_count']} words)"
    )

    selected_article = articles[selected_index]

    # Display article preview
    with st.expander("📝 Article Preview", expanded=False):
        st.markdown(selected_article['content'][:300] + "...")

    # Language selection
    st.subheader("🌐 Select Target Languages")

    translator = get_translation_service()

    # Create checkboxes for languages
    col1, col2, col3 = st.columns(3)

    selected_languages = []

    languages_list = list(translator.LANGUAGES.items())
    third = len(languages_list) // 3

    with col1:
        for code, name in languages_list[:third]:
            if st.checkbox(f"{name} ({code})", key=f"lang_{code}"):
                selected_languages.append(code)

    with col2:
        for code, name in languages_list[third:third*2]:
            if st.checkbox(f"{name} ({code})", key=f"lang_{code}"):
                selected_languages.append(code)

    with col3:
        for code, name in languages_list[third*2:]:
            if st.checkbox(f"{name} ({code})", key=f"lang_{code}"):
                selected_languages.append(code)

    if selected_languages:
        st.info(f"🎯 {len(selected_languages)} language(s) selected: {', '.join([translator.LANGUAGES[lang] for lang in selected_languages])}")

    # Translation options
    st.subheader("⚙️ Translation Options")

    col1, col2 = st.columns(2)

    with col1:
        cultural_adaptation = st.checkbox(
            "Enable cultural adaptation",
            value=True,
            help="Adapt idioms and cultural references for target audience"
        )

    with col2:
        translate_seo = st.checkbox(
            "Translate SEO metadata",
            value=True,
            help="Also translate titles, descriptions, and keywords"
        )

    # SEO keywords
    if translate_seo and selected_article.get('seo_metadata'):
        seo_data = selected_article['seo_metadata']
        keywords_str = seo_data.get('keywords', '')
        if isinstance(keywords_str, list):
            keywords_str = ', '.join(keywords_str)

        st.text_input(
            "SEO Keywords",
            value=keywords_str,
            disabled=True,
            help="These keywords will be preserved/adapted in translations"
        )

    # Translate button
    st.markdown("---")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        translate_button = st.button(
            f"🚀 Translate to {len(selected_languages)} Language(s)" if selected_languages else "Select Languages",
            type="primary",
            use_container_width=True,
            disabled=len(selected_languages) == 0
        )

    # Perform translation
    if translate_button and selected_languages:
        try:
            # Extract SEO keywords
            seo_keywords = None
            if selected_article.get('seo_metadata'):
                keywords = selected_article['seo_metadata'].get('keywords', '')
                if isinstance(keywords, str):
                    seo_keywords = [k.strip() for k in keywords.split(',')]
                else:
                    seo_keywords = keywords

            # Initialize session state for translations
            if 'translations' not in st.session_state:
                st.session_state.translations = []

            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()

            # Translate to each language
            translation_results = []

            for i, target_lang in enumerate(selected_languages):
                status_text.text(f"Translating to {translator.LANGUAGES[target_lang]}...")
                progress_bar.progress((i + 1) / len(selected_languages))

                if cultural_adaptation:
                    result = translator.translate_with_cultural_adaptation(
                        selected_article['content'],
                        target_lang,
                        seo_keywords
                    )
                else:
                    result = translator.translate_content(
                        selected_article['content'],
                        target_lang,
                        seo_keywords
                    )

                translation_results.append(result)

                # Translate SEO metadata if requested
                if translate_seo and selected_article.get('seo_metadata'):
                    seo_meta = selected_article['seo_metadata']
                    seo_result = translator.translate_seo_metadata(
                        seo_meta.get('seo_title', ''),
                        seo_meta.get('meta_description', ''),
                        seo_keywords or [],
                        target_lang
                    )
                    result['seo_metadata'] = seo_result

            # Clear progress indicators
            progress_bar.empty()
            status_text.empty()

            # Store translations
            translation_data = {
                'source_article': selected_article,
                'source_index': selected_index,
                'translations': translation_results,
                'cultural_adaptation': cultural_adaptation
            }

            st.session_state.translations.append(translation_data)

            # Display results
            successful = [t for t in translation_results if t['success']]
            failed = [t for t in translation_results if not t['success']]

            if successful:
                st.success(f"✅ Successfully translated to {len(successful)} language(s)!")

            if failed:
                st.error(f"❌ Failed to translate to {len(failed)} language(s)")

            # Display translations
            st.markdown("---")
            st.subheader("📚 Translations")

            for result in translation_results:
                if result['success']:
                    lang_name = result['target_language_name']
                    lang_code = result['target_language']

                    with st.expander(f"🌍 {lang_name} ({lang_code})", expanded=False):
                        # Translated content
                        st.text_area(
                            "Translated Article",
                            value=result['translated'],
                            height=300,
                            key=f"trans_{lang_code}_{selected_index}"
                        )

                        # Cultural notes (if available)
                        if 'cultural_notes' in result:
                            st.info(f"**Cultural Adaptations:** {result['cultural_notes']}")

                        # SEO metadata (if available)
                        if 'seo_metadata' in result and result['seo_metadata'].get('success'):
                            seo = result['seo_metadata']
                            col1, col2 = st.columns(2)

                            with col1:
                                st.caption(f"**SEO Title:** {seo.get('title', 'N/A')}")

                            with col2:
                                st.caption(f"**Meta Desc:** {seo.get('description', 'N/A')}")

                            st.caption(f"**Keywords:** {', '.join(seo.get('keywords', []))}")

                        # Download button
                        st.download_button(
                            label=f"📥 Download {lang_name} version",
                            data=result['translated'],
                            file_name=f"groover_article_{lang_code}.md",
                            mime="text/markdown",
                            key=f"download_{lang_code}_{selected_index}"
                        )

                else:
                    st.error(f"❌ {result['target_language']}: {result.get('error', 'Unknown error')}")

        except ValueError as e:
            st.error(f"❌ {str(e)}")
            st.info("💡 Please add your ANTHROPIC_API_KEY to the .env file")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

    # Display existing translations
    if 'translations' in st.session_state and st.session_state.translations:
        st.markdown("---")
        st.subheader("📖 Translation History")

        for i, trans_data in enumerate(st.session_state.translations):
            source = trans_data['source_article']
            translations = trans_data['translations']
            successful = [t for t in translations if t['success']]

            with st.expander(
                f"📄 {source['source_filename']} → {len(successful)} language(s)",
                expanded=False
            ):
                for result in successful:
                    lang_name = result['target_language_name']
                    lang_code = result['target_language']

                    st.markdown(f"**{lang_name}** ({lang_code})")
                    st.caption(result['translated'][:200] + "...")

                    st.download_button(
                        label=f"📥 Download {lang_name}",
                        data=result['translated'],
                        file_name=f"groover_{source['source_filename']}_{lang_code}.md",
                        mime="text/markdown",
                        key=f"hist_download_{i}_{lang_code}"
                    )

                    st.markdown("---")

    # Translation statistics
    if 'translations' in st.session_state and st.session_state.translations:
        st.markdown("---")
        st.subheader("📊 Translation Statistics")

        total_translations = sum(
            len([t for t in trans['translations'] if t['success']])
            for trans in st.session_state.translations
        )

        all_langs = set()
        for trans in st.session_state.translations:
            for result in trans['translations']:
                if result['success']:
                    all_langs.add(result['target_language'])

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Translations", total_translations)

        with col2:
            st.metric("Languages Covered", len(all_langs))

        with col3:
            st.metric("Articles Translated", len(st.session_state.translations))
