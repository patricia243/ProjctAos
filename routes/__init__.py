from dotenv import load_dotenv
import os

load_dotenv()  # charge le contenu du fichier .env

# exemple d'utilisation
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///students.db")
SECRET_KEY = os.getenv("SECRET_KEY", "defaultkey")
DEBUG = os.getenv("DEBUG", "True") == "True"