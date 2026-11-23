"""Safe, in-memory extraction of resume text. Files are never retained."""
from io import BytesIO
from pathlib import Path

ALLOWED_EXTENSIONS = {".pdf", ".txt"}
MAX_PDF_PAGES = 15
MAX_EXTRACTED_CHARS = 100_000


class InvalidResume(ValueError):
    """A user-supplied resume cannot be safely processed."""


def validate_upload(filename, data, *, max_bytes=3 * 1024 * 1024):
    suffix = Path(filename or "").suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise InvalidResume("Use a .pdf or .txt file.")
    if not data:
        raise InvalidResume("The file is empty.")
    if len(data) > max_bytes:
        raise InvalidResume("The file is too large (3 MB maximum per resume).")
    if suffix == ".pdf" and not data.startswith(b"%PDF-"):
        raise InvalidResume("The PDF file signature is invalid.")
    if suffix == ".txt" and b"\x00" in data and not data.startswith((b"\xff\xfe", b"\xfe\xff")):
        raise InvalidResume("The text file appears to contain binary data.")
    return suffix


def extract_text(data, suffix):
    if suffix == ".txt":
        if data.startswith((b"\xff\xfe", b"\xfe\xff")):
            text = data.decode("utf-16")
        else:
            try:
                text = data.decode("utf-8-sig")
            except UnicodeDecodeError:
                text = data.decode("latin-1")
    elif suffix == ".pdf":
        import pdfplumber

        pages = []
        try:
            with pdfplumber.open(BytesIO(data)) as pdf:
                if len(pdf.pages) > MAX_PDF_PAGES:
                    raise InvalidResume("PDF exceeds the 15-page limit.")
                for page in pdf.pages:
                    pages.append(page.extract_text() or "")
                    if sum(map(len, pages)) > MAX_EXTRACTED_CHARS:
                        raise InvalidResume("Extracted text exceeds the safety limit.")
        except InvalidResume:
            raise
        except Exception as exc:
            raise InvalidResume("The PDF could not be parsed.") from exc
        text = "\n".join(pages)
    else:
        raise InvalidResume("Unsupported file format.")

    if len(text) > MAX_EXTRACTED_CHARS:
        raise InvalidResume("Extracted text exceeds the safety limit.")
    if not text.strip():
        raise InvalidResume("No selectable text found. Scanned PDFs are not supported.")
    return text
