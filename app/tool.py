from crewai_tools import CodeInterpreterTool, PDFSearchTool

code_interpreter = CodeInterpreterTool(unsafe_mode=True)


def get_pdf_search_tool(file_name: str):
    config = {
        "llm": {
            "provider": "ollama",
            "config": {
                "model": "llama3",
            },
        },
        "embedder": {
            "provider": "ollama",
            "config": {
                "model": "all-minilm",
            },
        },
    }
    return PDFSearchTool(pdf=file_name, config=config)
