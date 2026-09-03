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

## 3-bis. Come si classifica: tema e genere

**Questa sezione nasce da un errore vero, il 2026-08-31.** Erano finite in archivio 162 citazioni
con un genere scritto nel campo del tema («Narrativa», «Saggistica», «Poesia») o con temi inventati
(«arte», «morte», «Teatro»), e 164 con generi fuori elenco. Guardando l'ordine di inserimento si
vedono **21 citazioni consecutive marcate con lo stesso valore**, e giornate intere in cui più della
metà del lotto porta la stessa etichetta: il 30 agosto 86 citazioni su 154, il 29 agosto il 53% su
«verità». Non è un giudizio preso frase per frase, è un timbro applicato a un blocco. Il danno non
si vede subito: una citazione con un tema che non esiste **non compare in nessun filtro e in nessun
hub**, si raggiunge solo dalla ricerca.

### Il tema — obbligatorio, uno solo, fra questi sette

Si legge la citazione e si sceglie. Non esistono altri valori: quelli in `tools/labels.py` sono
tutti, e sono in minuscolo senza accenti (`liberta`, `verita`).

| Tema | Quando |
|---|---|
| `vita` | il vivere di ogni giorno, il mondo com'è, crescere, gli incipit che aprono una scena o presentano una persona. È il tema largo: quando nessun altro calza meglio, sta qui — non in `verita` |
| `amore` | amore, amicizia, legami familiari, desiderio, tenerezza, cura |
| `coraggio` | affrontare la paura, resistere, insistere, osare, il coraggio di scegliere |
| `liberta` | potere, oppressione, politica, regole, autonomia, dissenso, ingiustizia |
| `tempo` | memoria, invecchiare, il passare delle cose, passato e futuro, la morte come fine |
| `solitudine` | stare soli, sentirsi estranei, il silenzio, l'esilio, il non essere capiti |
| `verita` | **solo quando la verità, la conoscenza o l'inganno sono il soggetto della frase**: cosa possiamo sapere, cosa ci illude, l'arte che dice il vero. Non è il posto delle citazioni «di pensiero» in generale |

### Il genere — facoltativo, e appartiene all'opera

Sei valori, in `tools/labels.py`: `fantasy`, `fantascienza`, `distopia`, `horror`, `saggistica`,
`poesia`. Due regole:

1. **Il genere è una proprietà dell'opera, non della citazione.** Due righe dallo stesso libro hanno
   sempre lo stesso genere. Si decide guardando il libro, non la frase.
2. **Nel dubbio si lascia vuoto.** Il campo vuoto è la norma: oggi 405 opere su 523 non hanno
   genere, ed è giusto così. «Narrativa» non è un genere su un sito di citazioni da libri: lo sono
   quasi tutte. Un genere entra solo se dice davvero come si legge quel testo.

### Errori da non rifare

- **Non inventare valori.** Nessun tema o genere fuori dai due elenchi. Introdurne uno nuovo
  richiede l'ok dell'utente (§10), e per i generi vale la regola dei 4+ titoli.
- **Non scrivere un genere nel campo del tema.** Sono due campi diversi e non si sostituiscono.
- **Attenzione alle maiuscole.** `Fantascienza` non è `fantascienza`: il filtro non lo riconosce e
  la citazione sparisce dagli hub senza che nessuno se ne accorga.
- **Non timbrare un lotto.** Se in un lotto di dieci citazioni più di quattro finiscono nello stesso
  tema, quasi sempre è pigrizia, non un caso: si rilegge. Un archivio equilibrato oggi sta intorno a
  25/15/14/13/13/11/9 — un tema largo e sei specifici.

### Verifica, sempre

Dopo l'inserimento si lancia `python3 tools/build.py`. Da 2026-08-31 `check_links.py` confronta ogni
tema e ogni genere con `labels.py` e li conta fra i problemi, stampando accanto i valori validi.
**Se il build segnala anche un solo valore inesistente, non si fa commit: si corregge.**

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

> **Correzione di rotta del 2026-08-30.** Fotografia dell'archivio a 493 citazioni e 251 autori:
> **49 autori con una sola citazione, 176 con esattamente due, appena 26 con tre o piu'**, media
> 1,96. Il Novecento e' ancora il 58% e le opere anteriori al 1800 sono 36 su 493.
> I lotti hanno funzionato ma si sono fermati a meta': l'approfondimento si arresta a 2 citazioni
> per autore invece delle 3-4 previste, e nel frattempo entrano autori nuovi che ripartono da 1.
> Il risultato e' un archivio larghissimo e sottile, con quasi tutte le pagine autore sulla soglia
> minima.
>
> **Da qui in avanti, fino a nuovo ordine: nessun autore nuovo.** Si portano a 4 citazioni gli
> autori gia' presenti con piu' domanda di ricerca (elenco in `data/keywords.json`, foglio
> *Autori*), dando la precedenza a opere anteriori al Novecento. Un autore si considera chiuso a 4,
> non a 2.



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

**Il rovescio della stessa regola:** otto è la soglia sotto la quale una raccolta non si pubblica,
non la taglia a cui deve restare. Una raccolta si amplia ogni volta che entra in archivio una
citazione che le appartiene. Per ritrovare quelle già in archivio e mai valutate:

```
python3 tools/raccolte_da_ampliare.py            # quante candidate ha ciascuna
python3 tools/raccolte_da_ampliare.py mare       # le candidate, con la chiave da incollare
```

Lo strumento non decide niente: elenca le citazioni che nominano le parole della raccolta e che la
raccolta non contiene. Quali meritino di entrarci si legge una per una — è l'unica differenza fra
una selezione curata e un elenco generato da una parola chiave, ed è quella che `metodo.html`
promette a chi legge.

---

## 8. Procedura per ogni lotto

> **Attenzione:** dal 2026-08-28 (Fase 2 SEO) la fonte di verità delle citazioni è
> `data/citazioni.json`, non `index.html`. La home è generata da `tools/generate_home.py` e non
> pubblica il contesto, che resta esclusivo di `/citazioni/<slug>/`.

1. Scegliere il lotto dal punto 7 e cercare i candidati sulle fonti del punto 6.
2. Verificare ogni citazione: testo esatto, autore, opera, anno, luogo nel testo, traduttore.
3. Scartare senza rimpianti ciò che non si riesce a collocare, annotando il motivo.
4. Scrivere il contesto (prima la storia, poi il nome), assegnare umore e generi.
5. Cercare la copertina su Open Library **e guardarla** prima di accettarla; verificare che
   l'autore corrisponda, non fidarsi del match sul titolo.
6. Inserire la citazione in **`data/citazioni.json`**, che dalla Fase 2 SEO è la fonte di verità
   (`index.html` è un file generato: modificarlo a mano si perde al build successivo). Poi
   `python3 tools/build.py`, che rigenera home, pagina citazione, hub, immagini OG e sitemap.
6-ter. **Il contesto si scrive fra le 60 e le 90 parole.** È l'unico testo originale della pagina
   citazione: la frase è di altri, il blocco fonte è un dato, i tag e le correlate sono
   impaginazione. Un contesto deve dire **in che punto dell'opera siamo** e **perché quella frase
   conta lì**. Sotto le 40 parole quasi sempre si è solo detto dove sta la frase — «L'incipit del
   romanzo» ripete il luogo nel testo e non aggiunge niente; sopra le 90 si comincia a girare
   intorno, e si vede. Modello di riferimento, 43 parole già pubblicate: *«È don Abbondio a dirlo
   al cardinal Federigo Borromeo, che lo rimprovera per essersi rifiutato di celebrare il
   matrimonio…»* — chi parla, a chi, in quale momento, e cosa c'è in gioco.

   Non si allunga un contesto per farlo arrivare a 60 parole. Se non si sa altro dell'opera di
   quanto già scritto, si lascia com'è e si annota: un contesto corto e vero vale più di uno lungo
   e inventato. Per l'elenco di quelli da riprendere, in ordine di resa:

   ```
   python3 tools/contesti_da_ampliare.py            # da quali opere conviene cominciare
   python3 tools/contesti_da_ampliare.py 12         # le schede pronte, con testo, luogo, edizione
   python3 tools/contesti_da_ampliare.py --dialoghi # quelle che hanno un personaggio
   ```

6-quater. **`speaker`: chi pronuncia la frase.** Campo facoltativo di `data/citazioni.json`. Si
   compila **solo quando il luogo nel testo o il contesto dicono chi parla**, e resta vuoto per il
   narratore, per la voce dell'autore e in ogni caso di dubbio. Non si deduce dal titolo
   dell'opera: dedurlo è inventarlo. Quando c'è, l'H1 della pagina diventa *«Se vogliamo che tutto
   rimanga com'è…»: la frase di **Tancredi** in «Il Gattopardo» di Giuseppe Tomasi di Lampedusa*,
   e il dato finisce anche in `spokenByCharacter` dei dati strutturati. È la forma in cui la gente
   cerca davvero una battuta: prima il personaggio, poi l'autore.

6-bis. **Guardare se la citazione appartiene a una raccolta esistente**, e in quel caso aggiungere
   la sua chiave in `quote_keys` dentro `data/raccolte.json`. Dieci secondi per citazione. È il
   passaggio che per due settimane non è esistito, ed è il motivo per cui il 2026-09-03 le
   ventisette raccolte contenevano 234 citazioni su 749: erano state riempite fino alla soglia
   minima di otto e mai più riaperte, mentre l'archivio raddoppiava. Le raccolte non sono
   interrogazioni che si aggiornano da sole: sono elenchi scritti a mano, e restano fermi finché
   qualcuno non li tocca.
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
  contesto, tema, copertina guardata o nessuna copertina.
- Il tema si sceglie leggendo la citazione, una per una, secondo la tabella del punto 3-bis: e' il
  punto dove si e' gia' sbagliato timbrando lotti interi con lo stesso valore. Il genere appartiene
  all'opera e nel dubbio resta vuoto. Nessun valore fuori da tools/labels.py, maiuscole comprese.
- Se non riesci a collocare una citazione nel testo, SCARTALA e annota il motivo in LOG.md.
  Meglio consegnare 7 citazioni solide che 12 con tre incerte.
- Dai la precedenza al pubblico dominio, dove puoi anche allegare il link alla fonte
  (Wikisource, Liber Liber, Gutenberg, Perseus).
- Non modificare nessuna citazione già presente.

Prima di inserire qualsiasi cosa, mostrami l'elenco dei candidati con testo, autore, opera, anno,
luogo nel testo e fonte, e aspetta il mio ok. Poi inserisci in data/citazioni.json, lancia
python3 tools/build.py, esegui i controlli del punto 8, scrivi la riga in LOG.md e aggiorna
CLAUDE.md.
```

---

## 9-bis. Comandi in coda per Sonnet

Scritti qui perché non vadano persi con la conversazione in cui sono nati. Si danno **uno per
volta**, e mai mentre un lotto è a metà: interrompere un lotto lo lascia a pezzi.

| | lotto | stato |
|---|---|---|
| 1 | Riscrittura dei contesti brevi | **in corso** (2026-09-03, lotto 6) |
| 2 | Genere alle opere che ne sono prive | **il prossimo** — comando qui sotto |
| 3 | Ampliamento delle 20 raccolte tematiche rimaste | in coda, `tools/raccolte_da_ampliare.py` |
| 4 | «Frasi brevi» e «Incipit memorabili» | in coda, criterio diverso: vedi nota in fondo |
| 5 | Copertine delle 169 opere rimaste | bloccato: su Open Library non esiste un'edizione italiana con immagine. Si sblocca solo cambiando fonte o accettando l'edizione originale — decisione dell'utente |

### 2. Genere alle opere che ne sono prive

```
Leggi CLAUDE.md e CATALOGO.md, in particolare il punto 3-bis sulla classificazione.

Compito: assegnare il GENERE alle opere che ne sono prive. Solo il campo `genre` di
data/citazioni.json, più LOG.md. Non toccare testo, autore, contesto, tema, fonte.

LEGGI QUESTO PRIMA DI COMINCIARE, perché il compito non è quello che sembra. Le opere senza
genere sono 367 su 577, ma NON sono 367 caselle da riempire. I generi ammessi sono sei e sono
stretti: distopia, fantascienza, fantasy, horror, poesia, saggistica. Un romanzo realista —
Moravia, Ferrante, Camus, Austen, Tolstoj — non è nessuno dei sei, e il suo campo genere deve
restare vuoto. È il comportamento corretto, non una mancanza.

Quello che devi cercare sono le opere che UNO DEI SEI lo hanno davvero e a cui non è stato
assegnato: una raccolta di poesie senza `poesia`, un saggio senza `saggistica`, un romanzo di
fantascienza senza `fantascienza`. Mi aspetto qualche decina, non trecento. Se arrivi a
centocinquanta, ti sei messo a timbrare — ed è esattamente l'errore che questo archivio ha già
pagato una volta, quando 162 temi erano stati assegnati a lotti.

Per l'elenco delle opere da esaminare:

  python3 - <<'EOF'
  import json, collections
  qs=json.load(open('data/citazioni.json',encoding='utf-8'))
  op=collections.defaultdict(list)
  for q in qs: op[(q['author'],q['title'])].append(q)
  senza=sorted([k for k,v in op.items() if not any(x.get('genre') for x in v)])
  print(len(senza),'opere senza genere')
  for a,t in senza:
      q=op[(a,t)][0]
      print('%-28s %-40s %s' % (a[:28], t[:40], q.get('year','')))
  EOF

Regole:
1. Il genere appartiene all'OPERA, non alla citazione: se lo assegni, lo assegni a tutte le
   citazioni di quell'opera.
2. Un'opera può avere più generi separati da spazio (es. "fantascienza distopia"), ma solo se li
   ha entrambi davvero.
3. Nessun valore fuori da tools/labels.py, maiuscole comprese: sono minuscoli.
4. Nel dubbio si lascia vuoto. Sempre. "Forse è saggistica" significa no.
5. `poesia` va all'opera in versi (una raccolta, un poema, una singola poesia), non a un romanzo
   lirico. `saggistica` va a un testo che argomenta, non a un romanzo con dentro delle idee. Se
   questa distinzione ti sembra sottile su un caso, quel caso resta vuoto.
6. Lavora a lotti di 40 opere, non tutte in una volta.

Poi `python3 tools/build.py` e verifica che check_links dia zero problemi: se segnala anche un
solo genere inesistente, non fare commit.

In LOG.md, per ogni lotto: quante opere hai classificato, il conteggio per genere, e — la parte
che conta — tre o quattro esempi di opere che hai LASCIATO VUOTE e perché. Se su quaranta ne
classifichi otto, va benissimo.

Regole di convivenza: lavori in parallelo a un'altra sessione. Tocca solo data/citazioni.json e
LOG.md. Niente in tools/, templates/, assets/, né altri file .md. Mai `git stash`,
`git checkout -- .`, `git reset --hard`, `git clean`: se trovi modifiche non tue, lasciale e
committa solo i tuoi file elencandoli uno per uno. Prima di ogni push: `git pull --rebase`.
```

### Nota sul lotto 4

«Frasi brevi» e «Incipit memorabili» hanno un criterio meccanico — la lunghezza, il punto nel
testo — quindi `tools/raccolte_da_ampliare.py` le trova tutte (158 e 140 candidate) e la
tentazione è di incollarle in blocco. Allora però smettono di essere selezioni e diventano
elenchi, che è esattamente ciò che `metodo.html` promette di non essere. Vanno fatte a parte, e
la domanda non è «parla di questo» ma «questa frase regge da sola»: un giudizio molto più
difficile da delegare, da dare con un comando scritto apposta.

---

## 10. Lavoro in autonomia — parametri

Quando l'utente autorizza un agente a procedere da solo, valgono questi parametri. Sono scritti
per essere applicati senza interpretazione: se una decisione non rientra qui, ci si ferma e si chiede.

### Cosa si può fare senza chiedere

Cercare e verificare candidati; scartare; scrivere contesto, tema e genere **seguendo il punto
3-bis** (uno per uno, mai a lotti, mai valori inventati); recuperare la copertina; inserire le citazioni in `data/citazioni.json`; lanciare `tools/build.py`; eseguire i controlli;
scrivere in `LOG.md`; aggiornare la roadmap di `CLAUDE.md`; fare commit e push.

### Cosa richiede sempre l'ok dell'utente

- Modificare il **perimetro** del punto 1, o superare il tetto del 15% per filosofia e classici
  non narrativi.
- Introdurre un **nuovo umore o un nuovo genere** (per i generi resta la regola dei 4+ titoli).
- Pubblicare una **raccolta con meno di 8 citazioni**, o una **pagina opera senza scheda scritta**.
- Citare un autore sotto copyright **oltre le ~40 parole**.
- Qualsiasi modifica a `data/citazioni.json` che non sia l'aggiunta o la correzione di una
  citazione, e qualsiasi modifica ai generatori in `tools/`.
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
