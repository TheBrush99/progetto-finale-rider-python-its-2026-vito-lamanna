import os
from src.utils import inserisci_rider_nel_db, controllo_veicolo_valido, LISTA_VEICOLI_AMMESSI, list_rider_db, list_rider_filtrata_db

def inserisci_rider_handlers(dati_inseriti):
    try:
        if not dati_inseriti:
            return {"Errore":"Il body della richiesta è vuoto, inserisci i dati del driver."}, 400
        nome = dati_inseriti.get('name')
        veicolo = dati_inseriti.get('vehicle')
        consegne_totali = dati_inseriti.get('total_deliveries',0)
        if not nome or not veicolo:
            return {"Errore":"I campi 'name' e 'vehicle' sono obbligatori."}, 400
        if not controllo_veicolo_valido(veicolo):
            return {
                 "Errore validazione dati": f"Il veicolo '{veicolo}' non è valido.",
                 "Veicoli ammessi": LISTA_VEICOLI_AMMESSI
             }, 400
        if not isinstance(consegne_totali, int) or consegne_totali < 0:
             raise ValueError("Il campo 'total_deliveries' deve essere un numero intero maggiore o uguale a zero.") 
        id_generato = inserisci_rider_nel_db(nome, veicolo.lower(), consegne_totali)
        risposta = {
            "Messaggio":"Rider creato con successo!",
            "Rider":{
                "id": id_generato,
                "name": nome,
                "vehicle": veicolo.lower(),
                "total_deliveries": consegne_totali
            }
        }
        return risposta, 201
    except ValueError as e:
        return {"Errore validazione dati": str(e)}, 400
    except Exception as e:
        return {"Errore Server": str(e)}, 500
    
def list_rider_handlers(parametro_url):
    try:
        veicolo = parametro_url.get('vehicle')
        if veicolo is None:
            righe_db = list_rider_db()
            numero_rider = len(righe_db)
            messaggio = f"Elenco completo di tutti i {numero_rider} riders."
        else:
            if not controllo_veicolo_valido(veicolo):
                return {
                    "Errore validazione dati": f"Il veicolo '{veicolo}' non è valido.",
                    "Veicoli ammessi": LISTA_VEICOLI_AMMESSI
                }, 400
            righe_db = list_rider_filtrata_db(veicolo.lower())
            numero_rider = len(righe_db)
            messaggio = f"Elenco dei {numero_rider} riders che utilizzano come veicolo: {veicolo.lower()}"
        #formattazione di righe_db da tuple a dizionari JSON
        risultato_finale = []
        for riga in righe_db:
            rider_formattato ={
                "id": riga[0],
                "name": riga[1],
                "vehicle": riga[2],
                "total_deliveries": riga[3],
                "rating_average": float(riga[4]), # forza in float per evitare strani formati decimali nel JSON
                "total_reviews": riga[5]
            }
            risultato_finale.append(rider_formattato)
        risposta = {
            "Messaggio":messaggio,
            "Risultati":risultato_finale
        }
        return risposta, 200
    except Exception as e:
        return {"Errore Server nell'handler della GET": str(e)}, 500