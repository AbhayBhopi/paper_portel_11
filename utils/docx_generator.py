from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import io

def generate_docx(paper, questions):
    doc = Document()

    # Title
    title = doc.add_heading(paper.title, 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Subject info
    doc.add_paragraph(f"Subject: {paper.subject.name} ({paper.subject.code})")
    doc.add_paragraph(f"Teacher: {paper.teacher.full_name}")
    doc.add_paragraph('')

    # Questions
    for i, q in enumerate(questions, 1):
        doc.add_paragraph(f"Q{i}. {q.question_text}  [{q.marks} mark(s)]")

    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer
