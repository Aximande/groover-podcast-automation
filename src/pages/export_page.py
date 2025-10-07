"""
Export Page
Streamlit interface for exporting articles in multiple formats
"""

import streamlit as st
import json
from src.export_formats import get_format_exporter


def render_export_page():
    """Render the export page"""

    st.header("📊 Export Articles")

    # Check if articles exist
    if 'generated_articles' not in st.session_state or not st.session_state.generated_articles:
        st.warning("⚠️ No generated articles found. Please generate content first.")
        st.info("👈 Go to 'Generate Content' page to create articles")
        return

    articles = st.session_state.generated_articles

    st.success(f"✅ Ready to export {len(articles)} article(s)")

    # Select article to export
    st.subheader("📄 Select Article")

    selected_index = st.selectbox(
        "Choose an article",
        options=range(len(articles)),
        format_func=lambda i: f"{articles[i]['source_filename']} ({articles[i]['word_count']} words)"
    )

    selected_article = articles[selected_index]

    # Display article preview
    with st.expander("📝 Article Preview", expanded=False):
        st.markdown(selected_article['content'][:500] + "...")
        st.caption(f"Word count: {selected_article['word_count']} | Style: {selected_article['style']}")

    # Export options
    st.subheader("📤 Export Formats")

    exporter = get_format_exporter()

    # Get all formats
    all_formats = exporter.export_all_formats(
        selected_article['content'],
        selected_article.get('seo_metadata')
    )

    # Format selection
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### 📝 Text Formats")

        # Markdown
        st.download_button(
            label="📥 Markdown (.md)",
            data=all_formats['markdown'],
            file_name=f"groover_article_{selected_index + 1}.md",
            mime="text/markdown",
            use_container_width=True
        )

        # Plain text
        plain_text = all_formats['markdown'].replace('#', '').replace('*', '').replace('_', '')
        st.download_button(
            label="📥 Plain Text (.txt)",
            data=plain_text,
            file_name=f"groover_article_{selected_index + 1}.txt",
            mime="text/plain",
            use_container_width=True
        )

    with col2:
        st.markdown("#### 🌐 Web Formats")

        # HTML with CSS
        st.download_button(
            label="📥 HTML (styled)",
            data=all_formats['html'],
            file_name=f"groover_article_{selected_index + 1}.html",
            mime="text/html",
            use_container_width=True
        )

        # HTML without CSS
        st.download_button(
            label="📥 HTML (no CSS)",
            data=all_formats['html_no_css'],
            file_name=f"groover_article_{selected_index + 1}_plain.html",
            mime="text/html",
            use_container_width=True
        )

    with col3:
        st.markdown("#### 📊 Data Formats")

        # JSON export
        json_data = json.dumps(all_formats['json'], indent=2)
        st.download_button(
            label="📥 JSON",
            data=json_data,
            file_name=f"groover_article_{selected_index + 1}.json",
            mime="application/json",
            use_container_width=True
        )

        # WordPress data
        wordpress_json = json.dumps(all_formats['wordpress'], indent=2)
        st.download_button(
            label="📥 WordPress JSON",
            data=wordpress_json,
            file_name=f"groover_article_{selected_index + 1}_wordpress.json",
            mime="application/json",
            use_container_width=True
        )

    # Content components
    st.markdown("---")
    st.subheader("🎯 Content Components")

    tab1, tab2, tab3 = st.tabs(["📋 Key Quotes", "💡 Main Insights", "📱 Social Graphics"])

    with tab1:
        st.markdown("#### Key Quotes")
        quotes = all_formats['quotes']

        if quotes:
            for i, quote in enumerate(quotes, 1):
                st.info(f"**Quote {i}:** {quote}")

            # Download quotes
            quotes_text = "\n\n".join([f"{i}. {q}" for i, q in enumerate(quotes, 1)])
            st.download_button(
                label="📥 Download All Quotes",
                data=quotes_text,
                file_name=f"groover_quotes_{selected_index + 1}.txt",
                mime="text/plain"
            )
        else:
            st.caption("No quotes extracted from this article")

    with tab2:
        st.markdown("#### Main Insights")
        insights = all_formats['insights']

        if insights:
            for i, insight in enumerate(insights, 1):
                st.success(f"**Insight {i}:** {insight}")

            # Download insights
            insights_text = "\n\n".join([f"{i}. {ins}" for i, ins in enumerate(insights, 1)])
            st.download_button(
                label="📥 Download All Insights",
                data=insights_text,
                file_name=f"groover_insights_{selected_index + 1}.txt",
                mime="text/plain"
            )
        else:
            st.caption("No insights extracted from this article")

    with tab3:
        st.markdown("#### Social Media Graphics Text")
        graphics = all_formats['social_graphics']

        if graphics:
            for i, graphic in enumerate(graphics, 1):
                if graphic['type'] == 'title':
                    st.markdown(f"**🎨 Header Card**")
                    st.info(graphic['text'])
                elif graphic['type'] == 'quote':
                    st.markdown(f"**💬 Quote Card {i}**")
                    st.success(graphic['text'])
                elif graphic['type'] == 'insight':
                    st.markdown(f"**💡 Tip Card {i}**")
                    st.warning(graphic['text'])

            # Download graphics data
            graphics_json = json.dumps(graphics, indent=2)
            st.download_button(
                label="📥 Download Graphics JSON",
                data=graphics_json,
                file_name=f"groover_graphics_{selected_index + 1}.json",
                mime="application/json"
            )
        else:
            st.caption("No graphics generated")

    # WordPress preview
    st.markdown("---")
    st.subheader("🌐 WordPress Ready")

    with st.expander("📋 WordPress Data Preview", expanded=False):
        wp_data = all_formats['wordpress']

        col1, col2 = st.columns(2)

        with col1:
            st.text_input("Title", value=wp_data['title'], disabled=True)
            st.text_input("Status", value=wp_data['status'], disabled=True)
            st.text_input("SEO Title", value=wp_data.get('seo_title', ''), disabled=True)

        with col2:
            st.text_area("Excerpt", value=wp_data['excerpt'], height=80, disabled=True)
            st.text_area("Meta Description", value=wp_data.get('meta_description', ''), height=80, disabled=True)

        st.caption(f"**Categories:** {', '.join(wp_data['categories'])}")
        st.caption(f"**Tags:** {', '.join(wp_data['tags'])}")

        st.markdown("#### Content Preview (HTML)")
        st.code(wp_data['content'][:500] + "...", language="html")

    # Batch export
    st.markdown("---")
    st.subheader("📦 Batch Export")

    if len(articles) > 1:
        st.info(f"Export all {len(articles)} articles at once")

        col1, col2 = st.columns(2)

        with col1:
            export_format = st.selectbox(
                "Select batch export format",
                options=['markdown', 'html', 'json', 'wordpress_json'],
                format_func=lambda x: {
                    'markdown': 'Markdown (.md)',
                    'html': 'HTML (styled)',
                    'json': 'JSON',
                    'wordpress_json': 'WordPress JSON'
                }[x]
            )

        with col2:
            batch_export_button = st.button(
                "📥 Export All Articles",
                type="primary",
                use_container_width=True
            )

        if batch_export_button:
            batch_data = []

            for i, article in enumerate(articles):
                formats = exporter.export_all_formats(
                    article['content'],
                    article.get('seo_metadata')
                )

                if export_format == 'markdown':
                    batch_data.append(f"# Article {i+1}: {article['source_filename']}\n\n{formats['markdown']}\n\n---\n\n")
                elif export_format == 'html':
                    batch_data.append(formats['html'])
                elif export_format == 'json':
                    batch_data.append(formats['json'])
                elif export_format == 'wordpress_json':
                    batch_data.append(formats['wordpress'])

            if export_format in ['markdown', 'html']:
                batch_content = '\n\n'.join(batch_data)
                ext = 'md' if export_format == 'markdown' else 'html'

                st.download_button(
                    label=f"📥 Download All ({export_format.upper()})",
                    data=batch_content,
                    file_name=f"groover_articles_batch.{ext}",
                    mime="text/markdown" if export_format == 'markdown' else "text/html"
                )
            else:
                batch_json = json.dumps(batch_data, indent=2)

                st.download_button(
                    label="📥 Download All (JSON)",
                    data=batch_json,
                    file_name="groover_articles_batch.json",
                    mime="application/json"
                )

            st.success(f"✅ Batch export ready! ({len(articles)} articles)")

    else:
        st.caption("Only 1 article available. Generate more articles to use batch export.")

    # Export statistics
    st.markdown("---")
    st.subheader("📈 Export Statistics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Articles", len(articles))

    with col2:
        total_words = sum(a['word_count'] for a in articles)
        st.metric("Total Words", f"{total_words:,}")

    with col3:
        total_quotes = len(all_formats['quotes'])
        st.metric("Quotes", total_quotes)

    with col4:
        total_insights = len(all_formats['insights'])
        st.metric("Insights", total_insights)
