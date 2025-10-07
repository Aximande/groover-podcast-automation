"""
Multi-Format Output Generation Module
Converts articles to various formats: Markdown, HTML, WordPress, with SEO optimization
"""

import markdown2
import re
from typing import Dict, List, Optional
from datetime import datetime


class FormatExporter:
    """Handles conversion of articles to various output formats"""

    def __init__(self):
        self.markdown_extras = [
            'fenced-code-blocks',
            'tables',
            'header-ids',
            'metadata',
            'strike',
            'task_list'
        ]

    def extract_title(self, content: str) -> str:
        """Extract title from markdown content"""
        lines = content.strip().split('\n')
        for line in lines:
            if line.startswith('# '):
                return line.replace('# ', '').strip()
        return "Untitled Article"

    def extract_sections(self, content: str) -> List[Dict]:
        """Extract sections with headers"""
        sections = []
        current_section = {'title': 'Introduction', 'content': ''}

        for line in content.split('\n'):
            if line.startswith('##') and not line.startswith('###'):
                if current_section['content'].strip():
                    sections.append(current_section)
                current_section = {
                    'title': line.replace('##', '').strip(),
                    'content': ''
                }
            else:
                current_section['content'] += line + '\n'

        if current_section['content'].strip():
            sections.append(current_section)

        return sections

    def markdown_to_html(self, content: str, include_css: bool = True) -> str:
        """
        Convert Markdown to HTML

        Args:
            content: Markdown content
            include_css: Whether to include basic CSS styling

        Returns:
            HTML string
        """
        # Convert markdown to HTML
        html_content = markdown2.markdown(
            content,
            extras=self.markdown_extras
        )

        if not include_css:
            return html_content

        # Add basic CSS styling
        css = """
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }
            h1 {
                color: #2c3e50;
                border-bottom: 3px solid #3498db;
                padding-bottom: 10px;
            }
            h2 {
                color: #34495e;
                margin-top: 30px;
            }
            h3 {
                color: #7f8c8d;
            }
            p {
                margin-bottom: 15px;
            }
            code {
                background-color: #f4f4f4;
                padding: 2px 6px;
                border-radius: 3px;
                font-family: 'Courier New', monospace;
            }
            blockquote {
                border-left: 4px solid #3498db;
                margin-left: 0;
                padding-left: 20px;
                color: #555;
            }
            ul, ol {
                margin-bottom: 15px;
            }
        </style>
        """

        full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.extract_title(content)}</title>
    {css}
</head>
<body>
    {html_content}
</body>
</html>"""

        return full_html

    def to_wordpress_ready(self, content: str, seo_metadata: Optional[Dict] = None) -> Dict:
        """
        Format content for WordPress import

        Args:
            content: Markdown content
            seo_metadata: Optional SEO metadata

        Returns:
            Dictionary with WordPress-ready data
        """
        # Convert to HTML (without full page structure)
        html_content = markdown2.markdown(
            content,
            extras=self.markdown_extras
        )

        # Extract title
        title = self.extract_title(content)

        # Generate excerpt (first paragraph)
        paragraphs = re.findall(r'<p>(.*?)</p>', html_content, re.DOTALL)
        excerpt = paragraphs[0] if paragraphs else ""

        # Clean excerpt of HTML tags for plain text version
        excerpt_plain = re.sub(r'<[^>]+>', '', excerpt)[:150] + "..."

        wordpress_data = {
            'title': title,
            'content': html_content,
            'excerpt': excerpt_plain,
            'status': 'draft',  # or 'publish'
            'categories': [],
            'tags': [],
            'meta': {}
        }

        # Add SEO metadata if provided
        if seo_metadata:
            wordpress_data['seo_title'] = seo_metadata.get('seo_title', title)
            wordpress_data['meta_description'] = seo_metadata.get('meta_description', excerpt_plain)

            # Extract tags from keywords
            if 'keywords' in seo_metadata:
                keywords = seo_metadata['keywords']
                if isinstance(keywords, str):
                    wordpress_data['tags'] = [k.strip() for k in keywords.split(',')]
                else:
                    wordpress_data['tags'] = keywords

            # Suggested categories (music-related defaults)
            wordpress_data['categories'] = ['Music Industry', 'Artist Tips', 'Music Promotion']

        return wordpress_data

    def extract_key_quotes(self, content: str, num_quotes: int = 5) -> List[str]:
        """
        Extract key quotes from content

        Args:
            content: Article content
            num_quotes: Number of quotes to extract

        Returns:
            List of key quotes
        """
        # Find sentences with quotes
        quoted_sentences = re.findall(r'[^.!?]*"[^"]*"[^.!?]*[.!?]', content)

        if quoted_sentences:
            return quoted_sentences[:num_quotes]

        # If no quoted text, extract impactful sentences
        sentences = re.split(r'[.!?]+', content)

        # Filter for impactful sentences (questions, statements with emphasis)
        impactful = []
        for sentence in sentences:
            sentence = sentence.strip()
            if (len(sentence.split()) > 8 and len(sentence.split()) < 25 and
                ('?' in sentence or '!' in sentence or any(word in sentence.lower()
                for word in ['important', 'key', 'essential', 'must', 'should', 'never']))):
                impactful.append(sentence + '.')

        return impactful[:num_quotes]

    def extract_main_insights(self, content: str, num_insights: int = 3) -> List[str]:
        """
        Extract main insights from content

        Args:
            content: Article content
            num_insights: Number of insights to extract

        Returns:
            List of main insights
        """
        insights = []

        # Look for bullet points and numbered lists
        bullet_points = re.findall(r'[•\-\*]\s+(.+)', content)
        numbered_points = re.findall(r'\d+\.\s+(.+)', content)

        all_points = bullet_points + numbered_points

        # Prioritize points with emojis (Groover style)
        emoji_points = [p for p in all_points if re.search(r'[\U0001F300-\U0001F9FF]', p)]

        if emoji_points:
            insights = emoji_points[:num_insights]
        elif all_points:
            insights = all_points[:num_insights]
        else:
            # Extract from headers as insights
            headers = re.findall(r'##\s+(.+)', content)
            insights = headers[:num_insights]

        return insights

    def create_social_graphics_text(self, content: str) -> List[Dict]:
        """
        Create text optimized for social media graphics

        Args:
            content: Article content

        Returns:
            List of graphic-ready text snippets
        """
        graphics = []

        # Get quotes
        quotes = self.extract_key_quotes(content, 3)
        for quote in quotes:
            graphics.append({
                'type': 'quote',
                'text': quote,
                'style': 'quote-card'
            })

        # Get insights
        insights = self.extract_main_insights(content, 3)
        for insight in insights:
            graphics.append({
                'type': 'insight',
                'text': insight,
                'style': 'tip-card'
            })

        # Extract title as a graphic
        title = self.extract_title(content)
        graphics.insert(0, {
            'type': 'title',
            'text': title,
            'style': 'header-card'
        })

        return graphics

    def export_json(self, content: str, metadata: Optional[Dict] = None) -> Dict:
        """
        Export article as structured JSON

        Args:
            content: Article content
            metadata: Optional metadata

        Returns:
            JSON-serializable dictionary
        """
        sections = self.extract_sections(content)

        export_data = {
            'title': self.extract_title(content),
            'content': content,
            'html': self.markdown_to_html(content, include_css=False),
            'sections': sections,
            'quotes': self.extract_key_quotes(content),
            'insights': self.extract_main_insights(content),
            'social_graphics': self.create_social_graphics_text(content),
            'word_count': len(content.split()),
            'export_date': datetime.now().isoformat()
        }

        if metadata:
            export_data['metadata'] = metadata

        return export_data

    def export_all_formats(self, content: str, metadata: Optional[Dict] = None) -> Dict:
        """
        Export to all available formats

        Args:
            content: Article content
            metadata: Optional metadata

        Returns:
            Dictionary with all formats
        """
        return {
            'markdown': content,
            'html': self.markdown_to_html(content, include_css=True),
            'html_no_css': self.markdown_to_html(content, include_css=False),
            'wordpress': self.to_wordpress_ready(content, metadata),
            'json': self.export_json(content, metadata),
            'quotes': self.extract_key_quotes(content),
            'insights': self.extract_main_insights(content),
            'social_graphics': self.create_social_graphics_text(content)
        }


def get_format_exporter() -> FormatExporter:
    """Factory function to get format exporter instance"""
    return FormatExporter()
