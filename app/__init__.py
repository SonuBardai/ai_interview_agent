import os
from langtrace_python_sdk import langtrace
from dotenv import load_dotenv

# load .env file
load_dotenv()

# Initialize langtrace
langtrace_api_key = os.getenv("LANGTRACE_API_KEY")
if not langtrace_api_key:
    raise ValueError("LANGTRACE_API_KEY not found in environment variables")
langtrace.init(api_key=langtrace_api_key)
