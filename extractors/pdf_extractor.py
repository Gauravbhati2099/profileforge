import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io


pytesseract.pytesseract.tesseract_cmd = (
    r"D:\New folder\tesseract.exe"
)

MIN_TEXT_THRESHOLD = 100


def extract_native_text(file_path: str) -> str:
    """
    Extract text from PDFs that already contain a text layer.
    """

    text_parts = []

    with fitz.open(file_path) as doc:
        for page in doc:
            page_text = page.get_text("text")

            if page_text:
                text_parts.append(page_text)

    return "\n".join(text_parts)


def extract_ocr_text(file_path: str) -> str:
    """
    OCR fallback for scanned/image PDFs.
    """

    text_parts = []

    with fitz.open(file_path) as doc:

        total_pages = len(doc)

        for page_num, page in enumerate(doc, start=1):

            print(
                f"[OCR] page {page_num}/{total_pages}"
            )

            pix = page.get_pixmap(
                matrix=fitz.Matrix(2, 2),
                alpha=False
            )

            img_bytes = pix.tobytes("png")

            image = Image.open(
                io.BytesIO(img_bytes)
            )

            page_text = pytesseract.image_to_string(
                image
            )

            if page_text:
                text_parts.append(page_text)

    return "\n".join(text_parts)


def clean_text(text: str) -> str:
    """
    Basic cleanup before chunking.
    """

    lines = []

    for line in text.splitlines():
        line = line.strip()

        if line:
            lines.append(line)

    return "\n".join(lines)


def extract_pdf(file_path: str) -> str:
    """
    Main PDF extraction entrypoint.
    """

    print(f"[PDF] processing: {file_path}")

    try:
        text = extract_native_text(file_path)

        text = clean_text(text)

        if len(text) >= MIN_TEXT_THRESHOLD:
            print(
                f"[PDF] native extraction successful ({len(text)} chars)"
            )
            return text

        print(
            "[PDF] insufficient native text detected, switching to OCR"
        )

        text = extract_ocr_text(file_path)

        text = clean_text(text)

        print(
            f"[PDF] OCR extraction successful ({len(text)} chars)"
        )

        return text

    except Exception as e:

        print(f"[PDF ERROR] {e}")

        try:
            print("[PDF] attempting OCR fallback")

            text = extract_ocr_text(file_path)

            text = clean_text(text)

            return text

        except Exception as ocr_error:

            print(
                f"[OCR ERROR] {ocr_error}"
            )

            return ""