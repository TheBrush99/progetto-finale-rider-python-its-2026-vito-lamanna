from flask import Blueprint, request, jsonify
from src.handlers.riders_handlers import inserisci_rider

riders_bp = Blueprint("riders", __name__, url_prefix="/riders")

@riders_bp.route('/insert_rider', methods=['POST'])
def insert_rider():
    try:
        dati_inseriti = request.get_json()
        risposta_json, codice_http = inserisci_rider(dati_inseriti)
        if risposta_json and codice_http:
            return jsonify(risposta_json), codice_http
    except Exception as e:
        return jsonify({"Errore": str(e)}), 400