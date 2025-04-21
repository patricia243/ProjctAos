from flask import Blueprint, request, jsonify
from models import db, Grade

grades_bp = Blueprint('grades', __name__, url_prefix='/grades')

@grades_bp.route('/', methods=['GET'])
def get_grades():
    grades = Grade.query.all()
    return jsonify([grade.to_dict() for grade in grades])

@grades_bp.route('/', methods=['POST'])
def add_grade():
    data = request.get_json()
    if not data or 'subject' not in data or 'score' not in data or 'student_id' not in data:
        return jsonify({'error': 'Données incomplètes'}), 400

    new_grade = Grade(subject=data['subject'], score=data['score'], student_id=data['student_id'])
    db.session.add(new_grade)
    db.session.commit()
    return jsonify(new_grade.to_dict()), 201
