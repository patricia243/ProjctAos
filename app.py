from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# ---------------- Modèle Student ----------------
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'email': self.email}

# ---------------- Modèle Grade ----------------
class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(120), nullable=False)
    score = db.Column(db.Float, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    student = db.relationship('Student', backref=db.backref('grades', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'subject': self.subject,
            'score': self.score,
            'student_id': self.student_id
        }

# ---------------- Page d'accueil ----------------
@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>API Étudiants</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { background-color: #f8f9fa; padding: 2rem; font-family: 'Segoe UI', sans-serif; }
            .container { background-color: white; padding: 2rem; border-radius: 10px; box-shadow: 0 0 15px rgba(0,0,0,0.1); }
            h1 { color: #0d6efd; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Bienvenue sur l'API Étudiants 📘</h1>
            <p>Voici les routes disponibles :</p>
            <ul>
                <li><strong>GET /students</strong> : Liste des étudiants</li>
                <li><strong>POST /students</strong> : Ajouter un étudiant</li>
                <li><strong>GET /students/&lt;id&gt;</strong> : Détails d’un étudiant</li>
                <li><strong>GET /grades</strong> : Liste des notes</li>
                <li><strong>POST /grades</strong> : Ajouter une note</li>
            </ul>
        </div>
    </body>
    </html>
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

@app.route('/students/<int:id>', methods=['GET'])
def get_student(id):
    student = Student.query.get_or_404(id)
    return jsonify(student.to_dict())

@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    student = Student.query.get_or_404(id)
    data = request.get_json()
    if 'name' in data:
        student.name = data['name']
    if 'email' in data:
        student.email = data['email']
    
    db.session.commit()
    return jsonify(student.to_dict())

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

# ---------------- Lancement ----------------
if __name__ == '__main__':
    app.run(debug=True, port=8080)
