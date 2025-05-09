from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Ajout de la colonne created_at

    def __repr__(self):
        return f'<Student {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'created_at': self.created_at.isoformat()  # Renvoi de la date en format ISO 8601
        }


class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(120), nullable=False)
    score = db.Column(db.Float, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)

    student = db.relationship('Student', backref=db.backref('grades', lazy=True))

    def __repr__(self):
        return f'<Grade {self.subject} - {self.score} (Student ID: {self.student_id})>'

    def to_dict(self):
        return {
            'id': self.id,
            'subject': self.subject,
            'score': self.score,
            'student_id': self.student_id
        }
