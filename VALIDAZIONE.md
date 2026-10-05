# Validazione strutturale

Il controllo riusabile e' `python3 tools/check_links.py`. Esamina tutte le pagine HTML pubblicate
e termina con codice 1 quando trova un errore verificabile. `python3 tools/build.py` lo esegue
automaticamente in modalita' diagnostica: il referto resta visibile, ma non blocca la generazione.
Questo evita che un'euristica interrompa un lotto editoriale; prima di pubblicare, il comando
diretto deve comunque chiudersi con `Problemi totali: 0`.

## Cosa controlla

- un solo `title`, una sola meta description, un solo canonical e valori unici nel sito;
- canonical uguale all'URL pubblico pulito;
- esattamente un `<h1>` e un `<main>` per pagina, senza salti nella gerarchia degli heading;
- breadcrumb visibile sulle pagine di dettaglio che lo prevedono e tipi JSON-LD minimi per rotta;
- URL interni puliti, link risolvibili, pagine non orfane;
- sitemap figlie valide e coerenza in entrambe le direzioni (URL->file e pagina indicizzabile->sitemap);
- ogni immagine con attributo `alt`; file locali, copertine, tassonomia e traduttori restano coperti
  dai controlli gia' presenti nello stesso script.

La validita' interna dei grafi JSON-LD e' verificata anche da `tools/controlla_jsonld.py`, richiamato
dal build subito dopo il controllo strutturale.

## Controllo mobile

Lo scorrimento orizzontale dipende da layout, font e viewport e non e' verificabile leggendo il solo
HTML. Dopo una modifica a markup o CSS si apre la pagina a 375x812 e 390x844 e si esegue
`tools/check_mobile_overflow.js` nel contesto della pagina. L'esito corretto ha `ok: true`, larghezza
del documento non superiore alla viewport e nessun elemento in `offenders`. Va ripetuto almeno su
home, una citazione, un autore e la tipologia di pagina modificata.

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
