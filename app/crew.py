from crewai import Crew
from .task.question import (
    get_question_generation_task,
    get_question_validation_task,
)
from .task.answer import (
    get_answer_evaluation_task,
)
from .task.job_details import (
    get_job_details_extraction_task,
)
from .agent.question import get_question_generator, get_question_validator
from .agent.answer import get_answer_evaluator
from .agent.job_details import get_job_details_extractor
from crewai_tools import PDFSearchTool


def get_job_details_from_pdf_crew(rag_tool: PDFSearchTool):
    job_details_extractor = get_job_details_extractor(rag_tool=rag_tool)
    # job_details_evaluator = get_job_details_evaluator(rag_tool=rag_tool)

    job_details_extraction_task = get_job_details_extraction_task(job_details_extractor)
    # job_details_evaluation_task = get_job_details_evaluation_task(job_details_evaluator)

    agents = [
        job_details_extractor,
        # job_details_evaluator
    ]
    tasks = [
        job_details_extraction_task,
        # job_details_evaluation_task
    ]

    crew = Crew(
        agents=agents,
        tasks=tasks,
        verbose=True,
    )

    return crew


def get_question_generation_crew():
    # generate the question
    question_generator = get_question_generator()
    question_generation_task = get_question_generation_task(question_generator)

    # validate the question
    question_validator = get_question_validator()
    question_validation_task = get_question_validation_task(question_validator)

    crew = Crew(
        agents=[question_generator, question_validator],
        tasks=[question_generation_task, question_validation_task],
        verbose=True,
    )

    return crew


def get_answer_evaluation_crew():
    answer_evaluator = get_answer_evaluator()

    answer_evaluation_task = get_answer_evaluation_task(answer_evaluator)

    crew = Crew(
        agents=[answer_evaluator],
        tasks=[answer_evaluation_task],
        verbose=True,
    )
    return crew
