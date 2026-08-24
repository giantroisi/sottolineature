# Sottolineature — guida al progetto

Sito statico di citazioni da libri, verificate e curate a mano. Live su https://sottolineature.vercel.app (protetto da password come deterrente, non come sicurezza reale — password: `Calude1!`).

## Principi (non negoziabili)

1. **La correttezza prima di tutto.** Testo della citazione, autore, titolo, anno, contesto: ogni altro miglioramento (design, funzionalità, velocità) è secondario. Meglio scartare una citazione bella ma non verificabile che pubblicarla dubbia.
2. **L'esperienza deve funzionare per pubblici diversi** — giovani e adulti, studenti e insegnanti. Non ottimizzare solo per un tipo di visitatore (vedi le tre "interviste" a persone diverse più sotto).
3. **Ogni progresso, fatto o da fare, va tracciato.** Non fidarsi della sola memoria conversazionale: usare `LOG.md` per i lotti di citazioni e questo file per lo stato generale del progetto. Aggiornare la sezione Roadmap qui sotto ogni volta che si completa o si scopre qualcosa, senza aspettare che l'utente chieda "aggiornami".

## Come verificare una citazione

Le regole complete, scritte per i visitatori del sito, sono in `metodo.html` — questa è la versione operativa per chi lavora sul progetto.

**Fonti, in ordine di preferenza:**
1. Wikisource o l'edizione originale (testo di pubblico dominio o comunque reperibile integralmente)
2. Wikiquote, ma solo se riporta già un riferimento a capitolo/edizione — mai come unica fonte
3. Almeno due fonti indipendenti concordanti sul testo esatto (non due siti che si copiano a vicenda)

**Scartare sempre:**
- citazioni che esistono solo su siti aggregatori senza modo di risalire al testo pubblicato
- frasi attribuite al libro ma che appartengono solo al film/serie tratti da esso
- wording che cambia in modo sostanziale tra fonti senza modo di stabilire quale sia corretto
- citazioni il cui contesto (chi parla, quando) non è verificabile con la stessa fonte del testo

Ogni scarto va motivato in `LOG.md`, non semplicemente omesso.

**Copertine:** da Open Library (`covers.openlibrary.org`). Prima di accettare un `cover_i`: verificare che l'autore del risultato corrisponda (match sul cognome, non fidarsi del solo title-match), poi **guardare l'immagine** prima di pubblicarla — è già capitato che un cover_i "corretto" fosse in realtà una scansione di scheda di lettura scolastica o di pagina bibliografica. Se non si trova un'edizione affidabile, meglio nessuna copertina (la tile con le iniziali dell'autore si genera da sola via JS) che un'immagine sbagliata. Per le poesie senza edizione autonoma, la copertina di un'antologia dell'autore è un compromesso accettabile.

**Contesto:** da quando introdotto (Dante/Dostoevskij come prova), è lo standard per ogni nuova citazione. Regola di scrittura: **prima la storia in linguaggio semplice, poi il nome/riferimento** — mai dare per scontato che chi legge conosca già il libro. Quando rilevante, includere l'edizione o la traduzione a cui il testo fa riferimento.

**Ruolo degli strumenti:** la ricerca delle fonti si avvale di IA per velocizzare il lavoro — va detto apertamente, è scritto anche in `metodo.html`. Quello che non si delega mai è la verifica: ogni citazione è controllata contro le fonti prima di pubblicare.

## Convenzioni tecniche

- **Sito statico puro**: `index.html` (tutto: markup + CSS + JS inline), più `metodo.html`, nessun build step. Deploy automatico su push a `main` via integrazione Git di Vercel.
- **Card**: `<article class="card" data-category="..." data-genre="...(opzionale, multi-valore separato da spazi)">`, contiene `card-quote`, `card-citation` (autore/titolo/anno), `card-context` (opzionale), `card-hint`. Il toggle "Sottolinea", il campo nota e il pulsante "Condividi" vengono iniettati via JS su ogni card, non sono nel markup statico.
- **Condividi**: genera un'immagine 1080×1080 via canvas e usa `navigator.share` con file quando supportato (apre il foglio di condivisione nativo, utile per storie/post Instagram), altrimenti scarica il PNG come fallback.
- **Categorie** (mood, un solo valore, `data-category`): vita, amore, coraggio, liberta, tempo, solitudine, verita. Presentate esplicitamente come "un'atmosfera, non una classificazione" — non aggiungerne altre senza una ragione forte, il punto è restare poche e larghe.
- **Generi** (opzionali, multi-valore, `data-genre`, separati da spazio): fantasy, fantascienza, distopia, horror, saggistica. Regola per aggiungerne uno nuovo: **serve un numero sensato di titoli già presenti sul sito** (indicativamente 4+) prima di introdurre un filtro — altrimenti si scarta l'idea (vedi Giallo/Avventura, scartati per un solo titolo a testa).
- **Copertine mancanti**: gestite da un tile placeholder generato via JS (iniziali autore su colore derivato dal nome), non lasciare mai il buco vuoto.
- **Tema chiaro/scuro**: manuale via bottone in alto a sinistra, salvato in `localStorage['sottolineature-theme']`. Mai legarlo a `prefers-color-scheme` (richiesta esplicita passata, l'utente si era confuso quando cambiava da solo).
- **`localStorage` usato per**: `sottolineature-underlined` (array chiavi `autore|titolo`), `sottolineature-notes` (oggetto chiave→testo nota), `sottolineature-theme`.
- **Verifica prima di pubblicare**: server locale (`python3 -m http.server`) + Browser tool, sbloccare il gate con `sessionStorage.setItem('sottolineature-unlocked','1')` invece di digitare la password, controllare chiaro/scuro e mobile, poi commit + push + conferma deploy (`npx vercel ls sottolineature` o controllo diretto dell'URL).
- **`LOG.md`**: append-only, una riga per lotto (manuale o da routine), formato `- YYYY-MM-DD HH:MM UTC — added N quotes (total now T) — dettagli di cosa aggiunto/scartato e perché`.

## Roadmap

Aggiornata: 2026-08-24.

### Fatto
- 253 citazioni, 34 copertine recuperate + tile placeholder per le mancanti, contesto su 18 citazioni (6 aggiunte con citazioni nuove, 12 aggiunte retroattivamente a citazioni già presenti — standard per le nuove da qui in poi)
- 18 citazioni taggate per genere (Fantasy, Fantascienza, Distopia, Horror/Gotico, Saggistica), tag multipli supportati
- Logo SVG (niente più sfocatura), favicon con la "S" del logo
- Citazione in evidenza: senza box, Sottolinea sincronizzato con la griglia, Copia citazione, Condividi (Web Share API con fallback a download)
- Nota personale su "Sottolinea" (anche in stampa)
- Vista stampabile + pulsante "Stampa o esporta questa selezione"
- Fix allineamento griglia con risultati dispari, stato vuoto per ricerche senza risultati
- Pagina di metodo/trasparenza (`metodo.html`)
- Pulizia repo (rimosso residuo Netlify, `.gitignore` aggiornato)

### Da fare
- **Contesto per le restanti ~235 citazioni** — il cantiere grande, da fare a lotti
- **Autrici/autori fantasy contemporanei** (Sarah J. Maas, Leigh Bardugo, Rick Riordan...) — richiesto dalla lettrice più giovane, stessa rigidità di verifica delle altre citazioni
- **Stato della routine cloud automatica** — da riverificare con l'utente, non è implementabile in autonomia

### Idee scartate (per memoria, non riproporre senza nuovo contenuto)
- Tag "Giallo/Poliziesco" e "Avventura": solo 1-2 titoli a testa sul sito, troppo pochi per un filtro utile
