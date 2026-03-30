from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file, session
from werkzeug.security import generate_password_hash
from models import db, User, Subject, Paper, PaperQuestion, Question
from routes.auth import admin_required
from utils.pdf_generator import generate_pdf
from utils.docx_generator import generate_docx

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    teachers = User.query.filter_by(role='teacher').all()
    subjects = Subject.query.all()
    papers = Paper.query.order_by(Paper.created_at.desc()).all()
    return render_template('admin/dashboard.html',
                           teachers=teachers, subjects=subjects, papers=papers)


@admin_bp.route('/create-teacher', methods=['GET', 'POST'])
@admin_required
def create_teacher():
    subjects = Subject.query.all()

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        full_name = request.form.get('full_name', '').strip()
        subject_ids = request.form.getlist('subjects')  # list of subject ids

        if User.query.filter_by(username=username).first():
            flash('Username already exists.')
            return render_template('admin/create_teacher.html', subjects=subjects)

        teacher = User(
            username=username,
            password_hash=generate_password_hash(password),
            full_name=full_name,
            role='teacher'
        )
        for sid in subject_ids:
            subject = Subject.query.get(int(sid))
            if subject:
                teacher.subjects.append(subject)

        db.session.add(teacher)
        db.session.commit()
        flash(f'Teacher {full_name} created successfully.')
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/create_teacher.html', subjects=subjects)


@admin_bp.route('/edit-teacher/<int:teacher_id>', methods=['GET', 'POST'])
@admin_required
def edit_teacher(teacher_id):
    teacher = User.query.get_or_404(teacher_id)
    subjects = Subject.query.all()

    if request.method == 'POST':
        teacher.full_name = request.form.get('full_name', '').strip()
        new_password = request.form.get('password', '')
        if new_password:
            teacher.password_hash = generate_password_hash(new_password)

        subject_ids = request.form.getlist('subjects')
        teacher.subjects = []
        for sid in subject_ids:
            subject = Subject.query.get(int(sid))
            if subject:
                teacher.subjects.append(subject)

        db.session.commit()
        flash('Teacher updated.')
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/create_teacher.html', teacher=teacher, subjects=subjects)


@admin_bp.route('/papers')
@admin_required
def view_papers():
    papers = Paper.query.order_by(Paper.created_at.desc()).all()
    return render_template('admin/view_papers.html', papers=papers)


@admin_bp.route('/download/<int:paper_id>')
@admin_required
def download_paper(paper_id):
    paper = Paper.query.get_or_404(paper_id)
    questions = (Question.query
                 .join(PaperQuestion)
                 .filter(PaperQuestion.paper_id == paper_id)
                 .order_by(PaperQuestion.order_num)
                 .all())

    fmt = request.args.get('fmt', 'pdf')

    if fmt == 'docx':
        buffer = generate_docx(paper, questions)
        return send_file(buffer,
                         as_attachment=True,
                         download_name=f"{paper.title}.docx",
                         mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    else:
        buffer = generate_pdf(paper, questions)
        return send_file(buffer,
                         as_attachment=True,
                         download_name=f"{paper.title}.pdf",
                         mimetype='application/pdf')