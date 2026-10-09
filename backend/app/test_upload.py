
from io import BytesIO
from unittest.mock import patch

from fastapi.testclient import TestClient
from reportlab.pdfgen import canvas

from backend.app.main import app

client = TestClient(app)


def create_test_pdf():
    pdf_buffer = BytesIO()

    pdf = canvas.Canvas(pdf_buffer)
    pdf.drawString(100, 750, "This is a test PDF document.")
    pdf.save()

    pdf_buffer.seek(0)
    return pdf_buffer


def test_upload_pdf():
    fake_pdf = create_test_pdf()

    with patch(
        "backend.app.main.split_document",
        return_value=5
    ):
        response = client.post(
            "/upload",
            files={
                "file": (
                    "test.pdf",
                    fake_pdf,
                    "application/pdf"
                )
            }
        )

    assert response.status_code == 200