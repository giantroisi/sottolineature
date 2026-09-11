# «Cita questa frase» — brief

Data: 11 settembre 2026. Intervento su sottolineature.it.
Da fare DOPO i cinque di SEO-INTERVENTI-2026-09-10.md, o insieme al
numero 2 (che riorganizza il blocco .actions della pagina citazione).

## Perché

Le query reali di sottolineature in Search Console non sono «frasi di X».
Su 39 query, il gruppo più numeroso è fatto da persone che **digitano un
verso** per sapere da dove viene: «amor ch'a nullo amato amar perdona»
compare in otto grafie diverse, poi «l'inferno sono gli altri», «e il
naufragar m'è dolce in questo mare significato».

Non cercano una frase da postare: cercano una fonte. E gli aggregatori
che occupano quelle SERP — frasicelebri.it, libreriamo.it, aforisticamente,
Pinterest — non dicono mai da quale capitolo viene la frase.

Sottolineature quel dato ce l'ha per quasi tutte le citazioni, e non lo
mostra in forma utilizzabile. Questo intervento lo rende usabile.

Effetto collaterale utile lato ricerca: il blocco introduce nelle pagine
le parole «capitolo», «edizione», «traduttore», che sono il vocabolario
di chi studia.

## I dati, e quanto sono coperti

Da data/citazioni.json, su 846 citazioni:

    quote, author, title, year   846  (100%)
    source_locus                 843  (100%)
    source_url                   600  ( 71%)
    source_edition               551  ( 65%)
    source_translator            425  ( 50%)
    speaker                      101  ( 12%)

Quindi una citazione completa si può comporre per praticamente tutte.

## Cosa fare

Aggiungere alla pagina citazione un blocco «Come si cita questa frase»
con il testo già pronto e un pulsante per copiarlo.

### Formato

Una forma sola, senza inversione cognome/nome — il nome va scritto come
sta nel dato:

    <Autore>, «<citazione>», <Titolo>[, trad. di <Traduttore>]
    [, <edizione>], <anno>, <locus>. Testo: <source_url>

Esempio reale:

    Alessandro Manzoni, «Il coraggio, uno, non se lo può dare»,
    I promessi sposi, edizione definitiva, 1840, capitolo XXV.
    Testo: https://it.wikisource.org/wiki/I_promessi_sposi_(1840)/Capitolo_XXV

NON invertire in «Manzoni, A.»: l'archivio contiene Sant'Agostino, Marco
Aurelio, Omero, J.R.R. Tolkien, Fëdor Dostoevskij. L'inversione
automatica sbaglia su troppi casi e il guadagno è nullo.

### Regole sui campi mancanti

- `source_translator` vuoto  -> si omette il segmento «trad. di …»
- `source_edition` vuoto     -> si omette
- `source_url` vuoto         -> si omette la frase «Testo: …»
- `source_locus` vuoto (3 casi) -> si omette, e il blocco si genera lo stesso
- Se mancano sia locus sia edizione sia url, il blocco NON si mostra:
  meglio niente che una citazione che non serve a citare.

### Dove e come

- Il blocco sta **dopo il contesto**, insieme agli altri controlli
  (vedi l'intervento 2 di SEO-INTERVENTI-2026-09-10.md, che sposta
  .actions dopo .quote-detail).
- Deve funzionare **senza JavaScript**: il testo della citazione va
  renderizzato nell'HTML, non costruito al volo. Un `<details>` con
  dentro il testo selezionabile è sufficiente e coerente con lo stile del
  sito. Il pulsante «copia» è un `js-only` che si aggiunge sopra, come già
  avviene per «Copia citazione».
- Riusare il meccanismo di copia già presente nella pagina, non
  scriverne uno nuovo.
- Nessun markup nuovo se si può evitare: usare le classi esistenti.

### Schema

Se la pagina ha già un nodo `Quotation` o `CreativeWork`, aggiungere la
stringa della citazione come `citation`. Non inventare tipi nuovi e non
toccare il `BreadcrumbList`.

## Cosa NON fare

- Non toccare il `<title>` né l'`<h1>` delle pagine citazione: verificato
  il 4 settembre su 749 pagine che il formato attuale è migliore
  dell'alternativa.
- Non aggiungere pagine.
- Non generare la citazione in più formati (APA, MLA, Chicago): sono
  norme anglosassoni, il pubblico è italiano e scolastico, e ogni formato
  in più è una superficie in più che si può sbagliare.

## Verifica

1. `python3 tools/build.py` chiude con 0 problemi, `check_links` 0,
   `controlla_jsonld` 0.
2. Su /citazioni/alessandro-manzoni-i-promessi-sposi-addio-monti-sorgenti/
   il blocco mostra capitolo VIII ed edizione 1840.
3. Su una citazione tradotta (per esempio una di Dostoevskij) compare
   «trad. di …».
4. Su una citazione senza edizione il segmento è assente e la frase resta
   grammaticale — nessuna virgola doppia, nessuno spazio prima del punto.
5. Contare quante pagine generano il blocco: atteso ~843 su 846.
6. Con JavaScript disattivato il testo della citazione è comunque
   leggibile e selezionabile.
7. Ricordare che l'HTML generato è tracciato in git e Vercel non fa build:
   committare anche le pagine rigenerate.
