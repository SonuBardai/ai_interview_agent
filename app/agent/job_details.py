from crewai_tools import PDFSearchTool
from app.llm import llm
from crewai import Agent


def get_job_details_extractor(rag_tool: PDFSearchTool):
    return Agent(
        role="Job details extractor",
        goal="Extract job title, job description, and skills from the document in order to perform an interview for job candidates",
        backstory="You are an expert job document analyzer. "
        "You're working on extracting the job title, job description, and skills from a document that will be used to set up an interview for job candidates.",
        allow_delegation=False,
        llm=llm,
        verbose=True,
        tools=[rag_tool],
    )


def get_job_details_evaluator(rag_tool: PDFSearchTool):
    return Agent(
        role="Job details evaluator",
        goal="Evaluate the extracted job details in order to perform an interview for job candidates",
        backstory="You are an expert at analyzing job role analysis against job documents and refining the details to match the actual job requirements. "
        "You're working on evaluating the extracted job details in order to perform an interview for job candidates.",
        allow_delegation=False,
        llm=llm,
        verbose=True,
        tools=[rag_tool],
    )
