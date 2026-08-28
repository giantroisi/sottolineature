# Catalogo — regole di ampliamento

Documento operativo del 2026-08-28, nato dalla decisione dell'utente: **il catalogo può crescere,
purché restino citazioni da libri.** Qui c'è cosa significa in pratica, cosa entra, cosa no, e in
che ordine conviene raccogliere. Vale insieme a `CLAUDE.md` (costituzione e metodo di verifica),
`SEO.md` (architettura) e `SEO-KEYWORDS.md` (dove sta la domanda).

Fotografia al momento della scrittura: **283 citazioni, 206 autori**.

---

## 1. Il perimetro, in una riga

> **Entra solo ciò che è tracciabile a un'opera scritta e pubblicata, con il punto preciso del
> testo in cui si trova.**

Questa riga fa tutto il lavoro, e risolve da sola i casi dubbi:

| Caso | Verdetto | Perché |
|---|---|---|
| Nietzsche, *Così parlò Zarathustra* | **entra** | è un libro, con parte e capitolo |
| Sant'Agostino, *Confessioni* | **entra** | è un libro, con libro e paragrafo |
| Marco Aurelio, *Colloqui con se stesso* | **entra** | è un libro, con libro e paragrafo |
| Seneca, *Lettere a Lucilio* | **entra** | è un libro, con numero di lettera |
| Socrate | **non entra come autore** | non ha scritto nulla: la frase è di Platone, e va attribuita a Platone con il dialogo |
| "Citazioni latine", massime, motti | **non entrano** | non hanno un'opera di riferimento |
| Einstein, Gandhi, Steve Jobs | **non entrano** | frasi che circolano senza testo pubblicato tracciabile |
| Battuta di un film tratto da un libro | **non entra** | è dello sceneggiatore, non del romanzo — regola già in `CLAUDE.md` |
| Testo di una canzone | **non entra** | non è un libro |

**Quindi sì ai filosofi, ai classici greci e latini, ai saggi, alla poesia — a patto che si citi
l'opera.** Non è un allargamento del perimetro: è lo stesso perimetro applicato con coerenza.
La domanda giusta non è "questo autore è un romanziere?" ma "posso indicare pagina, capitolo o
paragrafo?".

Un solo avvertimento di equilibrio: se i filosofi diventassero metà del catalogo, il sito
smetterebbe di essere quello che è. Tetto ragionevole: **non più del 15% delle citazioni da
filosofia e classici non narrativi**, saggistica compresa.

---

## 2. Requisiti d'ingresso di una citazione

Una citazione entra solo se ha **tutte** queste cose. Se ne manca una, si scarta e si annota il
motivo in `LOG.md` — non si pubblica "in attesa di completare".

1. **Testo esatto**, verificato secondo le regole di `CLAUDE.md` (Wikisource o edizione originale;
   Wikiquote solo con riferimento a capitolo/edizione e mai da sola; altrimenti due fonti
   indipendenti concordanti).
2. **Autore, titolo, anno** corretti — l'anno è quello della prima pubblicazione dell'opera.
3. **Luogo nel testo**: capitolo, parte, libro, canto, verso, atto/scena, numero di lettera o
   paragrafo. *Oggi 253 citazioni su 283 ce l'hanno: da qui in avanti è un requisito d'ingresso,
   non un lavoro di recupero.*
4. **Traduttore ed edizione**, quando il testo è tradotto. Una traduzione diversa è un testo
   diverso: senza sapere quale si è usata, la citazione non è verificabile.
5. **Contesto** in linguaggio semplice, prima la storia poi il nome — regola già in uso.
6. **Copertina** verificata guardandola, o nessuna copertina (la tile placeholder si genera da sé).
7. **Categoria** (uno dei 7 umori) e, se pertinente, uno o più generi.
8. **La citazione deve reggersi da sola.** Chi non ha letto il libro deve capirla leggendo la
   frase più il contesto. Se per capirla serve la trama, non è una citazione: è un estratto.

**Collegamento alla fonte online quando esiste** (Wikisource, Liber Liber, Gutenberg): oggi ce
l'hanno solo 39 citazioni su 283. È il contenuto che nessun aggregatore ha — vale più di venti
citazioni nuove senza fonte.

---

## 3. Attribuzione: a chi appartiene la frase

- **All'autore che ha scritto**, non a chi parla. Zarathustra → Nietzsche. Il Grande Inquisitore
  → Dostoevskij. Francesca da Rimini → Dante. Chi parla va nel contesto, dove è interessante.
- **Al testo che la contiene per primo.** Se una frase compare in un'opera e viene ripresa
  altrove, si cita l'originale.
- **Mai a un personaggio storico che non l'ha scritta.** Socrate si cita come Platone, *Fedone*.
- Un'attribuzione sbagliata già pubblicata si corregge e si annota (è già successo con Mahfouz:
  la frase era di *Vicolo del mortaio*, non de *Il palazzo del desiderio*).

---

## 4. Lunghezza e diritti

*Nota: non sono indicazioni legali, sono criteri prudenziali di redazione. Per una valutazione
giuridica serve un avvocato.*

- **Autori di pubblico dominio** (in Italia, di norma 70 anni dalla morte dell'autore): testo
  libero. **Attenzione alla traduzione**, che ha un copyright proprio e più recente: una
  traduzione moderna di Dostoevskij non è di pubblico dominio anche se Dostoevskij lo è. Per i
  tradotti conviene o una traduzione storica libera, o una citazione breve con traduttore indicato.
- **Autori sotto copyright**: citazione **breve**, sempre con autore, opera ed edizione. Criterio
  pratico del progetto: **massimo 3 righe, indicativamente 40 parole.** Oggi la media è di 18
  parole e solo 15 citazioni superano le 40: la regola è già rispettata di fatto, va solo scritta.
- Mai riprodurre un brano lungo, una poesia intera o una porzione che sostituisca la lettura.
- La fonte va sempre indicata: è anche la condizione che rende legittima la citazione.

---

## 5. Equilibrio del catalogo — dove è sbilanciato oggi

I numeri servono a scegliere i prossimi lotti, non a fare pulizia di quelli passati.

**Per secolo dell'opera:**

| Secolo | Citazioni | Nota |
|---|---:|---|
| XX | 173 (61%) | fortemente sovrarappresentato |
| XIX | 55 (19%) | |
| XXI | 36 (13%) | |
| Dal XV al XVIII | 13 (4,6%) | **quasi assente** |
| Antichità e Medioevo | 1 | **assente** |

Il catalogo è per tre quarti novecentesco. È anche il quarto meno utile: i classici sono di
pubblico dominio (verifica rapida, fonte linkabile), sono ciò che si studia a scuola, e sono la
metà del pubblico che il progetto dichiara di voler servire. **Il riequilibrio verso i classici è
la direttrice principale di crescita.**

**Per umore:** verità 80, vita 56, tempo 39, amore 36, coraggio 30, libertà 22, solitudine 20.
"Verità" fa da raccoglitore di tutto ciò che non sta altrove: nei prossimi lotti conviene
assegnarla solo quando è davvero il tema, e alimentare le tre categorie più magre.

**Per autore:** 156 autori su 206 hanno **una sola** citazione, 19 ne hanno 3 o più. Questa è la
ragione per cui 180 pagine autore rischiavano il `noindex`. **Approfondire vale più che allargare:**
portare 30 autori da 1 a 3 citazioni è più utile che aggiungere 60 autori nuovi.

**Per genere:** solo 38 citazioni su 283 hanno un genere. Non è un problema di per sé — i generi
sono un filtro, non una tassonomia — ma horror (4) e saggistica (6) sono sotto la soglia dei 4+
titoli che li giustifica.

---

## 6. Fonti, in ordine di preferenza

1. **Wikisource** (it e altre lingue) — testo integrale, citabile per capitolo, collegabile.
2. **Liber Liber** e **Progetto Gutenberg** — classici italiani e stranieri di pubblico dominio.
3. **Perseus Digital Library** per i greci e i latini, con riferimento canonico (libro, paragrafo).
4. **Internet Archive** in prestito digitale, per verificare un'edizione moderna.
5. **Google Libri**, solo dove l'anteprima mostra davvero il passo.
6. **Sito dell'editore** per le edizioni italiane recenti.
7. **Wikiquote** — mai come fonte unica, solo se riporta già capitolo/edizione, e sempre da
   riscontrare altrove.

**Da non usare mai come fonte:** aggregatori di frasi, Pinterest, raccolte social, elenchi di
"frasi celebri" senza riferimento. Sono la ragione per cui il 90% delle citazioni in circolazione
in italiano è sbagliato o mal attribuito.

---

## 7. Piano dei lotti, in ordine di ritorno

Lotti da **10-15 citazioni**, mai di più: oltre quella soglia la verifica si degrada e gli errori
passano. Ogni lotto si chiude con `python3 tools/build.py`, una riga in `LOG.md` e un commit.

**Lotto 1 — Amicizia (10-12 citazioni).** È il buco più grande del sito: 3.940 di volume di
ricerca contro 3 citazioni. Dove cercare, tutto pubblico dominio: Cicerone *De amicitia*,
Montaigne *Saggi* (I, 28), Manzoni, Dumas *I tre moschettieri*, Twain, Dickens. Da verificare uno
per uno — questi sono punti di partenza per la ricerca, non citazioni già validate.

**Lotto 2 — Approfondire i 9 autori a più alta domanda**, portandoli a 3-4 citazioni: Wilde
(oggi 1), Shakespeare (2), Dante (2), D'Annunzio (1), Pavese (2), Leopardi (2), Pirandello (2),
Seneca (1), Merini (1). Tutti già in archivio, quasi tutti di pubblico dominio: è il lavoro con il
rapporto sforzo/risultato migliore di tutti.

**Lotto 3 — Classici e filosofi citati per opera**, per riequilibrare il secolo: Agostino
*Confessioni*, Platone *Fedone* e *Repubblica*, Marco Aurelio *Colloqui con se stesso*, Seneca
*Lettere a Lucilio*, Epitteto *Manuale*, Boezio *Consolazione della filosofia*, Nietzsche
*Così parlò Zarathustra*, Schopenhauer *Aforismi sulla saggezza del vivere*. Tetto del 15%.

**Lotto 4 — Canone scolastico italiano poco coperto**, per le pagine opera che hanno domanda e
una citazione sola: Ariosto, Tasso, Goldoni, Alfieri, Foscolo, Verga, Deledda, Svevo, Saba,
Montale, Quasimodo, Calvino, Morante, Ginzburg.

**Lotto 5 — Temi con domanda e copertura vicina alla soglia**: bellezza, sogni, cambiamento,
tristezza. Bastano 2-4 citazioni ciascuno per sbloccare quattro raccolte.

**Lotto 6 — Temi con domanda alta e copertura quasi nulla**: guerra (1.730 di volume, 1 citazione),
natura (1.350 / 3), animali (1.180 / 1), musica (1.040 / 1), montagna (1.000 / 2), figli (900 / 1),
infanzia (770 / 1), lavoro (760 / 1), pace (590 / 1).

**Lotto 7 — Contemporanei sotto copyright**, con citazione breve e fonte completa: Bukowski
(1.870 di volume), Camilleri (540), e gli autori richiesti già in sospeso — Sarah J. Maas e Leigh
Bardugo, che restano da fare da tempo perché manca una fonte italiana tracciabile.

**Regola che vale su tutti i lotti:** non si aggiunge una citazione *perché serve a riempire una
casella*. Prima deve essere una buona citazione; il tema è il criterio di ricerca, non di
accettazione. Una raccolta con otto citazioni mediocri vale meno di una raccolta che non esiste.

---

## 8. Procedura per ogni lotto

1. Scegliere il lotto dal punto 7 e cercare i candidati sulle fonti del punto 6.
2. Verificare ogni citazione: testo esatto, autore, opera, anno, luogo nel testo, traduttore.
3. Scartare senza rimpianti ciò che non si riesce a collocare, annotando il motivo.
4. Scrivere il contesto (prima la storia, poi il nome), assegnare umore e generi.
5. Cercare la copertina su Open Library **e guardarla** prima di accettarla; verificare che
   l'autore corrisponda, non fidarsi del match sul titolo.
6. Inserire in `index.html` a mano, poi `python3 tools/build.py`.
7. **Controlli automatici prima del commit:** nessun contesto identico su due citazioni diverse,
   nessuna fonte identica su due citazioni diverse, nessun title duplicato, nessuna citazione
   senza luogo nel testo.
8. Riga in `LOG.md` con il formato in uso, commit, push, conferma del deploy.

## 9. Comando per Sonnet 5

```
Leggi CLAUDE.md, CATALOGO.md e SEO-KEYWORDS.md.

Esegui il Lotto 1 di CATALOGO.md: 10-12 citazioni sull'amicizia da libri, verificate.

Vincoli, in ordine di importanza:
- Vale il perimetro del punto 1 di CATALOGO.md: entra solo ciò che è tracciabile a un'opera
  scritta e pubblicata, con il punto preciso del testo. Niente massime senza opera, niente frasi
  da film, niente aggregatori come fonte.
- Ogni citazione deve avere tutti i requisiti del punto 2: testo verificato, autore/titolo/anno,
  luogo nel testo (capitolo, libro, canto, verso, lettera), traduttore ed edizione se tradotta,
  contesto, umore, copertina guardata o nessuna copertina.
- Se non riesci a collocare una citazione nel testo, SCARTALA e annota il motivo in LOG.md.
  Meglio consegnare 7 citazioni solide che 12 con tre incerte.
- Dai la precedenza al pubblico dominio, dove puoi anche allegare il link alla fonte
  (Wikisource, Liber Liber, Gutenberg, Perseus).
- Non modificare nessuna citazione già presente.

Prima di inserire qualsiasi cosa, mostrami l'elenco dei candidati con testo, autore, opera, anno,
luogo nel testo e fonte, e aspetta il mio ok. Poi inserisci in index.html, lancia
python3 tools/build.py, esegui i controlli del punto 8, scrivi la riga in LOG.md e aggiorna
CLAUDE.md.
```

---

## 10. Lavoro in autonomia — parametri

Quando l'utente autorizza un agente a procedere da solo, valgono questi parametri. Sono scritti
per essere applicati senza interpretazione: se una decisione non rientra qui, ci si ferma e si chiede.

### Cosa si può fare senza chiedere

Cercare e verificare candidati; scartare; scrivere contesto, umore, generi; recuperare la
copertina; inserire le card in `index.html`; lanciare `tools/build.py`; eseguire i controlli;
scrivere in `LOG.md`; aggiornare la roadmap di `CLAUDE.md`; fare commit e push.

### Cosa richiede sempre l'ok dell'utente

- Modificare il **perimetro** del punto 1, o superare il tetto del 15% per filosofia e classici
  non narrativi.
- Introdurre un **nuovo umore o un nuovo genere** (per i generi resta la regola dei 4+ titoli).
- Pubblicare una **raccolta con meno di 8 citazioni**, o una **pagina opera senza scheda scritta**.
- Citare un autore sotto copyright **oltre le ~40 parole**.
- Qualsiasi modifica a `index.html` che non sia l'aggiunta o la correzione di una card.
- Rimuovere una citazione già pubblicata. *(Correggere un errore accertato si fa invece subito,
  annotandolo: la correttezza viene prima.)*

### Parametri numerici di un lotto

| Parametro | Valore |
|---|---|
| Citazioni per lotto | 10-15, mai di più |
| Fonti richieste per citazione | 1 primaria, oppure 2 indipendenti concordanti |
| Citazioni per autore | max 4 (6 solo per i maggiori già presenti con 3+) |
| Citazioni dalla stessa opera | max 3 |
| Umore dominante in un lotto | max 30% delle citazioni del lotto |
| Umori da alimentare per primi | solitudine, libertà, coraggio (i più magri) |
| Umore "verità" | assegnarlo solo quando è davvero il tema, non come raccoglitore |
| Quota di opere anteriori al 1900 | almeno metà del lotto, finché il Novecento resta sopra il 55% |
| Citazioni con link a fonte primaria | almeno metà del lotto |
| Lunghezza | max ~40 parole; oltre, solo se pubblico dominio e con una ragione |

### Condizioni di arresto (fermarsi e riferire, non insistere)

- Si scarta **più della metà** dei candidati di un lotto: il filone è esaurito o le fonti sono
  deboli. Meglio cambiare lotto che abbassare l'asticella.
- Non si trova una fonte primaria o due fonti concordanti **per più di metà** dei candidati.
- Un controllo automatico fallisce e la causa non è chiara.
- Si scopre un errore in una citazione già pubblicata: si corregge, si annota, **si riferisce**.
- Si sta per prendere una decisione che rientra nell'elenco "richiede sempre l'ok".

### Controlli obbligatori prima di ogni commit

1. Nessun testo di citazione duplicato nell'archivio.
2. Nessun contesto identico su due citazioni diverse *(è già successo)*.
3. Nessuna fonte identica su due citazioni diverse.
4. Nessun title o meta description duplicati dopo il build.
5. Nessuna citazione priva del luogo nel testo.
6. Ogni copertina nuova **guardata**, non solo accettata dal match sul titolo *(è già capitato che
   un `cover_i` corretto fosse la scansione di una scheda scolastica)*.

### Ritmo e tracciamento

Un lotto alla volta, chiuso completamente prima di aprire il successivo: verifica → inserimento →
build → controlli → riga in `LOG.md` → commit. La roadmap di `CLAUDE.md` si aggiorna a fine
sessione o ogni tre lotti, quello che viene prima. **Mai spuntare una voce "quasi fatta".**

### La regola che sta sopra tutte

Nel dubbio si scarta. Una citazione in meno non si vede; una citazione sbagliata su un sito che
si presenta come verificato a mano toglie credibilità a tutte le altre.
