from app import app
from models import db, Subject, Paper, Question, PaperQuestion, UploadedFile, user_subjects

with app.app_context():
    # 1. Clear out user_subjects mapping
    db.session.execute(user_subjects.delete())
    
    # 2. Delete all dependencies since the old subjects are being totally removed
    PaperQuestion.query.delete()
    UploadedFile.query.delete()
    Paper.query.delete()
    Question.query.delete()
    
    # 3. Delete old subjects
    Subject.query.delete()
    
    # 4. Insert new subjects
    subjects = [
        Subject(name='Computer Network and Cloud Computing', code='BTAIC501'),
        Subject(name='Machine Learning', code='BTAIC502'),
        Subject(name='2. Business Communication', code='BTAIHM503B'),
        Subject(name='1. Advanced Database System', code='BTAIPE504A'),
        Subject(name='3. Software Engineering and Testing', code='BTAIOE505C'),
        Subject(name='Deep Learning', code='BTAIC601'),
        Subject(name='Advanced Machine Learning', code='BTAIC602'),
        Subject(name='4. Web Development', code='BTAIPE603D'),
        Subject(name='1. Big Data Analytics', code='BTAIOE604A'),
        Subject(name='1. Development Engineering', code='BTAIHM605A'),
    ]
    db.session.add_all(subjects)
    
    db.session.commit()
    print("Database subjects fully updated to the new list, and old data wiped.")
