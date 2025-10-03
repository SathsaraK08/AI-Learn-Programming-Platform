"""
AI Content Generator Service
Uses Google Gemini API to generate educational content
"""

import google.generativeai as genai
from typing import Dict, Optional, List
from loguru import logger
from app.core.config import settings


class AIContentGenerator:
    """
    Generates educational content using Google Gemini API
    Creates explanations, examples, analogies, quizzes, and practice exercises
    """

    def __init__(self):
        """Initialize Gemini API"""
        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
            logger.success("✅ Gemini AI initialized successfully")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Gemini AI: {e}")
            raise

    def generate_lesson_content(
        self,
        title: str,
        keywords: List[str],
        difficulty: str = "beginner"
    ) -> Dict:
        """
        Generate complete lesson content for a topic

        Args:
            title: Lesson title
            keywords: List of relevant keywords
            difficulty: beginner, intermediate, or advanced

        Returns:
            Dictionary containing lesson content
        """
        try:
            keywords_str = ", ".join(keywords)

            prompt = f"""
You are an expert programming teacher creating content for absolute beginners (even children can understand).

Topic: {title}
Keywords: {keywords_str}
Difficulty: {difficulty}

Generate a comprehensive lesson with the following sections:

1. **Simple Explanation** (2-3 sentences):
   - Explain the concept in the simplest way possible
   - Use everyday language

2. **Real-World Analogy**:
   - Provide a relatable real-world analogy (like comparing classes to cookie cutters)
   - Make it memorable and fun

3. **Why It Matters**:
   - Explain why this concept is important
   - Give practical use cases

4. **Code Example** (Python):
   - Provide a simple, well-commented code example
   - Make it practical and runnable
   - Include comments explaining each part

5. **Step-by-Step Breakdown**:
   - Break down the code example line by line
   - Explain what each part does

6. **Common Mistakes**:
   - List 3 common mistakes beginners make
   - Explain how to avoid them

7. **Practice Challenge**:
   - Create a simple coding challenge (not too hard)
   - Provide clear instructions
   - Include expected output

Format your response as JSON with these keys:
{{
  "explanation": "...",
  "analogy": "...",
  "why_it_matters": "...",
  "code_example": "...",
  "breakdown": ["step1", "step2", ...],
  "common_mistakes": ["mistake1", "mistake2", "mistake3"],
  "practice_challenge": {{
    "description": "...",
    "starter_code": "...",
    "expected_output": "..."
  }}
}}
"""

            logger.info(f"Generating lesson content for: {title}")
            response = self.model.generate_content(prompt)

            # Parse response (assuming JSON format)
            import json
            content = json.loads(response.text.strip().replace("```json", "").replace("```", ""))

            logger.success(f"✅ Generated lesson content for: {title}")
            return content

        except Exception as e:
            logger.error(f"❌ Error generating lesson content: {e}")
            return self._get_fallback_content(title)

    def generate_quiz(
        self,
        title: str,
        keywords: List[str],
        num_questions: int = 5
    ) -> Dict:
        """
        Generate a quiz for a topic

        Args:
            title: Topic title
            keywords: Relevant keywords
            num_questions: Number of quiz questions

        Returns:
            Dictionary containing quiz questions
        """
        try:
            keywords_str = ", ".join(keywords)

            prompt = f"""
Create a quiz for the topic: {title}
Keywords: {keywords_str}

Generate {num_questions} multiple-choice questions that test understanding.

Requirements:
- Mix of easy and challenging questions
- 4 options per question (A, B, C, D)
- Include explanation for correct answer
- Make questions practical and relevant

Format as JSON:
{{
  "questions": [
    {{
      "question": "...",
      "options": {{
        "A": "...",
        "B": "...",
        "C": "...",
        "D": "..."
      }},
      "correct_answer": "A",
      "explanation": "..."
    }}
  ]
}}
"""

            logger.info(f"Generating quiz for: {title}")
            response = self.model.generate_content(prompt)

            import json
            quiz = json.loads(response.text.strip().replace("```json", "").replace("```", ""))

            logger.success(f"✅ Generated quiz with {len(quiz['questions'])} questions")
            return quiz

        except Exception as e:
            logger.error(f"❌ Error generating quiz: {e}")
            return {"questions": []}

    def generate_mini_game(
        self,
        title: str,
        keywords: List[str]
    ) -> Dict:
        """
        Generate a mini-game concept for practicing the topic

        Args:
            title: Topic title
            keywords: Relevant keywords

        Returns:
            Dictionary with game description and code
        """
        try:
            keywords_str = ", ".join(keywords)

            prompt = f"""
Create a fun, simple mini-game that helps practice: {title}
Keywords: {keywords_str}

The game should:
- Be playable in the terminal/browser
- Reinforce the concept through interaction
- Be fun and engaging
- Include score/progress tracking

Format as JSON:
{{
  "game_name": "...",
  "description": "...",
  "instructions": ["step1", "step2", ...],
  "starter_code": "...",
  "learning_goal": "..."
}}
"""

            logger.info(f"Generating mini-game for: {title}")
            response = self.model.generate_content(prompt)

            import json
            game = json.loads(response.text.strip().replace("```json", "").replace("```", ""))

            logger.success(f"✅ Generated mini-game: {game.get('game_name', 'Unnamed')}")
            return game

        except Exception as e:
            logger.error(f"❌ Error generating mini-game: {e}")
            return {}

    def _get_fallback_content(self, title: str) -> Dict:
        """Fallback content if AI generation fails"""
        return {
            "explanation": f"This lesson covers {title}. Content generation temporarily unavailable.",
            "analogy": "Think of this like learning to ride a bike - practice makes perfect!",
            "why_it_matters": "This is a fundamental concept in programming.",
            "code_example": "# Example code will be generated",
            "breakdown": ["Content generation in progress"],
            "common_mistakes": ["Content will be available soon"],
            "practice_challenge": {
                "description": "Practice challenge coming soon",
                "starter_code": "# Your code here",
                "expected_output": "Output example"
            }
        }


# Global AI generator instance
ai_generator = AIContentGenerator()
