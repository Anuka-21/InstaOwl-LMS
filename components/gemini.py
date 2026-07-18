import streamlit as st
import json
import os
import re
from typing import Iterable

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - keeps fallback mode usable before install
    def load_dotenv(*_args, **_kwargs):
        return False

try:
    from google import genai
    from google.genai import types
except ImportError:  # pragma: no cover - app still works with local AI fallbacks
    genai = None
    types = None

load_dotenv()

MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

SYSTEM_PROMPT = """
You are AI Owl, the AI tutor inside InstaOwl LMS.

Be friendly, encouraging, explain concepts step by step,
generate quizzes when asked, and keep answers concise.
"""


class AIServiceError(RuntimeError):
    """Raised when the hosted AI service is unavailable."""


def get_api_key():
    """Read API key from Streamlit Cloud Secrets or local .env"""
    try:
        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass

    return os.getenv("GEMINI_API_KEY")


def get_ai_status() -> tuple[bool, str]:
    if genai is None or types is None:
        return False, "Gemini SDK is not installed."

    if not get_api_key():
        return False, "Gemini API key not configured."

    return True, "Gemini connected."


def _client():
    ready, message = get_ai_status()

    if not ready:
        raise AIServiceError(message)

    return genai.Client(api_key=get_api_key())


def _to_contents(messages: list[dict[str, str]]):
    contents = []

    for message in messages:
        text = str(message.get("content", "")).strip()
        if not text:
            continue

        role = "user" if message.get("role") == "user" else "model"
        contents.append(
            types.Content(
                role=role,
                parts=[types.Part.from_text(text=text)],
            )
        )

    if not contents:
        contents.append(
            types.Content(
                role="user",
                parts=[types.Part.from_text(text="Help me learn something useful today.")],
            )
        )

    return contents


def _latest_user_text(messages: list[dict[str, str]]) -> str:
    for message in reversed(messages):
        if message.get("role") == "user" and message.get("content"):
            return message["content"]

    return ""


def _fallback_tutor_reply(prompt: str) -> str:
    topic = prompt.strip() or "this topic"
    lower_prompt = topic.lower()

    if "quiz" in lower_prompt:
        return f"""Absolutely — here is a quick practice quiz on **{topic}**:

1. What is the main purpose of {topic}?
2. Which real-world example best explains {topic}?
3. What common mistake should learners avoid?

Try answering in your own words, then ask me to check them."""

    if "summar" in lower_prompt or "notes" in lower_prompt:
        return """Paste your notes here and I’ll turn them into:

- A short summary
- Key terms
- Exam-ready bullet points
- 3 quick revision questions"""

    if "homework" in lower_prompt or "solve" in lower_prompt:
        return f"""Let’s solve it step by step:

1. Identify what the question is asking.
2. List the facts or formulas you already know.
3. Work through one small step at a time.

Send the exact homework question and I’ll guide you without just dumping the answer."""

    return f"""Here’s a simple way to understand **{topic}**:

- Start with the core idea in one sentence.
- Connect it to a real-life example.
- Practice one small question immediately.

For **{topic}**, focus on the definition, why it matters, and where it is used. Want me to make this into a quiz or a study plan?"""


def _stream_text(text: str) -> Iterable[str]:
    for line in text.splitlines(keepends=True):
        yield line


def _generate_text(prompt: str, *, json_mode: bool = False) -> str:
    config_kwargs = {"system_instruction": SYSTEM_PROMPT}
    if json_mode:
        config_kwargs["response_mime_type"] = "application/json"

    response = _client().models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(**config_kwargs),
    )

    return (response.text or "").strip()


def ask_gemini(messages: list[dict[str, str]]):

    response = _client().models.generate_content(
        model=MODEL,
        contents=_to_contents(messages),
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT
        ),
    )

    return response.text.strip()

def ask_gemini_stream(messages: list[dict[str, str]]):

    response_stream = _client().models.generate_content_stream(
        model=MODEL,
        contents=_to_contents(messages),
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT
        ),
    )

    for chunk in response_stream:
        if getattr(chunk, "text", None):
            yield chunk.text

def _fallback_quiz(topic: str, difficulty: str, questions: int) -> list[dict[str, object]]:
    topic = topic.strip() or "General Knowledge"
    templates = [
        (
            f"What is the best first step when learning {topic}?",
            ["Memorize random facts", "Understand the core idea", "Skip examples", "Avoid practice"],
            "Understand the core idea",
        ),
        (
            f"Why are examples useful in {topic}?",
            ["They connect ideas to real situations", "They replace all theory", "They make practice unnecessary", "They remove definitions"],
            "They connect ideas to real situations",
        ),
        (
            f"What should you do after studying a concept in {topic}?",
            ["Close the book immediately", "Practice one question", "Ignore mistakes", "Change subjects instantly"],
            "Practice one question",
        ),
        (
            f"Which habit improves mastery of {topic}?",
            ["Regular revision", "Only reading once", "Skipping feedback", "Guessing every answer"],
            "Regular revision",
        ),
        (
            f"What does a {difficulty.lower()} question usually test?",
            ["A suitable level of understanding", "Only handwriting", "Internet speed", "Random guessing"],
            "A suitable level of understanding",
        ),
    ]

    quiz = []
    for index in range(max(1, int(questions))):
        question, options, answer = templates[index % len(templates)]
        quiz.append(
            {
                "question": question,
                "options": options,
                "answer": answer,
                "explanation": f"The best answer is '{answer}' because it reflects a useful learning habit for {topic}.",
            }
        )

    return quiz


def generate_quiz(topic: str, difficulty: str, questions: int) -> str:
    topic = topic.strip() or "General Knowledge"
    questions = int(questions)
    prompt = f"""
Generate {questions} multiple choice questions.

Topic: {topic}
Difficulty: {difficulty}

Return ONLY valid JSON in this exact shape:
[
  {{
    "question": "...",
    "options": ["...", "...", "...", "..."],
    "answer": "...",
    "explanation": "One short sentence explaining why the answer is correct."
  }}
]

The answer value must exactly match one option string.
The explanation must be student-friendly and concise.
"""

    try:
        return _generate_text(prompt, json_mode=True)
    except Exception:
        return json.dumps(_fallback_quiz(topic, difficulty, questions), indent=2)


def _extract_json_array(text: str) -> str:
    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:json)?", "", cleaned, flags=re.IGNORECASE).strip()
    cleaned = re.sub(r"```$", "", cleaned).strip()

    if cleaned.startswith("["):
        return cleaned

    match = re.search(r"\[[\s\S]*\]", cleaned)
    if match:
        return match.group(0)

    raise ValueError("AI response did not contain a JSON array.")


def _normalise_answer(answer: str, options: list[str]) -> str:
    answer = str(answer).strip()
    option_letters = {"A": 0, "B": 1, "C": 2, "D": 3}
    letter = answer[:1].upper()

    if letter in option_letters and option_letters[letter] < len(options):
        return options[option_letters[letter]]

    for option in options:
        if answer.lower() == option.lower():
            return option

    for option in options:
        if answer.lower() in option.lower() or option.lower() in answer.lower():
            return option

    return options[0]


def parse_quiz_response(text: str) -> list[dict[str, object]]:
    data = json.loads(_extract_json_array(text))
    if not isinstance(data, list):
        raise ValueError("Quiz JSON must be a list.")

    quiz = []
    for item in data:
        if not isinstance(item, dict):
            continue

        question = str(item.get("question", "")).strip()
        options = item.get("options", [])
        if not question or not isinstance(options, list):
            continue

        options = [str(option).strip() for option in options if str(option).strip()]
        if len(options) < 2:
            continue

        quiz.append(
            {
                "question": question,
                "options": options[:4],
                "answer": _normalise_answer(str(item.get("answer", "")), options[:4]),
                "explanation": str(item.get("explanation", "")).strip()
                or "Review the key concept and compare it with each option.",
            }
        )

    if not quiz:
        raise ValueError("Quiz JSON did not include valid questions.")

    return quiz


def generate_quiz_items(topic: str, difficulty: str, questions: int) -> list[dict[str, object]]:
    try:
        return parse_quiz_response(generate_quiz(topic, difficulty, questions))
    except Exception:
        return _fallback_quiz(topic, difficulty, questions)


def generate_syllabus(course_name: str, level: str, duration: str, audience: str, topics: str) -> str:
    course_name = course_name.strip() or "Personalized Learning Course"
    topics = topics.strip() or "core concepts, examples, practice, assessment"
    prompt = f"""
Create a clean Markdown syllabus for:

Course: {course_name}
Level: {level}
Duration: {duration}
Audience: {audience}
Topics: {topics}

Include weekly modules, learning outcomes, activities, quizzes, project work,
and certificate criteria. Keep it practical for an LMS.
"""

    try:
        return _generate_text(prompt)
    except Exception:
        return f"""# {course_name}

### Level
{level}

### Duration
{duration}

### Audience
{audience}

## Learning Outcomes
- Understand the foundations of {course_name}
- Apply key ideas through guided practice
- Complete quizzes and a final project

## Weekly Plan
### Week 1 — Foundations
- Introduction and key vocabulary
- Real-world examples
- Quick diagnostic quiz

### Week 2 — Core Skills
- Guided lessons on {topics}
- Practice worksheet
- Reflection activity

### Week 3 — Application
- Case studies
- Mini project
- Peer review

### Week 4 — Assessment
- Revision
- Final quiz
- Certificate checklist
"""


def generate_lesson(lesson: str, level: str) -> str:
    lesson = lesson.strip() or "Today’s Lesson"
    prompt = f"""
Create a tutor-friendly lesson outline for "{lesson}" at {level} level.
Include objectives, explanation, example, activity, quiz questions, and homework.
"""

    try:
        return _generate_text(prompt)
    except Exception:
        return f"""## {lesson}

### Objectives
- Understand the main idea
- Apply it to one example
- Check learning with practice

### Explanation
Start with the definition, then connect it to a familiar real-life situation.

### Classroom Activity
Ask learners to solve one guided example, then explain their reasoning.

### Quick Quiz
1. What is the main idea of {lesson}?
2. Where can you use it?
3. What mistake should you avoid?

### Homework
Write a short explanation of {lesson} and solve two practice questions.
"""


def generate_course_outline(topic: str, level: str) -> str:
    topic = topic.strip() or "New Course"
    prompt = f"""
Generate a concise LMS course outline for "{topic}" at {level} level.
Include 5 modules, lesson goals, quiz ideas, and a final assessment.
"""

    try:
        return _generate_text(prompt)
    except Exception:
        return f"""## {topic} Course Outline

1. Introduction to {topic}
2. Core Concepts
3. Worked Examples
4. Practice and Feedback
5. Final Project and Assessment

Each module includes a short lesson, one activity, one quiz, and a progress checkpoint.
"""
