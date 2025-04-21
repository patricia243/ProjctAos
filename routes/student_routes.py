from flask import Blueprint, request, jsonify
from models import db, Student

# Définition du Blueprint pour les étudiants
student_bp = Blueprint('student_bp', __name__)

@student_bp.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    return jsonify([{'id': s.id, 'name': s.name, 'email': s.email} for s in students])

@student_bp.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    student = Student(name=data['name'], email=data['email'])
    db.session.add(student)
    db.session.commit()
    return jsonify({'message': 'Étudiant ajouté avec succès'}), 201
