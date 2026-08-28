# SEO — audit, architettura e piano di lavoro

Documento operativo. Scritto il 2026-08-28 su richiesta dell'utente, dopo lettura completa di
`index.html`, delle 256 pagine `citazioni/`, dei 205 hub (`autori/`, `temi/`, `generi/`),
di `tools/build.py` e della sitemap. Vale come estensione della sezione "Da fare — SEO" di `CLAUDE.md`.

**Regola che governa tutto il resto:** vale la costituzione del progetto. La correttezza di frasi,
autori, anni, contesti e fonti viene prima di qualunque guadagno di posizionamento. Nessun dato
inventato per riempire una pagina — meglio una pagina in meno.

---

## 1. Verdetto in breve

Il sito è messo meglio della media dei siti di citazioni italiani: contesto verificato su 254/256
frasi, pagina di metodo, dati strutturati, hub per autore/tema/genere, sitemap generata da build.
Questo è un patrimonio reale.

Il problema non è quello che manca: è **il rapporto tra URL e contenuto unico**.

| | |
|---|---|
| Citazioni (unità di contenuto originale) | 256 |
| URL pubblicati in sitemap | 463 |
| Opere distinte | 249 |
| Autori distinti | 193 |
| Autori con **una sola** citazione | ~150 |
| Volte in cui la stessa frase compare in HTML indicizzabile | **4-5** (home + tema + genere + autore + pagina citazione) |

Tradotto: si sono creati 463 indirizzi per 256 blocchi di testo, e ogni blocco è stato copiato
su tutti gli indirizzi che lo riguardano. Per Google questo non è un sito con 463 pagine: è un
sito con ~256 contenuti e 200 pagine che li ripetono. L'esito tipico è la casella
"Scansionata — attualmente non indicizzata" su una fetta grande dell'archivio, e la homepage
che si mangia il traffico che dovrebbe andare alle pagine figlie.

Non è un errore di esecuzione — le pagine sono fatte bene. È un errore di **regola di
distribuzione del contenuto**, e si corregge senza buttare via niente.

---

## 2. Cosa tenere così com'è

Da non toccare, funziona:

- `metodo.html` — è il più forte segnale di affidabilità del sito e nessun aggregatore ce l'ha.
- Contesto in linguaggio semplice prima del riferimento: è contenuto originale vero, non riempitivo.
- `tools/build.py` come unico entry point con `index.html` fonte di verità. L'impianto è quello giusto:
  tutto quello che segue si implementa dentro questo schema, non contro.
- Canonical, Open Graph, alt text reali sulle copertine, 404 personalizzato con `noindex`.
- I filtri umore/genere resi `<a>` reali verso gli hub con `preventDefault()` lato client: è la
  soluzione corretta, tenerla come modello per ogni futuro filtro.

---

## 3. I sei problemi strutturali, in ordine di gravità

### 3.1 La homepage è un superset di tutto il sito
`index.html` pesa 313 KB e contiene le 256 card complete: frase, attribuzione **e contesto**.
Ogni pagina citazione è quindi, agli occhi di un crawler, un sottoinsieme della home. Quando due
URL contengono lo stesso testo e uno dei due lo contiene tutto, il secondo perde.

Decisione presa: **teaser in home, testo pieno solo sulla pagina citazione.** La frase e
l'attribuzione restano in home (sono l'etichetta dell'elemento in lista, è legittimo ripeterle);
il **contesto esce dall'HTML della home e degli hub e diventa esclusivo della pagina dedicata**.
L'esperienza "vedo tutto a primo colpo" resta intatta: le card in home non mostravano il contesto
come elemento primario, e chi lo vuole ha un clic.

Effetto collaterale gradito: la home scende da ~313 KB a circa un terzo.

### 3.2 Le pagine citazione sono frammenti, non documenti
Prendendo `citazioni/george-orwell-1984.html` come campione:

- **non c'è nessun `<h1>`** — la frase è in un `<p class="card-quote">`. È il difetto tecnico
  più grave del sito, ripetuto 256 volte;
- il `<title>` è `George Orwell — 1984 | Sottolineature`, **identico** a quello che avrà la
  seconda citazione dalla stessa opera e sovrapponibile a quello della pagina autore;
- non c'è briciola di pane visibile, solo un "← Tutte le citazioni";
- non c'è navigazione di sito: da lì si torna solo alla home;
- il `BreadcrumbList` in JSON-LD ha due soli livelli e usa come `name` del secondo l'intero
  tag title (`George Orwell — 1984 | Sottolineature`), che non è un nome di briciola;
- manca la semantica della citazione (`<blockquote>`/`<cite>`);
- l'immagine di copertina, che sulla pagina dedicata è l'elemento LCP, ha `loading="lazy"`,
  nessuna `width`/`height` e nessun `preconnect` verso `covers.openlibrary.org`: ritardo di
  caricamento e spostamento del layout garantiti;
- l'immagine social è sempre `og-banner.png`, uguale per tutte le 256 pagine.

### 3.3 Gli hub sotto soglia sono duplicati mascherati
Con 193 autori per 256 citazioni, la maggior parte delle pagine autore contiene **una riga**, la
stessa che sta sulla pagina citazione, sulla home e sull'hub tema. Una pagina che elenca un solo
elemento non è una pagina: è un filtro travestito da pagina. Vale anche per gli hub tema/genere
finché restano semplici liste senza testo proprio.

Regola da introdurre (**gate di indicizzazione**), calcolata da `build.py`:

> Un hub entra in sitemap ed è indicizzabile solo se ha **≥ 3 citazioni** *oppure* **≥ 80 parole
> di testo editoriale originale** (scheda autore, introduzione al tema). Altrimenti riceve
> `<meta name="robots" content="noindex,follow">` ed esce dalla sitemap, **ma resta linkato**:
> serve come percorso di scansione, non come pagina di atterraggio.

Non è una rinuncia: è una lista d'attesa. Appena l'autore arriva a 3 citazioni o riceve la sua
scheda, la pagina entra da sola al build successivo.

**Il numero da tenere presente prima di applicare il gate:** oggi solo **13 autori su 193** hanno
3 o più citazioni, e **242 opere su 249** ne hanno una sola. Applicato così com'è, il gate
metterebbe in `noindex` circa 180 pagine autore. È la fotografia onesta della situazione — quelle
180 pagine oggi *non* stanno portando traffico, stanno diluendo il sito — ed è esattamente il
motivo per cui le schede autore della Fase 6 non sono un abbellimento ma la condizione per
riaccenderle. Se il gate a 3 sembra troppo severo si può partire da 2, ma la soglia va scelta
adesso e scritta in `build.py`, non lasciata al caso.

### 3.4 Manca il livello "opera", che è dove sta la domanda italiana
Le persone non cercano "citazioni sulla libertà di George Orwell". Cercano **"frasi 1984"**,
**"citazioni promessi sposi"**, **"frasi il piccolo principe"**. Oggi quella domanda non ha una
pagina su cui atterrare: c'è la pagina autore (generica) e la pagina citazione (una frase sola).

Va introdotto `/opere/<autore>-<titolo>/`. **Non in automatico su tutte e 249** — sarebbe
esattamente la fabbrica di doorway page che affossa i siti di citazioni. Solo dove esiste una
scheda vera scritta a mano (3-5 righe su cos'è il libro, anno, edizione/traduzione di
riferimento) e/o più di una citazione. Si parte dal canone scolastico, ~40 titoli.

### 3.5 URL fragili e host non canonico
- `citazioni/alessandro-manzoni-i-promessi-sposi-2.html`: il suffisso numerico dipende
  dall'**ordine** delle card in `index.html`. Se un giorno si toglie la citazione n.1, la n.2
  diventa n.1 e **cambia URL in silenzio**. Su 7 opere è già così. Questo è il modo tipico in cui
  un sito statico rigenerato da script si autodistrugge nel tempo.
- Estensione `.html` esposta e `metodo.html` invece di `/metodo/`.
- 512 link interni puntano a `../index.html` invece che a `/`: si crea la coppia duplicata
  `/` + `/index.html`.
- Il sito risponde anche su `sottolineature.vercel.app`: una copia completa del sito su un altro
  host. I canonical la mitigano, un 301 la elimina.
- Nessun `vercel.json` nel repo: nessuna politica di URL, nessuna intestazione di cache.

### 3.6 Sitemap e segnali di aggiornamento
Nessun `<lastmod>`, nessuna data di pubblicazione per citazione, nessun feed. Un sito che aggiunge
contenuto regolarmente e non lo segnala in nessun modo si fa scansionare più di rado di quanto meriti.

---

## 4. La domanda diretta: ogni citazione deve avere il suo URL?

**Sì — ma la scelta è corretta solo se rispetta tre condizioni, altrimenti si ritorce contro.**

1. **La pagina dedicata deve essere l'unico posto dove vive il blocco unico.** Il blocco unico non
   è la frase (25 parole che stanno ovunque, anche fuori dal sito): è **contesto + fonte
   verificabile + collegamenti all'autore, all'opera e al tema**. Se quel blocco esiste anche
   altrove, la pagina dedicata non ha una ragione di esistere che Google possa riconoscere.
2. **Deve essere un documento, non un frammento.** `<h1>`, briciola di pane visibile, navigazione,
   dati strutturati collegati fra loro, citazioni correlate. Una pagina da 80 parole senza titolo
   è, in termini di qualità, indistinguibile da una pagina generata in massa.
3. **Lo slug deve essere stabile per sempre.** Un URL che cambia perché è cambiato l'ordine in un
   file sorgente è un URL che perde tutto quello che ha accumulato.

Corollario importante, contro l'istinto di moltiplicare le pagine:

> **Quando un'opera ha una sola citazione, la pagina citazione *è già* la pagina dell'opera.**
> Non creare entrambe. La pagina opera nasce alla seconda citazione o quando c'è una scheda vera
> da scrivere.

E l'anti-pattern da non commettere mai su questo sito: **non generare pagine da combinazioni di
filtri** (tema × genere, autore × tema, "frasi brevi sull'amore di autori russi"). È il modo più
veloce per prendere un declassamento per contenuto di scarsa qualità.

---

## 5. Architettura target

```
/                                  Home. Ricerca, filtri, in evidenza, griglia con teaser.
                                   Nessun contesto nell'HTML. Legge ?q= per la ricerca.
/citazioni/                        Archivio completo paginato (/citazioni/pagina-2/ ...)
/citazioni/<slug>/                 LA PAGINA. Frase + contesto + fonte + correlate.   [256]
/autori/                           Indice A-Z di tutti gli autori
/autori/<autore>/                  Hub autore + scheda 80-120 parole      [193, gate attivo]
/opere/                            Indice delle opere con scheda
/opere/<autore>-<titolo>/          Scheda opera + tutte le sue citazioni  [~40 a regime]
/temi/                             Indice dei 7 umori
/temi/<tema>/                      Hub umore + introduzione editoriale 300-600 parole   [7]
/generi/                           Indice dei generi
/generi/<genere>/                  Hub genere + introduzione editoriale                [5]
/raccolte/                         Indice delle raccolte
/raccolte/<slug>/                  Raccolte curate a mano, la leva di traffico     [cresce]
/metodo/                           Come verifichiamo (già esistente, da spostare)
/privacy/                          In sospeso (servono i dati del titolare)
/feed.xml                          Ultime 20 citazioni aggiunte
/sitemap.xml  /robots.txt  /404.html
```

**Perché `/raccolte/` separato dai `/temi/`.** I 7 umori sono una scelta di prodotto — "un'atmosfera,
non una classificazione" — e vanno lasciati pochi e larghi, come stabilito. Ma la domanda di ricerca
italiana è fatta di intenti stretti: *frasi sui libri e sulla lettura*, *citazioni sull'amicizia*,
*frasi brevi*, *citazioni sul mare*, *frasi per la maturità*. Metterli fra gli umori snaturerebbe il
prodotto; metterli in `/raccolte/` come pagine curate a mano, con un'introduzione scritta e una
selezione ragionata, dà accesso a quel traffico senza toccare i filtri. **Una raccolta si pubblica
solo se ha almeno 8 citazioni pertinenti già sul sito e un'introduzione scritta a mano.**

**"Frasi" o "citazioni".** In Italia il volume di ricerca sta su *frasi*; il registro del sito sta
su *citazioni*. Non è un conflitto: il marchio e i percorsi restano "citazioni", ma i titoli e gli
H1 degli hub usano entrambe le parole in modo naturale — *"Frasi e citazioni sulla libertà"*,
*"Frasi da 1984 di George Orwell"*. Nessun infarcimento: una volta nel titolo, una nell'H1, mai
nel corpo se non serve.

---

## 6. Regole non negoziabili da qui in avanti

1. **Unicità del blocco.** Il contesto e la fonte di una citazione esistono in un solo HTML del
   sito: `/citazioni/<slug>/`. Home, hub, correlate mostrano frase e attribuzione, mai il contesto.
2. **Gate di indicizzazione.** Nessun URL entra in sitemap senza ≥3 elementi o ≥80 parole proprie.
   Lo decide `build.py`, non il giudizio a occhio.
3. **Slug immutabile.** Gli slug vivono in `tools/slugs.json`, si **leggono**, non si ricalcolano.
   Ogni cambio genera automaticamente un 301 in `tools/redirects.json`, che `build.py` riversa in
   `vercel.json`. Uno slug non si cancella mai.
4. **Nessuna pagina generata da combinazioni di filtri.**
5. **Nessun `sameAs`, ISBN, data o traduttore inventato.** I collegamenti a Wikipedia/Wikidata si
   mettono solo dopo aver aperto la pagina e verificato che sia la persona/opera giusta. Vale la
   stessa regola già in uso per i `cover_i` di Open Library.
6. **`build.py` resta l'unico entry point** e da ora stampa a fine esecuzione un rapporto:
   URL totali, URL indicizzabili, hub sotto soglia, citazioni senza fonte, slug nuovi, 301 aggiunti.
7. **Ogni fase chiusa si annota** in `CLAUDE.md` (stato) e i lotti di contenuto in `LOG.md`,
   come già si fa per le citazioni.

---

## 7. Piano di lavoro in fasi

Ogni fase è chiudibile da sola e ha un controllo di accettazione. Non passare alla successiva
senza aver superato il controllo.

### Fase 0 — Fondamenta tecniche (nessun contenuto nuovo)

1. **`vercel.json`** alla radice:
   ```json
   {
     "cleanUrls": true,
     "trailingSlash": true,
     "redirects": [],
     "headers": [
       { "source": "/assets/(.*)", "headers": [{ "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }] }
     ]
   }
   ```
   Con `cleanUrls` + `trailingSlash` Vercel serve `citazioni/foo.html` su `/citazioni/foo/` e
   rimanda i vecchi indirizzi con un 308 permanente **senza rinominare i file**: la migrazione
   non richiede di toccare la struttura del repo, solo i link interni. L'array `redirects` verrà
   riempito da `build.py` a partire da `tools/redirects.json`.
2. **Host canonico.** 301 da `www` all'apice (o viceversa, basta sceglierne uno) e da
   `sottolineature.vercel.app` a `sottolineature.it`. Se il redirect fra domini non è comodo,
   il minimo accettabile è `X-Robots-Tag: noindex` sul dominio `.vercel.app`.
3. **Link interni.** Sostituire tutti i `../index.html` con `/`, `index.html#slug` con `/#slug`,
   `metodo.html` con `/metodo/`, `../autori/x.html` con `/autori/x/`. Da fare nei generatori in
   `tools/`, non a mano sui file generati.
4. **`tools/slugs.json`.** Generarlo **una volta** dallo stato attuale, congelando gli slug
   esistenti così come sono — inclusi i `-2`. Chiave: `autore|titolo|prime 6 parole della frase`.
   Da qui in avanti gli slug si leggono da lì. Per le citazioni nuove su un'opera già presente
   lo schema è `<autore>-<titolo>-<3 parole significative dell'incipit>`, mai un numero.
   *Non rinominare i 7 slug numerati esistenti*: il beneficio è estetico, il rischio è reale.
5. **CSS condiviso.** Estrarre il blocco `:root`/card/tema ripetuto in 463 file in
   `/assets/site.css` (una sola richiesta, cache di un anno). `index.html` può tenere il suo
   inline, è l'unica pagina che ci guadagna.
6. **Navigazione di sito** in testa a ogni pagina generata: *Citazioni · Temi · Generi · Autori ·
   Metodo*. Oggi le pagine interne sono cul-de-sac.
7. **`preconnect`** verso `covers.openlibrary.org` in tutte le pagine con copertine;
   `width`/`height` espliciti su ogni `<img class="card-cover">`.

**Controllo:** `/citazioni/george-orwell-1984/` risponde 200; `/citazioni/george-orwell-1984.html`
risponde 308 verso di essa; `/` e `/index.html` non coesistono nei link interni (grep a zero);
la sitemap contiene solo URL puliti; nessun link interno rotto (crawl locale con `python3 -m
http.server` + uno script che segue tutti gli href e riporta gli stati).

### Fase 1 — Da frammento a documento: le 256 pagine citazione

Tutto dentro `tools/generate_quote_pages.py`.

1. **`<h1>` = il testo della citazione.** Se supera i 200 caratteri, `<h1>` = incipit troncato a
   parola intera + `…`, e il testo integrale sotto in `<blockquote>`.
2. **Semantica:** `<figure><blockquote><p>…</p></blockquote><figcaption>— <a>Autore</a>,
   <cite>Titolo</cite> · anno</figcaption></figure>`.
3. **`<title>` distintivo:** `«{incipit ~45 caratteri}…» — {Autore}, {Opera}`. Mai due title
   identici sul sito: `build.py` deve fallire se ne trova due uguali.
4. **`<meta description>`:** frase completa se breve, altrimenti frase troncata + prima riga di
   contesto. Anche qui: nessun duplicato.
5. **Briciola di pane visibile** che rispecchia esattamente il JSON-LD:
   `Sottolineature › Autori › {Autore} › {Opera, se ha pagina} › questa citazione`.
6. **JSON-LD in `@graph`** con `@id` collegati, al posto dei due oggetti scollegati di oggi:
   `WebPage` → `Quotation` (con `isPartOf` verso il `Book` e `creator` verso la `Person`) →
   `Book` (`name`, `author`, `datePublished`) → `Person` → `BreadcrumbList`.
   `sameAs` verso Wikipedia/Wikidata **solo se verificato a mano**, mai dedotto dal nome.
7. **Immagine LCP:** copertina senza `lazy`, con `fetchpriority="high"` e dimensioni esplicite.
8. **Immagine social per citazione:** pre-generare 256 PNG 1200×630 in `/assets/og/<slug>.png`
   riusando la composizione già scritta per il canvas di condivisione (via Playwright a build
   time), e puntarci `og:image`/`twitter:image`. È il singolo intervento con il miglior ritorno
   sulle condivisioni.
9. **Blocco correlate più ricco:** stesso autore (già c'è), stessa opera, stesso tema — con
   etichette che dicono *perché* sono correlate.

**Controllo:** validare 5 pagine campione con il test dei risultati strutturati di Google e con
un validatore schema.org; `build.py` non segnala title/description duplicati; l'H1 esiste su
tutte e 256 (grep di conteggio); test di velocità su una pagina citazione con LCP < 2,5 s.

### Fase 2 — De-duplicazione e gate di indicizzazione

1. **Togliere `card-context` dall'HTML** di `index.html` (generazione delle card), degli hub
   tema/genere/autore e delle correlate. Resta solo su `/citazioni/<slug>/`.
   Attenzione: `index.html` è la fonte di verità scritta a mano e **il contesto lì dentro va
   conservato** — è la sorgente da cui i generatori lo prendono. Va nascosto all'output HTML
   pubblicato della home, non cancellato dal sorgente. Se questo risulta scomodo, l'alternativa
   pulita è estrarre le citazioni in `data/citazioni.json` e far diventare `index.html` un file
   generato come gli altri — decisione da prendere consapevolmente, perché cambia il flusso di
   lavoro descritto in `CLAUDE.md`.
2. **Gate di indicizzazione** in `build.py`: hub con <3 citazioni e senza testo proprio →
   `noindex,follow` + fuori sitemap, ma linkati.
3. **Sitemap con `<lastmod>`.** Serve una data per citazione: aggiungere `data-added="YYYY-MM-DD"`
   sulle card. Ricostruire le date passate da `LOG.md` **solo dove il lotto è identificabile con
   certezza**; per le altre nessuna data inventata — si parte da qui in avanti.
4. **`/feed.xml`** con le ultime 20 citazioni per data di aggiunta.
5. **JSON-LD `WebSite` + `SearchAction`** sulla home, con `/?q={search_term_string}`. Richiede che
   la home legga il parametro `?q=` al caricamento e precompili la ricerca: piccola aggiunta al JS
   esistente, utile anche agli utenti (rende condivisibile una ricerca).
6. **`ItemList`/`CollectionPage`** sugli hub, con gli elementi in ordine.
7. **Pagine indice mancanti:** `/citazioni/` paginato (30 per pagina, self-canonical su ogni
   pagina), `/autori/` A-Z, `/temi/`, `/generi/`. Oggi quelle cartelle sono vicoli ciechi.

**Controllo:** una frase presa a caso deve comparire con il suo contesto in **un solo** file HTML
pubblicato (`grep -rl` sul contesto restituisce 1 risultato); il rapporto di `build.py` mostra
URL indicizzabili < URL totali con la differenza spiegata; la sitemap contiene solo URL indicizzabili.

### Fase 3 — La fonte verificabile su ogni citazione *(il lavoro che vale di più)*

Aggiungere a ogni card un blocco fonte: **edizione di riferimento, capitolo/parte/atto/verso,
traduttore quando il testo è tradotto, collegamento a Wikisource o alla fonte primaria dove esiste.**

Questo è l'unico contenuto che nessun aggregatore italiano ha, è esattamente ciò che il sito già
dichiara di fare in `metodo.html`, ed è la ragione per cui un motore di ricerca (e un insegnante)
dovrebbero preferire questa pagina a un sito di frasi. Si lavora a lotti, con le regole di verifica
già in `CLAUDE.md`, e si annota ogni lotto in `LOG.md` come per i contesti.
Nel markup: `<p class="card-source">`, e nel JSON-LD `citation` / `isPartOf` arricchiti.

Ordine dei lotti: prima le opere di pubblico dominio con testo su Wikisource (Dante, Manzoni,
Leopardi, Verga, Pirandello, Shakespeare in traduzione), dove la verifica è rapida e il
collegamento esterno è di qualità.

### Fase 4 — Livello opera

`/opere/<autore>-<titolo>/` per i ~40 titoli del canone scolastico e per tutte le opere con ≥2
citazioni. Ogni pagina: scheda di 3-5 righe scritta a mano (cos'è il libro, anno, edizione e
traduzione di riferimento), tutte le citazioni dell'opera come lista con collegamento, blocco
sull'autore. H1: *"Frasi e citazioni da {Opera} di {Autore}"*.
JSON-LD `Book` con `@id` stabile, riusato da tutte le pagine citazione dell'opera.
**Nessuna pagina opera senza scheda scritta.**

### Fase 5 — Hub editoriali e raccolte

- **Temi (7):** introduzione di 300-600 parole scritta a mano per ciascuno. Sono 7 pagine: è un
  investimento piccolo su quelle che possono diventare le pagine più visitate del sito.
- **Generi (5):** stessa cosa, più corta.
- **Raccolte:** partire con 6-8, ognuna con ≥8 citazioni pertinenti già presenti e introduzione
  scritta. Candidate naturali per questo archivio: *frasi sui libri e sulla lettura*,
  *citazioni sull'amicizia*, *frasi brevi*, *citazioni sul mare e sul viaggio*,
  *frasi sul tempo che passa*, *citazioni per iniziare un discorso*.
  Una raccolta senza introduzione scritta non si pubblica.

### Fase 6 — Schede autore e misura

- **Schede autore** di 80-120 parole verificate, a lotti, dando la precedenza agli autori più
  cercati e a quelli con più citazioni. Ogni scheda pubblicata fa entrare la pagina in sitemap
  automaticamente grazie al gate.
- **Search Console** (richiede l'account dell'utente): verifica proprietà, invio sitemap,
  controllo mensile del rapporto Indicizzazione pagine — la metrica da guardare non è la
  posizione media, è **quante delle 256 pagine citazione risultano indicizzate**.
- **Bing Webmaster Tools** + **IndexNow** (Vercel lo supporta con una chiave statica): notifica
  immediata degli URL nuovi.
- Nessun analytics con cookie senza informativa privacy: se serve una misura, usare una soluzione
  senza cookie e comunque **prima** pubblicare la privacy policy già in sospeso.

---

## 8. Cosa non fare

- Non generare le 249 pagine opera in automatico.
- Non generare raccolte combinando filtri.
- Non aggiungere temi o generi per intercettare ricerche: la regola dei 4+ titoli in `CLAUDE.md` resta.
- Non riscrivere gli slug esistenti per farli più belli.
- Non mettere `sameAs`, ISBN o traduttori non verificati per arricchire i dati strutturati.
- Non comprare o scambiare link. Un sito di citazioni verificate a mano ha una strada naturale per
  i collegamenti in entrata: insegnanti, biblioteche, blog letterari. Quella funziona e non si ritorce.

---

## 9. Il comando da dare a Sonnet 5

Tre comandi separati. **Non darli tutti insieme**: le fasi 0-2 sono automatizzabili e vanno
verificate prima di aprire il cantiere editoriale.

### 9.1 Comando principale — Fasi 0, 1 e 2

```
Sei un ingegnere SEO senior che lavora sul repo di sottolineature.it (sito statico su Vercel,
index.html è la fonte di verità, tools/build.py è l'unico entry point di generazione).

Prima di scrivere una riga di codice, leggi in quest'ordine: CLAUDE.md (la costituzione del
progetto e la roadmap), SEO.md (l'audit e il piano che devi eseguire), tools/build.py,
tools/generate_quote_pages.py, tools/generate_hub_pages.py, tools/labels.py, e almeno una pagina
per tipo fra citazioni/, temi/, generi/, autori/.

Esegui le Fasi 0, 1 e 2 del piano descritto in SEO.md, in quest'ordine, fermandoti al controllo
di accettazione di ogni fase prima di passare alla successiva.

Vincoli non negoziabili:
- La correttezza di frasi, autori, titoli, anni e contesti viene prima di tutto. Non modificare
  MAI il testo di una citazione, il nome di un autore, un titolo o un anno per ragioni SEO.
  Non inventare nessun dato: niente sameAs, ISBN, traduttori, date o edizioni non verificati.
- Non toccare i contenuti: questa è un'operazione strutturale su markup, URL, metadati e
  generatori. L'unico contenuto che puoi spostare è il contesto, che deve smettere di comparire
  nell'HTML pubblicato di home e hub e restare esclusivo di /citazioni/<slug>/.
- Ogni modifica alle pagine generate passa dai generatori in tools/, mai a mano sui file generati.
- Gli slug esistenti non si cambiano, inclusi i 7 con suffisso -2. Vanno congelati in
  tools/slugs.json e da lì in avanti letti, non ricalcolati.
- Il sito deve funzionare identico per uno studente e per un insegnante, su mobile e desktop,
  in tema chiaro e scuro. Nessuna regressione di esperienza: se un intervento SEO peggiora l'uso,
  fermati e chiedi.

Metodo di lavoro:
- Lavora a fasi. Alla fine di ogni fase esegui il controllo di accettazione scritto in SEO.md e
  riportamene l'esito con numeri, non con aggettivi.
- Verifica sempre eseguendo, non a occhio: python3 -m http.server, uno script che segue tutti i
  link interni e riporta i codici di stato, grep di conteggio per H1/title duplicati/contesti
  ripetuti, e un controllo visivo su una pagina per tipo in chiaro e scuro, mobile e desktop.
- Dopo ogni modifica a index.html o ai generatori, lancia python3 tools/build.py e controlla che
  il rapporto finale torni.
- Aggiungi a build.py un rapporto di fine esecuzione: URL totali, URL indicizzabili, hub sotto
  soglia, title duplicati, description duplicate, pagine senza H1, slug nuovi, 301 aggiunti.
  Il build deve fallire con errore se trova due title identici o una pagina citazione senza H1.
- Aggiorna la sezione Roadmap di CLAUDE.md a ogni fase chiusa, come prescrive la costituzione,
  e annota in LOG.md solo ciò che riguarda le citazioni.
- Fai un commit separato per fase, con messaggio che dice cosa cambia e cosa verifica.
  Non pushare finché non ti do conferma sul risultato della Fase 0.

Se durante il lavoro trovi un conflitto fra una raccomandazione di SEO.md e una decisione già
presa in CLAUDE.md (per esempio sul layout della home o sui filtri), fermati e chiedimi:
CLAUDE.md ha la precedenza finché non decido io di cambiarla.

Comincia dalla Fase 0 e mostrami vercel.json e il diff dei generatori prima di rigenerare tutto.
```

### 9.2 Comando per la Fase 3 (fonte verificabile) — a lotti

```
Leggi CLAUDE.md (regole di verifica) e SEO.md (Fase 3). Aggiungi il blocco fonte alle citazioni
di sottolineature.it, lavorando su un lotto di 15 citazioni alla volta, partendo dalle opere di
pubblico dominio con testo integrale su Wikisource.

Per ogni citazione: edizione di riferimento, capitolo/parte/atto/verso, traduttore se il testo è
tradotto, collegamento alla fonte primaria dove esiste. Valgono le regole di verifica di CLAUDE.md:
Wikisource o edizione originale, Wikiquote solo con riferimento a capitolo/edizione e mai da sola,
altrimenti due fonti indipendenti concordanti. Se non riesci a stabilire con certezza il
riferimento, LASCIA IL CAMPO VUOTO e annota lo scarto con la ragione: una fonte sbagliata è
molto peggio di una fonte assente su un sito che si presenta come verificato a mano.

Il blocco fonte va aggiunto in index.html (fonte di verità) e propagato dai generatori solo alla
pagina /citazioni/<slug>/, mai agli hub. Dopo ogni lotto: python3 tools/build.py, controllo che
nessuna fonte sia finita per errore su due citazioni diverse, riga in LOG.md con il formato in uso,
commit.
```

### 9.3 Comando per le Fasi 4-6 (contenuto editoriale)

```
Leggi CLAUDE.md e SEO.md. Esegui la Fase 4 del piano: il livello /opere/.

Costruisci le pagine opera SOLO per le opere con almeno 2 citazioni sul sito e per i titoli del
canone scolastico italiano che hai già in archivio, e SOLO se puoi scrivere per ciascuna una
scheda di 3-5 righe verificata (cos'è il libro, anno di pubblicazione, edizione e traduzione di
riferimento). Nessuna pagina opera senza scheda scritta: se non hai le informazioni verificate,
l'opera non entra in questa fase.

Prima di generare qualsiasi cosa, mostrami l'elenco delle opere candidate con il motivo di
inclusione e aspetta il mio ok. Poi genera dalle stesse funzioni in tools/, applica il gate di
indicizzazione, rilancia il build e aggiorna CLAUDE.md.
```

---

## 10. Come si misura se sta funzionando

Non guardare le posizioni nei primi mesi. In ordine di importanza:

1. **Pagine indicizzate / pagine inviate** in Search Console. Obiettivo realistico a tre mesi
   dalla Fase 2: oltre l'80% delle pagine citazione indicizzate. Oggi, senza gli interventi
   descritti, la previsione onesta è molto più bassa.
2. **Quali URL ricevono i clic.** Se il 90% arriva sulla home, l'architettura non sta funzionando:
   il segnale di successo è il traffico che atterra sulle pagine citazione, opera e raccolta.
3. **Query di tipo "frase esatta"** — chi cerca un pezzo di frase che ricorda a metà. È il nostro
   pubblico naturale e la pagina dedicata è l'unica risposta possibile.
4. **Collegamenti in entrata da domini scolastici e bibliotecari.** È il segnale che la scelta
   di verificare le fonti sta producendo l'effetto che deve produrre.
