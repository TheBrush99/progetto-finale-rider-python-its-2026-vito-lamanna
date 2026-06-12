# Progetto Riders - Versione Estesa (con UI e Docker)

Questo branch (`feature/frontend-ui`) rappresenta una versione estesa del progetto originale, che include un'interfaccia grafica, un sistema completo di orchestrazione con Docker e numerose patch di sicurezza lato server.

## Novità di questa versione

1. **Interfaccia Grafica Dedicata:** Interfaccia pulita senza dashboard eccessive, che espone in modo chiaro le carte dei Rider e permette di visualizzare dinamicamente la media voti.
2. **Dockerizzazione Completa:** L'intero ecosistema (Flask + PostgreSQL) si avvia in un click senza dover installare dipendenze locali.
3. **Messa in sicurezza (Hardening):** 
   - Prevenzione del crash del DB validando tutti i dati in RAM (Python) prima di inviarli a Postgres.
   - Patch del "Trucco dei Booleani" (impedisce che valori come `True` bypassino i controlli sugli interi).
   - Patch dei "Nomi Fantasma" (impedisce l'inserimento di stringhe vuote o di soli spazi).
   - Tolleranza delle query URL secondo gli standard REST.
4. **Protezione dei Segreti:** Rimozione di credenziali hard-coded e lettura dinamica da file sicuri `.env`.

## Come avviare il progetto

Hai due opzioni per avviare questo progetto: con Docker (consigliato per sviluppatori esterni) o in locale.

### Opzione A: Avvio rapido con Docker (Raccomandato)
Se hai Docker Desktop installato, ti basta un solo comando per far partire contemporaneamente l'App Web e il Database configurato:
```powershell
docker-compose up --build
```
Il sito sarà visibile su `http://localhost:5000`.

### Opzione B: Avvio manuale locale (Python VENV)
Se preferisci sviluppare alla vecchia maniera o non hai Docker:
1. Rinomina il file `.env.example` in `.env` e imposta le tue credenziali locali (se hai postgres installato su Windows).
2. Attiva l'ambiente virtuale:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
3. Fai partire il server:
   ```powershell
   python main.py
   ```

## Crash Test
Nel progetto è presente uno script didattico chiamato `crash_test.py`. Serve a dimostrare che l'API è resiliente. Puoi eseguirlo con:
```powershell
python crash_test.py
```
Se il progetto risponde con una serie di "TEST SUPERATO (400)", significa che l'API ha difeso correttamente il database dagli inserimenti corrotti.
