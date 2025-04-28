from crewai import Task, Agent
from pydantic import BaseModel
from . import AnyType
from typing import List, Literal


class TestCase(BaseModel):
    input: AnyType
    expected_output: AnyType


class QuestionGenerationOutput(BaseModel):
    question: str
    difficulty: int
    test_cases: list[TestCase]


class MCQOption(BaseModel):
    option: str
    is_correct: bool


class FinalQuestionOutput(BaseModel):
    question: str
    difficulty: int
    question_type: Literal["code", "multiple_choice"]
    test_cases: List[TestCase] = []
    options: List[MCQOption] = []


def get_question_generation_task(question_generator: Agent):
    return Task(
        agent=question_generator,
        description=(
            "Generate ONE interview question based on the job description `{job_description}` and `{skills}`. "
            "Based on the job type the question should be either:\n"
            "- A coding question with test cases (question_type = 'code')\n"
            "- A multiple-choice question with 4 options (question_type = 'multiple_choice')\n\n"
            "For coding questions:\n"
            "- Based on data structures or algorithms\n"
            "- Include a `test_cases` field with static input and expected output.\n"
            "- Do NOT include options.\n\n"
            "For multiple-choice questions:\n"
            "- Include an `options` list with 4 options. One must be marked as correct (is_correct = true).\n"
            "- Do NOT include test cases.\n\n"
            "All questions should include a `difficulty` from 1-10.\n"
            "Start easy and adapt difficulty based on previous_scores: `{previous_scores}`"
        ),
        expected_output="A single interview question with test cases or multiple choice options",
        output_json=QuestionGenerationOutput,
    )


def get_question_validation_task(question_validator: Agent):
    return Task(
        agent=question_validator,
        description="Validate the generated interview questions and test cases."
        "Provide feedback on the relevance and accuracy of the questions and test cases."
        "Provide areas for improvement based on the test cases."
        "Provide the question_type to help the candidate on how to answer the question. Is it a 'code' or 'system_design' or 'general' type?. ",
        expected_output="Final set of interview questions and test cases ready to be presented to the interviewee",
        output_json=FinalQuestionOutput,
    )
