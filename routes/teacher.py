from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.utils import secure_filename
from models import db, User, Subject, Question, Paper, PaperQuestion, UploadedFile
from routes.auth import teacher_required
from utils.file_handler import allowed_file
import os
from config import Config

teacher_bp = Blueprint('teacher', __name__)


# ---------------- DASHBOARD ----------------
@teacher_bp.route('/dashboard')
@teacher_required
def dashboard():
    user = User.query.get(session['user_id'])
    papers = Paper.query.filter_by(teacher_id=user.id).order_by(Paper.created_at.desc()).all()
    return render_template('teacher/dashboard.html', user=user, papers=papers, subjects=user.subjects)


# ---------------- QUESTION BANK ----------------
@teacher_bp.route('/questions')
@teacher_required
def question_bank():
    user = User.query.get(session['user_id'])
    subject_ids = [s.id for s in user.subjects]
    questions = Question.query.filter(Question.subject_id.in_(subject_ids)).all()
    subjects = user.subjects
    return render_template('teacher/question_bank.html', questions=questions, subjects=subjects)


@teacher_bp.route('/questions/add', methods=['POST'])
@teacher_required
def add_question():
    question_text = request.form.get('question_text', '').strip()
    marks = int(request.form.get('marks', 1))
    q_type = request.form.get('q_type', 'short')
    subject_id = int(request.form.get('subject_id'))

    if not question_text:
        flash('Question text cannot be empty.')
        return redirect(url_for('teacher.question_bank'))

    q = Question(question_text=question_text, marks=marks, q_type=q_type, subject_id=subject_id)
    db.session.add(q)
    db.session.commit()
    flash('Question added.')
    return redirect(url_for('teacher.question_bank'))


@teacher_bp.route('/questions/delete/<int:q_id>', methods=['POST'])
@teacher_required
def delete_question(q_id):
    q = Question.query.get_or_404(q_id)
    if PaperQuestion.query.filter_by(question_id=q_id).first():
        flash('Cannot delete — question is used in a paper.')
    else:
        db.session.delete(q)
        db.session.commit()
        flash('Question deleted.')
    return redirect(url_for('teacher.question_bank'))


# ---------------- CREATE PAPER ----------------
@teacher_bp.route('/paper/create', methods=['POST'])
@teacher_required
def create_paper():
    title = request.form.get('title', '').strip()
    subject_id = int(request.form.get('subject_id'))
    exam_type = request.form.get('exam_type', 'class_test')
    user_id = session['user_id']

    if not title:
        flash('Paper title is required.')
        return redirect(url_for('teacher.dashboard'))

    paper = Paper(title=title, subject_id=subject_id, teacher_id=user_id, exam_type=exam_type)
    db.session.add(paper)
    db.session.commit()

    return redirect(url_for('teacher.paper_builder', paper_id=paper.id))


# ---------------- PAPER BUILDER ----------------
@teacher_bp.route('/paper/<int:paper_id>/build', methods=['GET', 'POST'])
@teacher_required
def paper_builder(paper_id):
    paper = Paper.query.get_or_404(paper_id)
    user = User.query.get(session['user_id'])

    if paper.teacher_id != user.id:
        flash('Access denied.')
        return redirect(url_for('teacher.dashboard'))

    if request.method == 'POST':
        title = request.form.get('title')
        subject_id = request.form.get('subject_id')
        exam_type = request.form.get('exam_type')
        if title and subject_id:
            paper.title = title
            paper.subject_id = int(subject_id)
            if exam_type:
                paper.exam_type = exam_type
            
            exam_date = request.form.get('exam_date')
            if exam_date is not None:
                paper.exam_date = exam_date
            
            semester = request.form.get('semester')
            if semester is not None:
                paper.semester = semester
                
            header_title = request.form.get('header_title')
            if header_title is not None:
                paper.header_title = header_title
                
            branch = request.form.get('branch')
            if branch is not None:
                paper.branch = branch
            
            # Save question texts directly from the template
            for pq in paper.questions:
                q_text = request.form.get(f'question_text_{pq.id}')
                if q_text is not None:
                    pq.question.question_text = q_text
                if pq.question.q_type == 'mcq':
                    pq.question.opt_a = request.form.get(f'opt_a_{pq.id}')
                    pq.question.opt_b = request.form.get(f'opt_b_{pq.id}')
                    pq.question.opt_c = request.form.get(f'opt_c_{pq.id}')
                    pq.question.opt_d = request.form.get(f'opt_d_{pq.id}')
            
            db.session.commit()
            flash('Paper details and questions saved.')
        return redirect(url_for('teacher.paper_builder', paper_id=paper.id))

    # Auto-generate or pad fixed template layout based on exam type
    target_count = 25 if paper.exam_type == 'university' else 10
    current_count = len(paper.questions)
    
    if current_count < target_count:
        if paper.exam_type == 'university':
            # 12 MCQs + 2(Q2) + 2(Q3) + 3(Q4) + 3(Q5) + 3(Q6) = 25
            marks_layout = [1]*12 + [6]*13
            types_layout = ['mcq']*12 + ['long']*13
        else:
            marks_layout = [1, 1, 1, 1, 1, 5, 5, 5, 5, 5]
            types_layout = ['mcq', 'mcq', 'mcq', 'mcq', 'mcq', 'long', 'long', 'long', 'long', 'long']
            
        for i in range(current_count, target_count):
            q = Question(question_text='', marks=marks_layout[i], q_type=types_layout[i], subject_id=paper.subject_id)
            db.session.add(q)
            db.session.flush()
            pq = PaperQuestion(paper_id=paper.id, question_id=q.id, order_num=i)
            db.session.add(pq)
        db.session.commit()

    subject_ids = [s.id for s in user.subjects]
    all_questions = Question.query.filter(Question.subject_id.in_(subject_ids)).all()
    added_ids = [pq.question_id for pq in paper.questions]

    return render_template('teacher/paper_builder.html',
                           paper=paper,
                           subjects=user.subjects,
                           all_questions=all_questions,
                           added_ids=added_ids)


# ---------------- OLD (BANK) ADD QUESTION ----------------
@teacher_bp.route('/paper/<int:paper_id>/add-question', methods=['POST'])
@teacher_required
def add_question_to_paper(paper_id):
    question_id = int(request.form.get('question_id'))
    paper = Paper.query.get_or_404(paper_id)

    exists = PaperQuestion.query.filter_by(paper_id=paper_id, question_id=question_id).first()
    if not exists:
        order_num = PaperQuestion.query.filter_by(paper_id=paper_id).count()
        pq = PaperQuestion(paper_id=paper_id, question_id=question_id, order_num=order_num)
        db.session.add(pq)
        db.session.commit()

    return redirect(url_for('teacher.paper_builder', paper_id=paper_id))


# ---------------- 🔥 NEW CUSTOM QUESTION ----------------
@teacher_bp.route('/paper/<int:paper_id>/add-custom-question', methods=['POST'])
@teacher_required
def add_custom_question(paper_id):
    question_text = request.form.get('question_text')
    marks = int(request.form.get('marks', 1))
    q_type = request.form.get('q_type', 'short')

    if not question_text:
        flash("Question cannot be empty!")
        return redirect(url_for('teacher.paper_builder', paper_id=paper_id))

    paper = Paper.query.get_or_404(paper_id)

    q = Question(
        question_text=question_text,
        marks=marks,
        q_type=q_type,
        subject_id=paper.subject_id
    )
    db.session.add(q)
    db.session.commit()

    order_num = len(paper.questions)
    pq = PaperQuestion(
        paper_id=paper.id,
        question_id=q.id,
        order_num=order_num
    )
    db.session.add(pq)
    db.session.commit()

    flash("Question added successfully!")
    return redirect(url_for('teacher.paper_builder', paper_id=paper.id))


# ---------------- REMOVE QUESTION ----------------
@teacher_bp.route('/paper/<int:paper_id>/remove-question/<int:pq_id>')
@teacher_required
def remove_question_from_paper(paper_id, pq_id):
    pq = PaperQuestion.query.get_or_404(pq_id)
    db.session.delete(pq)
    db.session.commit()
    return redirect(url_for('teacher.paper_builder', paper_id=paper_id))


# ---------------- FILE UPLOAD ----------------
@teacher_bp.route('/paper/<int:paper_id>/upload', methods=['POST'])
@teacher_required
def upload_file(paper_id):
    file = request.files.get('file')

    if not file or file.filename == '':
        flash('No file selected.')
        return redirect(url_for('teacher.paper_builder', paper_id=paper_id))

    if not allowed_file(file.filename):
        flash('Only PDF/DOCX allowed.')
        return redirect(url_for('teacher.paper_builder', paper_id=paper_id))

    filename = secure_filename(file.filename)
    filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
    file.save(filepath)

    ext = filename.rsplit('.', 1)[1].lower()
    record = UploadedFile(paper_id=paper_id, filename=filename, file_type=ext)
    db.session.add(record)
    db.session.commit()

    flash('File uploaded successfully.')
    return redirect(url_for('teacher.paper_builder', paper_id=paper_id))


# ---------------- SUBMIT ----------------
@teacher_bp.route('/paper/<int:paper_id>/submit', methods=['POST'])
@teacher_required
def submit_paper(paper_id):
    paper = Paper.query.get_or_404(paper_id)
    paper.status = 'submitted'
    db.session.commit()
    flash('Paper submitted to HOD.')
    return redirect(url_for('teacher.dashboard'))


# ---------------- DELETE PAPER ----------------
@teacher_bp.route('/paper/<int:paper_id>/delete')
@teacher_required
def delete_paper(paper_id):
    paper = Paper.query.get_or_404(paper_id)
    user = User.query.get(session['user_id'])
    
    if paper.teacher_id != user.id:
        flash('Access denied.')
        return redirect(url_for('teacher.dashboard'))

    PaperQuestion.query.filter_by(paper_id=paper.id).delete()
    UploadedFile.query.filter_by(paper_id=paper.id).delete()
    db.session.delete(paper)
    db.session.commit()
    flash('Paper deleted successfully.')
    return redirect(url_for('teacher.dashboard'))