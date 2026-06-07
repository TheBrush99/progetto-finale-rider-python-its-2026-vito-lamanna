from flask import Flask
from src.routes import riders_bp
from src.utils import inizializza_db
import sys

def create_app():
    app = Flask(__name__)
    try:
        inizializza_db()
    except Exception as e:
        print(f"ERRORE DI AVVIO: Impossibile connettersi a PostgreSQL. \nDettaglio: {e}")
        sys.exit(1)
    app.register_blueprint(riders_bp)
    return app