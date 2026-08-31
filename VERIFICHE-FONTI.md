# Verifica delle fonti — 2026-08-31

Le 23 citazioni che il build segnalava senza blocco fonte, controllate una per una sul testo
pubblicato o sull'originale in lingua. Il metodo è quello del sito: **non entra niente che non sia
tracciabile a un'opera scritta e pubblicata, con il punto preciso del testo.** Aggregatori di frasi,
Goodreads, Pinterest e blog di citazioni non contano come fonte, mai — sono il posto da cui questi
errori sono partiti.

Esito finale: **13 compilate**, **3 corrette**, **5 tolte dal catalogo**. Le otto decisioni di
contenuto sono state prese dall'utente il 2026-08-31 e sono eseguite; l'archivio è passato da 621 a
616 citazioni e **tutte e 616 hanno ora il punto del testo**.

---

## Compilate

Per ognuna il punto del testo è accertato. Dove edizione e traduttore sono vuoti, non li ho potuti
confermare su una fonte editoriale: meglio un campo vuoto che un dato inventato.

| Autore, opera | Punto del testo | Nota |
|---|---|---|
| Victor Hugo, *Notre-Dame de Paris* | libro IX, cap. IV «Grès et cristal» | francese verificato su Wikisource |
| Octavio Paz, *Il labirinto della solitudine* | cap. I «El pachuco y otros extremos» | spagnolo verificato su due PDF indipendenti |
| Stefan Zweig, *Novella degli scacchi* | racconto del dottor B. sull'isolamento | trad. Silvia Montis, Newton Compton 2014 |
| Arundhati Roy, *Il dio delle piccole cose* | cap. 12 «Kochu Thomban» | trad. Chiara Gabutti, Guanda 1997 |
| Toni Morrison, *Sula* | parte «1937», risposta a Eva | originale inglese verificato |
| J.K. Rowling, *Harry Potter e i Doni della Morte* | cap. 35 «King's Cross» | trad. Beatrice Masini, Salani 2008 |
| Amin Maalouf, *Il manoscritto di Samarcanda* | incipit del romanzo | francese verificato su Internet Archive |
| Roberto Bolaño, *2666* | parte quinta, «La parte di Arcimboldi» | trad. Ilide Carmignani, Adelphi |
| Haruki Murakami, *1Q84* | Libro 1, cap. 15 | trad. Giorgio Amitrano, Einaudi 2011 |
| Elena Ferrante, *Storia del nuovo cognome* | parte seconda, l'esame di maturità di Elena | edizioni e/o, 2012 |
| Fernando Pessoa, *Tabacaria* | incipit | opera corretta in parallelo: non è il *Libro dell'inquietudine* |
| Louisa May Alcott, *Piccole donne* | parte seconda, cap. 44 | |
| Rainer Maria Rilke, *Lettere a un giovane poeta* | quarta lettera, 16 luglio 1903 | |

### Riserve sul testo, da controllare sul cartaceo

Il **punto** è certo, la **formulazione italiana** no. Sono differenze reali, non pignolerie: in
quattro casi la frase pubblicata dal sito dice qualcosa che l'originale non dice.

- **Ferrante** — la citazione con i puntini fabbrica una frase che nel libro non esiste. Il testo è:
  «Penso che la bellezza sia un inganno. *Come il giardino leopardiano? Non sapevo niente di giardini
  leopardiani, ma risposi: Sì. Come il mare in un giorno sereno. O come un tramonto. O come il cielo
  di notte.* È cipria passata sopra l'orrore. *Se la si toglie, restiamo soli col nostro spavento.*»
  Manca uno scambio di battute intero e la chiusa, che è la parte che dà senso a tutto.
- **Murakami, *1Q84*** — l'inglese dice «there's salvation in life», non «una grande consolazione»,
  e dice «even one person» (anche una sola persona), non «anche se si è soli»: probabilmente è da lì
  che nasce l'errore. La formulazione del sito è da considerare non attestata.
- **Murakami, *Kafka sulla spiaggia*** — nell'originale è una **tempesta di sabbia** (砂嵐), non una
  tempesta generica, e il passo è l'incipit del libro, non il capitolo 5 come si legge in rete.
- **Bolaño** — la frase gemella che segue, «Scrivere, invece, è quasi sempre vuoto», è il contrappeso
  su cui l'antitesi regge; tagliata, la citazione dice mezza cosa.
- **Roy** — nel testo c'è l'inciso «questo è sicuro» e una seconda frase, «Nessuna bestia può
  uguagliarne la portata e la potenza».
- **Zweig** — la frase attacca con «Perché come è noto», che la lega al ragionamento precedente.
- **Rilke** — «Sii paziente...» è una ri-traduzione dall'inglese che circola online; Rilke dà del
  **Lei** a Kappus. Da riallineare all'edizione Adelphi (trad. Leone Traverso).
- **Alcott** — la frase è un troncamento: «Lovely weather so far; I don't know how long it will last,
  but I'm not afraid of storms...». Ed è **Amy**, non Jo. Il cap. 44 appartiene alla parte del 1869,
  che in Italia esce come *Piccole donne crescono*: opera e anno andrebbero corretti.
- **Hugo** — manca *souvent*: «continua **spesso** a verdeggiare», non «anche».
- **Morrison** — «make somebody else» risponde letteralmente a «have some babies»: è un rifiuto della
  maternità, non un aforisma sull'autodeterminazione. Il contesto va tenuto presente.

---

## Decise ed eseguite il 2026-08-31

Otto citazioni non potevano restare come stavano. L'utente ha deciso; qui c'è cosa è stato fatto e
perché, così fra un anno si sa. Ogni URL sparito ha il suo redirect 301 in `tools/redirects.json`:
nessuna pagina rimasta a 404.

### Opera corretta — la frase è autentica, sbagliato era il libro

1. **Simone Weil** — «L'attenzione è la forma più rara e più pura della generosità» non è in
   *L'ombra e la grazia*. È una **lettera a Joë Bousquet del 13 aprile 1942**, il poeta rimasto
   paralizzato da una ferita della Grande Guerra. Controllato il testo francese integrale della
   *Pesanteur et la grâce*: «générosité» non compare nel capitolo sull'attenzione né altrove.
   → opera e anno corretti, contesto riscritto, 301 dal vecchio indirizzo.
2. **Elias Canetti** — non è in *Auto da fé* ma è un appunto del **1944** nella *Provincia dell'uomo*
   (Adelphi 1978, trad. Furio Jesi). Prova decisiva: la traduzione di Jesi coincide **parola per
   parola** con la frase che il sito pubblicava, quindi veniva da lì.
   → opera, anno e traduttore corretti, contesto riscritto, 301.

### Testo ripristinato

3. **Suzanne Collins** — «Che i giochi abbiano inizio» non è una citazione, è un modo di dire. La
   battuta esiste, per intero e con chi la pronuncia: **Claudius Templesmith**, in chiusura del
   **capitolo 10**, «Signore e signori, che i settantaquattresimi Hunger Games abbiano inizio!».
   → testo sostituito con quello completo, contesto riscritto, 301 (cambiando il testo cambia lo slug).

### Tolte dal catalogo

Nessuna di queste cinque era tracciabile a un punto del testo. La regola del sito è quella, e
tenerle valeva meno che perderle.

4. **J.M. Barrie, «Solo chi sogna può volare!»** — non è nel romanzo. Nel testo integrale di *Peter
   and Wendy* «dream/dreams» ricorre tre volte e mai a proposito del volo; nel libro si vola con i
   «lovely wonderful thoughts» e la polvere di fata. In più «Le avventure di Peter Pan» è il titolo
   del **cartone Disney del 1953**, non del romanzo del 1911: la citazione sbagliava frase e opera.
   Era l'unica citazione di Barrie, quindi è sparita anche la sua pagina autore → 301 su `/autori/`.
   Era anche in due raccolte, «Frasi brevi» e «I sogni»: tolta da entrambe. «I sogni» scendeva così
   a 7 citazioni, sotto la soglia di 8, e sarebbe uscita di pubblicazione: rimpiazzata con Erri De
   Luca, *Montedidio* — «in italiano esistono due parole, sonno e sogno, dove il napoletano ne porta
   una sola, suonno» — e riscritta la chiusa dell'introduzione, che citava proprio Barrie.
5. **Sibilla Aleramo, *Una donna*** — la più netta, perché il testo è **fuori diritti e integrale**
   su Gutenberg e Internet Archive: cercate «fusione», «complementari», «armonioso», nessuna
   occorrenza. Frase fluttuante.
6. **Amos Oz, *Una storia di amore e di tenebra*** — nessuna fonte oltre a un blog, che peraltro la
   riporta più lunga e diversa. Da cercare, se mai si riaprisse, nei capitoli sul prozio Yosef
   Klausner (trad. Elena Loewenthal, Feltrinelli 2003).
7. **Alba de Céspedes, *Quaderno proibito*** — risulta stampata **sulla copertina dell'Oscar
   Mondadori 1978** come richiamo editoriale, e non è mai stata associata a una voce del diario. Il
   diario di Valeria va dal 26 novembre 1950 al 27 maggio 1951: è lì che andrebbe cercata.
8. **Naguib Mahfouz, *Vicolo del mortaio*** — in arabo la frase affine dice un'altra cosa: «com'è
   brutta una parola d'amore quando sfugge da una bocca annoiata, **come uno sputo**!». La versione
   italiana perde la similitudine e aggiunge «pronunciata freddamente».

Nell'occasione sono stati chiusi anche tre 404 vecchi, rimasti da rimozioni precedenti senza
redirect: *Barbablù* di Amélie Nothomb, *Gelo* di Thomas Bernhard e una delle *Anime morte* di
Gogol', più le pagine autore di Nothomb e Bernhard.

---

## Perché conta

Un sito che dichiara «citazioni verificate a mano, senza algoritmo» vive di questo. Cinque di queste
otto erano esattamente il tipo di frase che gira in rete staccata dal libro: attribuita all'opera
sbagliata, tagliata fino a dire un'altra cosa, o inventata di sana pianta e appiccicata a un titolo
famoso. Sono uscite. Le 616 rimaste hanno tutte un punto del testo.
