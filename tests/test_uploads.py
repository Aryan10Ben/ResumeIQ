from io import BytesIO

import pytest
from reportlab.pdfgen import canvas

from resumeiq.parser import InvalidResume, extract_text, validate_upload


def pdf_bytes(text="Python Flask React"):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.drawString(70, 700, text)
    pdf.save()
    return buffer.getvalue()


def test_real_pdf_roundtrip():
    data = pdf_bytes()
    suffix = validate_upload("cv.pdf", data)
    assert "Python" in extract_text(data, suffix)


def test_invalid_pdf_signature():
    with pytest.raises(InvalidResume, match="signature"):
        validate_upload("resume.pdf", b"this is not a PDF")


def test_rejects_oversized_and_empty_files():
    with pytest.raises(InvalidResume, match="empty"):
        validate_upload("empty.txt", b"")
    with pytest.raises(InvalidResume, match="large"):
        validate_upload("huge.txt", b"x" * 11, max_bytes=10)


def test_rejects_binary_text_and_invalid_extensions():
    with pytest.raises(InvalidResume, match="binary"):
        validate_upload("not-text.txt", b"\x00\x01\x02")
    with pytest.raises(InvalidResume, match=r"\.pdf or \.txt"):
        validate_upload("payload.exe", b"hello")


def test_supports_utf8_and_utf16_txt():
    assert extract_text("Résumé: Python".encode("utf-8"), ".txt").startswith("Résumé")
    assert "Python" in extract_text("Python".encode("utf-16"), ".txt")


def test_scanned_or_corrupt_pdf_error_is_safe():
    with pytest.raises(InvalidResume, match="could not be parsed"):
        extract_text(b"%PDF-not-a-real-document", ".pdf")
