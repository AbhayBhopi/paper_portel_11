import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
import io

def generate_pdf(paper, questions):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=20, leftMargin=20, topMargin=20, bottomMargin=20)
    elements = []
    
    styles = getSampleStyleSheet()
    centered = ParagraphStyle(name='Centered', parent=styles['Normal'], alignment=TA_CENTER)
    bold_centered = ParagraphStyle(name='BoldCentered', parent=styles['Normal'], alignment=TA_CENTER, fontName='Helvetica-Bold')
    italic_centered = ParagraphStyle(name='ItalicCentered', parent=styles['Normal'], alignment=TA_CENTER, fontName='Helvetica-Oblique', fontSize=9)
    
    exam_title = paper.header_title or ("MIDSEM EXAM QP" if paper.exam_type == 'class_test' else "UNIVERSITY EXAM QP")
    
    # Check for logos existences
    logo1_path = os.path.join('static', 'logo1.png')
    logo1 = Image(logo1_path, width=50, height=50) if os.path.exists(logo1_path) else ''
    
    logo2_path = os.path.join('static', 'logo2.jpg')
    logo2 = Image(logo2_path, width=50, height=50) if os.path.exists(logo2_path) else ''

    if paper.exam_type == 'university':
        header_content = [
            Paragraph("<b>DR. BABASAHEB AMBEDKAR TECHNOLOGICAL UNIVERSITY, LONERE</b>", bold_centered),
            Spacer(1, 5),
            Paragraph(f"<b>{paper.header_title or 'Supplementary Summer Examination - 2024'}</b>", bold_centered)
        ]
        header_table = Table([[header_content]], colWidths=[555])
        header_table.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BOX', (0,0), (-1,-1), 1.5, colors.black),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('TOPPADDING', (0,0), (-1,-1), 8)
        ]))
        elements.append(header_table)

        branch_text = paper.branch or "Artificial Intelligence and Data Science Engineering And Allied"
        meta_data = [
            [f"Course: B. Tech.", Paragraph(f"<b>Branch :</b> {branch_text}", styles['Normal']), f"Semester : {paper.semester or 'V'}"],
        ]
        meta_table1 = Table(meta_data, colWidths=[120, 335, 100])
        meta_table1.setStyle(TableStyle([
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 10),
            ('ALIGN', (1,0), (1,-1), 'CENTER'),
            ('ALIGN', (2,0), (2,-1), 'RIGHT'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOX', (0,0), (-1,-1), 1.5, colors.black),
        ]))
        elements.append(meta_table1)
        
        meta_data2 = [[f"Subject Code & Name: {paper.subject.code}  {paper.subject.name}"]]
        t2 = Table(meta_data2, colWidths=[555])
        t2.setStyle(TableStyle([
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 10),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOX', (0,0), (-1,-1), 1.5, colors.black)
        ]))
        elements.append(t2)
        
        meta_data3 = [
            [f"Max Marks: 60", f"Date: {paper.exam_date or ''}", f"Duration: 3 Hr."]
        ]
        t3 = Table(meta_data3, colWidths=[185, 185, 185])
        t3.setStyle(TableStyle([
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 10),
            ('ALIGN', (1,0), (1,0), 'CENTER'),
            ('ALIGN', (2,0), (2,0), 'RIGHT'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOX', (0,0), (-1,-1), 1.5, colors.black)
        ]))
        elements.append(t3)

        inst_content = [
            Paragraph("<i><b>Instructions to the Students:</b></i>", styles['Normal']),
            Paragraph("<i>1. All the questions are compulsory.</i>", styles['Normal']),
            Paragraph("<i>2. The level of question/expected answer as per OBE or the Course Outcome (CO) on which the question is based is mentioned in ( ) in front of the question.</i>", styles['Normal']),
            Paragraph("<i>3. Use of non-programmable scientific calculators is allowed.</i>", styles['Normal']),
            Paragraph("<i>4. Assume suitable data wherever necessary and mention it clearly.</i>", styles['Normal'])
        ]
        inst_table = Table([[inst_content]], colWidths=[555])
        inst_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1.5, colors.black),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('TOPPADDING', (0,0), (-1,-1), 5)
        ]))
        elements.append(inst_table)

    else:
        # Top Header section (with box border)
        header_content = [
            Paragraph("SHREEYASH PRATISHTHAN'S", centered),
            Paragraph("<font color='crimson'><b>SHREEYASH COLLEGE OF ENGINEERING & TECHNOLOGY, CHH.SAMBHAJINAGAR</b></font>", bold_centered),
            Paragraph("Satara Parisar, Beed By-Pass Road, Chh.Sambhajinagar -431010 (M.S.)", centered),
            Paragraph("<b>NAAC Accredited, ISO Certified Institute</b>", bold_centered),
            Paragraph(f"<b><u>{exam_title}</u></b>", bold_centered)
        ]
        
        # We use a 3-column table for the header so we can put logos left and right
        header_table = Table([[logo1, header_content, logo2]], colWidths=[60, 435, 60])
        header_table.setStyle(TableStyle([
            ('ALIGN', (0,0), (0,0), 'CENTER'),
            ('VALIGN', (0,0), (0,0), 'MIDDLE'),
            ('ALIGN', (2,0), (2,0), 'CENTER'),
            ('VALIGN', (2,0), (2,0), 'MIDDLE'),
            ('VALIGN', (1,0), (1,0), 'TOP'),
            ('BOX', (0,0), (-1,-1), 1.5, colors.black),
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
            ('TOPPADDING', (0,0), (-1,-1), 10)
        ]))
        elements.append(header_table)

        # Meta Info (with side and bottom borders)
        meta_data = [
            [f"Course: Computer Science & Engineering (DS)", f"Sem: {paper.semester or ''}"],
            [f"Subject Name: {paper.subject.name}", f"Subject Code: {paper.subject.code}"],
            [f"Max Marks: {60 if paper.exam_type == 'university' else 20}", f"Duration: {'3 Hr.' if paper.exam_type == 'university' else '1 Hr.'}"],
            [f"Date: {paper.exam_date or ''}", ""]
        ]
        meta_table = Table(meta_data, colWidths=[355, 200])
        meta_table.setStyle(TableStyle([
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 10),
            ('ALIGN', (1,0), (1,-1), 'RIGHT'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOX', (0,0), (-1,-1), 1.5, colors.black),
        ]))
        elements.append(meta_table)

        # Instructions (with side and bottom borders)
        inst_content = [
            Paragraph("<b>Instructions to the Students:</b>", styles['Normal']),
            Paragraph("[1] Use of non-programmable calculator is allowed", styles['Normal']),
            Paragraph("[2] Draw the diagram wherever necessary", styles['Normal']),
            Paragraph("[3] Assume suitable data wherever necessary and mention it clearly", styles['Normal'])
        ]
        inst_table = Table([[inst_content]], colWidths=[555])
        inst_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1.5, colors.black),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('TOPPADDING', (0,0), (-1,-1), 5)
        ]))
        elements.append(inst_table)
    
    # Questions Table
    q_data = [['Q. No.', 'Question', 'Level', 'CO', 'Mark']]
    if paper.exam_type == 'university':
        q_data.append(['Q.1', 'Attempt following Questions', '', '', '12 X 1'])
        for i in range(12):
            if i >= len(questions): break
            q = questions[i]
            q_text = q.question_text
            if q.q_type == 'mcq':
                q_text += f"<br/>(A) {q.opt_a or ''}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(B) {q.opt_b or ''}<br/>(C) {q.opt_c or ''}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(D) {q.opt_d or ''}"
            q_data.append([str(i+1), Paragraph(q_text, styles['Normal']), 'L1', 'CO1', ''])

        if len(questions) > 12:
            q_data.append(['Q.2', 'Solve Any One of the following', '', '', '1 X 6'])
            labels = ['(A)', '(B)', '(C)']
            for i in range(2):
                idx = 12 + i
                if idx >= len(questions): break
                q_data.append([labels[i], Paragraph(questions[idx].question_text, styles['Normal']), 'L2', 'CO2', ''])

        if len(questions) > 14:
            q_data.append(['Q.3', 'Solve Any One of the following', '', '', '1 X 6'])
            for i in range(2):
                idx = 14 + i
                if idx >= len(questions): break
                q_data.append([labels[i], Paragraph(questions[idx].question_text, styles['Normal']), 'L2', 'CO2', ''])

        if len(questions) > 16:
            q_data.append(['Q.4', 'Solve Any Two of the following', '', '', '2 X 6'])
            for i in range(3):
                idx = 16 + i
                if idx >= len(questions): break
                q_data.append([labels[i], Paragraph(questions[idx].question_text, styles['Normal']), 'L2', 'CO3', ''])

        if len(questions) > 19:
            q_data.append(['Q.5', 'Solve Any Two of the following', '', '', '2 X 6'])
            for i in range(3):
                idx = 19 + i
                if idx >= len(questions): break
                q_data.append([labels[i], Paragraph(questions[idx].question_text, styles['Normal']), 'L3', 'CO4', ''])

        if len(questions) > 22:
            q_data.append(['Q.6', 'Solve Any Two of the following', '', '', '2 X 6'])
            for i in range(3):
                idx = 22 + i
                if idx >= len(questions): break
                q_data.append([labels[i], Paragraph(questions[idx].question_text, styles['Normal']), 'L3', 'CO4', ''])
    else:
        q_data.append(['Q.1', 'Attempt following Questions', '', '', '1 X 5'])
        
        for i in range(5):
            if i >= len(questions): break
            q = questions[i]
            q_text = q.question_text
            if q.q_type == 'mcq':
                q_text += f"<br/>(A) {q.opt_a or ''}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(B) {q.opt_b or ''}<br/>(C) {q.opt_c or ''}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(D) {q.opt_d or ''}"
            q_data.append([str(i+1), Paragraph(q_text, styles['Normal']), 'L1' if i < 4 else 'L2', 'CO1', ''])
            
        if len(questions) > 5:
            q_data.append(['Q.2', 'Solve Any Two of the following', '', '', '2 X 5'])
            labels = ['(A)', '(B)', '(C)']
            levels = ['L1', 'L2', 'L2']
            cos = ['CO1', 'CO2', 'CO2']
            for i in range(3):
                idx = 5 + i
                if idx >= len(questions): break
                q_data.append([labels[i], Paragraph(questions[idx].question_text, styles['Normal']), levels[i], cos[i], ''])
                
        if len(questions) > 8:
            q_data.append(['Q.3', 'Solve Any One of the following', '', '', '1 X 5'])
            labels = ['(A)', '(B)']
            for i in range(2):
                idx = 8 + i
                if idx >= len(questions): break
                q_data.append([labels[i], Paragraph(questions[idx].question_text, styles['Normal']), 'L2', 'CO2', ''])

    t = Table(q_data, colWidths=[40, 385, 40, 40, 50], repeatRows=1)
    
    table_styles = [
        ('BOX', (0,0), (-1,-1), 1.5, colors.black),
        ('INNERGRID', (0,0), (-1,-1), 1, colors.black),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('ALIGN', (1,0), (1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
    ]
    
    for row_idx, row in enumerate(q_data):
        if row[0] in ['Q.1', 'Q.2', 'Q.3', 'Q.4', 'Q.5', 'Q.6']:
            table_styles.append(('FONTNAME', (0,row_idx), (-1,row_idx), 'Helvetica-Bold'))
            
    t.setStyle(TableStyle(table_styles))
    elements.append(t)
    
    doc.build(elements)
    buffer.seek(0)
    return buffer
