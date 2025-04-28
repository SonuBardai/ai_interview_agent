from crewai import Agent, Task
from pydantic import BaseModel


class JobDetails(BaseModel):
    job_title: str
    job_description: str
    skills: list[str]


def get_job_details_extraction_task(agent: Agent):
    return Task(
        agent=agent,
        description="""Extract job title, job description, and skills from the document in order to perform an interview for job candidates
        **Return the skills as a flat list of lowercase keywords or technology names only** 
        (e.g., ['python', 'django', 'flask', 'git', 'postgresql']). 
        Do not include full sentences or soft skills. Do not include years of experience or preference notes. 
        Only extract concrete technologies, programming languages, tools, and frameworks.
        """,
        expected_output="Relevant job details extracted in order to perform an interview",
        output_json=JobDetails,
    )


def get_job_details_evaluation_task(agent: Agent):
    return Task(
        agent=agent,
        description="Evaluate the extracted job details in order to perform an interview for job candidates",
        expected_output="Final set of job details evaluated against the provided document",
        output_json=JobDetails,
    )
