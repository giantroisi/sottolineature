# Keyword — scrematura, mappatura e piano d'uso

Documento operativo del 2026-08-28. Estensione di `SEO.md`; il lavoro spuntabile sta nella
roadmap di `CLAUDE.md` (Fase 7).

**Dati di partenza:** export fornito dall'utente da uno strumento professionale — 6.000 keyword,
colonne Keyword / Intent / Vol / Concorrenza / CPC / andamento mensile / KD / KO.
Volume grezzo sommato: **333.780 ricerche/mese**.

**File prodotti:**
- `archivio/sottolineature-keyword-map.xlsx` — foglio di lavoro completo (Sintesi, Keywords,
  Opere, Autori, Da acquisire, Raccolte candidate, Escluse). *Non versionato* (`archivio/` è
  in `.gitignore`), è lo strumento di lavoro umano.
- `data/keywords.json` — versione dati, versionata, leggibile da `tools/build.py`.

**Due avvertenze da tenere presenti ogni volta che si guardano questi numeri:**

1. **I volumi sono stime dello strumento, non dati di Google.** Servono a ordinare le priorità,
   non a fare previsioni. Non scrivere da nessuna parte "questa pagina porterà N visite".
2. **La classificazione è un primo passaggio automatico, precisione stimata attorno al 90%.**
   Ogni riga va confermata a occhio prima di diventare una pagina. La colonna "copertura" è un
   indicatore grezzo (corrispondenza di radici di parola nel testo della citazione e nel contesto):
   dice *dove guardare*, non *quali citazioni scegliere*. La selezione delle citazioni di una
   raccolta si fa leggendole, come tutto il resto del progetto.

---

## 1. Il difetto della lista, da correggere prima di rifare l'analisi

Tutte e 6.000 le keyword contengono la radice *citazion-*. La lista è stata generata a partire da
un unico seme. Ne restano fuori interi universi di ricerca:

| Seme | Presenza nella lista |
|---|---|
| citazioni / citazione | 6.000 |
| frasi / frase | 106 (solo perché co-occorrono con "citazioni") |
| aforismi | 115 |
| massime, detti, proverbi, pensieri | 25 |

**In Italia il volume su *frasi* è più alto di quello su *citazioni*.** *frasi 1984*,
*frasi sulla vita*, *frasi belle sui libri* sono query che questa lista non vede affatto.

**Da fare:** un secondo export con semi `frasi`, `aforismi`, `massime`, `pensieri`, e con i semi
di entità (`frasi + <titolo>`, `frasi + <autore>`) per i 40 titoli e i 199 autori già in archivio.
Finché non c'è, tutto quello che segue va letto come **la metà della fotografia**.

---

## 2. Come sono state scremate

Dedup per significato prima di tutto: *citazioni amore* / *citazioni sull'amore* / *citazioni
d'amore* / *citazioni damore* sono **una sola** intenzione. Da 6.000 righe si scende a
**3.990 gruppi**; 2.010 keyword erano varianti.

Poi cinque filtri, in quest'ordine:

1. **Intento incompatibile** — la query chiede qualcosa che non siamo (riassunti, trame, pdf,
   "come citare in bibliografia", atti giudiziari).
2. **Fuori ambito** — la query non riguarda citazioni *da libri*.
3. **Entità in archivio** — l'opera o l'autore c'è già: la keyword mappa su una pagina esistente.
4. **Entità non in archivio** — l'opera o l'autore non c'è: diventa lista della spesa, non pagina.
5. **Tema o raccolta** — tutto il resto, raggruppato per argomento e confrontato con la copertura
   reale dell'archivio.

### Il risultato, ed è la cosa più importante di tutto il documento

| Classe | Keyword | Volume | % del volume |
|---|---:|---:|---:|
| Tema o raccolta | 4.298 | 183.410 | **54,9%** |
| Fuori ambito | 843 | 55.560 | 16,6% |
| Testa generica (*citazioni*, *citazioni famose*, *citazioni belle*) | 134 | 51.950 | 15,6% |
| Autore in archivio | 424 | 21.000 | 6,3% |
| Autore o opera **non** in archivio | 137 | 12.290 | 3,7% |
| Opera in archivio | 147 | 8.100 | 2,4% |
| Intento incompatibile | 17 | 1.470 | 0,4% |

**Solo l'8,7% del volume mappa su pagine che il sito ha già.** Il 54,9% sta su query tematiche a
cui, con 262 citazioni, l'archivio non può ancora rispondere onestamente. Il 32,6% va scartato.

La conclusione non è confortante ma è quella giusta: **il collo di bottiglia non è più
l'architettura, è la dimensione dell'archivio.** L'impianto costruito nelle fasi 0-5 è
sovradimensionato rispetto al contenuto che deve distribuire. Questa lista, quindi, serve
soprattutto come **elenco di ciò che conviene raccogliere**, e solo in seconda battuta come
piano editoriale.

---

## 3. Cosa fare, in ordine

### A. Ottimizzare quello che c'è già (nessun contenuto nuovo, resa immediata)

Le 40 pagine opera e le 199 pagine autore esistono: vanno solo allineate al modo in cui le persone
cercano. Title e H1 devono contenere **sia "frasi" sia "citazioni"** in forma naturale.

Le entità con più domanda, tutte con pagina già online:

| Volume | Pagina | Citazioni in archivio |
|---:|---|---:|
| 1.680 | `/opere/antoine-de-saint-exupery-il-piccolo-principe/` | 2 |
| 1.610 | `/autori/oscar-wilde/` | 1 |
| 1.580 | `/autori/william-shakespeare/` | 2 |
| 1.220 | `/autori/dante-alighieri/` | 2 |
| 970 | `/autori/gabriele-d-annunzio/` | 1 |
| 730 | `/autori/cesare-pavese/` | 2 |
| 720 | `/autori/giacomo-leopardi/` | 2 |
| 700 | `/autori/luigi-pirandello/` | 2 |
| 670 | `/autori/seneca/` | 1 |
| 650 | `/autori/alda-merini/` | 1 |
| 470 | `/opere/j-r-r-tolkien-il-signore-degli-anelli/` | 1 |
| 420 | `/opere/jane-austen-orgoglio-e-pregiudizio/` | 1 |

Salta all'occhio: **le pagine con più domanda sono anche quelle con meno citazioni.** Oscar Wilde
ha 1.610 di volume e **una** citazione. Prima ancora di ritoccare i title, questi sono i 12 autori
su cui aggiungere citazioni: è lo stesso lavoro che serve alle raccolte, fatto dove rende di più.

### B. Pagine opera da creare (l'opera è in archivio, la pagina no)

Da valutare una per una, con la regola della Fase 4 — **serve una scheda verificata, e con una
sola citazione la pagina citazione è già la pagina dell'opera**:

| Volume | Opera | Citazioni |
|---:|---|---:|
| 770 | Alice nel paese delle meraviglie — Lewis Carroll | 1 |
| 290 | Il grande Gatsby — F. Scott Fitzgerald | 1 |
| 280 | Cime tempestose — Emily Brontë | 1 |
| 220 | L'amore ai tempi del colera — García Márquez | 1 |
| 170 | Cent'anni di solitudine — García Márquez | 2 |
| 170 | Oceano mare — Alessandro Baricco | 1 |
| 160 | Piccole donne — Louisa May Alcott | 1 |

Tutte tranne una hanno **una sola citazione**. La mossa corretta non è creare sette pagine opera
sottili: è **portare queste opere a 2-3 citazioni** e poi creare la pagina. Nel frattempo la
pagina citazione fa già il suo lavoro.

### C. Raccolte pronte da costruire subito (6)

Copertura sufficiente in archivio, verificata sul testo delle citazioni:

| Volume | Raccolta | Citazioni disponibili (frase / frase+contesto) |
|---:|---|---|
| 3.420 | viaggio e cammino | 8 / 13 |
| 2.370 | donne | 5 / 15 |
| 860 | felicità | 10 / 11 |
| 680 | ricordo e memoria | 8 / 19 |
| 350 | occhi e sguardo | 8 / 10 |
| 320 | notte | 8 / 11 |

Regola invariata: **≥8 citazioni pertinenti scelte leggendole, più un'introduzione scritta a mano.**
Se leggendole se ne salvano meno di 8, la raccolta non si pubblica e passa al punto E.

### D. Raccolte quasi pronte (4) — mancano 2-4 citazioni ciascuna

bellezza (630), sogni (570), cambiamento (350), tristezza (210).

### E. La lista della spesa: cosa raccogliere, in ordine di ritorno

Sono i temi con la domanda più alta e la copertura più bassa. **Questa è la vera indicazione
operativa che esce dalla lista keyword:**

| Volume | Tema | Citazioni in archivio |
|---:|---|---:|
| 3.940 | **amicizia** | 3 |
| 1.730 | guerra | 1 |
| 1.350 | natura | 3 |
| 1.180 | animali | 1 |
| 1.110 | filosofia | 0 |
| 1.040 | musica | 1 |
| 1.000 | montagna | 2 |
| 900 | figli | 1 |
| 770 | infanzia e bambini | 1 |
| 760 | lavoro | 1 |
| 590 | pace | 1 |

**Amicizia è il buco più grande del sito:** quasi 4.000 di volume e tre citazioni. Dieci citazioni
verificate sull'amicizia valgono più di dieci pagine nuove costruite sul contenuto che c'è.

### F. Autori e opere da acquisire

| Volume | Chi/cosa | Nota |
|---:|---|---|
| 1.870 | Bukowski | in commercio, serve edizione italiana tracciabile |
| 1.860 | Harry Potter | J.K. Rowling è già in archivio con una citazione |
| 1.460 | Sant'Agostino | pubblico dominio, verifica agevole |
| 830 | Nietzsche | pubblico dominio |
| 730 | Ready Player One | narrativa contemporanea, sotto copyright |
| 620 | Freud | pubblico dominio in traduzione da verificare |
| 550 | Platone / 440 Socrate / 300 Aristotele | pubblico dominio |
| 550 | Chiamami col tuo nome | sotto copyright |
| 540 | Camilleri | sotto copyright |
| 430 | Schopenhauer | pubblico dominio |

Da fare prima gli autori di pubblico dominio: verifica più rapida, fonte primaria linkabile,
nessun problema di diritti. **Attenzione:** filosofi e classici greco-latini allargano il perimetro
del sito oltre "citazioni da libri" — è una scelta di identità, non solo di SEO. Va decisa
dall'utente prima di partire, non data per scontata perché il volume è alto.

### G. Cosa si scarta, e perché (32,6% del volume)

| Volume | Motivo | Esempi |
|---:|---|---|
| 14.540 | film, serie TV, franchise | Harry Potter (film), Peaky Blinders, Star Wars, cartoni animati |
| 9.700 | ricorrenze e auguri | compleanno, matrimonio, buongiorno, Natale |
| 8.570 | altra lingua o dialetto | citazioni latine, napoletane, in inglese |
| 7.140 | personaggi non letterari | Einstein, Gandhi, Steve Jobs, Van Gogh |
| 6.140 | musica e canzoni | testi di canzoni, rapper, Sanremo |
| 3.890 | social, immagini, meme | per Instagram, sfondi, "citazioni improbabili" |
| 2.740 | motivazionale e business | coaching, leadership, vendite |
| 1.470 | intento non servibile | riassunti, trame, pdf, tesine |
| 1.280 | religiose non letterarie | Bibbia, Vangelo, Papa Francesco |
| 1.020 | sport | |
| 540 | bibliografia e ambito giuridico | "come citare in APA", atto di citazione |

**Non sono keyword sbagliate: sono keyword di un altro sito.** Inseguirle significherebbe
pubblicare frasi non tracciabili a un testo pubblicato, cioè rompere la regola su cui è costruito
tutto il progetto. Il caso più insidioso è *citazioni latine* (8.570 con le altre lingue): sembra
letterario e non lo è — sono massime senza opera di riferimento, esattamente ciò che `metodo.html`
promette di non fare. Se un giorno si vorrà entrare lì, si entra con Seneca, Cicerone e Marco
Aurelio **citati per opera e libro**, non con un elenco di motti.

Le keyword di **testa** (*citazioni*, *citazioni famose*, *citazioni belle*: 51.950, il 15,6%) non
si inseguono con pagine dedicate: sono la home e l'indice `/citazioni/`. Non creare mai una pagina
"citazioni belle".

---

## 4. Le regole che restano valide qualunque cosa dica la lista

1. **Una keyword non genera una pagina.** Le pagine sono quelle previste dall'architettura; le
   keyword decidono solo l'ordine in cui si riempiono.
2. **Nessuna pagina prima del contenuto.** Raccolta = ≥8 citazioni scelte leggendole +
   introduzione scritta a mano. Pagina opera = scheda verificata. Nessuna eccezione per volume alto.
3. **Un intento, una pagina.** Se una keyword può stare sia su un tema sia su una raccolta, decide
   una sola pagina; l'altra la linka. La cannibalizzazione tra `/temi/` e `/raccolte/` è il rischio
   numero uno di questa fase.
4. **Volume alto non è una ragione sufficiente.** *Citazioni latine* e *citazioni motivazionali*
   hanno volume: non hanno una fonte tracciabile a un testo pubblicato.
5. **La lista non decide l'identità del sito.** Filosofi antichi, autori sotto copyright, temi
   fuori dal perimetro letterario: sono decisioni dell'utente, prese prima di raccogliere.

## 5. Procedura, passo per passo

1. **Secondo export** con i semi `frasi`, `aforismi`, `massime` e con i semi di entità. Rifare
   la mappatura unendo i due file. *(Serve l'utente e il suo strumento.)*
2. **Ottimizzazione title/H1** delle 40 pagine opera e delle 199 pagine autore, con l'ordine di
   priorità del punto A. Lavoro sui generatori, nessun contenuto nuovo.
3. **Lotto citazioni "amicizia"** — 10-12 citazioni verificate. È il buco più grande.
4. **Le 6 raccolte pronte**, una alla volta: selezione leggendo, introduzione, pubblicazione.
5. **Lotti citazioni sugli autori a più alta domanda** (Wilde, Shakespeare, Dante, D'Annunzio,
   Pavese, Leopardi, Pirandello, Seneca, Merini) fino a 3-4 citazioni a testa.
6. **Pagine opera** per i titoli del punto B che nel frattempo sono arrivati a 2+ citazioni.
7. **Decisione dell'utente** su filosofi antichi e autori contemporanei sotto copyright, poi
   eventuali lotti di acquisizione.
8. Rivedere `data/keywords.json` dopo ogni lotto: le raccolte in lista d'attesa che superano la
   soglia si spostano da sole in "pronta".

## 6. Comando per Sonnet 5

```
Leggi CLAUDE.md, SEO.md e SEO-KEYWORDS.md, poi apri data/keywords.json.

Esegui il punto 2 della procedura di SEO-KEYWORDS.md: allineare title e H1 delle pagine opera e
autore alla domanda di ricerca reale, usando in modo naturale sia "frasi" sia "citazioni"
(es. "Frasi e citazioni da 1984 di George Orwell", "Frasi e citazioni di Oscar Wilde").

Vincoli:
- Solo title, meta description e H1. Non toccare il testo delle citazioni, gli autori, i titoli,
  gli anni, i contesti o le fonti. Non aggiungere parole chiave nel corpo delle pagine.
- Le modifiche passano dai generatori in tools/, mai a mano sui file generati.
- Nessun title duplicato: il build deve continuare a fallire se ne trova due uguali.
- Non creare nessuna pagina nuova in questo passaggio.

Poi rilancia python3 tools/build.py, verifica il rapporto finale, e riportami quante pagine hanno
cambiato title, quante description, e se qualche controllo è fallito. Aggiorna la Fase 7 in
CLAUDE.md spuntando ciò che hai chiuso.
```

---

## 7. Aggiornamento del 2026-08-30: 16 raccolte diventate pubblicabili — tutte pubblicate lo stesso giorno

La copertura era stata calcolata quando l'archivio aveva 262 citazioni. Il 2026-08-30 ne aveva
621, e il quadro era cambiato senza che nessuno se ne accorgesse: **sedici raccolte avevano
superato la soglia delle otto citazioni pertinenti**. Sono state pubblicate tutte, una alla volta,
nell'ordine di domanda di ricerca, leggendo i candidati (non limitandosi a contarli) e scrivendo
un'introduzione a mano per ciascuna — dettagli lotto per lotto in `LOG.md`. Numero finale di
citazioni pubblicate per raccolta (diverso dal conteggio-candidati della tabella originale,
perché la lettura ha scartato i falsi positivi lessicali):

| Volume | Raccolta | Citazioni pubblicate | Stato |
|---:|---|---:|---|
| 3.420 | viaggio e cammino | 14 | pubblicata |
| 2.370 | donne | 11 | pubblicata |
| 1.730 | guerra | 10 | pubblicata |
| 1.350 | natura | 10 | pubblicata |
| 1.180 | animali | 11 | pubblicata |
| 900 | figli | 9 | pubblicata |
| 860 | felicita | 9 | pubblicata |
| 770 | infanzia | 9 | pubblicata |
| 760 | lavoro | 10 | pubblicata |
| 680 | ricordo e memoria | 10 | pubblicata |
| 530 | famiglia | 10 | pubblicata |
| 530 | arte | 9 | pubblicata |
| 350 | occhi e sguardo | 9 | pubblicata |
| 320 | notte | 9 | pubblicata |
| 300 | stelle e cielo | 9 | pubblicata |
| 220 | silenzio | 9 | pubblicata |

Nessuna raccolta e' stata scartata: tutte e sedici hanno superato agevolmente la soglia minima di
otto citazioni genuinamente pertinenti dopo la lettura manuale. Restano vicine alla soglia (5-7
citazioni, da riprendere in un lotto futuro se l'archivio cresce): musica, montagna, pace, cibo,
speranza, inverno, denaro, liberta come prigionia.

**Vale sempre la regola:** il numero dice dove guardare, non quali citazioni scegliere. Una
raccolta si pubblica solo dopo aver letto le citazioni candidate e aver scritto l'introduzione a
mano; se leggendole se ne salvano meno di otto, la raccolta non si pubblica.

`data/keywords.json` e' stato aggiornato: le sedici raccolte hanno ora verdetto "pubblicata"
insieme alle dieci gia' pubblicate in precedenza.
