# Validazione strutturale

Il controllo riusabile e' `python3 tools/check_links.py`. Esamina tutte le pagine HTML pubblicate
e termina con codice 1 quando trova un errore verificabile. `python3 tools/build.py` lo esegue
automaticamente in modalita' diagnostica: il referto resta visibile, ma non blocca la generazione.
Questo evita che un'euristica interrompa un lotto editoriale; prima di pubblicare, il comando
diretto deve comunque chiudersi con `Problemi totali: 0`.

## Cosa controlla

- un solo `title`, una sola meta description, un solo canonical e valori unici nel sito;
- canonical uguale all'URL pubblico pulito;
- esattamente un `<h1>` e un landmark principale (`<main>` oppure `role="main"`) per pagina, senza salti nella gerarchia degli heading;
- breadcrumb visibile sulle pagine di dettaglio che lo prevedono e tipi JSON-LD minimi per rotta;
- URL interni puliti, link risolvibili, pagine non orfane;
- sitemap figlie valide e coerenza in entrambe le direzioni (URL->file e pagina indicizzabile->sitemap);
- immagini dichiarate in sitemap: HTTPS/host canonico, file locale esistente e
  stesso riferimento presente come `img` nella pagina associata; query di cache
  ed entita' XML/HTML ammesse, frammenti e percorsi fuori progetto rifiutati;
- ogni immagine con attributo `alt`; file locali, copertine, tassonomia e traduttori restano coperti
  dai controlli gia' presenti nello stesso script.

La validita' interna dei grafi JSON-LD e' verificata anche da `tools/controlla_jsonld.py`, richiamato
dal build subito dopo il controllo strutturale.

## Controllo mobile

Test di regressione del validatore (senza dipendenze aggiuntive):
`python3 -m unittest discover -s tools -p 'test_structural_validation.py'`.
Usa un sito fittizio in una cartella temporanea, mai l'archivio reale: verifica
che markup, canonical, link e sitemap errati siano rifiutati, mentre immagini
decorative, pagine private e stringhe negli script non creino falsi positivi.
Include una guardia per la larghezza esplicita delle colonne mobile nel template.
Il markup pubblico usa anche `role="main"`: e' ammesso, ma i landmark duplicati
(anche misti fra ruolo esplicito e tag semantico) sono rifiutati.
Otto ulteriori scenari coprono le immagini in sitemap, incluse query di cache,
file mancanti, host errato, percorsi fuori progetto e immagini presenti soltanto
come stringhe JavaScript. Una stessa immagine puo' essere usata da piu' pagine.

Lo scorrimento orizzontale dipende da layout, font e viewport e non e' verificabile leggendo il solo
HTML. Dopo una modifica a markup o CSS si apre la pagina a 375x812 e 390x844 e si confronta
`document.documentElement.scrollWidth` con `innerWidth`: la larghezza del documento non deve
superare la viewport. Vanno controllati anche i contenitori e i singoli elementi. Ripetere almeno su
home, una citazione, un autore e la tipologia di pagina modificata.

Per la home ripetere anche **senza reload** il passaggio desktop -> 390 px,
390 -> 844 -> 390 px e 700 -> 701 -> 375 px, nei due temi. Una pagina corretta
all'apertura puo' conservare dimensioni intrinseche obsolete dopo il resize:
il 2026-10-12 questo controllo ha rilevato 520 px di documento su viewport 390.

## Eccezioni e falsi positivi evitati

- `alt=""` e' valido per immagini decorative; viene segnalata solo l'assenza dell'attributo.
- La 404 e `/le-mie-sottolineature/` sono volutamente fuori sitemap. La raccolta personale non ha
  un'entita' pubblica e non richiede JSON-LD.
- Il breadcrumb visibile e' obbligatorio solo sulle pagine citazione, opera e raccolta, dove il
  template lo prevede; sulle altre pagine resta obbligatorio il `BreadcrumbList` strutturato.
- Un heading dello stesso livello o di livello superiore e' valido; viene segnalato solo un salto
  in discesa, per esempio da `h2` a `h4`.
- Gli scroller orizzontali intenzionali con `overflow-x:auto` o `scroll` non sono segnalati se il
  loro contenitore resta dentro la viewport.
- I link esterni non vengono aperti dal controllo locale: sono dati editoriali e richiedono la
  verifica delle fonti prevista da `CLAUDE.md`.
