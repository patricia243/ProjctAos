from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate



app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# ---------------- Modèle Student ----------------
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }

# ---------------- Modèle Grade ----------------
class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(120), nullable=False)
    score = db.Column(db.Float, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'subject': self.subject,
            'score': self.score,
            'student_id': self.student_id
        }

# ---------- Créer la base de données ----------
with app.app_context():
    db.create_all()

# ---------------- Page d'accueil ----------------
@app.route('/')
def home():
    return '''
    <h1>Bienvenue sur l'API Étudiants</h1>
    <p>Voici les routes disponibles :</p>
    <ul>
        <li><strong>GET /students</strong> : Liste des étudiants</li>
        <li><strong>POST /students</strong> : Ajouter un étudiant</li>
        <li><strong>GET /grades</strong> : Liste des notes</li>
        <li><strong>POST /grades</strong> : Ajouter une note</li>
    </ul>
    '''

# ---------------- Routes Students ----------------
@app.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    return jsonify([student.to_dict() for student in students])

@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({'error': 'Données manquantes'}), 400

    new_student = Student(name=data['name'], email=data['email'])
    db.session.add(new_student)
    db.session.commit()
    return jsonify(new_student.to_dict()), 201

# ---------------- Routes Grades ----------------
@app.route('/grades', methods=['GET'])
def get_grades():
    grades = Grade.query.all()
    return jsonify([grade.to_dict() for grade in grades])

@app.route('/grades', methods=['POST'])
def add_grade():
    data = request.get_json()
    if not data or 'subject' not in data or 'score' not in data or 'student_id' not in data:
        return jsonify({'error': 'Données incomplètes'}), 400

    new_grade = Grade(subject=data['subject'], score=data['score'], student_id=data['student_id'])
    db.session.add(new_grade)
    db.session.commit()
    return jsonify(new_grade.to_dict()), 201

# ---------------- Lancer l'application ----------------
if __name__ == '__main__':
    app.run(debug=True)
