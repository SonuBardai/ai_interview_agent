from .crew import (
    get_question_generation_crew,
    get_answer_evaluation_crew,
    get_job_details_from_pdf_crew,
)
from .tool import get_pdf_search_tool


def extract_job_details(job_document: str):
    rag_tool = get_pdf_search_tool(file_name=job_document)
    job_details_extractor_crew = get_job_details_from_pdf_crew(rag_tool=rag_tool)
    result = job_details_extractor_crew.kickoff()
    return result.json_dict


def get_question(job: dict, previous_scores: list[int]):
    if not job:
        raise ValueError("Job details are required")
    crew = get_question_generation_crew()
    result = crew.kickoff(inputs={**job, "previous_scores": str(previous_scores)})
    return result.json_dict


def evaluate_answer(answer: str, question: str, test_cases: list[dict], question_type: str, job: dict):
    crew = get_answer_evaluation_crew()
    result = crew.kickoff(
        inputs={
            "answer": answer,
            "question": question,
            "question_type": question_type,
            "test_cases": test_cases,
            **job,
        }
    )
    return result.json_dict
