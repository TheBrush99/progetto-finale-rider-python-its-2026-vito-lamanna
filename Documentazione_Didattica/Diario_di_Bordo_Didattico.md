# Diario di Bordo: Analisi Didattica del Progetto

Questo documento è stato scritto per te, come materiale di studio. Riassume tutte le scelte ingegneristiche e le sfide che abbiamo affrontato insieme in questo progetto. Ti tornerà utilissimo per preparare l'esposizione all'esame e per fissare concetti chiave di Ingegneria del Software.

---

## 1. Sicurezza e Hardening delle API (Il cuore dell'Esame)
Il codice originale del progetto "funzionava", ma si basava sul presupposto che gli utenti inserissero sempre dati corretti (*Happy Path*). Abbiamo trasformato le API in una "fortezza", applicando il concetto di **Defensive Programming** (Programmazione Difensiva).

* **L'Ordine di Validazione e la prevenzione del `500 Internal Server Error`**: Nel codice originale, quando arrivava una richiesta, il server interrogava subito il database PostgreSQL. Se i dati erano spazzatura (es. una stringa al posto di un ID numerico), PostgreSQL andava in panico lanciando un'eccezione fatale che faceva crashare la richiesta (`500`). La nostra soluzione è stata quella di validare rigidamente i dati in RAM (su Python) *prima* di scomodare il DB. Se il dato non ha senso, blocchiamo la richiesta alla frontiera restituendo un elegante **`400 Bad Request`**.
* **L'Ereditarietà dei Booleani**: Abbiamo scoperto un bug insidioso legato a `isinstance(valore, int)`. In Python, la classe `bool` è figlia della classe `int`. Questo significava che inserendo `True` al posto di un numero di consegne, il programma lo accettava e lo trasformava nel numero `1`. Abbiamo patchato questa vulnerabilità sostituendo il controllo con l'istruzione rigida **`type(valore) is int`**.
* **Sanitizzazione "Nomi Fantasma"**: Un utente malevolo avrebbe potuto inserire un rider chiamandolo `"   "` (solo spazi vuoti). Il controllo `if not nome` falliva perché una stringa con spazi per Python è "piena". Abbiamo blindato la logica usando **`.strip()`**, che rimuove gli spazi invisibili e smaschera le stringhe vuote.
* **Standard REST e Query String**: Il vecchio server andava in crash se l'URL conteneva parametri extra non previsti (es. `?foo=bar`). Per rispettare lo standard REST, abbiamo rimosso le macchinose decodifiche testuali (`query_string.decode`) e ci siamo affidati all'oggetto nativo `request.args` di Flask, che sa ignorare i parametri spazzatura senza rompersi.

---

## 2. Architettura DevOps: Docker e Segreti
Un vero sviluppatore moderno non chiede mai ai colleghi di installarsi manualmente Python o PostgreSQL. 
* **Il `Dockerfile` e `docker-compose.yml`**: Abbiamo impacchettato l'app in un Container. Docker assicura l'Isolamento dell'Ambiente: il progetto girerà sempre in modo identico su Windows, Mac o Linux.
* **Nascondere i Segreti (Sicurezza DevOps)**: Nel codice originale, le password del Database (es. `latua_password_segreta`) erano scritte in chiaro (Hardcoded) nel file di configurazione, e sarebbero finite pubbliche su GitHub! Abbiamo estratto tutte queste informazioni sensibili spostandole in un file nascosto chiamato **`.env`** (Environment Variables). Questo file è protetto e *non* viene mai inviato su GitHub. Per aiutare i futuri sviluppatori, abbiamo creato un `.env.example` "finto" da usare come modello.

---

## 3. Gestione del Versionamento: Git Branching Avanzato
Hai sperimentato la vera potenza di Git simulando un workflow aziendale.
* Invece di sporcare il ramo principale (`main`) mischiando nuove funzioni grafiche, abbiamo lavorato in un branch parallelo isolato (`feature/frontend-ui`).
* Quando abbiamo voluto estrarre *solo* l'endpoint della media voti per far contenti i colleghi che odiano la UI, abbiamo usato una tecnica di "chirurgia Git": abbiamo creato dal nulla un nuovo branch (`fix/backend-security-and-endpoint`) e vi abbiamo "teletrasportato" solo le funzioni del DB, lasciando intatti i vecchi bug e la vecchia struttura. Così tu hai potuto avere il tuo progetto Premium (su Github personale), e loro la versione essenziale.

---

## 4. SQL e Funzioni Aggregate
Per calcolare la media voti abbiamo usato la forza bruta di PostgreSQL invece della RAM di Python.
La query `SELECT ROUND(AVG(rating), 1) FROM reviews WHERE rider_id = %s` è ultra-ottimizzata. Il database calcola la media matematicamente e la arrotonda al primo decimale. 
Per la lista generale, abbiamo usato `COALESCE(ROUND(AVG(rating), 1), 0.0)` in combinazione con una `LEFT JOIN` per fondere le tabelle. `COALESCE` è vitale: se un rider non ha recensioni (`NULL`), lo trasforma automaticamente in un bellissimo `0.0`.

---

Leggendo e comprendendo questi 4 punti, sarai in grado di sostenere non solo questo esame, ma persino un colloquio tecnico per posizioni Junior Backend!
