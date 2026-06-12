# Capire il Progetto: Guida Passo Passo per Umani

Se ti senti perso tra codici, script e terminali, non preoccuparti. In questo documento spiegheremo il progetto come se stessimo costruendo un ristorante. Nessun termine tecnico difficile, solo la logica pura di come funziona tutto l'ingranaggio.

---

## 1. Cos'è questo progetto?
L'idea di base è semplice: abbiamo creato il sistema gestionale per un'azienda di consegne a domicilio (tipo Glovo o Deliveroo).
Il nostro sistema deve permettere di:
- Assumere nuovi corrieri (**Riders**) indicando che veicolo usano.
- Vedere la lista di tutti i corrieri (o filtrarli per chi usa la moto, l'auto, ecc.).
- Permettere ai clienti di lasciare una recensione (da 1 a 5 stelle) per un corriere.
- Calcolare in automatico la **Media Voti** di ciascun corriere.

---

## 2. L'Architettura: I tre piani del Ristorante
Immagina il tuo progetto informatico come un grandissimo ristorante diviso su tre piani. Ognuno ha un compito specifico e *non* fa il lavoro degli altri.

### 🍽️ Piano Terra: Il Frontend (L'Interfaccia Utente)
*Cosa include: I file HTML, CSS e JavaScript nella cartella `static`.*
È la sala da pranzo del ristorante. Qui c'è la grafica, i bottoni colorati, i moduli da compilare. Il cliente vede solo questo. Quando il cliente preme il bottone "Aggiungi Rider", il Frontend chiama il Cameriere (API) per ordinare l'azione.

### 🏃‍♂️ Primo Piano: Il Backend (Il Motore in Python/Flask)
*Cosa include: Tutti i file `.py` dentro la cartella `src`.*
È il cervello del ristorante, il Direttore di Sala. Non si occupa di estetica, riceve solo l'ordine dal Frontend, controlla che la richiesta sia valida (es. "Il nome inserito non è vuoto?"), applica le regole aziendali e poi dà ordini al piano di sotto.

### 🗄️ Cantina: Il Database (PostgreSQL)
*Cosa include: Il database gestito dal container `db` in Docker.*
È il magazzino sotterraneo. Il suo unico scopo è ricordare le cose. Non ragiona, si limita ad obbedire: memorizza i nomi dei rider, le recensioni e risponde alle domande ("Dammi la lista di tutte le recensioni"). È rigidissimo: se gli chiedi di salvare una parola al posto di un numero, va in panico (ecco perché il Backend deve filtrare i dati prima di mandarli in cantina!).

---

## 3. Il viaggio di una richiesta: Cosa succede quando clicchi un bottone?
Facciamo finta che tu sia sul sito e inserisca il rider "Vito" con il veicolo "Moto", poi premi Invia.

1. **Il Click (Frontend):** Il tuo browser raccoglie la parola "Vito" e "Moto" e le spedisce impacchettate via Internet al server.
2. **La Porta d'Ingresso (Routes):** Il pacchetto arriva in `src/routes.py`. Questo file è il "buttafuori". Guarda l'etichetta del pacchetto e dice: *"Ah, questo pacchetto è indirizzato alla rotta `/insert_rider`. Lo passo all'ufficio di competenza!"*.
3. **Il Controllo Qualità (Handlers):** Il pacchetto arriva in `src/handlers/riders_handlers.py`. Qui Python ispeziona il contenuto: *"Vediamo... Il nome è vuoto? No, c'è scritto Vito. Il veicolo Moto è consentito? Sì, è nella lista dei veicoli ammessi. I dati sono sani."*.
4. **Il Magazziniere (Postgres Handlers):** Una volta superati i controlli, i dati vengono passati a `src/postgres/postgres_handlers.py`. Questo file è l'unico autorizzato ad aprire la porta della Cantina (il Database). Traduce i dati in una lingua che il DB capisce (il linguaggio **SQL**) dicendo: `INSERT INTO riders (name, vehicle) VALUES ('Vito', 'moto')`.
5. **Il Ritorno:** Il database salva "Vito", genera un ID univoco (es. ID numero 5) e lo urla al magazziniere. L'informazione fa il percorso inverso fino ad arrivare al Frontend, che mostra una spunta verde sullo schermo: "Rider creato con successo!".

---

## 4. Perché lo abbiamo diviso in tanti file? (Separation of Concerns)
All'inizio potevamo scrivere tutto in un unico enorme file `main.py`. Perché non l'abbiamo fatto?
Per il principio della **Separazione delle Responsabilità**.
- Se un domani decidi di cambiare il Database (da PostgreSQL a MySQL), dovrai modificare **solo** il file `postgres_handlers.py`. Il resto dell'app non se ne accorgerà nemmeno.
- Se decidi di cambiare l'interfaccia grafica (facendo un'app per smartphone al posto di un sito web), dovrai buttare solo la cartella `static` del Frontend. Il tuo Backend Python rimarrà intatto e perfetto.

Questo significa scrivere codice "Scalabile" e "Manutenibile".

---

## 5. La Scatola Magica: Docker
Perché abbiamo usato Docker? 
Immagina di aver costruito un motore perfetto sul tuo PC. Quando lo passi al tuo collega, a lui non funziona perché ha una versione di Python diversa o perché non ha scaricato PostgreSQL. 
Con Docker, tu prendi il tuo ristorante, lo metti dentro un "Container" (un container da nave cargo), e lo spedisci chiuso. Dentro quel container c'è **già tutto**: l'esatta versione di Python, il database, le configurazioni. Il tuo collega deve solo scaricare il container e premere "Play" (`docker-compose up`). Il programma girerà magicamente su qualsiasi computer, Windows, Mac o Linux, senza dover installare null'altro.

---

## Conclusione
Questo progetto è un esempio da manuale di **Architettura a 3 Livelli** (Frontend, Backend, Database), protetto da tecniche di **Programmazione Difensiva** (i controlli anti-hacker che abbiamo inserito) e pacchettizzato con moderne metodologie **DevOps** (Docker e variabili segrete nel file `.env`). 

Spero che questa spiegazione ti abbia fatto visualizzare l'ingranaggio dietro lo schermo. Ora il codice non è più magia, è pura logica!
