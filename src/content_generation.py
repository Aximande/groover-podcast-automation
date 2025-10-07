"""
Content Generation Module using Anthropic Claude API
Generates blog articles from podcast transcripts in Groover's tone and style
Supports A/B testing with and without Groover reference articles
"""

import os
from typing import Dict, List, Optional
from anthropic import Anthropic
from dotenv import load_dotenv
from src.groover_examples import get_groover_examples_loader

load_dotenv()


class ContentGenerator:
    """Handles content generation using Claude API"""

    # Groover's tone and style guide based on analyzed articles
    GROOVER_STYLE_GUIDE = """
    Groover's Writing Style:
    - Casual, friendly, and conversational tone
    - Direct address to musicians and artists ("you")
    - Use of emojis strategically for visual breaks and emphasis
    - Short, punchy paragraphs for easy reading
    - Practical, actionable advice
    - Mix of inspiration and pragmatism
    - Industry insights made accessible
    - Examples and real-world scenarios
    - Summary sections with bullet points using emojis
    - Clear structure with headers
    - Focus on empowering independent artists
    """

    def __init__(self, model: str = "claude-sonnet-4-5-20250929"):
        self.client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        self.model = model
        self.examples_loader = get_groover_examples_loader()

    def generate_article(
        self,
        transcript: str,
        style: str = "long",
        editorial_angle: Optional[str] = None,
        custom_instructions: Optional[str] = None,
        use_examples: bool = False,
        num_examples: int = 2
    ) -> Dict:
        """
        Generate a blog article from podcast transcript

        Args:
            transcript: Corrected podcast transcript
            style: 'long' (2000+ words) or 'short' (500-800 words)
            editorial_angle: Optional specific angle/focus for the article
            custom_instructions: Additional instructions for generation
            use_examples: Whether to include Groover article examples (A/B testing)
            num_examples: Number of example articles to include if use_examples=True

        Returns:
            Dictionary with generated article and metadata
        """
        # Determine word count target
        word_count = "2000-2500" if style == "long" else "500-800"

        # Build the generation prompt with or without examples
        if use_examples:
            examples_context = self.examples_loader.create_examples_context(
                num_examples=num_examples,
                target_length=style,
                max_words_per_example=800
            )

            system_prompt = f"""{self.GROOVER_STYLE_GUIDE}

{examples_context}

You are a content writer for Groover, the music promotion platform. Your job is to transform podcast transcripts into engaging blog articles that help musicians grow their careers.

Use the examples above to match Groover's exact writing style, structure, and tone."""
        else:
            system_prompt = f"""{self.GROOVER_STYLE_GUIDE}

You are a content writer for Groover, the music promotion platform. Your job is to transform podcast transcripts into engaging blog articles that help musicians grow their careers."""

        user_prompt = f"""Transform the following podcast transcript into a compelling blog article for Groover's blog.

TARGET WORD COUNT: {word_count} words

{"EDITORIAL ANGLE: " + editorial_angle if editorial_angle else ""}

{"ADDITIONAL INSTRUCTIONS: " + custom_instructions if custom_instructions else ""}

REQUIREMENTS:
1. Create an engaging, SEO-friendly title
2. Write in Groover's casual, musician-friendly tone
3. Structure with clear headers and sections
4. Use emojis strategically for visual breaks (like the examples: =�, <�, =�)
5. Include actionable takeaways for musicians
6. Add a compelling summary/intro section with bullet points
7. End with a strong call-to-action or bottom line
8. Make complex industry concepts accessible
9. Use "you" to directly address the reader (musicians)
10. Keep paragraphs short and punchy

PODCAST TRANSCRIPT:
{transcript}

Generate the complete article following Groover's style."""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=4000 if style == "long" else 2000,
                temperature=0.7,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )

            article_content = message.content[0].text

            return {
                'success': True,
                'content': article_content,
                'word_count': len(article_content.split()),
                'style': style,
                'editorial_angle': editorial_angle,
                'model_used': self.model,
                'use_examples': use_examples,
                'num_examples_used': num_examples if use_examples else 0,
                'ab_test_variant': 'with_examples' if use_examples else 'without_examples'
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def generate_multiple_angles(
        self,
        transcript: str,
        num_angles: int = 3
    ) -> List[Dict]:
        """
        Generate multiple editorial angles from a single transcript

        Args:
            transcript: Podcast transcript
            num_angles: Number of different angles to generate

        Returns:
            List of angle suggestions
        """
        prompt = f"""Analyze this podcast transcript and suggest {num_angles} different editorial angles for blog articles.

For each angle:
1. Provide a compelling article title
2. Describe the key focus/angle
3. Explain why this would resonate with musicians
4. Suggest 3-5 main talking points

TRANSCRIPT:
{transcript}

Return your analysis in a clear, structured format."""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                temperature=0.8,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            angles_text = message.content[0].text

            return {
                'success': True,
                'angles_text': angles_text,
                'num_angles': num_angles
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def generate_seo_metadata(self, article_content: str) -> Dict:
        """
        Generate SEO-optimized title and meta description

        Args:
            article_content: Generated article content

        Returns:
            Dictionary with SEO metadata
        """
        prompt = f"""Based on this blog article, generate SEO-optimized metadata:

1. SEO Title (max 60 characters, compelling and keyword-rich)
2. Meta Description (max 160 characters, engaging summary with call-to-action)
3. 5-7 relevant keywords/tags
4. Suggested URL slug

ARTICLE:
{article_content[:1000]}...

Return in this exact format:
SEO Title: [title]
Meta Description: [description]
Keywords: [keyword1, keyword2, ...]
URL Slug: [slug]"""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=500,
                temperature=0.5,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            metadata_text = message.content[0].text

            # Parse the response
            lines = metadata_text.strip().split('\n')
            metadata = {}

            for line in lines:
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip().lower().replace(' ', '_')
                    metadata[key] = value.strip()

            return {
                'success': True,
                **metadata
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def generate_social_snippets(self, article_content: str) -> Dict:
        """
        Generate social media snippets from article

        Args:
            article_content: Article content

        Returns:
            Dictionary with social media snippets
        """
        prompt = f"""Create engaging social media snippets from this article for different platforms:

1. Twitter/X (max 280 characters, include 2-3 relevant hashtags)
2. Instagram caption (engaging, 125-150 characters, use emojis)
3. LinkedIn post (professional but engaging, 150-200 characters)
4. 3-5 key quotes perfect for graphics/cards

ARTICLE:
{article_content[:1500]}...

Format clearly for each platform."""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                temperature=0.7,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            return {
                'success': True,
                'snippets': message.content[0].text
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def enhance_with_groover_context(self, article_content: str) -> Dict:
        """
        Enhance article by adding relevant Groover product mentions/CTAs

        Args:
            article_content: Original article content

        Returns:
            Enhanced article with Groover context
        """
        groover_context = """
        Groover helps artists get their music heard by connecting them directly with curators,
        radios, playlist makers, and labels. Artists get guaranteed feedback and real opportunities
        for coverage, playlist adds, and record deals.
        """

        prompt = f"""Enhance this article by naturally integrating mentions of Groover where relevant.

GROOVER CONTEXT:
{groover_context}

GUIDELINES:
- Add 1-2 natural mentions of how Groover can help with the topics discussed
- Include a relevant call-to-action at the end
- Don't be overly promotional - keep it helpful and organic
- Maintain the article's flow and value

ORIGINAL ARTICLE:
{article_content}

Return the enhanced article."""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                temperature=0.6,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            return {
                'success': True,
                'enhanced_content': message.content[0].text
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }


def get_content_generator(model: str = "claude-sonnet-4-5-20250929") -> ContentGenerator:
    """Factory function to get content generator instance"""
    if not os.getenv('ANTHROPIC_API_KEY'):
        raise ValueError("ANTHROPIC_API_KEY not found in environment variables")

    return ContentGenerator(model)
