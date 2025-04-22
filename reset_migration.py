from app import app, db

with app.app_context():
    with db.engine.connect() as conn:
        conn.execute("DROP TABLE IF EXISTS student")
        conn.execute("DROP TABLE IF EXISTS grade")
        print("Tables supprimées.")
