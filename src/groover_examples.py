"""
Groover Reference Articles Loader
Loads example articles to use as tone/style references in prompts
"""

import os
import random
from typing import List, Dict, Optional


class GrooverExamplesLoader:
    """Handles loading and managing Groover reference articles"""

    def __init__(self, examples_dir: str = "groover_tone_of_voice"):
        self.examples_dir = examples_dir
        self.articles = []
        self.load_articles()

    def load_articles(self) -> None:
        """Load all Groover example articles from directory"""
        if not os.path.exists(self.examples_dir):
            return

        for filename in os.listdir(self.examples_dir):
            if filename.endswith('.txt') and filename.startswith('ArticleGroover'):
                filepath = os.path.join(self.examples_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        self.articles.append({
                            'filename': filename,
                            'content': content,
                            'word_count': len(content.split())
                        })
                except Exception as e:
                    print(f"Error loading {filename}: {e}")

    def get_random_examples(self, num_examples: int = 2) -> List[Dict]:
        """
        Get random example articles

        Args:
            num_examples: Number of examples to return

        Returns:
            List of article dictionaries
        """
        if not self.articles:
            return []

        num_to_select = min(num_examples, len(self.articles))
        return random.sample(self.articles, num_to_select)

    def get_examples_by_length(self, target_length: str = 'long', num_examples: int = 2) -> List[Dict]:
        """
        Get examples closest to target length

        Args:
            target_length: 'long' (2000+) or 'short' (500-800)
            num_examples: Number of examples

        Returns:
            List of article dictionaries
        """
        if not self.articles:
            return []

        # Define length criteria
        if target_length == 'long':
            target_words = 2000
        else:
            target_words = 650

        # Sort by proximity to target word count
        sorted_articles = sorted(
            self.articles,
            key=lambda x: abs(x['word_count'] - target_words)
        )

        return sorted_articles[:num_examples]

    def create_examples_context(
        self,
        num_examples: int = 2,
        target_length: Optional[str] = None,
        max_words_per_example: int = 800
    ) -> str:
        """
        Create formatted context string with examples for prompt

        Args:
            num_examples: Number of examples to include
            target_length: Optional length preference
            max_words_per_example: Max words to include from each example

        Returns:
            Formatted examples context string
        """
        if not self.articles:
            return ""

        # Get examples
        if target_length:
            examples = self.get_examples_by_length(target_length, num_examples)
        else:
            examples = self.get_random_examples(num_examples)

        if not examples:
            return ""

        # Build context
        context_parts = ["Here are examples of Groover's writing style:\n"]

        for i, article in enumerate(examples, 1):
            # Truncate if too long
            words = article['content'].split()
            if len(words) > max_words_per_example:
                truncated_content = ' '.join(words[:max_words_per_example]) + '...'
            else:
                truncated_content = article['content']

            context_parts.append(f"\n--- EXAMPLE {i} ---\n{truncated_content}\n")

        context_parts.append("\nUse these examples to understand Groover's tone, style, and structure. Match this casual, musician-friendly approach.\n")

        return ''.join(context_parts)

    def get_all_articles(self) -> List[Dict]:
        """Get all loaded articles"""
        return self.articles

    def get_stats(self) -> Dict:
        """Get statistics about loaded articles"""
        if not self.articles:
            return {
                'count': 0,
                'total_words': 0,
                'avg_words': 0,
                'min_words': 0,
                'max_words': 0
            }

        word_counts = [a['word_count'] for a in self.articles]

        return {
            'count': len(self.articles),
            'total_words': sum(word_counts),
            'avg_words': sum(word_counts) // len(word_counts),
            'min_words': min(word_counts),
            'max_words': max(word_counts)
        }


def get_groover_examples_loader(examples_dir: str = "groover_tone_of_voice") -> GrooverExamplesLoader:
    """Factory function to get examples loader"""
    return GrooverExamplesLoader(examples_dir)
