from crewai import Agent
from app.llm import llm

from app.tool import code_interpreter


def get_answer_evaluator():
    return Agent(
        role="Technical Interview Answer Evaluator",
        goal="Evaluate the user's answer based on the question type and test cases or multiple choice options.",
        backstory=(
            "You are an expert in evaluating technical interview answers. "
            "You receive a question (either coding or multiple choice) for the job of {job_title}, and the user's answer. "
            "If it's a coding question, you use the provided test cases to evaluate the correctness. "
            "If it's a multiple choice question, you check if the selected answer is correct."
        ),
        allow_delegation=False,
        llm=llm,
        verbose=True,
        tools=[code_interpreter],
    )
