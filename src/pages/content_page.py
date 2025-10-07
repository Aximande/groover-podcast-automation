"""
Content Generation Page
Streamlit interface for generating blog articles from transcriptions
"""

import streamlit as st
from src.content_generation import get_content_generator
from src.correction import get_correction_service


def render_content_page():
    """Render the content generation page"""

    st.header("✍️ Generate Content")

    # Check if transcriptions exist
    if 'transcriptions' not in st.session_state or not st.session_state.transcriptions:
        st.warning("⚠️ No transcriptions found. Please transcribe audio files first.")
        st.info("👈 Go to 'Transcribe' page to get started")
        return

    transcriptions = st.session_state.transcriptions

    st.success(f"✅ Ready to generate content from {len(transcriptions)} transcription(s)")

    # Select transcription
    st.subheader("📄 Select Transcription")

    selected_index = st.selectbox(
        "Choose a transcription",
        options=range(len(transcriptions)),
        format_func=lambda i: f"{transcriptions[i]['filename']} ({len(transcriptions[i]['text'].split())} words)"
    )

    selected_transcript = transcriptions[selected_index]

    # Display transcript preview
    with st.expander("📝 Transcript Preview", expanded=False):
        st.text_area(
            "Transcript",
            value=selected_transcript['text'][:500] + "..." if len(selected_transcript['text']) > 500 else selected_transcript['text'],
            height=150,
            disabled=True
        )

    # Correction options
    st.subheader("🔧 Transcript Correction (Optional)")

    col1, col2 = st.columns([2, 1])

    with col1:
        apply_correction = st.checkbox(
            "Apply smart correction before generating content",
            value=True,
            help="Uses GPT-4 to correct transcription errors and improve accuracy"
        )

    # Custom terms input
    st.markdown("#### 🎯 Custom Terms & Names")
    st.caption("Add specific terms, artist names, labels, or terminology that should be preserved correctly")

    custom_terms_input = st.text_area(
        "Custom terms (one per line or comma-separated)",
        placeholder="e.g.:\nSpotify\nBillie Eilish\nUniversal Music Group\nLoFi",
        height=100,
        help="Enter custom terms, artist names, labels, or specific terminology"
    )

    # Parse custom terms
    custom_terms = []
    if custom_terms_input.strip():
        # Support both comma-separated and newline-separated
        if '\n' in custom_terms_input:
            custom_terms = [term.strip() for term in custom_terms_input.split('\n') if term.strip()]
        else:
            custom_terms = [term.strip() for term in custom_terms_input.split(',') if term.strip()]

        if custom_terms:
            st.info(f"📋 {len(custom_terms)} custom term(s) added: {', '.join(custom_terms[:5])}{'...' if len(custom_terms) > 5 else ''}")

    # Content generation options
    st.subheader("📝 Content Options")

    col1, col2, col3 = st.columns(3)

    with col1:
        article_style = st.selectbox(
            "Article Length",
            options=['long', 'short'],
            format_func=lambda x: f"Long Form (2000+ words)" if x == 'long' else "Short Form (500-800 words)"
        )

    with col2:
        enhance_groover = st.checkbox(
            "Add Groover CTAs",
            value=True,
            help="Naturally integrate Groover mentions and calls-to-action"
        )

    with col3:
        use_examples = st.checkbox(
            "Use Example Articles",
            value=False,
            help="Include Groover's actual articles as style references (A/B testing)"
        )

    # A/B Testing section
    if use_examples:
        st.info("🔬 **A/B Testing Mode:** Using Groover's reference articles to improve style matching")

        num_examples = st.slider(
            "Number of example articles to use",
            min_value=1,
            max_value=5,
            value=2,
            help="More examples = better style matching (but longer prompts)"
        )

    else:
        num_examples = 2  # Default if not using examples

    # Editorial angle
    editorial_angle = st.text_input(
        "Editorial Angle (optional)",
        placeholder="e.g., 'Focus on independent artists and DIY promotion'",
        help="Specify a particular angle or focus for the article"
    )

    # Additional instructions
    custom_instructions = st.text_area(
        "Additional Instructions (optional)",
        placeholder="Any specific requirements or style preferences...",
        height=80
    )

    # Generate button
    st.markdown("---")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        generate_button = st.button(
            "🚀 Generate Article",
            type="primary",
            use_container_width=True
        )

    with col2:
        generate_angles_button = st.button(
            "💡 Suggest Editorial Angles",
            use_container_width=True
        )

    # Generate editorial angles
    if generate_angles_button:
        try:
            generator = get_content_generator()

            with st.spinner("Analyzing transcript for editorial angles..."):
                # Use corrected or original transcript
                transcript_to_use = selected_transcript['text']

                if apply_correction:
                    with st.spinner("Correcting transcript..."):
                        corrector = get_correction_service()
                        correction_result = corrector.correct_transcript(
                            transcript_to_use,
                            use_gpt4=True,
                            custom_terms=custom_terms if custom_terms else None
                        )
                        if correction_result['success']:
                            transcript_to_use = correction_result['corrected']

                result = generator.generate_multiple_angles(transcript_to_use, num_angles=3)

                if result['success']:
                    st.success("✅ Editorial angles generated!")
                    st.markdown("### 💡 Suggested Editorial Angles")
                    st.markdown(result['angles_text'])
                else:
                    st.error(f"❌ Error: {result.get('error')}")

        except ValueError as e:
            st.error(f"❌ {str(e)}")
            st.info("💡 Please add your ANTHROPIC_API_KEY to the .env file")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

    # Generate article
    if generate_button:
        try:
            generator = get_content_generator()

            # Step 1: Correction (if enabled)
            transcript_to_use = selected_transcript['text']

            if apply_correction:
                with st.spinner("🔧 Correcting transcript with custom terms..."):
                    corrector = get_correction_service()

                    correction_result = corrector.correct_transcript(
                        transcript_to_use,
                        use_gpt4=True,
                        custom_terms=custom_terms if custom_terms else None
                    )

                    if correction_result['success']:
                        transcript_to_use = correction_result['corrected']
                        st.success("✅ Transcript corrected!")

                        # Show corrections made
                        if correction_result.get('fuzzy_corrections'):
                            with st.expander("🔍 Corrections Applied", expanded=False):
                                for corr in correction_result['fuzzy_corrections'][:10]:
                                    st.caption(f"• {corr['original']} → {corr['suggestion']}")
                    else:
                        st.warning(f"⚠️ Correction failed: {correction_result.get('error')}")

            # Step 2: Generate article
            spinner_text = f"✨ Generating {article_style} article"
            if use_examples:
                spinner_text += f" (with {num_examples} example reference(s))"
            spinner_text += "..."

            with st.spinner(spinner_text):
                article_result = generator.generate_article(
                    transcript=transcript_to_use,
                    style=article_style,
                    editorial_angle=editorial_angle if editorial_angle else None,
                    custom_instructions=custom_instructions if custom_instructions else None,
                    use_examples=use_examples,
                    num_examples=num_examples
                )

                if not article_result['success']:
                    st.error(f"❌ Generation failed: {article_result.get('error')}")
                    return

                article_content = article_result['content']

            # Step 3: Enhance with Groover context (if enabled)
            if enhance_groover:
                with st.spinner("🎯 Adding Groover context..."):
                    enhance_result = generator.enhance_with_groover_context(article_content)
                    if enhance_result['success']:
                        article_content = enhance_result['enhanced_content']

            # Step 4: Generate SEO metadata
            with st.spinner("📊 Generating SEO metadata..."):
                seo_result = generator.generate_seo_metadata(article_content)

            # Step 5: Generate social snippets
            with st.spinner("📱 Creating social media snippets..."):
                social_result = generator.generate_social_snippets(article_content)

            # Display results
            success_msg = f"🎉 Article generated! ({article_result['word_count']} words)"
            if use_examples:
                success_msg += f" | 🔬 A/B Test: WITH examples ({num_examples} refs)"
            else:
                success_msg += " | 🔬 A/B Test: WITHOUT examples"

            st.success(success_msg)

            # Store in session state
            if 'generated_articles' not in st.session_state:
                st.session_state.generated_articles = []

            article_data = {
                'source_filename': selected_transcript['filename'],
                'content': article_content,
                'word_count': article_result['word_count'],
                'style': article_style,
                'seo_metadata': seo_result if seo_result['success'] else {},
                'social_snippets': social_result if social_result['success'] else {},
                'custom_terms': custom_terms,
                'ab_test_variant': article_result.get('ab_test_variant', 'unknown'),
                'use_examples': use_examples,
                'num_examples_used': article_result.get('num_examples_used', 0)
            }

            st.session_state.generated_articles.append(article_data)

            # Display article
            st.markdown("---")
            st.markdown("### 📄 Generated Article")

            # Article editor
            edited_article = st.text_area(
                "Article Content (editable)",
                value=article_content,
                height=500,
                key=f"article_{len(st.session_state.generated_articles)}"
            )

            # SEO Metadata
            if seo_result.get('success'):
                st.markdown("### 📊 SEO Metadata")
                col1, col2 = st.columns(2)

                with col1:
                    if 'seo_title' in seo_result:
                        st.text_input("SEO Title", value=seo_result['seo_title'], disabled=True)
                    if 'url_slug' in seo_result:
                        st.text_input("URL Slug", value=seo_result['url_slug'], disabled=True)

                with col2:
                    if 'meta_description' in seo_result:
                        st.text_area("Meta Description", value=seo_result['meta_description'], height=80, disabled=True)

                if 'keywords' in seo_result:
                    st.caption(f"**Keywords:** {seo_result['keywords']}")

            # Social Snippets
            if social_result.get('success'):
                with st.expander("📱 Social Media Snippets", expanded=False):
                    st.markdown(social_result['snippets'])

            # Download options
            st.markdown("### 💾 Download")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.download_button(
                    label="📥 Download Article (TXT)",
                    data=edited_article,
                    file_name=f"groover_article_{selected_transcript['filename']}.txt",
                    mime="text/plain"
                )

            with col2:
                st.download_button(
                    label="📥 Download Article (MD)",
                    data=edited_article,
                    file_name=f"groover_article_{selected_transcript['filename']}.md",
                    mime="text/markdown"
                )

            st.info("✅ Article saved! Go to 'Export' page for more export options.")

        except ValueError as e:
            st.error(f"❌ {str(e)}")
            st.info("💡 Please add your ANTHROPIC_API_KEY to the .env file")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

    # Display existing articles
    if 'generated_articles' in st.session_state and st.session_state.generated_articles:
        st.markdown("---")
        st.subheader("📚 Generated Articles")

        for i, article in enumerate(st.session_state.generated_articles):
            with st.expander(f"📄 {article['source_filename']} ({article['word_count']} words)", expanded=False):
                st.markdown(article['content'][:300] + "...")

                st.caption(f"Style: {article['style']} | Custom terms: {', '.join(article.get('custom_terms', [])[:3]) if article.get('custom_terms') else 'None'}")

                st.download_button(
                    label="📥 Download",
                    data=article['content'],
                    file_name=f"groover_article_{i+1}.md",
                    mime="text/markdown",
                    key=f"download_existing_{i}"
                )
