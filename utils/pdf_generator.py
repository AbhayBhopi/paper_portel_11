from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
import io

def generate_pdf(paper, questions):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    def draw_page_header(c, y):
        # University Header Box
        c.setStrokeColor(colors.black)
        c.setLineWidth(1.5)
        c.rect(1.5*cm, y - 2.8*cm, width - 3*cm, 2.8*cm)

        # University name
        c.setFont("Helvetica-Bold", 11)
        c.drawCentredString(width/2, y - 0.8*cm, "DR. BABASAHEB AMBEDKAR TECHNOLOGICAL UNIVERSITY, LONERE")

        # Exam title
        c.setFont("Helvetica", 9)
        c.drawCentredString(width/2, y - 1.4*cm, "Regular/Supplementary Winter Examination - 2024")

        # Horizontal line
        c.line(1.5*cm, y - 1.7*cm, width - 1.5*cm, y - 1.7*cm)

        # Course and Semester row
        c.setFont("Helvetica-Bold", 9)
        c.drawString(1.8*cm, y - 2.1*cm, f"Course: {paper.subject.name} ({paper.subject.code})")
        c.drawString(width/2, y - 2.1*cm, f"Semester: ___________")

        # Horizontal line
        c.line(1.5*cm, y - 2.4*cm, width - 1.5*cm, y - 2.4*cm)

        # Date and Max Marks row
        c.drawString(1.8*cm, y - 2.75*cm, "Date: ___________")
        c.drawString(width/2, y - 2.75*cm, f"Max. Marks: {sum(q.marks for q in questions)}")

        return y - 3.2*cm

    def draw_student_info(c, y):
        # Student info box
        c.setLineWidth(1)
        c.rect(1.5*cm, y - 1.2*cm, width - 3*cm, 1.2*cm)
        c.line(width/2, y - 1.2*cm, width/2, y)

        c.setFont("Helvetica-Bold", 9)
        c.drawString(1.8*cm, y - 0.7*cm, "Student Name: _______________________________")
        c.drawString(width/2 + 0.3*cm, y - 0.7*cm, "Roll No.: _______________________________")

        return y - 1.6*cm

    def draw_instructions(c, y):
        instructions = [
            "1. All questions are compulsory.",
            "2. Question No. 1 and 2 are compulsory and carry 5 marks each.",
            "3. Attempt any 3 questions from Question No. 3 to 6, each carrying 10 marks.",
            "4. Draw neat diagrams wherever necessary.",
            "5. Assume suitable data if necessary.",
        ]
        c.setFont("Helvetica-Bold", 9)
        c.drawString(1.8*cm, y, "Instructions to Students:")
        y -= 0.45*cm
        c.setFont("Helvetica", 8.5)
        for inst in instructions:
            c.drawString(2*cm, y, inst)
            y -= 0.4*cm
        return y - 0.3*cm

    def draw_table_header(c, y):
        c.setLineWidth(1)
        # Table border
        col_widths = [1.2*cm, 11*cm, 2.5*cm, 2*cm]
        table_width = sum(col_widths)
        table_x = 1.5*cm
        row_h = 0.7*cm

        # Header row
        c.rect(table_x, y - row_h, table_width, row_h)
        # Column dividers
        x = table_x
        for w in col_widths[:-1]:
            x += w
            c.line(x, y - row_h, x, y)

        c.setFont("Helvetica-Bold", 9)
        c.drawCentredString(table_x + col_widths[0]/2, y - 0.5*cm, "Q. No.")
        c.drawCentredString(table_x + col_widths[0] + col_widths[1]/2, y - 0.5*cm, "Questions")
        c.drawCentredString(table_x + col_widths[0] + col_widths[1] + col_widths[2]/2, y - 0.5*cm, "Marks")
        c.drawCentredString(table_x + col_widths[0] + col_widths[1] + col_widths[2] + col_widths[3]/2, y - 0.5*cm, "CO")

        return y - row_h, col_widths, table_x

    def draw_question_row(c, y, q_num, text, marks, col_widths, table_x, is_sub=False):
        row_h = max(1*cm, 0.5*cm * (len(text)//80 + 1))
        c.rect(table_x, y - row_h, sum(col_widths), row_h)
        x = table_x
        for w in col_widths[:-1]:
            x += w
            c.line(x, y - row_h, x, y)

        c.setFont("Helvetica", 9)
        label = f"  {q_num}" if not is_sub else f"    {q_num}"
        c.drawString(table_x + 0.2*cm, y - 0.6*cm, label)

        # Word wrap question text
        max_w = col_widths[1] - 0.4*cm
        words = text.split()
        line = ""
        lines = []
        for word in words:
            test = line + word + " "
            if c.stringWidth(test, "Helvetica", 9) < max_w:
                line = test
            else:
                lines.append(line.strip())
                line = word + " "
        if line:
            lines.append(line.strip())

        text_y = y - 0.35*cm
        for ln in lines[:3]:
            c.drawString(table_x + col_widths[0] + 0.2*cm, text_y, ln)
            text_y -= 0.35*cm

        c.drawCentredString(table_x + col_widths[0] + col_widths[1] + col_widths[2]/2, y - 0.6*cm, str(marks))
        return y - row_h

    # ── Start drawing ──────────────────────────────────────────
    y = height - 1*cm
    y = draw_page_header(c, y)
    y = draw_student_info(c, y)
    y -= 0.3*cm
    y = draw_instructions(c, y)
    y -= 0.3*cm

    y, col_widths, table_x = draw_table_header(c, y)

    # Split questions into sections:
    # Q1 & Q2: compulsory (5 marks each), shown as-is
    # Q3–Q6: optional groups of 3 sub-questions (10 marks each group)

    compulsory = questions[:2]
    optional = questions[2:]

    # Draw Q1 and Q2
    for i, q in enumerate(compulsory, 1):
        if y < 3*cm:
            c.showPage()
            y = height - 1.5*cm
            y, col_widths, table_x = draw_table_header(c, y)
        y = draw_question_row(c, y, i, q.question_text, q.marks, col_widths, table_x)

    # Draw Q3–Q6 as groups of 3
    group_marks = 10
    for group_i, group_start in enumerate(range(0, len(optional), 3), 3):
        group = optional[group_start:group_start+3]
        if not group:
            break

        # Group header row
        if y < 4*cm:
            c.showPage()
            y = height - 1.5*cm
            y, col_widths, table_x = draw_table_header(c, y)

        row_h = 0.7*cm
        c.rect(table_x, y - row_h, sum(col_widths), row_h)
        x = table_x
        for w in col_widths[:-1]:
            x += w
            c.line(x, y - row_h, x, y)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(table_x + 0.2*cm, y - 0.5*cm, f"Q.{group_i}")
        c.drawString(table_x + col_widths[0] + 0.2*cm, y - 0.5*cm, "Attempt any TWO of the following:")
        c.drawCentredString(table_x + col_widths[0] + col_widths[1] + col_widths[2]/2, y - 0.5*cm, str(group_marks))
        y -= row_h

        sub_labels = ['a)', 'b)', 'c)']
        for j, q in enumerate(group):
            if y < 3*cm:
                c.showPage()
                y = height - 1.5*cm
                y, col_widths, table_x = draw_table_header(c, y)
            y = draw_question_row(c, y, sub_labels[j], q.question_text, q.marks, col_widths, table_x, is_sub=True)

    # Footer
    c.setFont("Helvetica", 8)
    c.drawCentredString(width/2, 1*cm, "Page 1")

    c.save()
    buffer.seek(0)
    return buffer
