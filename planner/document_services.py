"""Local OCR/extraction with safe failure; move to a worker for production scale."""
from pathlib import Path
from django.conf import settings
from .models import AcademicDocument, DocumentAnalysis
from .ai_services import complete


def queue_extraction(document: AcademicDocument):
    suffix = Path(document.file.name).suffix.lower()
    try:
        if suffix == ".pdf":
            from pypdf import PdfReader
            text = "\n".join(page.extract_text() or "" for page in PdfReader(document.file).pages)
        else:
            from PIL import Image
            import pytesseract
            document.file.open("rb")
            text = pytesseract.image_to_string(Image.open(document.file))
        document.extracted_text = text[:50000]
        document.extraction_status = "complete" if text.strip() else "needs_review"
    except Exception:
        document.extraction_status = "pending"
    document.save(update_fields=("extracted_text", "extraction_status"))
    if document.extracted_text and document.document_type in {"syllabus", "question_paper"}:
        build_analysis(document)


def build_analysis(document: AcademicDocument):
    lines = [line.strip(" -•\t") for line in document.extracted_text.splitlines()]
    topics = list(dict.fromkeys(line for line in lines if 4 < len(line) < 120))[:30]
    fallback = "Extracted topics are ready for review and can be used by the study planner."
    summary = complete(f"Summarize this student's {document.get_document_type_display()} in two short sentences, emphasizing study priorities:\n{document.extracted_text[:6000]}", fallback)
    DocumentAnalysis.objects.update_or_create(document=document, defaults={"topics": topics, "summary": summary, "priority_score": min(100, len(topics) * 3)})
