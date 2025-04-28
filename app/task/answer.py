from crewai import Task, Agent
from pydantic import BaseModel
from typing import Optional, List
from . import AnyType


class AnsweredTestCase(BaseModel):
    input: AnyType
    expected_output: AnyType
    actual_output: AnyType


class AnswerEvaluationOutput(BaseModel):
    score: int
    feedback: str
    passed_test_cases: Optional[List[AnsweredTestCase]] = []
    failed_test_cases: Optional[List[AnsweredTestCase]] = []
    correct_option: Optional[str] = None
    is_correct: Optional[bool] = None


def get_answer_evaluation_task(answer_evaluator: Agent):
    return Task(
        agent=answer_evaluator,
        description=(
            "Evaluate the user's answer `{answer}` for the given interview question `{question}`. "
            "The question_type is `{question_type}`.\n\n"
            "**If question_type is 'code':**\n"
            "- Use test cases `{test_cases}` to validate the code.\n"
            "- Only use the code interpreter if the programming language is 'python'.\n"
            "- Provide score out of 10, feedback, and list of passed and failed test cases.\n\n"
            "**If question_type is 'multiple_choice':**\n"
            "- The answer will be the user's selected option.\n"
            "- Check it against the correct option.\n"
            "- Provide a score out of 10 (10 if correct, 0 if wrong), indicate the correct option, and whether the answer was correct.\n\n"
            "Do NOT attempt to use the code interpreter for multiple choice questions."
        ),
        expected_output="An evaluation of the user's answer",
        output_json=AnswerEvaluationOutput,
    )
