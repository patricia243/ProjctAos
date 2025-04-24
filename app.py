from flask import Flask, request, jsonify, render_template_string, redirect, url_for
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
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>Bienvenue</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="bg-light text-center py-5">
        <div class="container">
            <h1 class="mb-4">🎓 Bienvenue sur l'API Étudiants</h1>
            <p class="lead">Cliquez ci-dessous pour ajouter un nouvel étudiant et une note.</p>
            <a href="{{ url_for('formulaire') }}" class="btn btn-primary btn-lg">Ajouter </a>
        </div>
    </body>
    </html>
    ''')


# ---------------- Formulaire HTML ----------------
@app.route('/formulaire', methods=['GET', 'POST'])
def formulaire():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        score = float(request.form['score'])

        student = Student(name=name, email=email)
        db.session.add(student)
        db.session.commit()

        grade = Grade(subject=subject, score=score, student_id=student.id)
        db.session.add(grade)
        db.session.commit()

        # Redirection avec message de succès
        return redirect(url_for('formulaire', success=1))

    # Afficher le message s’il est dans l’URL
    success = request.args.get('success')

    return render_template_string('''
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>Formulaire Étudiant</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="bg-light py-5">
        <div class="container bg-white p-5 rounded shadow">
            <h2 class="mb-4 text-primary">Ajouter un étudiant et une note</h2>

            {% if success %}
                <div class="alert alert-success" role="alert">
                    ✅ Étudiant ajouté avec succès !
                </div>
            {% endif %}

            <form method="POST">
                <div class="mb-3">
                    <label for="name" class="form-label">Nom</label>
                    <input type="text" class="form-control" name="name" required>
                </div>
                <div class="mb-3">
                    <label for="email" class="form-label">Email</label>
                    <input type="email" class="form-control" name="email" required>
                </div>
                <div class="mb-3">
                    <label for="subject" class="form-label">Matière</label>
                    <input type="text" class="form-control" name="subject" required>
                </div>
                <div class="mb-3">
                    <label for="score" class="form-label">Note</label>
                    <input type="number" class="form-control" name="score" min="0" max="100" required>
                </div>
                <button type="submit" class="btn btn-success">Soumettre</button>
                <a href="{{ url_for('home') }}" class="btn btn-secondary">Retour</a>
            </form>
        </div>
    </body>
    </html>
    ''', success=success)
# ---------------- Routes API JSON ----------------
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
