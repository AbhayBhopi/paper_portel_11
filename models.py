from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='teacher')

    subjects = db.relationship('Subject', secondary='user_subjects', backref='users')
    papers = db.relationship('Paper', backref='teacher', lazy=True)


class Subject(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), nullable=False)

    questions = db.relationship('Question', backref='subject', lazy=True)
    papers = db.relationship('Paper', backref='subject', lazy=True)


user_subjects = db.Table('user_subjects',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('subject_id', db.Integer, db.ForeignKey('subjects.id'), primary_key=True)
)


class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    marks = db.Column(db.Integer, nullable=False, default=1)
    q_type = db.Column(db.String(20), nullable=False, default='short')


class Paper(db.Model):
    __tablename__ = 'papers'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='draft')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    questions = db.relationship('PaperQuestion', backref='paper', lazy=True, order_by='PaperQuestion.order_num')
    uploaded_files = db.relationship('UploadedFile', backref='paper', lazy=True)


class PaperQuestion(db.Model):
    __tablename__ = 'paper_questions'
    id = db.Column(db.Integer, primary_key=True)
    paper_id = db.Column(db.Integer, db.ForeignKey('papers.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    order_num = db.Column(db.Integer, nullable=False, default=0)

    question = db.relationship('Question')


class UploadedFile(db.Model):
    __tablename__ = 'uploaded_files'
    id = db.Column(db.Integer, primary_key=True)
    paper_id = db.Column(db.Integer, db.ForeignKey('papers.id'), nullable=False)
    filename = db.Column(db.String(200), nullable=False)
    file_type = db.Column(db.String(10), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)


def init_db(app):
    with app.app_context():
        db.create_all()

        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                password_hash=generate_password_hash('admin123'),
                full_name='HOD Admin',
                role='admin'
            )
            db.session.add(admin)

        if Subject.query.count() == 0:
            subjects = [
                Subject(name='Mathematics', code='MATH101'),
                Subject(name='Physics', code='PHY101'),
                Subject(name='Chemistry', code='CHEM101'),
                Subject(name='Computer Science', code='CS101'),
            ]
            db.session.add_all(subjects)

        db.session.commit()
        print("Database initialized. Admin login: admin / admin123")
