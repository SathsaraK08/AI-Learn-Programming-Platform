"""
XML Topic Parser Service
Parses XML files containing course topics and lessons
Provides topic data to AI for content generation
"""

import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Optional
from loguru import logger
import xmltodict


class Topic:
    """Represents a learning topic/lesson"""

    def __init__(self, topic_id: str, title: str, keywords: List[str], difficulty: str = "beginner"):
        self.id = topic_id
        self.title = title
        self.keywords = keywords
        self.difficulty = difficulty

    def __repr__(self):
        return f"Topic(id={self.id}, title={self.title}, difficulty={self.difficulty})"


class Module:
    """Represents a course module containing multiple topics"""

    def __init__(self, module_id: str, name: str):
        self.id = module_id
        self.name = name
        self.topics: List[Topic] = []

    def add_topic(self, topic: Topic):
        self.topics.append(topic)

    def __repr__(self):
        return f"Module(id={self.id}, name={self.name}, topics={len(self.topics)})"


class Course:
    """Represents a complete course with modules"""

    def __init__(self, course_id: str, name: str, language: str):
        self.id = course_id
        self.name = name
        self.language = language
        self.modules: List[Module] = []

    def add_module(self, module: Module):
        self.modules.append(module)

    def __repr__(self):
        return f"Course(id={self.id}, name={self.name}, modules={len(self.modules)})"


class XMLTopicParser:
    """
    Parses XML topic files and provides structured data
    Supports dynamic topic loading and updates
    """

    def __init__(self, topics_directory: str = "data/topics"):
        # If relative path, make it relative to project root
        topics_path = Path(topics_directory)
        if not topics_path.is_absolute():
            # Get project root (3 levels up from this file: services -> app -> backend -> root)
            project_root = Path(__file__).resolve().parent.parent.parent.parent
            self.topics_dir = project_root / topics_directory
        else:
            self.topics_dir = topics_path

        self.courses: Dict[str, Course] = {}
        logger.info(f"Initialized XMLTopicParser with directory: {self.topics_dir}")

    def parse_course_file(self, xml_file_path: Path) -> Optional[Course]:
        """
        Parse a single XML course file

        Args:
            xml_file_path: Path to XML file

        Returns:
            Course object or None if parsing fails
        """
        try:
            logger.info(f"Parsing course file: {xml_file_path}")

            with open(xml_file_path, 'r', encoding='utf-8') as f:
                data = xmltodict.parse(f.read())

            course_data = data.get('course', {})
            course_id = course_data.get('@id', '')
            course_name = course_data.get('name', '')
            language = course_data.get('@language', 'python')

            course = Course(course_id, course_name, language)

            # Parse modules
            modules_data = course_data.get('modules', {}).get('module', [])
            if not isinstance(modules_data, list):
                modules_data = [modules_data]

            for module_data in modules_data:
                module_id = module_data.get('@id', '')
                module_name = module_data.get('name', '')
                module = Module(module_id, module_name)

                # Parse lessons/topics
                lessons_data = module_data.get('lessons', {}).get('lesson', [])
                if not isinstance(lessons_data, list):
                    lessons_data = [lessons_data]

                for lesson_data in lessons_data:
                    lesson_id = lesson_data.get('@id', '')
                    title = lesson_data.get('title', '')
                    difficulty = lesson_data.get('@difficulty', 'beginner')
                    keywords_str = lesson_data.get('keywords', '')
                    keywords = [k.strip() for k in keywords_str.split(',') if k.strip()]

                    topic = Topic(lesson_id, title, keywords, difficulty)
                    module.add_topic(topic)

                course.add_module(module)

            logger.success(f"Successfully parsed course: {course_name} with {len(course.modules)} modules")
            return course

        except Exception as e:
            logger.error(f"Error parsing XML file {xml_file_path}: {e}")
            return None

    def load_all_courses(self) -> Dict[str, Course]:
        """
        Load all XML course files from topics directory

        Returns:
            Dictionary of course_id -> Course objects
        """
        if not self.topics_dir.exists():
            logger.warning(f"Topics directory does not exist: {self.topics_dir}")
            return {}

        xml_files = list(self.topics_dir.glob("*.xml"))
        logger.info(f"Found {len(xml_files)} XML course files")

        for xml_file in xml_files:
            course = self.parse_course_file(xml_file)
            if course:
                self.courses[course.id] = course

        logger.success(f"Loaded {len(self.courses)} courses successfully")
        return self.courses

    def get_course(self, course_id: str) -> Optional[Course]:
        """Get a specific course by ID"""
        return self.courses.get(course_id)

    def get_all_topics(self) -> List[Topic]:
        """Get all topics from all courses"""
        topics = []
        for course in self.courses.values():
            for module in course.modules:
                topics.extend(module.topics)
        return topics

    def get_topic_by_id(self, topic_id: str) -> Optional[Topic]:
        """Find a topic by its ID across all courses"""
        for course in self.courses.values():
            for module in course.modules:
                for topic in module.topics:
                    if topic.id == topic_id:
                        return topic
        return None

    def reload_courses(self):
        """Reload all courses from disk (for dynamic updates)"""
        logger.info("Reloading all courses...")
        self.courses.clear()
        return self.load_all_courses()


# Global parser instance
xml_parser = XMLTopicParser()
