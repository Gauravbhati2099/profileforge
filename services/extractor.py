from pathlib import Path

from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="llama3.2:3b",
    temperature=0,
    format="json"
)

def extract_profile(resume_text: str):

    prompt = Path(
        "prompts/extraction.txt"
    ).read_text(
        encoding="utf-8"
    )

    response = llm.invoke(
        f"{prompt}\n\nResume:\n{resume_text}"
    )

    return response.content