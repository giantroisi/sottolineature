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

- **Sito statico puro**: `index.html` (tutto: markup + CSS + JS inline), più `metodo.html`, nessun build step per il deploy (Vercel serve i file così come sono). Deploy automatico su push a `main` via integrazione Git di Vercel — **se non parte da sola** (è già successo), fare `npx vercel --prod` a mano.
- **`index.html` resta la fonte di verità per le citazioni**, modificato sempre a mano (Edit diretto, mai script). Dopo ogni modifica alle card (aggiunta/rimozione citazione, contesto, copertina, categoria, genere) **lanciare `python3 tools/build.py`** per rigenerare `citazioni/`, `temi/`, `generi/`, `autori/` e `sitemap.xml` di conseguenza — altrimenti quelle pagine restano disallineate rispetto a `index.html`.
- **Card**: `<article class="card" data-category="..." data-genre="...(opzionale, multi-valore separato da spazi)">`, contiene `card-quote`, `card-citation` (autore/titolo/anno), `card-context` (opzionale), `card-hint`. Il toggle "Sottolinea", il campo nota e il pulsante "Condividi" vengono iniettati via JS su ogni card, non sono nel markup statico.
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
- 256 citazioni, 213 copertine recuperate + tile placeholder per le 43 mancanti, contesto su 37 citazioni (9 aggiunte con citazioni nuove, 28 aggiunte retroattivamente a citazioni già presenti — standard per le nuove da qui in poi). Nota: il numero di copertine era rimasto non aggiornato per diversi lotti passati (indicava ancora "34", risalente a uno stato molto più piccolo del sito) — corretto qui al valore reale contato dal file
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
- Pagina dedicata per ogni citazione (`citazioni/<slug>.html`, 256 pagine), generate da `tools/generate_quote_pages.py` a partire da `index.html` — ognuna con URL proprio, meta description, canonical, Open Graph/Twitter card. Ogni card sull'index ha un link "Link" verso la sua pagina. Aggiunto atterraggio via hash (`index.html#slug`) che azzera i filtri e scorre/evidenzia la citazione — **da riverificare**: l'ultima sessione si è chiusa prima di confermarlo in modo affidabile in browser
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

### Da fare — SEO
- **Contenuto "sottile" sulle pagine citazione senza contesto** (~216/256) — l'unico punto dell'audit del 2026-08-27 rimasto aperto, si risolve mano a mano che si scrivono i contesti mancanti (vedi sotto)
- Da fare in futuro, non urgente: sottomettere `sitemap.xml` a Google Search Console (richiede accesso all'account dell'utente, non automatizzabile); considerare pagine autore anche per Sarah J. Maas/Leigh Bardugo una volta aggiunte le loro citazioni

### Da fare
- **Informativa privacy** — richiesta dall'utente, in sospeso: servono nome/ragione ed email da usare come titolare del trattamento (dati che non si possono inventare in un documento legale). Nessun cookie/tracking sul sito, solo `localStorage` funzionale — confermato controllando il codice
- **Contesto per le restanti ~216 citazioni** — il cantiere grande, da fare a lotti
- **Sarah J. Maas e Leigh Bardugo** — restano da aggiungere (Rick Riordan fatto): nessuna citazione italiana verificabile trovata finora, serve una fonte tracciabile al testo pubblicato (anteprima Google Libri o editore), non solo blog/trame
- **Copertine per le 43 citazioni che ne sono prive** — in gran parte poesie/estratti senza edizione autonoma su Open Library; per queste la tile con le iniziali resta la soluzione, ma vale un ultimo giro mirato su quelle che un'edizione ce l'hanno
- **Stato della routine cloud automatica** — da riverificare con l'utente, non è implementabile in autonomia

### Idee scartate (per memoria, non riproporre senza nuovo contenuto)
- Tag "Giallo/Poliziesco" e "Avventura": solo 1-2 titoli a testa sul sito, troppo pochi per un filtro utile
- Centrare il logo dell'immagine condivisa sul baricentro dell'inchiostro invece che sull'ingombro: provato e bocciato, spostava il logo troppo a sinistra. Su questo lockup l'occhio legge i bordi, non la massa. La soluzione giusta al "non sembra centrato" è stata invece allargare l'URL sotto, che fa da base stabile.
- Filetto dorato tra citazione e attribuzione: rimosso, "sembrava messo a caso" — galleggiava in uno spazio già vuoto senza separare nulla. La gerarchia la fa la tipografia, non le linee.
- Due pulsanti di condivisione ("storia" e "post") per far scegliere il formato: provati e rimossi, appesantivano l'interfaccia. Il pulsante resta uno solo e il formato lo decide il codice (`DEFAULT_SHARE_FORMAT`). Entrambi i formati restano definiti in `SHARE_FORMATS`, così cambiare scelta è una riga.
