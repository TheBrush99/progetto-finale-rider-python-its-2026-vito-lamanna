import urllib.request
import urllib.error
import json
import time

# Aspetta un attimo per assicurarsi che Flask sia pronto
time.sleep(1)

def fetch(method, url, data=None):
    req = urllib.request.Request(url, method=method)
    if data is not None:
        req.add_header('Content-Type', 'application/json')
        req.data = json.dumps(data).encode('utf-8')
    try:
        with urllib.request.urlopen(req) as response:
            return response.status, json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode())
    except Exception as e:
        return 0, str(e)

print("=== INIZIO CRASH TEST ===\n")

print("TEST 1: L'ordine delle validazioni (Invio id recensione come stringa 'ciao')")
print("Payload: {\"rider_id\": \"ciao\", \"customer_name\": \"Mario\", \"rating\": 5}")
status, res = fetch('POST', 'http://localhost:5000/riders/insert_review', {"rider_id": "ciao", "customer_name": "Mario", "rating": 5})
print(f"> Status HTTP: {status} (Dovrebbe essere 400 Bad Request)")
print(f"> Risposta del Server:\n{json.dumps(res, indent=2)}\n")

print("TEST 2: Il trucco dei Booleani (Invio 'total_deliveries' come 'true' boolean invece di numero)")
print("Payload: {\"name\": \"Rider Booleano\", \"vehicle\": \"moto\", \"total_deliveries\": true}")
status, res = fetch('POST', 'http://localhost:5000/riders/insert_rider', {"name": "Rider Booleano", "vehicle": "moto", "total_deliveries": True})
print(f"> Status HTTP: {status} (Dovrebbe rifiutarlo)")
print(f"> Risposta del Server:\n{json.dumps(res, indent=2)}\n")

print("TEST 3: I Nomi Fantasma (Invio nome come 3 spazi vuoti)")
print("Payload: {\"name\": \"   \", \"vehicle\": \"auto\"}")
status, res = fetch('POST', 'http://localhost:5000/riders/insert_rider', {"name": "   ", "vehicle": "auto"})
print(f"> Status HTTP: {status} (Dovrebbe bloccarlo)")
print(f"> Risposta del Server:\n{json.dumps(res, indent=2)}\n")

print("TEST 4: Fragilità dell'URL (Invio parametro sconosciuto '?foo=bar')")
print("GET /riders/list_rider?foo=bar")
status, res = fetch('GET', 'http://localhost:5000/riders/list_rider?foo=bar')
print(f"> Status HTTP: {status} (Dovrebbe ignorare 'foo=bar' e restituire la lista 200)")
print(f"> Risposta del Server:\n{json.dumps(res, indent=2)}\n")

print("=== FINE CRASH TEST ===")
