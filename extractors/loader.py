import os

from extractors.pdf_extractor import extract_pdf
from extractors.docx_extractor import extract_docx
from extractors.text_extractor import extract_txt


def detect_type(file_path: str):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        return "pdf"

    if ext == ".docx":
        return "docx"

    if ext == ".txt":
        return "txt"

    return None


def load_file(file_path: str) -> str:
    file_type = detect_type(file_path)

    print(f"[loader] {file_path} -> {file_type}")

    try:
        if file_type == "pdf":
            return extract_pdf(file_path)

        elif file_type == "docx":
            return extract_docx(file_path)

        elif file_type == "txt":
            return extract_txt(file_path)

        else:
            print(f"[SKIP] unsupported: {file_path}")
            return None

    except Exception as e:
        print(f"[ERROR] {file_path}: {e}")
        return None