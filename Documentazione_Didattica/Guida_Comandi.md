# Guida ai Comandi del Progetto Riders

Questa è la tua "Cheat Sheet" (lista rapida) di tutti i comandi necessari per gestire il tuo progetto in ogni situazione. 
Sei attualmente nel branch `feature/frontend-ui` (versione Premium con interfaccia grafica e Docker).

---

## 🐋 1. Avvio Rapido con Docker (Raccomandato)
Docker è il modo più pulito per avviare il progetto. Crea un "computer virtuale" che ha già Python e PostgreSQL configurati e pronti all'uso.

**Per avviare il Server Web e il Database:**
```powershell
docker-compose up --build
```
*(Questo comando legge il tuo file `.env`, costruisce l'app, fa partire il database, lo popola con i dati fittizi e mette il sito online su http://localhost:5000)*

**Per spegnere e pulire tutto (A fine giornata):**
```powershell
docker-compose down
```

**Per spegnere e DISTRUGGERE il database (Tabula Rasa):**
```powershell
docker-compose down -v
```
*(Usa la `-v` se vuoi resettare completamente i dati che avevi inserito e ripartire da zero alla prossima accensione).*

---

## 🐍 2. Avvio Locale Senza Docker (Metodo Classico)
Se preferisci non usare Docker e vuoi sviluppare testando l'app direttamente sul tuo PC Windows. Assicurati di avere PostgreSQL acceso in background.

**Passo 1: Attivare l'Ambiente Virtuale (VENV)**
```powershell
.\venv\Scripts\Activate.ps1
```
*(Vedrai comparire la scritta `(venv)` verde all'inizio della riga del terminale).*

**Passo 2: Avviare il Server Flask**
```powershell
python main.py
```
*(Ora il sito è online su http://localhost:5000).*

---

## 💣 3. Test e Sicurezza

**Eseguire lo Stress Test (Crash Test)**
Se vuoi dimostrare al professore quanto è solido il tuo backend, lancia questo comando mentre il server (Docker o locale) è acceso. Fallo da un secondo terminale:
```powershell
python crash_test.py
```
*(Il terminale si riempirà di test automatici che cercheranno di "hackerare" il sistema, fallendo e ottenendo dei perfetti errori 400).*

---

## 🐙 4. Gestione GitHub (Invio aggiornamenti)
Se fai nuove modifiche al codice e vuoi aggiornare i tuoi repository online:

```powershell
# 1. Aggiungi tutte le modifiche
git add .

# 2. Crea un pacchetto di salvataggio (Commit)
git commit -m "Il tuo messaggio descrittivo qui"

# 3. Invialo al tuo profilo personale
git push vito_premium feature/frontend-ui:main

# 4. Invialo all'organizzazione dell'esame
git push org_premium feature/frontend-ui:main
```
