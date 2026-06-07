import os
from src.utils import inserisci_rider_nel_db

def inserisci_rider(dati_inseriti):
    try:
        if not dati_inseriti:
            return {"Errore":"Il body della richiesta deve essere un JSON valido."}, 400
        nome = dati_inseriti.get('name')
        veicolo = dati_inseriti.get('vehicle')
        consegne_totali = dati_inseriti.get('total_deliveries',0)
        if not nome or not veicolo:
            return {"Errore":"I campi 'name' e 'vehicle' sono obbligatori."}, 400
        id_generato = inserisci_rider_nel_db(nome, veicolo, consegne_totali)
        risposta = {
            "Messaggio":"Rider creato con successo!",
            "Rider":{
                "id": id_generato,
                "name": nome,
                "vehicle": veicolo,
                "total_deliveries": consegne_totali
            }
        }
        return risposta, 201
    except Exception as e:
        return {"Errore Server": str(e)}, 500