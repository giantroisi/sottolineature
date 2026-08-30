# Sottolineature — guida al progetto

Sito statico di citazioni da libri, verificate e curate a mano. Live su https://sottolineature.it (dominio registrato su Hostinger, DNS gestito lì con un record A verso Vercel `76.76.21.21`; resta raggiungibile anche su https://sottolineature.vercel.app). **Pubblico**, senza password — il gate d'accesso c'era in origine come deterrente e per un periodo di rifinitura del sito, poi rimosso il 2026-08-25 a lavoro concluso.

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

- **Sito statico puro**: file già pronti serviti da Vercel così come sono, nessun build step lato server. Deploy automatico su push a `main` via integrazione Git di Vercel — **se non parte da sola** (è già successo), fare `npx vercel --prod` a mano.
- **`data/citazioni.json` è la fonte di verità per le citazioni** (dal 2026-08-28, Fase 2 SEO): un array che preserva l'ordine di visualizzazione in home, un oggetto per citazione con `quote`, `author`, `title`, `year`, `context`, `cover`, `category`, `genre` (stringa vuota se assente), `added` (data `YYYY-MM-DD` o `null` se non ricostruibile con certezza). **Si edita quel file, mai `index.html` a mano.** Dopo ogni modifica (aggiunta/rimozione citazione, contesto, copertina, categoria, genere) **lanciare `python3 tools/build.py`**, che rigenera in ordine `index.html`, `citazioni/`, `temi/`, `generi/`, `autori/`, `assets/og/` e `sitemap.xml`. `index.html` è un file generato come gli altri: modificarlo a mano viene perso al giro successivo.
- **`templates/home_template.html`** è la parte fissa della home (header, filtri, script, footer) — qui si tocca markup/stile/comportamento che non dipende dalla singola citazione. Contiene i placeholder `{{CARDS}}`, `{{COUNT}}` e `{{COUNT_WORDS}}` (il numero in lettere nel paragrafo introduttivo, calcolato da `tools/generate_home.py::italian_number_words`), sostituiti a ogni build.
- **Il contesto (`card-context`) è pubblicato solo su `/citazioni/<slug>/`**, mai in home: la home mostra citazione, autore, titolo, anno e copertina ma non il contesto, per non competere con la pagina citazione sullo stesso testo (altrimenti Google vede due pagine con lo stesso contenuto e non sa quale preferire). Il contesto resta comunque nella fonte di verità (`data/citazioni.json`), da lì lo leggono sia `generate_quote_pages.py` (lo pubblica) sia `generate_home.py` (non lo pubblica).
- **Card**: `<article class="card" data-category="..." data-genre="...(opzionale, multi-valore separato da spazi)">`, contiene `card-quote`, `card-citation` (autore/titolo/anno), `card-hint` (il contesto non è più nel markup della home, vedi sopra). Il toggle "Sottolinea", il campo nota e il pulsante "Condividi" vengono iniettati via JS su ogni card, non sono nel markup statico.
- **Attenzione se si corregge il testo di una citazione già pubblicata** (refuso, wording impreciso rispetto alla fonte, ecc.): la chiave che congela lo slug in `tools/slugs.json` include le prime 6 parole della citazione (`quote_key()` in `generate_quote_pages.py`), quindi cambiare il testo cambia la chiave e genera uno slug **nuovo** al prossimo `build.py`, invece di riusare quello congelato — l'URL non deve cambiare per una correzione di refuso. Prima di correggere il testo: rinominare a mano in `slugs.json` la chiave vecchia con quella nuova (stesse prime 6 parole aggiornate), mantenendo il valore (slug) invariato — poi lanciare `build.py` e controllare che non compaiano pagine o immagini OG orfane nel rapporto finale. Scoperto e risolto durante la Fase 3 (lotto 1) su Boccaccio e Machiavelli.
- **Condividi**: genera un'immagine via canvas nel formato di `DEFAULT_SHARE_FORMAT` (oggi `post`, 1080×1350) e usa `navigator.share` con file quando supportato (apre il foglio di condivisione nativo, utile per storie/post Instagram), altrimenti scarica il PNG come fallback. Il formato `storia` (1080×1920) tiene margini verticali ampi perché Instagram sovrappone la propria interfaccia sopra e sotto.
- **Due trappole del canvas già incontrate**, da non ripetere: (1) `ctx.filter` non è affidabile su Safari — viene ignorato in silenzio; per ricolorare il logo si usa `globalCompositeOperation = 'source-in'`, che funziona ovunque. (2) `ctx.letterSpacing` aggiunge spazio anche **dopo** l'ultima lettera, quindi un testo centrato risulta spostato a sinistra di metà spaziatura: va compensato sommando `spacing/2` alla x.
- **Verificare le immagini generate misurando i pixel**, non a occhio: si estrae il blob intercettando `URL.createObjectURL`, poi si controllano dimensioni, colore di sfondo e centratura dei blocchi con PIL. Gli scarti di pochi pixel non si vedono ma si sommano.
- **Categorie** (mood, un solo valore, `data-category`): vita, amore, coraggio, liberta, tempo, solitudine, verita. Presentate esplicitamente come "un'atmosfera, non una classificazione" — non aggiungerne altre senza una ragione forte, il punto è restare poche e larghe.
- **Generi** (opzionali, multi-valore, `data-genre`, separati da spazio): fantasy, fantascienza, distopia, horror, saggistica. Regola per aggiungerne uno nuovo: **serve un numero sensato di titoli già presenti sul sito** (indicativamente 4+) prima di introdurre un filtro — altrimenti si scarta l'idea (vedi Giallo/Avventura, scartati per un solo titolo a testa).
- **Copertine mancanti**: gestite da un tile placeholder generato via JS (iniziali autore su colore derivato dal nome), non lasciare mai il buco vuoto.
- **Tema chiaro/scuro**: manuale via bottone in alto a sinistra, salvato in `localStorage['sottolineature-theme']`. Mai legarlo a `prefers-color-scheme` (richiesta esplicita passata, l'utente si era confuso quando cambiava da solo).
- **`localStorage` usato per**: `sottolineature-underlined` (array chiavi `autore|titolo`), `sottolineature-notes` (oggetto chiave→testo nota), `sottolineature-theme`.
- **Verifica prima di pubblicare**: server locale (`python3 -m http.server`) + Browser tool, controllare chiaro/scuro e mobile, poi commit + push + conferma deploy (`npx vercel ls sottolineature` o controllo diretto dell'URL). Il sito non ha più un gate d'accesso (rimosso il 2026-08-25), quindi non serve più sbloccarlo prima di testare.
- **`LOG.md`**: append-only, una riga per lotto (manuale o da routine), formato `- YYYY-MM-DD HH:MM UTC — added N quotes (total now T) — dettagli di cosa aggiunto/scartato e perché`.

## Roadmap

Aggiornata: 2026-08-28.

### Fatto
- Citazioni in crescita continua, non un traguardo fisso — il conteggio esatto è sempre in `data/citazioni.json`/`LOG.md`, non tenerlo aggiornato qui a ogni lotto. 245 copertine recuperate + tile placeholder per le mancanti, **contesto su 254/256 citazioni al momento della chiusura del cantiere contesto** — cifra storica, non aggiornata a ogni lotto successivo. Nota: il numero di copertine era rimasto non aggiornato per diversi lotti passati (indicava ancora "34", risalente a uno stato molto più piccolo del sito) — corretto qui al valore reale contato dal file
- **216 contesti aggiunti in una sola giornata (2026-08-28), in autonomia**, su richiesta esplicita dell'utente ("puoi procedere senza i miei ok? l'importante è che segui la costituzione") — dettagli completi in LOG.md, in più lotti, ripresi anche dopo un'interruzione per limite settimanale di ricerca web esaurito e poi ripristinato. Restano solo 2 citazioni senza contesto, entrambe scartate per la stessa ragione — nessuna fonte (incluso Wikiquote) attribuisce un parlante o capitolo preciso: Dostoevskij (Delitto e castigo), Sciascia (Il giorno della civetta). Lezione operativa: quando lo stesso autore/titolo compare più volte sul sito, un contesto scritto per una citazione può finire applicato per errore anche alle altre con lo stesso titolo se lo script di inserimento non controlla i duplicati — sempre bene un controllo automatico post-inserimento (nessun contesto identico su citazioni diverse) prima di pubblicare
- **Corretta un'attribuzione errata già pubblicata**: la citazione di Naguib Mahfouz sulla "parola d'amore pronunciata freddamente" era attribuita a "Il palazzo del desiderio" (1957), ma appartiene in realtà a "Vicolo del mortaio" (Midaq Alley, 1947) — confermato da una fonte con dettagli narrativi specifici (Hamida, Abbas, l'arruolamento nell'esercito inglese) che nessuna fonte collegava invece a Il palazzo del desiderio. Corretti titolo, anno, copertina e aggiunto il contesto
- 35 citazioni taggate per genere (Fantasy 12, Fantascienza 9, Distopia 7, Saggistica 6, Horror/Gotico 4 — alcune ne hanno più d'uno), tag multipli supportati
- Prime 3 autrici/autori fantasy contemporanei: Rick Riordan (Percy Jackson), Neil Gaiman (Coraline), Terry Pratchett (Il tristo mietitore) — verificati su Wikiquote + una seconda fonte concordante ciascuno; Sarah J. Maas e Leigh Bardugo scartati per assenza di una fonte italiana tracciabile al testo pubblicato (solo blog/trame), da ritentare con accesso a un'anteprima editoriale
- Logo SVG (niente più sfocatura), favicon con la "S" del logo
- Citazione in evidenza: senza box, Sottolinea sincronizzato con la griglia, Copia citazione, Condividi (Web Share API con fallback a download)
- Immagine condivisa **1080×1350** (4:5), composizione centrata: virgolette dorate, citazione con corpo che si adatta alla lunghezza (scala 72→22px), attribuzione su due livelli (autore in maiuscolo spaziato e inchiostro pieno, opera e anno in corsivo serif), firma in basso con logo (92px) e URL sotto (22px, spaziatura 5px, più largo del logo così la firma appare centrata a occhio). Citazione e attribuzione sono un blocco unico centrato, così l'attribuzione resta legata al testo e non sembra parte della firma. I colori sono letti dai token CSS del tema attivo, quindi l'immagine segue chiaro/scuro e future modifiche alla palette
- Nota personale su "Sottolinea" (anche in stampa)
- Vista stampabile + pulsante "Stampa o esporta questa selezione"
- Fix allineamento griglia con risultati dispari, stato vuoto per ricerche senza risultati
- Pagina di metodo/trasparenza (`metodo.html`)
- Dominio personalizzato sottolineature.it collegato (record A su Hostinger, HTTPS automatico), incluso il www
- Pulizia repo (rimosso residuo Netlify, `.gitignore` aggiornato)
- Rimosso il gate con password: il sito è pubblico
- Immagine profilo Instagram: monogramma "S + piuma" estratto dal logo vettoriale (S e piuma ricomposte vicine, piuma leggermente più alta), sfondo `--paper`, margine per il ritaglio circolare — salvata in `archivio/instagram-avatar.png` (gitignored, asset locale)
- Pulsante chiaro/scuro ingrandito a 44px (target di tocco) su mobile, riposizionato leggermente più vicino al bordo
- Filtri "umore" e "genere" resi facet indipendenti: selezionarne uno azzera l'altro, così non capita più di restare bloccati su una combinazione (es. Coraggio + Fantasy) senza risultati. Su mobile il blocco Genere è ora un riquadro visivamente distinto (sfondo, bordo, pulsanti a pillola) invece di sembrare la prosecuzione dei filtri Umore
- Più respiro su mobile tra barra di ricerca, filtri e contenuto delle card (citazione/citazione bibliografica/contesto)
- Barra di ricerca con suggerimenti anticipatori: mentre si scrive, mostra fino a 7 corrispondenze tra autori e opere (etichettate), navigabili con le frecce e selezionabili con Invio/clic — chiude alla selezione o su Esc/blur
- Pulsante "×" per cancellare la ricerca: sostituisce l'icona nativa del browser (incoerente tra Safari/Chrome/Firefox) con un pulsante custom, sempre presente e ben visibile anche su mobile
- Logo e barra di ricerca restano visibili durante lo scroll: `.search-bar` è `position: sticky` con sfondo pieno, con un mini-logo che compare solo una volta "attaccata" in alto, rilevato via `IntersectionObserver` su un sentinel invisibile appena sopra la barra (classe `.is-stuck`, aggiunta/rimossa via JS). Lo z-index della barra sticky è tenuto sotto quello del pulsante tema (15 contro 20) apposta: su schermi stretti il pulsante tema si trova all'interno della fascia orizzontale della barra sticky, e con uno z-index più alto la barra lo avrebbe coperto — verificato misurando i bounding rect, non solo a occhio. Il mini-logo è `mark-quill.png` (256×256, S + piuma ritagliate strette dallo stesso monogramma usato per l'avatar Instagram), non la "S" sola del favicon — sostituito su richiesta esplicita perché giudicato più iconico
- Barra di ricerca spostata subito sotto il logo, sopra la citazione in evidenza — richiesto esplicitamente per vedere "tutto a primo colpo". Ha richiesto di eliminare il layout a due colonne `.top-row` (logo a sinistra, citazione a destra): un elemento `position: sticky` non può restare agganciato oltre i confini del proprio contenitore diretto, e `.top-row` finiva subito dopo la citazione — tenendoci la barra dentro, lo sticky si sarebbe "staccato" scendendo nella griglia sottostante. Ora logo, barra e citazione sono impilati verticalmente su tutte le larghezze, non solo su mobile
- Pagina dedicata per ogni citazione (`citazioni/<slug>.html`, 256 pagine), generate da `tools/generate_quote_pages.py` a partire da `index.html` — ognuna con URL proprio, meta description, canonical, Open Graph/Twitter card. Ogni card sull'index ha un link "Link" verso la sua pagina. Aggiunto atterraggio via hash (`index.html#slug`) che azzera i filtri e scorre/evidenzia la citazione. **Bug trovato e corretto**: usava `requestAnimationFrame`, che i browser sospendono sui tab in background — se un link viene aperto in una scheda non subito in primo piano (tasto centrale, nuova scheda), lo scroll non partiva mai. Sostituito con chiamata diretta a `scrollIntoView`, più un fallback che aspetta l'evento `visibilitychange` se la pagina risulta `document.hidden` al caricamento, così l'atterraggio funziona comunque appena l'utente apre la scheda. Non verificabile visivamente in questa sessione perché lo strumento di test del browser riporta sempre `document.hidden: true` sulle proprie schede — verificato invece a livello di codice (calcolo slug corretto, card trovata correttamente, `scrollIntoView` funziona quando chiamato fuori dal blocco condizionale)
- **Audit SEO del 2026-08-27 chiuso quasi per intero, in autonomia** (dettagli tecnici per chi riprende il lavoro):
  - `robots.txt` con riferimento a `sitemap.xml`
  - `og-banner.png` (1200×630, logo + tagline su sfondo `--paper`) sostituisce il placeholder quadrato ovunque come immagine OG/Twitter condivisa
  - Meta description, canonical, Open Graph/Twitter card aggiunti a `index.html` e `metodo.html` (prima assenti); `theme-color` aggiunto ovunque
  - Alt text reale (`Copertina di "titolo" di autore`) su tutte le 213 copertine, sia in `index.html` che nelle pagine citazione
  - **Pagine hub per tema/genere/autore** — il pezzo più grande: `temi/<categoria>.html` (7), `generi/<genere>.html` (5), `autori/<autore>.html` (193), generate da `tools/generate_hub_pages.py`. Ogni citazione linka le sue hub di tema/genere/autore (`.tags` in fondo alla pagina); i pulsanti filtro umore/genere sull'index sono ora `<a>` reali verso le hub corrispondenti (non solo `<button>` JS), con `e.preventDefault()` nel click handler per mantenere il filtro SPA lato client — i crawler li seguono, gli utenti restano nella SPA
  - Dati strutturati JSON-LD (`Quotation` + `BreadcrumbList`) su ogni pagina citazione
  - Citazioni correlate dello stesso autore in fondo a ogni pagina citazione (fino a 5)
  - `404.html` personalizzato, in stile col resto del sito, con `<meta name="robots" content="noindex">`
  - **`tools/build.py` è ora l'unico entry point da lanciare dopo aver modificato `index.html`**: orchestra `generate_quote_pages.py` + `generate_hub_pages.py` e scrive la sitemap unificata (463 URL). Le etichette di categoria/genere condivise vivono in `tools/labels.py`
  - Non fatto/rimandato: sottomissione della sitemap a Google Search Console (serve l'account dell'utente)
- **Fase 3 chiusa (2026-08-28): fonte verificabile su 232/256 citazioni (90%)** — edizione, locus
  (capitolo/parte/atto/verso), traduttore e link a Wikisource dove esiste, in 34 lotti lavorati in
  autonomia (dettagli per lotto in `LOG.md`). Tre attribuzioni sbagliate già pubblicate trovate e
  corrette durante la verifica, non solo segnalate (Ishiguro, Munro, Murgia), ognuna con redirect
  301 dal vecchio slug. Chiusa su istruzione esplicita dell'utente lasciando aperti, senza
  bloccare: quattro dubbi di attribuzione con evidenza più debole (Weil, Barrie, Maalouf, Collins)
  e 24 citazioni senza un riferimento strutturale verificabile con certezza — limite onesto della
  ricerca web per quei casi specifici, non lavoro interrotto a metà.
- **Fase 4 chiusa (2026-08-28): 40 pagine opera in `/opere/`** — 9 con ≥2 citazioni oggettive in
  archivio (incluso Il Signore degli Anelli, unificato dai 3 titoli-volume già presenti) + 31 del
  canone scolastico italiano con 1 sola citazione, elenco approvato dall'utente prima della
  generazione. Genere fantasy incluso su richiesta esplicita: degli altri titoli fantasy taggati
  solo Tolkien supera la soglia oggettiva, gli altri (inclusi i 3 libri di Harry Potter, opere
  realmente distinte) restano senza pagina dedicata per la regola "1 citazione = pagina citazione
  già pagina opera". Schede editoriali su fatti bibliografici incontrovertibili, senza
  edizione/traduttore forzati dove non verificabili con certezza. `Book` JSON-LD con `@id`
  condiviso tra le citazioni della stessa opera.
- **Fase 5 chiusa (2026-08-28): introduzioni editoriali + 5 raccolte curate.** Testi scritti a mano
  per i 7 temi (234-324 parole) e i 5 generi (104-178 parole), ognuno ancorato a citazioni reali
  dell'archivio (`data/hub_intros.json`); corretto anche un difetto grammaticale preesistente
  sull'H1 dei temi ("Citazioni su vita" → "Citazioni sulla vita"). 5 raccolte pubblicate in
  `/raccolte/` (Libri e scrittura, Il mare, La morte, Frasi brevi, Incipit memorabili), non le 6-8
  indicate in origine: due candidate (amicizia, frasi sul tempo che passa) scartate in curatela per
  non trovare ≥8 citazioni genuinamente pertinenti senza forzare il fit — stesso principio "meglio
  nessuna raccolta che una forzata" della Fase 3. Aggiunti anche gli indici `/opere/` e `/raccolte/`
  mancanti (il primo era stato dimenticato in Fase 4) e completato il gate di indicizzazione della
  Fase 2 (un hub sotto soglia ora entra comunque in sitemap se ha un'introduzione scritta a mano).
- **Schede autore completate per tutti i 193 autori (2026-08-28), Fase 6 in due lotti.** Lotto 1
  (43 autori con ≥2 citazioni, 72-97 parole) e lotto 2 (150 autori con 1 sola citazione, 55-104
  parole — più corte del target 80-120: per gli autori meno documentati non c'erano abbastanza
  fatti verificabili con certezza da aggiungere senza scivolare nel riempitivo, e la precisione ha
  avuto la priorità sulla lunghezza esatta). Effetto: **tutti i 522 URL del sito sono ora
  indicizzabili**, 0 pagine sotto soglia — il gate di indicizzazione della Fase 2/5 ha chiuso il
  cerchio. Gli altri tre punti di Fase 6 (Search Console, Bing/IndexNow, analytics) restano
  bloccati in attesa di azioni dirette dell'utente (account Google/Bing, privacy policy mai
  pubblicata) — non automatizzabili da qui.

### Da fare — SEO

**Riferimento:** `SEO.md` contiene l'audit completo del 2026-08-28 — perché si fa ognuna di
queste cose, i numeri su cui si basa, l'architettura target e i comandi pronti per l'agente.
`SEO-KEYWORDS.md` e `data/keywords.json` contengono la mappatura della domanda di ricerca
(Fase 7). `CATALOGO.md` contiene le regole di ampliamento del catalogo — perimetro, requisiti
d'ingresso di una citazione, attribuzione, diritti, equilibrio, piano dei lotti.
Qui sotto c'è il **lavoro operativo**: cosa toccare, in che ordine, e come si verifica
che sia fatto. Se le fonti divergono, `CLAUDE.md` ha la precedenza.

**Come si segna il progresso** (obbligatorio, vale la costituzione): si spunta `[x]` la voce
appena il suo controllo passa, si aggiorna la riga **Stato** qui sotto, e a fase chiusa si sposta
il riassunto della fase nella sezione "Fatto". I lotti di contenuto (fonti, schede, raccolte)
vanno anche in `LOG.md` con il formato in uso. Non spuntare mai una voce "quasi fatta".

**Stato: Fase 7 aperta il 2026-08-28 (mappatura keyword fatta; il secondo export con i semi
"frasi"/"aforismi" richiede l'utente). `CATALOGO.md` — Lotti 1 e 2 (amicizia, autori ad alta
domanda) fatti; **Lotto 3 (classici e filosofi per opera, 11 citazioni) e Lotto 4 (canone
scolastico poco coperto, 10 citazioni) fatti il 2026-08-28**, candidati del Lotto 3 mostrati e
approvati dall'utente, Lotto 4 e successivi in autonomia senza chiedere conferma a ogni
passaggio. **Lotto 5 (raccolte quasi pronte) parzialmente fatto il 2026-08-28**: pubblicate le
raccolte "Il cambiamento" (da citazioni già in archivio, nessuna nuova), "I sogni" e "La
tristezza" e "bellezza" (con nuove citazioni verificate). **Lotto 5 completo**: quattro raccolte
pubblicate (cambiamento, sogni, tristezza, bellezza). **Lotto 7 (contemporanei sotto copyright)
fatto il 2026-08-28**: Bukowski e Camilleri, 4 citazioni ciascuno, candidati mostrati e approvati
dall'utente; Sarah J. Maas e Leigh Bardugo scartati di nuovo, nessuna fonte con capitolo/pagina
verificabile. **Lotto 6 fatto il 2026-08-28** (8 citazioni): guerra (Remarque, Hemingway), animali
(Jack London), musica (Nietzsche), natura (Emerson), pace (Kant), lavoro (Primo Levi),
infanzia (Proust). Restano aperti solo montagna e figli, nessun candidato solido trovato con
lo stesso rigore — da riprendere in un lotto futuro. **Approfondimento avviato il 2026-08-28**
(punto 5 di CATALOGO.md, portare autori da 1 a 3 citazioni): 24 autori finora portati da 1 a 2
citazioni (Cervantes, Machiavelli, Austen, Boccaccio, Charlotte Brontë, Balzac, Voltaire,
Stevenson, Collodi, Omero, Pascoli, Sant'Agostino, Cicerone, Conrad, Stoker, George Eliot,
Allende, Buzzati, Fenoglio, Vittorini, Carlo Levi, Ammaniti, Blixen, Veronesi, Hurston, Canetti,
Szymborska, Heaney, Ondaatje, Zadie Smith, Coates, Atwood, Marilynne Robinson, Günter Grass,
Frank Herbert, Ray Bradbury, Tabucchi, Erri De Luca, Moravia, Silone, McEwan, Hosseini, Amado,
Aldous Huxley, Naguib Mahfouz, Arthur Conan Doyle, Emily Brontë, Charles Baudelaire, Francesco
Petrarca, Boezio, Gustave Flaubert, Mark Twain, Jules Verne, Thomas Hardy, Stendhal, Rainer
Maria Rilke, Arthur Schopenhauer, Epitteto, Jack London, Kurt Vonnegut, Pier Paolo Pasolini,
F. Scott Fitzgerald, Sylvia Plath, Virgilio, Fernando Pessoa, Boris Pasternak, Stefan Zweig,
Vittorio Alfieri, Marguerite Yourcenar, Giuseppe Tomasi di Lampedusa, Nikolaj Gogol', J.D.
Salinger, Carlo Goldoni, Anton Čechov, Ippolito Nievo, Umberto Saba, Daphne du Maurier,
Giorgio Bassani, Anna Maria Ortese, Salvatore Quasimodo, Erich Maria Remarque, Louisa May
Alcott, Lucy Maud Montgomery, Harper Lee, Sibilla Aleramo, Simone Weil, Goliarda Sapienza,
Michael Ende, Neil Gaiman, Paulo Coelho, Dacia Maraini, Mary Shelley, C.S. Lewis, Federico
García Lorca, Terry Pratchett, Philip Roth, Don DeLillo, Joan Didion, Alba de Céspedes,
Arundhati Roy, Suzanne Collins, Ursula K. Le Guin, Anne Frank, Doris Lessing, Curzio Malaparte,
Paolo Cognetti, Immanuel Kant, Michela Murgia, Leonardo Sciascia, Mario Vargas Llosa, H.G.
Wells, Truman Capote, Saul Bellow, William Golding, J.M. Coetzee);
ne restano 35 con una sola. **Bacino di candidati facilmente reperibili esaurito il
2026-08-29**: la maggior parte degli autori rimasti con una sola citazione non ha alcuna
sezione Citazioni utilizzabile su Wikiquote (solo incipit, o nessun numero di pagina/locus
verificabile). **Pivot a nuovi autori il 2026-08-29** (istruzione permanente già data:
"una volta completata anche quella, aggiungine di nuove"): archivio passato da 220 a 232
autori con l'aggiunta di E.M. Forster, T.S. Eliot, Agatha Christie, Rabindranath Tagore,
Bertolt Brecht, Iris Murdoch, Knut Hamsun, Anaïs Nin, Edith Wharton, Guy de Maupassant,
Nathaniel Hawthorne, Henry James, D.H. Lawrence, George Bernard Shaw, Henrik Ibsen, Alfred
Tennyson (ciascuno con una citazione, quindi sotto soglia di indicizzazione). Archivio a
236 autori, 463 citazioni. **Alternanza nuovi autori/approfondimento avviata**
(CATALOGO.md: "approfondire vale più che allargare"): E.M. Forster, Viktor E. Frankl, Guy
de Maupassant, Nathaniel Hawthorne portati da 1 a 2 citazioni; poi due nuovi autori,
Pearl S. Buck e Sinclair Lewis. Poi approfondimento: Agatha Christie (Dieci piccoli
indiani → +La sagra del delitto) e Bertolt Brecht (Madre Courage e i suoi figli →
+L'opera da tre soldi) portati da 1 a 2 citazioni. Poi due nuovi autori: Émile
Zola e Hans Christian Andersen. Poi approfondimento: Isaac Asimov e James Baldwin
portati da 1 a 2 citazioni. Poi due nuovi autori: Roald Dahl e Clarice Lispector. Poi un lotto misto: Douglas Adams (approfondimento,
1 a 2 citazioni) e Astrid Lindgren (nuovo autore). Poi approfondimento: Salman
Rushdie e Chimamanda Ngozi Adichie portati da 1 a 2 citazioni. Poi due nuovi
autori: Hannah Arendt e Anna Achmatova. Poi approfondimento: Roberto Bolaño e
Olga Tokarczuk portati da 1 a 2 citazioni. Poi due nuovi autori: Susan Sontag e
Wole Soyinka. Poi approfondimento: Amos Oz e Herta Müller portati da 1 a 2
citazioni. Poi due nuovi autori: Michel Houellebecq e Zbigniew Herbert. Poi
approfondimento: Chinua Achebe e Marguerite Duras portati da 1 a 2 citazioni.
Poi due nuovi autori: Maya Angelou e Audre Lorde. Poi approfondimento: Iris
Murdoch e Knut Hamsun portati da 1 a 2 citazioni. **Correzione di rotta del
2026-08-30 (CATALOGO.md §7, decisa da una sessione concorrente): stop agli
autori nuovi, si portano a 4 citazioni gli autori già in archivio con più
domanda di ricerca (`data/keywords.json`), precedenza alle opere anteriori al
Novecento.** Primo lotto sotto la nuova regola: Dante Alighieri, Victor Hugo,
Voltaire, Niccolò Machiavelli, Mark Twain, Jane Austen portati a **4 citazioni
ciascuno**. Corretto anche l'errore aperto sul Piccolo Principe (due citazioni
con lo stesso locus "capitolo XXI", ora distinte con la pagina). Secondo lotto:
Gabriele D'Annunzio, Cesare Pavese, Luigi Pirandello, Alda Merini, Primo Levi,
Pier Paolo Pasolini portati anch'essi a **4 citazioni ciascuno**. Terzo lotto:
Marco Aurelio, Virginia Woolf, Hermann Hesse, Pablo Neruda, Toni Morrison,
Michela Murgia, Paulo Coelho portati anch'essi a **4 citazioni ciascuno**.
Quarto lotto: Ernest Hemingway, Charles Baudelaire, Fernando Pessoa, Anne
Frank, Umberto Eco, Lev Tolstoj portati anch'essi a **4 citazioni ciascuno**.
Quinto lotto: Haruki Murakami, George Orwell, Emily Dickinson, Khalil Gibran,
Jean-Paul Sartre, Jorge Luis Borges portati anch'essi a **4 citazioni
ciascuno**. Sesto lotto: Giuseppe Ungaretti, Edgar Allan Poe, Marcel Proust,
David Foster Wallace, Ugo Foscolo, Francesco Petrarca portati anch'essi a
**4 citazioni ciascuno**. Settimo lotto: Douglas Adams, Erri De Luca, José
Saramago, Italo Svevo, Simone de Beauvoir portati anch'essi a **4 citazioni
ciascuno**. Ottavo lotto: Zadie Smith, Walt Whitman, Giovanni Verga, Isabel
Allende, Gustave Flaubert portati anch'essi a **4 citazioni ciascuno**.
Nono lotto: Alessandro Manzoni, Antoine de Saint-Exupéry, Giovanni Pascoli,
Virgilio, Rainer Maria Rilke, Leonardo Sciascia portati anch'essi a **4
citazioni ciascuno**. Decimo lotto: Jack Kerouac (da 1 a 4), Isaac Asimov,
Elsa Morante, Grazia Deledda, Philip Roth portati a **4 citazioni ciascuno**.
Undicesimo lotto: Milan Kundera, Alberto Moravia, Sibilla Aleramo, Sylvia
Plath, Simone Weil portati anch'essi a **4 citazioni ciascuno**. Archivio a
251 autori, 611 citazioni, 46 con una sola citazione, 78 con tre o più.
Lavoro da proseguire senza chiedere conferma, seguendo la nuova regola:
nessun autore nuovo, si chiude a 4 chi ha più domanda di ricerca
citazioni una volta esaurito, **anche per ore senza il controllo dell'utente** (istruzione del
2026-08-28). Script di inserimento aggiornato: rifiuta citazioni con `source_locus` vuoto o
"non indicato" — **ma "incipit" (o una descrizione equivalente della posizione, es. "inciso
nell'armadio della protagonista") è un locus valido di per sé**, non serve un numero di pagina
per l'apertura di un libro: non scartare candidati-incipit solo per mancanza di pagina. **Bug
corretto il 2026-08-29 in `tools/build.py`** (non introdotto da questa sessione, probabile
sessione concorrente): `gh.main()` girava prima che gli slug delle citazioni nuove fossero
salvati su `slugs.json`, quindi la build falliva sempre dopo ogni lotto — vedi LOG.md. Archivio
a 467 citazioni, 238
autori. **Deploy sospeso su richiesta
dell'utente**:
lavoro salvato in commit locali, nessun push fino a nuova indicazione — verificare `git log
origin/main..HEAD` prima di assumere che il sito pubblicato rifletta lo stato del repo.
Fase 0, Fase 1, Fase 2, Fase 3, Fase 4 e Fase 5 completate e live su sottolineature.it
(deploy Vercel confermato il 2026-08-28). Fase 6: schede autore fatte per tutti gli autori in
archivio, tutti gli URL del sito indicizzabili (0 sotto soglia — il numero esatto cresce con
l'archivio, verificarlo nel rapporto di `build.py`); il resto della fase (Search Console,
Bing/IndexNow, analytics) è bloccato in attesa di azioni dell'utente — non automatizzabile da qui,
vedi sezione Fase 6. Terminato il lavoro di piattaforma, **la Fase 1 (aggiungere citazioni) resta
aperta senza un traguardo fisso**: lotti post-roadmap dal 2026-08-28, uno via l'altro senza
fermarsi a chiedere conferma (istruzione permanente, vedi memoria), dettagli e conteggio aggiornato
in `LOG.md`. Fase 3 chiusa: 232/256
citazioni con fonte (90%, locus e/o
edizione/traduttore verificati, 34 lotti committati e pushati il 2026-08-28, dettagli per lotto in
`LOG.md`). Le 24 rimaste sono state cercate almeno una volta (molte due) senza trovare un
riferimento strutturale verificabile con certezza — non un lavoro interrotto a metà, ma il limite
onesto di quanto è verificabile via ricerca web per queste citazioni specifiche; chiusa così su
istruzione esplicita dell'utente, si può riprendere in un lotto dedicato solo se richiesto
esplicitamente in futuro.

Fase 4 completata il 2026-08-28: 40 pagine opera in `/opere/`, elenco approvato dall'utente prima
della generazione (canone scolastico + genere fantasy su richiesta esplicita). Dettagli nella
sezione Fase 4 qui sotto.

Fase 5 completata il 2026-08-28, su istruzione "Vai": introduzioni editoriali per i 7 temi e i 5
generi, 5 raccolte curate pubblicate (`/raccolte/`, non 6-8 come da indicazione iniziale — due
candidate scartate per mancanza di ≥8 citazioni genuinamente pertinenti, stesso principio di
rigore della Fase 3). Dettagli nella sezione Fase 5 qui sotto.

Fase 6, schede autore completate il 2026-08-28 in due lotti su istruzione "vai": lotto 1 (43
autori con ≥2 citazioni) e lotto 2 (i restanti 150 con 1 sola citazione), che hanno portato gli
autori indicizzabili da 13 a 193/193 — l'intero sito, 522 URL, è ora indicizzabile senza eccezioni.
Gli altri tre punti della fase (Search Console, Bing/IndexNow, analytics) restano bloccati: servono
rispettivamente l'account Google dell'utente, l'account Bing dell'utente, e la privacy policy del
sito (mai pubblicata, servono i dati del titolare) — nessuno dei tre è qualcosa che si possa fare
in autonomia da qui. Dettagli nella sezione Fase 6 qui sotto.

Nuovi lotti di citazioni post-roadmap, iniziati il 2026-08-28 su richiesta esplicita "aggiungi
nuove citazioni... dando priorità alla correttezza" e proseguiti in autonomia, un lotto via
l'altro, su istruzione "Continua ogni volta che finisci un lotto" (**vedi anche la memoria
permanente** `feedback_sottolineature_lotti_autonomi.md`: non fermarsi a chiedere il via libera tra
un lotto e l'altro, restando comunque fermo tutto il resto del rigore di verifica). Ogni lotto:
autori mai presenti in archivio, fonti verificate nell'ordine Wikisource > Wikiquote con
riferimento esplicito a capitolo/edizione > due fonti indipendenti concordanti, scheda autore
scritta per ogni nuovo nome così tutto l'archivio resta indicizzabile, scarti sempre motivati.
**Dettagli di ogni lotto — chi è stato aggiunto, chi scartato e perché, quali covertine sostituite
per mismatch di lingua o edizione — sono in `LOG.md`, una voce per lotto**: qui in CLAUDE.md non si
tiene più il dettaglio lotto per lotto, solo lo stato aggregato. Lotto 1: Omero, Virgilio, Marco
Aurelio, William Golding, Ralph Waldo Emerson, Olga Tokarczuk. Lotto 2: Nikolaj Gogol', Dacia
Maraini, Niccolò Ammaniti, George Eliot, Ralph Ellison — in quest'ultimo corretto anche un difetto
di `generate_quote_pages.py` (il link alla fonte diceva sempre "Testo su Wikisource" anche quando
la fonte era Wikiquote).

Tre correzioni di attribuzione fatte durante la verifica (non solo trovate, anche corrette e
pubblicate): Kazuo Ishiguro ("Quando eravamo orfani" → "Non lasciarmi"), Alice Munro ("La vista da
Castle Rock" → "Nemico, amico, amante..."), Michela Murgia ("Accabadora" → "Chirù") — ognuna con
redirect 301 dal vecchio URL, verificata su due ricerche indipendenti prima di correggere.

Quattro dubbi ancora aperti, segnalati in `LOG.md` con la ragione ma **non corretti** (evidenza
più debole delle tre correzioni sopra, serve una verifica diretta sul testo prima di agire):
Simone Weil ("L'ombra e la grazia" — potrebbe essere una lettera del 1942, non il libro), J.M.
Barrie ("Solo chi sogna può volare" — potrebbe essere del film Disney, non del romanzo), Amin
Maalouf ("In fondo all'Atlantico c'è un libro" — potrebbe appartenere a "Il periplo di
Baldassarre"), Suzanne Collins ("Che i giochi abbiano inizio" — la fonte trovata è del film, non
confermata nel romanzo).

Prossimo passo: il lavoro automatizzabile della roadmap SEO è esaurito, quindi la Fase 1
(aggiungere citazioni, senza un traguardo fisso) resta il lavoro di fondo di default — si continua
lotto dopo lotto in autonomia (istruzione permanente dell'utente, 2026-08-28), senza fermarsi a
chiedere il via libera tra un lotto e l'altro. Se richiesto esplicitamente: risolvere i quattro
dubbi aperti di Fase 3, ritentare le 24
citazioni storiche rimaste con fonti diverse da quelle già cercate, ampliare le raccolte quando
l'archivio crescerà abbastanza da sostenere le candidate scartate (amicizia, tempo che passa) o
nuove, oppure — quando l'utente vorrà occuparsene di persona — Search Console, Bing Webmaster Tools
e privacy policy, i tre punti di Fase 6 bloccati in attesa sua.**

Fase 0 chiusa il 2026-08-28: `vercel.json` (cleanUrls, trailingSlash, redirect host www/vercel.app,
cache su `/assets/`), `tools/slugs.json` congela i 256 slug citazione + 193 slug autore esistenti
(i generatori ora li leggono, non li ricalcolano), `tools/redirects.json` pronto per i 301 futuri,
`assets/site.css` estrae il CSS comune dai 463 file generati, link interni puliti ovunque
(generatori + index.html/metodo.html/404.html scritti a mano), navigazione di sito in testa a ogni
pagina generata (solo Citazioni · Metodo per ora: niente link a /temi/ /generi/ /autori/, quelle
pagine indice sono della Fase 2 e linkarle prima avrebbe creato link morti), preconnect +
width/height sulle copertine delle pagine citazione. Verificato con un crawl locale su 6330 link
interni (zero rotti) e controllo visivo chiaro/scuro/mobile su 5 pagine campione. Dettagli completi
del comando eseguito in `SEO.md` §9.1.

Fase 1 chiusa il 2026-08-28 (dettagli e scostamenti dal testo originale nella sezione qui sotto):
H1 = testo della citazione su tutte le 256 pagine, struttura `<figure><blockquote><figcaption>`,
`<title>` distintivo con incipit (0 duplicati, verificato da `build.py`), briciola di pane visibile
a 3 livelli (non 4: le pagine `/autori/` e `/opere/` non esistono ancora), JSON-LD `@graph` con
`@id` collegati (senza `sameAs`, mai verificato manualmente), `fetchpriority="high"` sulla copertina
LCP, 256 immagini OG 1200×630 generate con Pillow (non Playwright) via il nuovo
`tools/generate_og_images.py` integrato in `build.py`, correlate arricchite con sezione "stesso
tema" oltre a "stesso autore". `build.py` ora fallisce il build se manca un H1, un title è duplicato
o un'immagine OG non è stata generata. Non ancora fatto: test dei risultati strutturati di Google e
misura reale di LCP (nessun ambiente di misura disponibile in locale).

**Decisioni già prese con l'utente il 2026-08-28, da non rimettere in discussione:**
teaser in home con il contesto esclusivo della pagina citazione; migrazione a URL puliti con 301;
investimento editoriale su tutti e quattro i fronti (fonte verificabile, pagine opera, raccolte,
schede autore). Le tre alternative scartate sono elencate in `SEO.md`.

**Diagnosi in tre righe:** 463 URL per 256 citazioni, con ogni frase e il suo contesto replicati su
4-5 pagine; la home da 313 KB contiene l'intero archivio ed è quindi un superset di ogni pagina
figlia; le 256 pagine citazione non hanno `<h1>`. 150 autori su 193 hanno una sola citazione,
242 opere su 249 idem, solo 13 autori arrivano a 3 citazioni.

---

#### Fase 0 — Fondamenta tecniche (nessun contenuto nuovo, tutto automatizzabile)

- [ ] **`vercel.json`** alla radice con `"cleanUrls": true`, `"trailingSlash": true`, array
      `redirects` (vuoto all'inizio, lo riempie `build.py`) e header `Cache-Control:
      public, max-age=31536000, immutable` su `/assets/(.*)`.
      Nota: `cleanUrls` + `trailingSlash` servono `citazioni/foo.html` su `/citazioni/foo/` e
      rimandano i vecchi indirizzi con un 308 permanente **senza rinominare nessun file** — la
      migrazione tocca solo i link interni, non la struttura del repo.
- [ ] **Host canonico:** 301 da `www` all'apice e da `sottolineature.vercel.app` a
      `sottolineature.it`. Se il redirect fra domini non è praticabile, minimo accettabile
      `X-Robots-Tag: noindex` sul dominio `.vercel.app`. Oggi il sito esiste per intero su due host.
- [ ] **Link interni** — da correggere **nei generatori in `tools/`, mai a mano sui file generati**:
      `../index.html` → `/` (sono 512 occorrenze), `index.html#slug` → `/#slug`,
      `metodo.html` → `/metodo/`, `../autori/x.html` → `/autori/x/`, e così per temi e generi.
- [ ] **`tools/slugs.json`** — generarlo **una volta sola** dallo stato attuale, congelando gli
      slug esistenti così come sono, **inclusi i 7 con suffisso `-2`**. Chiave:
      `autore|titolo|prime 6 parole della frase`. Da qui in avanti gli slug si **leggono**, non si
      ricalcolano: oggi il suffisso numerico dipende dall'ordine delle card in `index.html`, quindi
      togliendo una citazione la successiva cambierebbe URL in silenzio.
      Per le citazioni nuove su un'opera già presente lo schema è
      `<autore>-<titolo>-<3 parole significative dell'incipit>`, mai un numero.
      **Non rinominare gli slug esistenti**: il beneficio è estetico, il rischio è reale.
- [ ] **`tools/redirects.json`** — ogni cambio di slug ci scrive dentro un 301 e `build.py` lo
      riversa in `vercel.json`. Uno slug non si cancella mai.
- [ ] **`/assets/site.css`** — estrarre il blocco `:root`/card/tema oggi ripetuto inline in 463
      file (~7 KB ciascuno). `index.html` può tenere il suo inline, è l'unica pagina che ci guadagna.
- [ ] **Navigazione di sito** in testa a ogni pagina generata: *Citazioni · Temi · Generi ·
      Autori · Metodo*. Oggi le pagine interne sono cul-de-sac con un solo link di ritorno.
- [ ] **Copertine:** `<link rel="preconnect" href="https://covers.openlibrary.org">` su tutte le
      pagine con copertine, e `width`/`height` espliciti su ogni `<img class="card-cover">`
      (oggi mancano: spostamento del layout garantito).

**Controllo di accettazione:** `/citazioni/george-orwell-1984/` risponde 200 e
`/citazioni/george-orwell-1984.html` risponde 308 verso di essa; `grep -r "index.html"` sui file
generati torna a zero; la sitemap contiene solo URL puliti; un crawl locale
(`python3 -m http.server` + script che segue tutti gli href) non trova nessun link rotto.

#### Fase 1 — Da frammento a documento: le 256 pagine citazione

Tutto dentro `tools/generate_quote_pages.py`.

- [x] **`<h1>` = il testo della citazione.** È il difetto tecnico più grave del sito, ripetuto 256
      volte: oggi la frase sta in un `<p class="card-quote">` e la pagina non ha nessun H1.
      Se la frase supera i 200 caratteri: H1 = incipit troncato a parola intera + `…`, testo
      integrale sotto.
- [x] **Semantica della citazione:**
      `<figure><blockquote><p>…</p></blockquote><figcaption>— <a>Autore</a>, <cite>Titolo</cite>
      · anno</figcaption></figure>`.
- [x] **`<title>` distintivo:** `«{incipit ~45 caratteri}…» — {Autore}, {Opera}`.
      Oggi le due citazioni dalla stessa opera hanno title identici
      (`George Orwell — 1984 | Sottolineature` per entrambe).
- [x] **`<meta description>`** senza duplicati: frase completa se breve, altrimenti frase troncata
      + prima riga di contesto.
- [x] **Briciola di pane visibile** — implementata come `Sottolineature › {Autore} ›
      {incipit troncato}`, **senza** i livelli "Autori" e "Opera" previsti dalla spec originale:
      `/autori/` (hub) è Fase 2 e `/opere/<slug>/` è Fase 4, nessuna delle due esiste ancora oggi.
      Linkarle prima avrebbe creato link morti — stessa regola già applicata al site-nav in Fase 0.
      Da estendere a 4 livelli quando quelle pagine esisteranno.
- [x] **JSON-LD in `@graph`** con `@id` collegati, al posto dei due oggetti scollegati attuali:
      `WebPage` → `Quotation` (`isPartOf` verso il `Book`, `creator` verso la `Person`) → `Book`
      (`name`, `author`, `datePublished`) → `Person` → `BreadcrumbList`.
      `sameAs` verso Wikipedia/Wikidata **non aggiunto**: nessun link è stato aperto e verificato
      persona-per-persona per i 193 autori, quindi si è preferito ometterlo piuttosto che rischiare
      un `sameAs` sbagliato. Da fare come lotto separato, con verifica manuale.
- [x] **Immagine LCP:** sulla pagina citazione la copertina è l'elemento LCP e oggi ha
      `loading="lazy"`. Tolto il lazy, aggiunto `fetchpriority="high"` e le dimensioni.
- [x] **Immagine social per citazione:** 256 PNG 1200×630 generati in `/assets/og/<slug>.png`,
      puntati da `og:image`/`twitter:image`. Riusa la stessa composizione (virgolette dorate,
      citazione in corsivo, autore, opera, url) del canvas di condivisione in `index.html`, ma
      **con Pillow invece di Playwright**: `tools/generate_og_images.py`, integrato in `build.py`
      (rigenera solo le immagini più vecchie di `data/citazioni.json`, fallisce il build se ne manca una).
      Scelta deliberata — stesso strumento già usato per `og-banner.png` in questo repo, zero
      dipendenze nuove da scaricare, stesso risultato visivo. Verificato a occhio sulla citazione
      più lunga del sito (485 caratteri) e su un caso breve, nessun overflow del frame.
- [x] **Correlate più ricche:** stesso autore e stesso tema, con sezioni separate ed etichettate
      (`Altre citazioni di {Autore}`, `Altre citazioni su {Tema}`). "Stessa opera" come terza
      categoria distinta non è stata aggiunta: 242 opere su 249 hanno una sola citazione in
      archivio, quindi in pratica coinciderebbe quasi sempre con "stesso autore" — nessun valore
      aggiunto per l'utente in questo dataset.

**Controllo di accettazione:** H1 presente su tutte e 256 (verificato via `build.py`, che ora fallisce
il build se manca); `build.py` non segnala title o description duplicati (0/0) né immagini OG mancanti;
verificato in browser su una pagina campione (Dante) in chiaro/scuro/mobile, console pulita, JSON-LD
valido (`JSON.parse` sul blocco `ld+json`). Non ancora fatto: validazione con il test dei risultati
strutturati di Google su 5 pagine campione e misura di LCP reale sotto i 2,5 s (richiede un ambiente
di misura che non ho qui in locale).

#### Fase 2 — De-duplicazione e gate di indicizzazione

- [x] **Togliere `card-context` dall'HTML pubblicato** di home, hub tema/genere/autore e correlate.
      Il contesto resta esclusivo di `/citazioni/<slug>/`. Gli hub e le correlate non l'hanno mai
      pubblicato (verificato via grep su `generate_hub_pages.py`/`generate_quote_pages.py` prima di
      partire); l'unico punto reale era la home, che mostrava tutti i 256 contesti in linea.
      **Nodo architetturale, risolto il 2026-08-28 con ok esplicito dell'utente:** `index.html` era
      sia la fonte scritta a mano sia il file servito su `/`, quindi non si poteva escludere il
      contesto dall'output senza toccare la fonte. Scelta fatta: **refactor dati completo**. Le 256
      citazioni sono ora in `data/citazioni.json` (fonte di verità, un oggetto per citazione,
      ordine di visualizzazione preservato), `templates/home_template.html` porta la parte fissa
      (header/filtri/script/footer) e `tools/generate_home.py` genera `index.html` a ogni build —
      esattamente come già succedeva per `citazioni/`, `temi/`, `generi/`, `autori/`. Nuovo flusso
      di lavoro per le citazioni: si edita `data/citazioni.json`, non più `index.html` a mano.
      Verificato: diff byte-per-byte prima/dopo su tutte le pagine generate (citazioni, hub, OG) —
      zero differenze, il refactor è a costo zero per tutto ciò che non è la home; su `index.html`
      il diff mostra solo la rimozione del contesto e l'encoding delle virgolette (`'` → `&#x27;`,
      innocuo, già lo standard usato da `generate_quote_pages.py`). Corretti anche due contatori
      statici disallineati trovati per errore durante il refactor (footer "253" e paragrafo
      introduttivo "Duecentocinquantatré", entrambi fermi a un conteggio vecchio): ora calcolati
      dinamicamente da `len(quotes)`, incluso un numero-in-lettere italiano generato da
      `italian_number_words()` in `generate_home.py`. Verificato in browser chiaro/scuro/mobile,
      ricerca e filtri funzionanti (dipendono solo da quote/autore/titolo, mai dal contesto).
- [x] **Gate di indicizzazione in `build.py`:** un hub (tema/genere/autore) è indicizzabile solo se
      ha **≥ 3 citazioni** (soglia scelta, in `MIN_INDEXABLE_QUOTES` in `generate_hub_pages.py`;
      la seconda condizione — ≥ 80 parole di testo editoriale — non si applica ancora a nessun hub,
      nessuno ha ancora un'introduzione scritta a mano, è un aggancio per la Fase 5/6). Sotto soglia:
      `<meta name="robots" content="noindex,follow">` in testa e fuori da `sitemap.xml`, ma il file
      resta generato e linkato (percorso di scansione). Risultato reale dopo il build: **13/193
      pagine autore indicizzabili, 180 in noindex** — esattamente l'effetto previsto in questo
      documento prima di partire. Temi (7/7) e generi (5/5) restano tutti indicizzabili, hanno
      sempre più di 3 citazioni.
- [x] **`<lastmod>` in sitemap** — campo `added` (`YYYY-MM-DD` o `null`) in `data/citazioni.json`,
      ricostruito da `LOG.md` con un matching a doppia chiave (autore **e** titolo devono comparire
      insieme, non uno dei due) contro le righe `— added N quotes (total now T) — aggiunte citazioni
      di ...`; le righe "aggiunto contesto retroattivo" o "recupero copertine" non contano come
      aggiunta. Risultato: **155/256 citazioni datate con certezza**, le altre 101 restano senza
      data (nessuna inventata) — sono per lo più il nucleo iniziale del sito, aggiunto prima che
      `LOG.md` tracciasse ogni lotto in modo identificabile riga per riga. Un conflitto vero trovato
      e risolto durante lo sviluppo: uno script di prima versione assegnava a Toni Morrison (Sula)
      la data 2026-08-18 (recupero copertine) invece di 2026-08-17 (aggiunta reale) perché il
      troncamento del testo del lotto si fermava alla parola sbagliata — corretto troncando sempre
      al primo punto e virgola della riga, che separa in modo affidabile "aggiunte" da tutto il
      resto in ogni riga di `LOG.md`.
- [x] **`/feed.xml`** — `tools/generate_feed.py`, le 20 citazioni con `added` più recente (fra le
      155 datate), linkato dalla home con `<link rel="alternate" type="application/rss+xml">`.
- [x] **JSON-LD `WebSite` + `SearchAction`** sulla home con `/?q={search_term_string}` (statico in
      `templates/home_template.html`, non cambia a ogni build), e il JS della home legge `?q=` al
      caricamento, precompila `searchInput` e chiama `applyFilters()` — verificato in browser su
      `/?q=Camus`: filtra correttamente alle 4 citazioni di Albert Camus.
- [x] **`ItemList`/`CollectionPage`** su ogni hub tema/genere/autore (`generate_hub_pages.py`) e su
      ognuna delle nuove pagine indice (sotto), con gli elementi in ordine e `@id` verso il
      `WebSite` della home. Validato: `JSON.parse` su tutti i blocchi `ld+json` generati.
- [x] **Pagine indice mancanti**, prima vicoli ciechi — `tools/generate_index_pages.py`:
      `/citazioni/` paginato 30 per pagina (9 pagine per 256 citazioni), ognuna self-canonical con
      `rel="prev"`/`rel="next"`; `/autori/` A-Z con conteggio per autore (elenca anche i 180 autori
      la cui pagina singola è in noindex — resta il percorso per raggiungerli); `/temi/`, `/generi/`
      con conteggio per hub. Tutte e quattro sempre indicizzabili (sono indici di navigazione, non
      soggetti al gate sopra). Verificato con un crawl locale su 734 link interni unici (zero rotti)
      e controllo visivo su `/citazioni/`, `/autori/`.
- [x] **Rapporto di fine build** in `build.py`: URL totali generati vs URL indicizzabili (con la
      differenza spiegata: hub sotto soglia), title duplicati, description duplicate, pagine senza
      H1, citazioni con data nota, citazioni con blocco fonte (0/256, Fase 3 non iniziata), immagini
      OG. **Il build fallisce** (`SystemExit(1)`) su title duplicato, H1 mancante o immagine OG
      mancante — invariato da Fase 1, esteso ma non indebolito.
      *Non implementato:* il conteggio "slug nuovi" e "301 aggiunti" del testo originale — il
      secondo è già coperto da "Redirect in vercel.json" nel rapporto esistente, il primo non
      sembrava aggiungere informazione utile oltre a quello che `slugs.json aggiornato` già stampa
      quando succede.

**Controllo di accettazione:** verificato — `grep -rl 'card-context'` sui file HTML pubblicati
restituisce solo i file in `citazioni/` (un risultato per citazione, mai su home/hub/correlate); il
rapporto di `build.py` mostra URL indicizzabili (295) < URL totali (475) con la differenza spiegata
(180 hub sotto soglia); la sitemap contiene solo i 295 URL indicizzabili.

#### Fase 3 — Fonte verificabile su ogni citazione *(il lavoro che vale di più)*

È l'unico contenuto che nessun aggregatore italiano ha, è quello che `metodo.html` già promette,
ed è la ragione per cui un motore di ricerca e un insegnante dovrebbero preferire questa pagina.

- [x] Blocco `<p class="card-source">` su ogni citazione: **edizione di riferimento,
      capitolo/parte/atto/verso, traduttore quando il testo è tradotto, collegamento a Wikisource
      o alla fonte primaria dove esiste.** Nel JSON-LD: `Quotation.citation`/`Quotation.sameAs`
      (verso il link esterno) e `Book.translator` (solo se noto) arricchiti. Implementato in
      `generate_quote_pages.py`, campi `source_edition`/`source_locus`/`source_translator`/
      `source_url` in `data/citazioni.json` (vuoti di default, mai un placeholder inventato).
- [x] Si lavora a **lotti di 15** (variabile secondo coerenza del lotto, come già per i contesti in
      `LOG.md`), con le regole di verifica già scritte più sopra in questo documento. **Se il
      riferimento non è stabilibile con certezza il campo resta vuoto** e lo scarto si annota con
      la ragione: su un sito che si presenta come verificato a mano, una fonte sbagliata è molto
      peggio di una fonte assente. **Chiusa il 2026-08-28 — 232/256 citazioni con fonte (90%), 34
      lotti chiusi e pushati** (dettagli per lotto in `LOG.md`). Lotto 1 (19
      citazioni): tutti i classici italiani di pubblico dominio con testo su Wikisource, trovate e
      corrette anche due discrepanze di wording rispetto alla fonte primaria (Boccaccio,
      Machiavelli) — la correttezza del testo viene prima della fonte che lo accompagna. Lotti 2-3:
      locus dedotto da contesto già verificato in lotti precedenti. Lotti 4-34: ricerca nuova via
      web, locus e/o edizione/traduttore solo quando verificabili con certezza. Durante la verifica
      sono emerse **tre attribuzioni sbagliate già pubblicate**, trovate e corrette (non solo
      segnalate): Ishiguro, Munro, Murgia — ognuna con redirect 301 dal vecchio slug, verificata su
      due ricerche indipendenti prima di correggere. **Quattro dubbi restano aperti**, segnalati in
      `LOG.md` ma non corretti perché l'evidenza è più debole (serve verifica diretta sul testo):
      Weil, Barrie, Maalouf, Collins (Hunger Games). Le **24 citazioni rimaste senza fonte** sono
      state cercate due o tre volte ciascuna, con angoli diversi, senza trovare un riferimento
      verificabile con certezza — limite onesto della ricerca web per questi casi specifici (spesso
      opere senza capitoli numerati, o citazioni troppo brevi/diffuse per essere ricondotte a un
      punto preciso del testo), non lavoro interrotto a metà. **Chiusa così su istruzione esplicita
      dell'utente** ("Chiudi la fase 3. Se ci sono dubbi procedi oltre", 2026-08-28): i quattro dubbi
      e le 24 citazioni senza fonte restano permanentemente aperti/segnalati, non bloccano la
      chiusura della fase, e non vanno ripresi se non su richiesta esplicita futura.
- [x] Ordine dei lotti: prima le opere di pubblico dominio con testo integrale su Wikisource
      (Dante, Manzoni, Leopardi, Verga, Pirandello, Shakespeare in traduzione), dove la verifica è
      rapida e il collegamento esterno è di qualità — fatto nel lotto 1.
- [x] Il blocco fonte va in `data/citazioni.json` (fonte di verità dalla Fase 2) e propagato dai
      generatori **solo** alla pagina citazione, mai agli hub. Dopo ogni lotto: `python3
      tools/build.py`, controllo che nessuna fonte sia finita per errore su due citazioni diverse
      (stessa trappola già vista con i contesti duplicati), riga in `LOG.md`, commit. Meccanismo
      implementato e verificato su 34 lotti, incluso il controllo duplicati (avviso non bloccante,
      vedi sopra) e la procedura di rinomina slug quando una correzione cambia titolo/testo.

#### Fase 4 — Livello opera (`/opere/<autore>-<titolo>/`)

È dove sta la domanda italiana reale: si cerca *"frasi 1984"*, *"citazioni promessi sposi"*, non
"citazioni sulla libertà di Orwell". Oggi quella domanda non ha una pagina su cui atterrare.

- [x] Costruite **40 pagine opera** (2026-08-28): 9 con ≥2 citazioni oggettive in archivio (incluso
      *Il Signore degli Anelli*, unificato in una sola opera dai 3 titoli-volume 33/237/238 già
      presenti — soddisfa da solo la soglia ≥2) + 31 titoli del canone scolastico italiano con
      1 sola citazione ciascuno (da Dante e Manzoni ai classici stranieri di liceo: Kafka, Orwell,
      Dostoevskij, Austen...). La clausola "canone scolastico" della regola è esplicitamente
      un'eccezione alla soglia ≥2, non ridondante con essa — coerente con l'esempio "frasi 1984"
      nel testo stesso di questa fase (*1984* ha 1 sola citazione).
      **Genere fantasy incluso su richiesta esplicita** ("aggiungi anche fantasy"): degli 12 titoli
      fantasy taggati in archivio, solo Il Signore degli Anelli supera la soglia ≥2 (unificato);
      gli altri (Narnia, Trono di Spade, i 3 libri di Harry Potter, Peter Pan, Coraline, Percy
      Jackson, Discworld) hanno 1 sola citazione ciascuno e **non** sono nel canone scolastico in
      senso stretto, quindi restano citazione=pagina opera senza pagina dedicata (vedi sotto) — non
      unificati forzatamente solo per raggiungere la soglia (es. i 3 libri di Harry Potter sono
      davvero 3 opere diverse, non varianti editoriali dello stesso libro come i volumi del
      Signore degli Anelli).
      Mai generate le altre ~210 opere rimanenti: solo l'elenco approvato, mai tutto l'archivio.
      Schema: `data/opere.json` (slug, autore, titolo, anno, `titles` per l'unione multi-volume,
      scheda editoriale di 3-5 righe). Scheda basata su fatti bibliografici pubblici e
      incontrovertibili (anno, genere, trama); **edizione/traduttore italiano lasciati vuoti per
      tutti i 40** — per classici tradotti più volte in italiano non esiste un'unica edizione
      "di riferimento" verificabile con certezza, e forzarne una sarebbe lo stesso errore che la
      Fase 3 ha imparato a evitare sulle fonti delle citazioni.
      Generatore: `tools/generate_opera_pages.py`, richiamato da `tools/build.py` **prima** di
      `generate_hub_pages.py`; `build_opera_map()` calcola la mappa (autore,titolo)→opera usata da
      `generate_quote_pages.py` per riusare lo stesso `Book` `@id` e aggiungere il link "Tutte le
      citazioni da «Opera» →" sulle pagine citazione corrispondenti.
- [x] Regola strutturale: **quando un'opera ha una sola citazione e non è nel canone scolastico
      approvato, la pagina citazione è già la pagina dell'opera** — non se ne crea una seconda.
- [x] H1: *"Frasi e citazioni da {Opera} di {Autore}"*. `Book` in JSON-LD con `@id` stabile
      (`/opere/<slug>/#book`), riusato da tutte le pagine citazione di quell'opera — verificato sui
      3 volumi del Signore degli Anelli, tutti puntano allo stesso `@id`.
- [x] Elenco delle 40 opere candidate mostrato e approvato dall'utente prima della generazione
      ("Procediamo" sul canone scolastico, poi "Aggiungi anche fantasy e procedi").

#### Fase 5 — Hub editoriali e raccolte

- [x] **Temi (7):** introduzione editoriale scritta a mano per ciascuno (234-324 parole, vicino ai
      300-600 target — niente riempitivo per arrivarci, meglio un testo denso e più corto che uno
      allungato senza contenuto), ogni essay ancorato a 4-6 citazioni realmente presenti nell'archivio
      (autore + opera citati per nome). Testi in `data/hub_intros.json`, iniettati da
      `generate_hub_pages.py` sopra le card. **Corretto anche un difetto grammaticale preesistente**
      nell'H1/title dei temi ("Citazioni su vita" → "Citazioni sulla vita", "Citazioni su libertà" →
      "Citazioni sulla libertà"): la preposizione articolata era generica ("su" per tutti tranne
      amore), ora è corretta per genere/numero di ciascun tema.
- [x] **Generi (5):** stessa cosa, testi più corti (104-178 parole), stesso file `data/hub_intros.json`.
- [x] **`/raccolte/<slug>/`** — **5 raccolte pubblicate** (non 6-8 come indicato in origine: due
      candidate previste qui sotto, *amicizia* e *frasi sul tempo che passa*, sono state scartate in
      fase di curatela per lo stesso principio di rigore della Fase 3 — "meglio nessuna raccolta che
      una forzata" — perché non si trovavano ≥8 citazioni genuinamente pertinenti in archivio senza
      stiracchiare il fit; *tempo che passa* inoltre avrebbe duplicato troppo da vicino il tema
      "Tempo" già esistente). Le 5 pubblicate, con criterio di selezione oggettivo (parola chiave sul
      testo, poi verifica manuale una per una, scartando i falsi positivi): *Libri e scrittura* (10),
      *Il mare* (8), *La morte* (9), *Frasi brevi* (12), *Incipit memorabili* (13). Dati in
      `data/raccolte.json` (slug, h1, introduzione, `quote_keys` — stessa chiave `autore|opera|prime
      6 parole` usata da `slugs.json`, una citazione può comparire in più raccolte, es. l'incipit di
      Huckleberry Finn è sia in *Libri e scrittura* sia in *Incipit memorabili*). Generatore:
      `tools/generate_raccolte_pages.py`; link di ritorno "In questa raccolta: {Titolo} →" aggiunto
      alle pagine citazione corrispondenti (stesso meccanismo del link opera di Fase 4). Indici
      `/opere/` e `/raccolte/` aggiunti a `generate_index_pages.py` (mancava anche `/opere/`, non
      generato durante la Fase 4).
      *Perché separate dai temi:* i 7 umori sono una scelta di prodotto — "un'atmosfera, non una
      classificazione", da tenere pochi e larghi — mentre la domanda di ricerca è fatta di intenti
      stretti. Le raccolte danno accesso a quel traffico senza snaturare i filtri.
- [x] Nei titoli e negli H1 degli hub usare in modo naturale sia "frasi" (dove sta il volume di
      ricerca in Italia) sia "citazioni" (il registro del sito): *"Frasi e citazioni sulla libertà"*.
      Una volta nel title, una nell'H1, mai infarcire il corpo. Applicato alle 5 raccolte (es. H1
      "Frasi brevi: le citazioni più corte", "Incipit memorabili: le più belle prime frasi").
- [x] Gate di indicizzazione (Fase 2) completato come previsto: un hub sotto le 3 citazioni ora entra
      comunque in sitemap se ha un'introduzione scritta a mano (`indexable = count >= 3 or
      bool(intro_paragraphs)` in `generate_hub_pages.py`) — non cambia nulla oggi (tutti i 7 temi e i
      5 generi sono già sopra soglia), ma chiude la regola lasciata a metà in Fase 2.

#### Fase 6 — Schede autore e misura

- [x] **Schede autore per tutti i 193 autori dell'archivio** (2026-08-28, due lotti). Lotto 1: i 43
      autori con ≥2 citazioni, 72-97 parole ciascuna. Lotto 2: i 150 autori con 1 sola citazione —
      lunghezza media più bassa (55-104 parole, media 70 sui 193 totali) perché per molti autori meno
      documentati non c'erano altrettanti fatti verificabili con certezza da aggiungere senza
      scivolare nel riempitivo o nella congettura; **la scelta è stata privilegiare la precisione
      sulla lunghezza esatta del target 80-120**, coerente con la stessa priorità data alla
      veridicità in Fase 3. Diciannove schede del lotto 2 risultate troppo corte (<55 parole) sono
      state riviste e ampliate con un fatto in più a testa prima della pubblicazione. Dati
      biografici sempre verificabili e incontrovertibili (nascita/morte, nazionalità, opere
      principali, un fatto distintivo). Testi in `data/hub_intros.json` sotto la chiave `autori`
      (keyed per nome esatto come compare in `data/citazioni.json`), iniettati da
      `generate_hub_pages.py` nel ramo autore di `main()`. Effetto sul gate di indicizzazione
      (Fase 2/5): **tutti i 193 autori sono ora indicizzabili** (prima erano 13, poi 43 dopo il
      lotto 1) — verificato nel rapporto di `build.py` (0 hub sotto soglia su 522 URL totali) e a
      campione in browser (Jane Austen, 1 sola citazione: nessun `noindex`, prima lo aveva).
- [x] **Google Search Console — fatto il 2026-08-30 dall'utente.** Proprietà di tipo *Dominio*
      su `sottolineature.it`, verificata con record TXT nel DNS (i nameserver sono di Hostinger,
      `*.dns-parking.com`). Sitemap inviata come URL completo: nelle proprietà Dominio il percorso
      relativo `sitemap.xml` viene rifiutato con "Indirizzo Sitemap non valido", serve
      `https://sottolineature.it/sitemap.xml`. **Da controllare ogni mese:** Indicizzazione →
      Pagine. La metrica non è la posizione media, è **quante pagine citazione risultano
      indicizzate sul totale inviato**
- [x] **Bing Webmaster Tools — fatto il 2026-08-30 dall'utente**, importando la proprietà da
      Search Console. Sitemap accettata lo stesso giorno: 780 URL individuati, 0 errori, 0 avvisi
- [x] **IndexNow — attivo dal 2026-08-30** (chiave `471381759dae4f3fbe0a6d769882507a` alla radice
      del sito, workflow `.github/workflows/indexnow.yml`). **Non rigenerare la chiave dalla pagina
      di Bing:** quella proposta lì servirebbe solo a chi parte da zero, e adottarla richiederebbe
      di cambiare sia il file alla radice sia il workflow
- [ ] **Analytics — bloccato**, non per motivi tecnici ma perché la privacy policy del sito è
      **ancora in sospeso** (serve i dati del titolare: nome, indirizzo, base giuridica). Nessun
      analytics con cookie va aggiunto prima che la policy sia pubblicata, e comunque solo con una
      soluzione senza cookie quando richiesto.

#### Fase 7 — Domanda di ricerca: mappatura keyword e lotti mirati

Riferimento completo: **`SEO-KEYWORDS.md`** (metodo, tabelle, motivi degli scarti) e
**`data/keywords.json`** (versione dati). Foglio di lavoro umano, non versionato:
`archivio/sottolineature-keyword-map.xlsx`.

Base: export di 6.000 keyword fornito dall'utente il 2026-08-28. **Il risultato che orienta tutta
la fase:** solo l'8,7% del volume mappa su pagine che il sito già ha, il 54,9% sta su query
tematiche che l'archivio da 262 citazioni non può ancora soddisfare, il 32,6% va scartato.
Il collo di bottiglia non è più l'architettura: è la dimensione dell'archivio. Questa lista serve
quindi prima come **elenco di ciò che conviene raccogliere**, poi come piano editoriale.

- [ ] **Secondo export keyword** con i semi `frasi`, `aforismi`, `massime`, `pensieri` e con i semi
      di entità (`frasi + <titolo>`, `frasi + <autore>`). La lista attuale è generata solo su
      *citazion-*: in Italia il volume su *frasi* è più alto e oggi è invisibile.
      **Richiede l'utente e il suo strumento — non automatizzabile.**
- [ ] **Title e H1 di opere e autori allineati alla domanda**, con "frasi" e "citazioni" usati
      entrambi in modo naturale (*"Frasi e citazioni da 1984 di George Orwell"*). Solo title,
      description e H1; dai generatori in `tools/`; nessun title duplicato; nessuna pagina nuova.
- [ ] **Lotto citazioni "amicizia"** (10-12 verificate). È il buco più grande del sito: 3.940 di
      volume contro 3 citazioni in archivio.
- [ ] **Le 6 raccolte con copertura sufficiente**, una alla volta, con selezione fatta *leggendo*
      le citazioni e introduzione scritta a mano: viaggio e cammino (3.420), donne (2.370),
      felicità (860), ricordo e memoria (680), occhi e sguardo (350), notte (320).
      Se leggendole se ne salvano meno di 8, la raccolta non si pubblica e torna in lista d'attesa.
- [ ] **Lotti citazioni sugli autori a più alta domanda**, fino a 3-4 citazioni a testa: Wilde
      (1.610 di volume, **1** citazione), Shakespeare (1.580 / 2), Dante (1.220 / 2), D'Annunzio
      (970 / 1), Pavese (730 / 2), Leopardi (720 / 2), Pirandello (700 / 2), Seneca (670 / 1),
      Merini (650 / 1). Le pagine con più domanda sono oggi quelle con meno contenuto.
- [ ] **Pagine opera** per i titoli con domanda che nel frattempo arrivano a 2+ citazioni:
      Alice nel paese delle meraviglie (770), Il grande Gatsby (290), Cime tempestose (280),
      L'amore ai tempi del colera (220), Cent'anni di solitudine (170), Oceano mare (170),
      Piccole donne (160). **Non crearle adesso**: hanno una citazione a testa, e con una sola
      citazione la pagina citazione è già la pagina dell'opera.
- [ ] **Raccolte quasi pronte**, quando arrivano a 8: bellezza (630), sogni (570),
      cambiamento (350), tristezza (210).
- [x] **Decisione dell'utente sul perimetro, presa il 2026-08-28:** il catalogo **può crescere,
      purché restino citazioni da libri**. Tradotto nella regola operativa scritta in `CATALOGO.md`:
      entra solo ciò che è tracciabile a un'opera scritta e pubblicata, con il punto preciso del
      testo. Quindi **sì a filosofi, classici greci e latini, saggi e poesia citati per opera**
      (Agostino *Confessioni*, Marco Aurelio *Colloqui*, Nietzsche *Zarathustra*), **no a massime
      senza opera di riferimento**, alle "citazioni latine" come genere, e a Socrate come autore
      (si cita Platone con il dialogo). Tetto: non più del 15% del catalogo da filosofia e classici
      non narrativi. Autori sotto copyright ammessi con citazione breve (max ~40 parole) e fonte
      completa
- [ ] **Acquisizioni ora sbloccate dalla decisione qui sopra**, tutte da citare per opera:
      Sant'Agostino *Confessioni* (1.460 di volume), Nietzsche *Così parlò Zarathustra* (830), Platone
      (550, con il dialogo — è anche il modo corretto di rendere le 440 di "Socrate"),
      Schopenhauer (430), Aristotele (300). Sotto copyright, con citazione breve e fonte completa:
      Bukowski (1.870), Camilleri (540). Restano esclusi *Ready Player One* e *Chiamami col tuo
      nome* solo finché non si trova una fonte italiana tracciabile al testo pubblicato.
      Il piano completo dei lotti è in `CATALOGO.md`, punto 7
- [ ] **Aggiornare `data/keywords.json` dopo ogni lotto**: le raccolte in lista d'attesa che
      superano la soglia si spostano da sole in "pronta".

**Cosa è già stato scartato e non va riproposto** (32,6% del volume, dettaglio in
`SEO-KEYWORDS.md`): film e serie TV (14.540), ricorrenze e auguri (9.700), altre lingue e dialetti
(8.570, comprese le *citazioni latine* — massime senza opera di riferimento), personaggi non
letterari (7.140), canzoni (6.140), social e meme (3.890), motivazionale e business (2.740),
riassunti/trame/pdf (1.470), religiose non letterarie (1.280), sport (1.020), bibliografia e
ambito giuridico (540). Le keyword di testa (*citazioni*, *citazioni famose*, *citazioni belle*:
51.950) sono la home e l'indice `/citazioni/`: non farne mai pagine dedicate.

**Controllo di accettazione:** ogni pagina pubblicata in questa fase ha ≥8 citazioni (raccolta) o
una scheda verificata (opera); nessun title duplicato dopo il build; nessuna pagina creata a
partire da una keyword senza il contenuto che la giustifica.

#### Da non fare, mai (anti-pattern per questo sito)

- Generare le 249 pagine opera in automatico.
- Generare pagine da combinazioni di filtri (tema × genere, autore × tema): è il modo più veloce
  per prendere un declassamento per contenuto di scarsa qualità.
- Aggiungere temi o generi per intercettare ricerche — la regola dei 4+ titoli resta.
- Riscrivere gli slug esistenti per farli più belli.
- Mettere `sameAs`, ISBN, traduttori, date o edizioni non verificati per arricchire i dati strutturati.
- Modificare il testo di una citazione, un nome, un titolo o un anno per ragioni SEO.
- Comprare o scambiare link. La strada naturale per i collegamenti in entrata di questo sito sono
  insegnanti, biblioteche e blog letterari.

#### Vecchie voci SEO ancora valide

- Contenuto "sottile" sulle pagine citazione senza contesto: **risolto**, solo 2/256 ne sono prive
- Pagine autore per Sarah J. Maas / Leigh Bardugo: da considerare una volta aggiunte le loro citazioni

### Da fare
- **Correzione di rotta sui lotti (2026-08-30), dettagli in `CATALOGO.md` §7:** stop agli autori
  nuovi, si porta a **4 citazioni** ciascuno gli autori gia' in archivio con piu' domanda di
  ricerca, con precedenza alle opere anteriori al Novecento. Motivo: 176 autori su 251 sono fermi
  a due citazioni e il Novecento resta il 58% dell'archivio
- **Errore di contenuto aperto:** due citazioni di *Il piccolo principe* hanno lo stesso
  riferimento, «capitolo XXI». Il build lo segnala a ogni esecuzione. Una delle due e' collocata
  male e va verificata sul testo
- **Contatto e "Segnala un errore" — in sospeso su richiesta dell'utente (2026-08-30):** manca solo
  un indirizzo email da pubblicare. Quando arriva (l'utente valuta se crearne uno dedicato tipo
  `ciao@sottolineature.it` su Hostinger, dove sta il dominio): email nel footer di ogni pagina, e
  sulla pagina citazione un link *Segnala un errore* che apre una mail precompilata con l'URL della
  citazione nell'oggetto. Su un sito costruito sulla verifica delle fonti e' anche il canale
  naturale per ricevere segnalazioni dagli insegnanti e guadagnare link in entrata. **Non pubblicare
  l'email personale dell'utente senza che sia lui a indicarla**
- **Informativa privacy** — richiesta dall'utente, in sospeso: servono nome/ragione ed email da usare come titolare del trattamento (dati che non si possono inventare in un documento legale). Nessun cookie/tracking sul sito, solo `localStorage` funzionale — confermato controllando il codice
- **Contesto per le ultime 2 citazioni** — Dostoevskij (Delitto e castigo), Sciascia (Il giorno della civetta): da ritentare solo se emerge una fonte primaria (es. testo del romanzo su Wikisource/Google Libri), non ha senso riprovare con le stesse ricerche generiche già fatte più volte
- **Sarah J. Maas e Leigh Bardugo** — restano da aggiungere (Rick Riordan fatto): nessuna citazione italiana verificabile trovata finora, serve una fonte tracciabile al testo pubblicato (anteprima Google Libri o editore), non solo blog/trame
- **Copertine per le 11 citazioni che ne sono ancora prive** — recuperate 32/43 in totale il 2026-08-28 (dettagli in LOG.md); delle 11 restanti, 2 sono poesie senza edizione autonoma (Leopardi, Pascoli — irrecuperabili), le altre 9 non hanno restituito su Open Library un'edizione con copertina disponibile nemmeno cercando per titolo originale (Kundera, Kafka "Il Castello", Simone Weil, Elif Shafak, Čechov, più Camus "L'estate" e Beauvoir "Il secondo sesso" scartati per copertine sbagliate/parziali) — probabilmente da lasciare alla tile placeholder
- **Stato della routine cloud automatica** — da riverificare con l'utente, non è implementabile in autonomia

### Idee scartate (per memoria, non riproporre senza nuovo contenuto)
- Tag "Giallo/Poliziesco" e "Avventura": solo 1-2 titoli a testa sul sito, troppo pochi per un filtro utile
- Centrare il logo dell'immagine condivisa sul baricentro dell'inchiostro invece che sull'ingombro: provato e bocciato, spostava il logo troppo a sinistra. Su questo lockup l'occhio legge i bordi, non la massa. La soluzione giusta al "non sembra centrato" è stata invece allargare l'URL sotto, che fa da base stabile.
- Filetto dorato tra citazione e attribuzione: rimosso, "sembrava messo a caso" — galleggiava in uno spazio già vuoto senza separare nulla. La gerarchia la fa la tipografia, non le linee.
- Due pulsanti di condivisione ("storia" e "post") per far scegliere il formato: provati e rimossi, appesantivano l'interfaccia. Il pulsante resta uno solo e il formato lo decide il codice (`DEFAULT_SHARE_FORMAT`). Entrambi i formati restano definiti in `SHARE_FORMATS`, così cambiare scelta è una riga.
