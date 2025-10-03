"""
Lessons API Routes
Handles lesson retrieval and AI content generation
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List, Optional
from pydantic import BaseModel
from loguru import logger

from app.services.xml_parser import xml_parser
from app.services.ai_generator import ai_generator


router = APIRouter()


# Pydantic Schemas
class LessonResponse(BaseModel):
    """Response model for lesson data"""
    id: str
    title: str
    keywords: List[str]
    difficulty: str
    module_id: str
    course_id: str


class LessonContentResponse(BaseModel):
    """Response model for full lesson content"""
    lesson_info: LessonResponse
    content: dict


class CourseListResponse(BaseModel):
    """Response model for course list"""
    id: str
    name: str
    language: str
    module_count: int


@router.get("/courses", response_model=List[CourseListResponse])
async def get_all_courses():
    """
    Get list of all available courses

    Returns:
        List of courses with basic info
    """
    try:
        courses = xml_parser.load_all_courses()

        return [
            CourseListResponse(
                id=course.id,
                name=course.name,
                language=course.language,
                module_count=len(course.modules)
            )
            for course in courses.values()
        ]
    except Exception as e:
        logger.error(f"Error fetching courses: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch courses")


@router.get("/courses/{course_id}/modules")
async def get_course_modules(course_id: str):
    """
    Get all modules in a course

    Args:
        course_id: Course identifier

    Returns:
        Course structure with modules and lessons
    """
    try:
        course = xml_parser.get_course(course_id)

        if not course:
            raise HTTPException(status_code=404, detail="Course not found")

        modules_data = []
        for module in course.modules:
            lessons_data = [
                {
                    "id": topic.id,
                    "title": topic.title,
                    "difficulty": topic.difficulty,
                    "keywords": topic.keywords
                }
                for topic in module.topics
            ]

            modules_data.append({
                "id": module.id,
                "name": module.name,
                "lesson_count": len(module.topics),
                "lessons": lessons_data
            })

        return {
            "course_id": course.id,
            "course_name": course.name,
            "language": course.language,
            "modules": modules_data
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching course modules: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch modules")


@router.get("/lessons/{lesson_id}", response_model=LessonContentResponse)
async def get_lesson(lesson_id: str, regenerate: bool = False):
    """
    Get full lesson content with AI-generated materials

    Args:
        lesson_id: Lesson identifier
        regenerate: Force regenerate content (default: False, uses cache)

    Returns:
        Complete lesson with AI-generated content
    """
    try:
        # Get lesson metadata from XML
        topic = xml_parser.get_topic_by_id(lesson_id)

        if not topic:
            raise HTTPException(status_code=404, detail="Lesson not found")

        logger.info(f"Fetching lesson: {topic.title}")

        # TODO: Check cache first (Redis) unless regenerate=True
        # For now, generate fresh content

        # Generate AI content
        content = ai_generator.generate_lesson_content(
            title=topic.title,
            keywords=topic.keywords,
            difficulty=topic.difficulty
        )

        # TODO: Find course_id and module_id (need to enhance XML parser)
        lesson_info = LessonResponse(
            id=topic.id,
            title=topic.title,
            keywords=topic.keywords,
            difficulty=topic.difficulty,
            module_id="unknown",  # TODO: Get from parser
            course_id="unknown"   # TODO: Get from parser
        )

        return LessonContentResponse(
            lesson_info=lesson_info,
            content=content
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating lesson content: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate lesson content")


@router.get("/lessons/{lesson_id}/quiz")
async def get_lesson_quiz(lesson_id: str, num_questions: int = 5):
    """
    Get quiz for a lesson

    Args:
        lesson_id: Lesson identifier
        num_questions: Number of questions (default: 5)

    Returns:
        Quiz with multiple-choice questions
    """
    try:
        topic = xml_parser.get_topic_by_id(lesson_id)

        if not topic:
            raise HTTPException(status_code=404, detail="Lesson not found")

        logger.info(f"Generating quiz for: {topic.title}")

        quiz = ai_generator.generate_quiz(
            title=topic.title,
            keywords=topic.keywords,
            num_questions=num_questions
        )

        return {
            "lesson_id": lesson_id,
            "lesson_title": topic.title,
            "quiz": quiz
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating quiz: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate quiz")


@router.get("/lessons/{lesson_id}/game")
async def get_lesson_game(lesson_id: str):
    """
    Get mini-game for practicing lesson concepts

    Args:
        lesson_id: Lesson identifier

    Returns:
        Mini-game description and starter code
    """
    try:
        topic = xml_parser.get_topic_by_id(lesson_id)

        if not topic:
            raise HTTPException(status_code=404, detail="Lesson not found")

        logger.info(f"Generating mini-game for: {topic.title}")

        game = ai_generator.generate_mini_game(
            title=topic.title,
            keywords=topic.keywords
        )

        return {
            "lesson_id": lesson_id,
            "lesson_title": topic.title,
            "game": game
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating mini-game: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate mini-game")


@router.post("/lessons/reload")
async def reload_topics():
    """
    Reload all topics from XML files
    Useful for dynamic updates

    Returns:
        Status message
    """
    try:
        courses = xml_parser.reload_courses()
        total_topics = len(xml_parser.get_all_topics())

        logger.success(f"Reloaded {len(courses)} courses with {total_topics} topics")

        return {
            "status": "success",
            "courses_loaded": len(courses),
            "total_topics": total_topics,
            "message": "Topics reloaded successfully"
        }

    except Exception as e:
        logger.error(f"Error reloading topics: {e}")
        raise HTTPException(status_code=500, detail="Failed to reload topics")
