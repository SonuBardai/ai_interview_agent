from crewai import Agent
from app.llm import llm


def get_question_generator():
    return Agent(
        role="Technical Interview Question Setter",
        goal=(
            "Create one thoughtful, relevant interview question for the job of {job_title}, "
            "based on the job description provided. The question must be either a coding question or a multiple choice question."
        ),
        backstory=(
            "You are an expert in technical interviews and assessment design. "
            "You're preparing an interview for the role of {job_title}. "
            "Using the job description below:\n\n{job_description}\n\n"
            "Your task is to extract the key responsibilities, skills, and knowledge areas, "
            "and generate one technical interview question based on them.\n\n"
            "You must decide whether the question will be:\n"
            "1. A **coding question** - include a `question`, `difficulty` (1-10), and a list of static `test_cases` (no code expressions).\n"
            "2. A **multiple choice question** - include a `question`, `difficulty` (1-10), and a list of 4 `options`, one marked `is_correct = true`.\n\n"
            "**Never mix both types.** Only provide one type of question in each response, and clearly set `question_type` to either 'code' or 'multiple_choice'."
        ),
        allow_delegation=False,
        llm=llm,
        verbose=True,
    )


def get_question_validator():
    return Agent(
        role="Question Validator",
        goal="Validate the generated interview questions and test cases",
        backstory="You are a senior technical hiring specialist with an expertise in validating technical interview questions and test cases. "
        "You receive a set of questions and test cases from the Interview Researcher for the job of {job_title}. "
        "Your job is to validate the questions and test cases and provide feedback on their relevance and accuracy. "
        "You also provide areas for improvement based on the test cases. ",
        allow_delegation=False,
        llm=llm,
        verbose=True,
    )
