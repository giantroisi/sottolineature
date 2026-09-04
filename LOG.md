# Log

- 2026-09-03 UTC — **campo `speaker` e misura vera dei contesti brevi** (nessuna citazione aggiunta
  o tolta). Aggiunto a `data/citazioni.json` il campo facoltativo **`speaker`**: chi pronuncia la
  frase. Quando c'è, l'H1 della pagina diventa *«Se vogliamo che tutto rimanga com'è…»: la frase di
  **Tancredi** in «Il Gattopardo» di Giuseppe Tomasi di Lampedusa*, e il nome finisce in
  `spokenByCharacter` dei dati strutturati. È la forma in cui la gente cerca una battuta: prima il
  personaggio, poi l'autore.
  - **45 speaker compilati, nessuno dedotto.** Vengono tutti da `source_locus`, cioè da un dato già
    verificato citazione per citazione: «parole di Tancredi», «battuta di Smerdjakov», «riflessione
    di Santiago», «monologo del capitano Nemo», «battuta di Atticus Finch». Dove il luogo nel testo
    dice «riflessione della narratrice», «lettera del 13 aprile 1942» o «discorso di laurea a
    Kenyon College» il campo resta vuoto: non c'è un personaggio, c'è l'autore o una voce senza
    nome. Nessun nome ricavato dal titolo dell'opera o dalla memoria.
  - **I contesti brevi non sono 623.** Il numero dell'avviso di `check_links` è vero ma grosso, e
    messo così porta fuori strada. La distribuzione: **2 assenti** (Dostoevskij *Delitto e
    castigo*, Sciascia *Il giorno della civetta*); **169 fra 1 e 19 parole**, di cui 147 sotto le
    15, e la maggioranza dice solo «L'incipit del romanzo», che ripete il luogo nel testo senza
    aggiungere niente; **159 fra 20 e 29**, spesso una frase sola; **293 fra 30 e 44**, che sono
    già buoni — densi e precisi, allungarli li annacquerebbe; **126 sopra le 45**, a posto. Il
    lavoro che rende è sui primi due scaglioni: **171 citazioni, non 623.**
  - Aggiunto `tools/contesti_da_ampliare.py`: le ordina per opera (un contesto scritto bene su
    un'opera da cui il sito cita quattro volte vale quattro volte) e stampa per ciascuna la scheda
    già pronta — testo, luogo nel testo, edizione, link online, contesto attuale, e l'avviso quando
    la frase sembra una battuta e quindi vuole anche `speaker`.
  - Scritti in `CATALOGO.md` i punti **6-ter** (il contesto sta fra 60 e 90 parole, e non si
    allunga per arrivarci: un contesto corto e vero vale più di uno lungo e inventato) e
    **6-quater** (quando si compila `speaker` e quando si lascia vuoto).
  - Build pulita, `check_links` 0 problemi su 1120 pagine.

- 2026-08-30 UTC — added 10 quotes, dodicesima applicazione della correzione di rotta (total now 621, 251 autori, 46 con una sola citazione, 83 con tre o più) — cinque autori ad alta domanda di ricerca portati a **4 citazioni ciascuno**: Goliarda Sapienza (+2, da L'arte della gioia cap. 42 e cap. 63 — unica opera disponibile su Wikiquote per quest'autrice, ricca comunque di materiale con locus per capitolo), Wisława Szymborska (+2, dalla poesia "La cipolla" in Grande numero p. 9 e da "Il silenzio delle piante" in Attimo p. 33 — diversificando da Amore a prima vista e Nulla è in regalo!), Antonio Tabucchi (+2, gli incipit di La testa perduta di Damasceno Monteiro e di Tristano muore. Una vita — diversificando da Sostiene Pereira), Natalia Ginzburg (+2, l'incipit de La famiglia Manzoni e da Le piccole virtù p. 149 — quest'ultima già presente con locus diverso, p. 121), Charles Dickens (+2, gli incipit di Grandi speranze, via Fruttero & Lucentini, e di Canto di Natale, trad. Maria Luisa Fehr, RCS 1997 — diversificando da Racconto di due città e Oliver Twist). Nessuna sovrapposizione con le citazioni già in archivio. Nessuna copertina reperibile per nessuna delle nuove opere. Build pulita, 0 errori. Nessuna attività concorrente rilevata in questo giro. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-30 UTC — added 10 quotes, undicesima applicazione della correzione di rotta (total now 611, 251 autori, 46 con una sola citazione, 78 con tre o più) — cinque autori ad alta domanda di ricerca portati a **4 citazioni ciascuno**: Milan Kundera (+2, gli incipit di L'immortalità e di La lentezza, entrambi Adelphi — diversificando da L'insostenibile leggerezza dell'essere e Il libro del riso e dell'oblio), Alberto Moravia (+2, gli incipit di Il conformista e di La noia — evitata La ciociara per i suoi temi legati alla guerra, diversificando da Gli indifferenti), Sibilla Aleramo (+2, da Amo dunque sono pp. 35 e 112 — diversificando da Una donna), Sylvia Plath (+2, dalle poesie "Specchio" p. 209 in Attraversando l'acqua e "Tempi normali" p. 239 in Il colosso — evitati i versi da Papà e Lady Lazarus per i loro temi più cupi e politicamente carichi, diversificando da La campana di vetro), Simone Weil (+2, l'incipit de La rivelazione greca e da Riflessioni sulle cause della libertà e dell'oppressione sociale p. 13 — diversificando da L'ombra e la grazia). Nessuna sovrapposizione con le citazioni già in archivio. Nessuna copertina reperibile per nessuna delle nuove opere. Build pulita, 0 errori. Nessuna attività concorrente rilevata in questo giro. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-30 UTC — added 11 quotes, decima applicazione della correzione di rotta (total now 601, 251 autori, 46 con una sola citazione, 73 con tre o più) — cinque autori ad alta domanda di ricerca portati a **4 citazioni ciascuno**: Jack Kerouac (+3, gli incipit di I vagabondi del Dharma, I sotterranei e Angeli di desolazione — partiva da una sola citazione, ora chiuso), Isaac Asimov (+2, da La fine dell'Eternità cap. 18 e da Destinazione Cervello — diversificando da Fondazione e dal Book of Science and Nature Quotations), Elsa Morante (+2, gli incipit di Aracoeli ed Menzogna e sortilegio, entrambi Einaudi — diversificando da La Storia e L'isola di Arturo), Grazia Deledda (+2, da La chiesa della solitudine, in Dieci romanzi, Newton Compton 1994, e l'incipit di Fior di Sardegna, Modernissima 1923 — diversificando da Canne al vento ed Elias Portolu), Philip Roth (+2, gli incipit di Zuckerman scatenato e di Addio, Columbus — evitati Il teatro di Sabbath e La lezione di anatomia per i loro temi più espliciti, diversificando da Pastorale americana). Nessuna sovrapposizione con le citazioni già in archivio. Nessuna copertina reperibile per nessuna delle nuove opere. Build pulita, 0 errori. Nessuna attività concorrente rilevata in questo giro. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-30 UTC — added 11 quotes, nona applicazione della correzione di rotta (total now 590, 251 autori, 47 con una sola citazione, 68 con tre o più) — sei autori ad alta domanda di ricerca portati a **4 citazioni ciascuno**: Alessandro Manzoni (+1, da Adelchi atto V scena VIII vv. 342-343 — diversificando da I promessi sposi e Il cinque maggio), Antoine de Saint-Exupéry (+2, gli incipit di Terra degli uomini, trad. Renato Prinzhofer, Mursia 1988, e di Volo di notte, trad. Cesare Giardini, Oscar Mondadori 2001 — diversificando da Il piccolo principe), Giovanni Pascoli (+2, dalle poesie "Novembre" in Myricae e "Il gelsomino notturno" in Canti di Castelvecchio — diversificando da X Agosto e Il lampo), Virgilio (+2, dalle Bucoliche, egloga II v. 17 "Nimium ne crede colori" ed egloga X v. 69 "Omnia vincit Amor" — diversificando dall'Eneide), Rainer Maria Rilke (+2, l'incipit e pp. 2-3 de I quaderni di Malte Laurids Brigge, trad. Furio Jesi, Garzanti — diversificando dalle Lettere a un giovane poeta), Leonardo Sciascia (+2, gli incipit de Il Consiglio d'Egitto e di Una storia semplice, Adelphi 1989 — diversificando da Il giorno della civetta e A ciascuno il suo). Nessuna sovrapposizione con le citazioni già in archivio. Nessuna copertina reperibile per nessuna delle nuove opere. Build pulita, 0 errori. Nessuna attività concorrente rilevata in questo giro. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-30 UTC — added 10 quotes, ottava applicazione della correzione di rotta (total now 579, 251 autori, 47 con una sola citazione, 63 con tre o più) — cinque autori ad alta domanda di ricerca portati a **4 citazioni ciascuno**: Zadie Smith (+2, due brevi aforismi da articoli su Internazionale, "Il fallimento riuscito" n. 725 e "Il blues della biblioteca" n. 958 — la pagina Wikiquote per quest'autrice contiene quasi solo interviste, non citazioni testuali dai romanzi oltre a Denti bianchi già presente), Walt Whitman (+2, dalle poesie "Io canto l'individuo" p. 7 e "Quando lessi il libro" p. 14 in Foglie d'erba, trad. Enzo Giachino, Einaudi — diversificando da Canto di me stesso e dalla poesia per Lincoln), Giovanni Verga (+2, da "La roba" p. 119 nelle Novelle rusticane e l'incipit di Storia di una capinera, Newton Compton 1993 — diversificando da I Malavoglia e Mastro-don Gesualdo), Isabel Allende (+2, gli incipit di Eva Luna, trad. Angelo Morino, e di Paula, trad. Gianni Guadalupi, entrambi Feltrinelli — diversificando da La casa degli spiriti), Gustave Flaubert (+2, gli incipit di L'educazione sentimentale, trad. Beniamino Dal Fabbro, Einaudi 1954, e di Bouvard e Pécuchet, trad. Sbarbaro/Rago, Einaudi 2015 — diversificando da Madame Bovary). Nessuna sovrapposizione con le citazioni già in archivio. Nessuna copertina reperibile con edizione italiana corrispondente per nessuna delle nuove opere. Build pulita, 0 errori. Nessuna attività concorrente rilevata in questo giro. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-30 UTC — added 10 quotes, settima applicazione della correzione di rotta (total now 569, 251 autori, 47 con una sola citazione, 58 con tre o più) — cinque autori ad alta domanda di ricerca portati a **4 citazioni ciascuno**: Douglas Adams (+2, da Ristorante al termine dell'universo e l'incipit di La vita, l'universo e tutto quanto — completa la serie della Guida galattica), Erri De Luca (+2, l'incipit di Montedidio e p. 9 sul napoletano "suonno" — diversificando da Il giorno prima della felicità), José Saramago (+2, gli incipit de Il racconto dell'isola sconosciuta, con copertina confermata su Open Library, e di Tutti i nomi — evitato Il vangelo secondo Gesù Cristo per il tema religioso, diversificando da Cecità e Le intermittenze della morte), Italo Svevo (+2, gli incipit di Corto viaggio sentimentale e di Una vita — diversificando da La coscienza di Zeno e Senilità), Simone de Beauvoir (+2, da Il sangue degli altri cap. V, trad. Dianella Selvatico Estense 2023, e da L'età forte cap. III p. 110, trad. Bruno Fonzi, Einaudi 1960 — diversificando da Il secondo sesso e Memorie d'una ragazza perbene). Nessuna sovrapposizione con le citazioni già in archivio. Verificato il bug della duplicazione traduttore: nessuna istanza. Build pulita, 0 errori. Nessuna attività concorrente rilevata in questo giro. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-30 UTC — added 11 quotes, sesta applicazione della correzione di rotta (total now 559, 251 autori, 47 con una sola citazione, 53 con tre o più) — sei autori ad alta domanda di ricerca portati a **4 citazioni ciascuno**: Giuseppe Ungaretti (+1, dalle Note a L'allegria in Vita d'un uomo, p. 518), Edgar Allan Poe (+2, gli incipit di I delitti della Rue Morgue e di Marginalia, trad. Carla Apollonio/Cristiana Mennella — evitato l'incipit de Il gatto nero per il suo tono cupo, la citazione sui libri e i margini si sposava bene col tema dell'archivio), Marcel Proust (+2, dall'edizione integrale Newton Compton 1990, pp. 4 e 16 — verificato che nessuna delle due condividesse per errore lo stesso locus di un'altra citazione dello stesso anno nel testo Wikiquote), David Foster Wallace (+2, da Il re pallido p. 47 e l'incipit di Una cosa divertente che non farò mai più — evitato l'incipit de La scopa del sistema per la sua descrizione fisica dettagliata), Ugo Foscolo (+2, dai sonetti "A Zacinto" e "Alla sera" — diversificando da Dei Sepolcri e dall'Ortis), Francesco Petrarca (+2, dalla Lettera ai posteri e dai Frammenti/Rime estravaganti p. 43, sui tiranni dell'antica Sicilia — diversificando dal Canzoniere). Nessuna sovrapposizione con le citazioni già in archivio. Nessuna copertina reperibile per nessuna delle nuove opere. Build pulita, 0 errori. Nessuna attività concorrente rilevata in questo giro. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-30 UTC — added 11 quotes, quinta applicazione della correzione di rotta (total now 548, 251 autori, 47 con una sola citazione, 48 con tre o più) — sei autori ad alta domanda di ricerca portati a **4 citazioni ciascuno**: Haruki Murakami (+1, l'incipit di L'arte di correre, trad. Antonietta Pastore, Einaudi 2009), George Orwell (+2, gli incipit di Fiorirà l'aspidistra e da Giorni in Birmania XVIII p. 233 — diversificando da 1984 e La fattoria degli animali, evitando Omaggio alla Catalogna per i suoi temi bellici), Emily Dickinson (+2, da due lettere — a Mrs. Henry Hills 1874 e a Mrs. J. G. Holland 1878 — fonte The Letters of Emily Dickinson su EmilyDickinson.it, a cura di Giuseppe Ierolli, come indicato da Wikiquote; le poesie e i "frammenti in prosa" disponibili non avevano un'edizione/pagina abbastanza chiara da citare con sicurezza), Khalil Gibran (+2, dai discorsi «Sul matrimonio» e «Sul lavoro» del Profeta, Newton Compton — diversificando da «Sui figli» e dall'amicizia), Jean-Paul Sartre (+2, da Le parole p. 37 sui libri come rifugio d'infanzia, trad. Luigi De Nardis, il Saggiatore 1964, e da La morte nell'anima p. 30, trad. Giorgio Monicelli, Oscar Mondadori 1971 — scartato l'incipit de Il muro per mancanza di un'edizione italiana verificabile in bibliografia), Jorge Luis Borges (+2, entrambe da Finzioni: l'incipit di "Tlön, Uqbar, Orbis Tertius" via Fruttero & Lucentini, e da "Pierre Menard, autore del Don Chisciotte" p. 40 — diversificando dal racconto "La biblioteca di Babele" già presente, stesso titolo dell'opera ma locus diverso). Nessuna sovrapposizione con le citazioni già in archivio. Nessuna copertina reperibile per nessuna delle nuove opere. Build pulita, 0 errori. Nessuna attività concorrente rilevata in questo giro. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-30 UTC — added 11 quotes, quarta applicazione della correzione di rotta (total now 537, 251 autori, 47 con una sola citazione, 43 con tre o più) — sei autori ad alta domanda di ricerca portati a **4 citazioni ciascuno**: Ernest Hemingway (+1, l'incipit di Per chi suona la campana, trad. Maria Napolitano Martone, Mondadori 1969, con copertina confermata su Open Library), Charles Baudelaire (+2, "I fari" su Watteau e "I gatti" da I fiori del male, trad. Claudio Rendina, Newton Compton 2011), Fernando Pessoa (+2, da L'educazione dello stoico pp. 35 e 51, a cura di Richard Zenith, Einaudi 2005 — diversificando dal Libro dell'inquietudine), Anne Frank (+2, dal Diario pp. 225 e 146-147, Mondadori 1966 — verificato che nessuna delle due condividesse il locus "p. 221" già usato), Umberto Eco (+2, gli incipit di L'isola del giorno prima e Numero zero, Bompiani 1994/2015 — diversificando da Il nome della rosa e Il pendolo di Foucault), Lev Tolstoj (+2, gli incipit di I cosacchi, trad. Gianlorenzo Pacini, Mondadori 2009, e La morte di Ivan Il'ič via Fruttero & Lucentini — scartato l'incipit di Resurrezione perché il taglio a 40 parole ne avrebbe lasciato la frase grammaticalmente sospesa, senza la principale). Nessuna sovrapposizione con le citazioni già in archivio. Nessuna copertina reperibile per le altre opere. Verificato il bug della duplicazione traduttore: nessuna istanza. Build pulita, 0 errori. **Nota di trasparenza**: nel frattempo una sessione concorrente ha ricostruito dalla cronologia git le 101 date `added` mancanti su citazioni preesistenti (commit `8beb909`) — verificato che il mio file, letto dopo quel commit, le includesse tutte prima di aggiungere le mie 11; nessun lavoro perso. Il rebuild consegunte ha quindi toccato quasi tutte le pagine del sito (nuovo `<lastmod>` ovunque), non solo quelle di questo lotto. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-30 UTC — added 11 quotes, terza applicazione della correzione di rotta (total now 526, 251 autori, 47 con una sola citazione, 38 con tre o più) — sette autori ad alta domanda di ricerca portati a **4 citazioni ciascuno**: Marco Aurelio (+1, Colloqui con sé stesso, Libro II 11, ed. 1989), Virginia Woolf (+1, La camera di Jacob, p. 139, trad. Anna Banti, Mondadori 1980 — diversificando da Una stanza tutta per sé, La signora Dalloway, Gita al faro), Hermann Hesse (+1, l'incipit di Narciso e Boccadoro, trad. Cristina Baseggio, Mondadori 1989 — diversificando da Demian, Siddhartha, Il lupo della steppa), Pablo Neruda (+2, "Ode al gatto" da Odi elementari e da Confesso che ho vissuto p. 171, trad. Stocchi/D'Amico, SugarCo 1979 — diversificando dai due sonetti d'amore già presenti), Toni Morrison (+2, entrambe da Amatissima, pp. 33 e 102, trad. Giuseppe Natale, Frassinelli 1988 — le uniche fonti con locus verificabile disponibili su Wikiquote per quest'autrice), Michela Murgia (+2, l'incipit di Accabadora e da Noi siamo tempesta p. 123 — diversificando da Chirù e completando la seconda opera già presente), Paulo Coelho (+2, entrambe dal Manuale del guerriero della luce, pp. 22 e 31, trad. Rita Desti, Bompiani 1997 — scartata una citazione da Brida per un'ellissi nel testo che ne rendeva incerta l'attribuzione precisa). Nessuna sovrapposizione con le citazioni già in archivio dello stesso autore. Nessuna copertina reperibile con edizione italiana corrispondente per nessuna delle nuove opere. Build pulita, 0 errori. Nessuna attività concorrente rilevata in questo giro. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-30 UTC — added 10 quotes, seconda applicazione della correzione di rotta (total now 515, 251 autori, 47 con una sola citazione, 34 con tre o più) — sei autori italiani del Novecento ad alta domanda di ricerca portati da 2/3 a **4 citazioni ciascuno**, tutti con locus reale (pagina/incipit): Gabriele D'Annunzio (+2 da "Il libro delle vergini", racconti "Le Vergini" p. 42 e "Favola sentimentale" p. 103 — diversificando da Il piacere e Alcyone), Cesare Pavese (+1, l'incipit di "La bella estate" — completa Verrà la morte..., La luna e i falò, Il mestiere di vivere), Luigi Pirandello (+1, da "Enrico IV" p. 165, sulle velleità e le maschere — completa Uno nessuno e centomila, Il fu Mattia Pascal, Sei personaggi), Alda Merini (+2, da "Corpo d'amore" p. 81 sul processo creativo e da "Mistica d'amore" — Magnificat p. 97 — diversificando da Vuoto d'amore e La Terra Santa), Primo Levi (+2, l'incipit di "Il sistema periodico" sui gas nobili e da "Ranocchi sulla luna e altri animali" — Quaestio de Centauris pp. 30-31, un bestiario fantastico — diversificando volutamente da Se questo è un uomo verso toni più leggeri), Pier Paolo Pasolini (+2, da "La Divina Mimesis" p. 29 e l'incipit di "Lettere luterane" — diversificando da Ragazzi di vita e Scritti corsari). Nessuna sovrapposizione con le citazioni già in archivio dello stesso autore. Nessuna copertina reperibile con edizione italiana corrispondente per nessuna delle nuove opere (solo placeholder su Open Library), lasciata vuota per tutte. Build pulita, 0 errori. Nessuna attività concorrente rilevata in questo giro. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-30 UTC — added 10 quotes, prima applicazione della correzione di rotta del 2026-08-30 (total now 505, 251 autori, 47 con una sola citazione, 30 con tre o più) — seguendo la nuova direttiva in `CATALOGO.md` §7 (nessun autore nuovo, si porta a 4 citazioni chi ha più domanda di ricerca in `data/keywords.json`, precedenza alle opere anteriori al Novecento), sei autori già in archivio portati da 2/3 a **4 citazioni ciascuno**: Dante Alighieri (+Purgatorio, canto I, vv. 1-3, incipit della cantica — mancava solo il Purgatorio per completare la trilogia), Victor Hugo (+Il Novantatré, "Lo spirito nutre, l'intelligenza vivifica...", parte II libro I cap. III, p. 102, trad. Oete Blatto, Newton 2004), Voltaire (+2 da "L'ingenuo", pp. 80 e 82, trad. Sara Di Gioacchino Corcos, Edipem 1974 — diversificando da Candido, già presente 2 volte), Niccolò Machiavelli (+2 dai "Discorsi sopra la prima deca di Tito Livio", libro I capp. IV e VI, a cura di Mario Martelli, Sansoni 1971 — diversificando da Il Principe), Mark Twain (+2 incipit, "Le avventure di Tom Sawyer" trad. Gianni Celati e "L'uomo che corruppe Hadleyburg" trad. Bruno Fonzi — diversificando da Huckleberry Finn), Jane Austen (+2 incipit, "Ragione e sentimento" trad. Pietro Meneghelli e "Persuasione" trad. Giulietta Cardone Cattaneo — diversificando da Orgoglio e pregiudizio). Tutte le nuove citazioni verificate su Wikiquote con locus reale (capitolo/canto/pagina/incipit), nessuna sovrapposizione con le citazioni già in archivio dello stesso autore. Scartata una citazione dal Dizionario filosofico di Voltaire (voce "Abramo") per il tono sarcastico su temi religiosi ebraico-islamici, troppo divisivo. Nessuna copertina reperibile con edizione italiana corrispondente per nessuna delle nuove opere, lasciata vuota per tutte. **Corretto anche l'errore di contenuto aperto**: le due citazioni del Piccolo Principe con lo stesso locus "capitolo XXI" ora distinte con il numero di pagina (p. 97 e p. 98, trad. Yasmina Melaouah, Gribaudo 2015, confermato su Wikiquote) — il warning di build è sparito. Build pulita, 0 errori. **Nota di trasparenza**: il working tree conteneva, non ancora mio, un lavoro sostanzioso di sessione concorrente (miglioramenti UX: ricerca in ogni pagina, correlate come schede, fix del cache-busting sugli asset) già committato separatamente; il mio `build.py` ha quindi rigenerato l'intero sito con i nuovi template, e il commit di questo lotto include perciò l'output di quel rebuild completo insieme alle mie 10 citazioni — non ho toccato asset o template. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-30 UTC — added 2 quotes, approfondimento (total now 495, 251 autori, 47 con una sola citazione) — proseguita l'alternanza con l'approfondimento di due autori già presenti con una sola citazione: Iris Murdoch ("L'arte ha sempre a che fare con l'assurdo e tende alla semplicità...", da Una testa tagliata, citato in Laura Bolgeri, Le donne hanno detto, Rizzoli 1990, p. 41, confermata su Wikiquote — nessuna sovrapposizione con la citazione già in archivio da La ragazza italiana) e Knut Hamsun (il dialogo "Amo tre cose, dico allora...", da Pan, cap. XXVI — nessuna edizione italiana verificabile con certezza, lasciata vuota, come da prassi già seguita per Golding; nessuna sovrapposizione con la citazione già in archivio da Fame). Nessuna copertina reperibile per nessuna delle due. Verificato il bug della duplicazione traduttore: nessuna istanza. Build pulita, 0 errori. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-30 UTC — added 2 quotes, 2 nuovi autori (total now 493, 251 autori, 49 con una sola citazione) — proseguita l'alternanza con due nuovi autori: Maya Angelou (l'incipit di "Il canto del silenzio", "Perché mi guardate? Non sono venuta per restare...", locus incipit — nessuna edizione italiana verificabile con certezza, lasciata vuota, come da prassi già seguita per Golding) e Audre Lorde (dal saggio "La poesia non è un lusso" in "Sorella Outsider", "Per le donne, quindi, la poesia non è un lusso...", a cura di Margherita Giacobino e Marta Gianello Guida, Il Dito e la Luna 2014, p. 117, confermata su Wikiquote — accorciata in coda per rientrare nel limite di 40 parole). Scartate le citazioni più politicamente cariche disponibili per entrambe (l'elogio funebre di Angelou per Coretta Scott King, che tocca anche Israele e Palestina; i passaggi di Lorde più specificamente centrati su razza), per lo stesso criterio di cautela sui contenuti divisivi già seguito. Nessuna copertina reperibile per nessuna delle due. Verificato il bug della duplicazione traduttore: nessuna istanza. Nuovi autori sotto soglia (noindex,follow) come da prassi. Build pulita, 0 errori. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-30 UTC — added 2 quotes, approfondimento (total now 491, 249 autori, 47 con una sola citazione) — proseguita l'alternanza con l'approfondimento di due autori già presenti con una sola citazione: Chinua Achebe (dal proverbio Ibo sul compito dello scrittore, "Fra gli Ibo c'è un proverbio...", da "The Role of a Writer in a New Nation", Nigeria Magazine n. 81, giugno 1964, p. 159, confermata su Wikiquote — nessuna sovrapposizione con la citazione già in archivio da Le cose crollano) e Marguerite Duras ("Il calciatore sta sul campo di gioco completamente esposto...", da "L'arcangelo Michel", L'Europeo n. 3, 15 gennaio 1988, confermata su Wikiquote — nessuna sovrapposizione con la citazione già in archivio da L'amante). Scartato in questo giro: Julio Cortázar (nessuna delle citazioni disponibili su Wikiquote ha un locus con pagina verificabile sull'opera originale, solo citazioni da antologie secondarie senza numero o articoli con solo l'anno). Nessuna copertina reperibile per nessuna delle due fonti (entrambe articoli di rivista). Verificato il bug della duplicazione traduttore: nessuna istanza. Build pulita, 0 errori. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-30 UTC — added 2 quotes, 2 nuovi autori (total now 489, 249 autori, 49 con una sola citazione) — proseguita l'alternanza con due nuovi autori: Michel Houellebecq ("È nel rapporto con gli altri che si prende coscienza di sé...", da "Piattaforma nel centro del mondo", trad. Sergio Claudio Perroni, Bompiani 2004, p. 77, confermata su Wikiquote — scartate le altre citazioni disponibili, alcune con riferimenti al nazismo o toni marcatamente misogini verso la psicanalisi, per lo stesso criterio di cautela già seguito su contenuti divisivi o offensivi) e Zbigniew Herbert (dal saggio "Presso i Dori" in "Un barbaro nel giardino", "Al mattino la roccia calcarea di Paestum è grigia...", locus p. 34 dell'edizione polacca originale con la traduzione italiana citata da Eleonora Battistini in un suo studio accademico sull'opera di Herbert, come indicato dalla stessa Wikiquote — nessuna edizione italiana del libro reperibile con certezza, quindi sourcing basato sulla fonte secondaria che Wikiquote stessa cita, come da prassi già seguita per Fruttero & Lucentini). Joseph Brodskij e Louise Erdrich risultano privi di voce su Wikiquote italiano, scartati. Nessuna copertina reperibile per nessuno dei due. Verificato il bug della duplicazione traduttore: nessuna istanza. Nuovi autori sotto soglia (noindex,follow) come da prassi. Build pulita, 0 errori. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-30 UTC — added 2 quotes, approfondimento (total now 487, 247 autori, 47 con una sola citazione) — proseguita l'alternanza con l'approfondimento di due autori già presenti con una sola citazione: Amos Oz ("Il fanatico è un punto esclamativo ambulante...", da "Cari fanatici", trad. Elena Loewenthal, Feltrinelli 2020, p. 27, confermata su Wikiquote — nessuna sovrapposizione con la citazione già in archivio da Una storia di amore e di tenebra) e Herta Müller ("Lager, s.n.: campo. Da quando so pensare, mia madre dice...", da "Parola d'autore. I lemmi del vocabolario europeo 2009", Corriere della Sera, 8 ottobre 2009, confermata su Wikiquote — nessuna sovrapposizione con la citazione già in archivio da Il paese delle prugne verdi). Scartate in questo giro le altre citazioni disponibili di Müller, quasi tutte centrate su Putin e la guerra in Ucraina: argomento politico attuale e divisivo, evitato per lo stesso criterio già seguito con altri autori in sessioni precedenti. Nessuna copertina reperibile per nessuna delle due fonti. Verificato il bug della duplicazione traduttore: nessuna istanza. Build pulita, 0 errori. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-30 UTC — added 2 quotes, 2 nuovi autori (total now 485, 247 autori, 49 con una sola citazione) — proseguita l'alternanza con due nuovi autori: Susan Sontag ("A mancarci è l'immaginazione, l'empatia: non siamo riusciti a fare nostra questa realtà", da "Davanti al dolore degli altri", Internazionale n. 490, 30 maggio 2003, p. 30, confermata su Wikiquote) e Wole Soyinka ("L'uomo muore in tutti coloro che conservano il silenzio di fronte alla tirannia", da "L'uomo è morto", trad. Carla Muschio, Jaca Book 1986, p. 29, confermata su Wikiquote). Scartato in questo giro: Colson Whitehead (nessun locus con pagina verificabile per l'unica citazione disponibile su Wikiquote). Nessuna copertina reperibile per nessuno dei due. Verificato il bug della duplicazione traduttore: nessuna istanza. Nuovi autori sotto soglia (noindex,follow) come da prassi. Build pulita, 0 errori. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-30 UTC — added 2 quotes, approfondimento (total now 483, 245 autori, 47 con una sola citazione) — proseguita l'alternanza con l'approfondimento di due autori già presenti con una sola citazione: Roberto Bolaño (l'incipit di "2666", "La prima volta che Jean-Claude Pelletier lesse Benno von Arcimboldi...", parte "La parte dei critici", trad. Ilide Carmignani, Adelphi 2007, confermata su Wikiquote — nessuna sovrapposizione con la citazione già in archivio, stesso titolo "2666" ma locus diverso) e Olga Tokarczuk ("Per me si fa politica in ogni momento della vita...", dall'intervista "Il mio caffè con la Szymborska", la Repubblica, 18 ottobre 2019, p. 41, confermata su Wikiquote — scartato l'incipit di "Guida il tuo carro sulle ossa dei morti" perché già presente in archivio come citazione esistente). Nessuna copertina reperibile per nessuna delle due fonti. Verificato il bug della duplicazione traduttore: nessuna istanza. Build pulita, 0 errori. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-30 UTC — added 2 quotes, 2 nuovi autori (total now 481, 245 autori, 49 con una sola citazione) — proseguita l'alternanza con due nuovi autori: Hannah Arendt ("Il progresso e la catastrofe sono il diritto e il rovescio della stessa medaglia", da "Gli incidenti ai tempi della globalizzazione", Internazionale n. 767, 24 ottobre 2008, p. 23, confermata su Wikiquote) e Anna Achmatova (dalla poesia "Loda soltanto", "Loda soltanto la quinta stagione dell'anno...", in Lo stormo bianco, trad. Gene Immediato, Fabbri 1997, p. 153, confermata su Wikiquote). Scartati in questo giro: Georges Perec (nessun locus con pagina verificabile, solo citazioni da antologie secondarie senza numero), Czesław Miłosz (pagina Wikiquote solo abbozzo, nessuna edizione italiana della poesia "Campo de' Fiori" verificabile con certezza, e il taglio a 40 parole ne avrebbe snaturato il senso tagliando via il verso più importante). Nessuna copertina reperibile per nessuno dei due (Arendt: fonte è un articolo di rivista, non un libro; Achmatova: nessun risultato utile su Open Library). Verificato il bug della duplicazione traduttore: nessuna istanza. Nuovi autori sotto soglia (noindex,follow) come da prassi. Build pulita, 0 errori. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-30 UTC — added 2 quotes, approfondimento (total now 479, 243 autori, 47 con una sola citazione) — proseguita l'alternanza con l'approfondimento di due autori già presenti con una sola citazione: Salman Rushdie ("L'alienazione non è forse mai stata tanto diffusa come oggi...", da "Le voci del mondo", Internazionale n. 592, 27 maggio 2005, p. 75, confermata su Wikiquote — nessuna sovrapposizione con la citazione già in archivio da I figli della mezzanotte) e Chimamanda Ngozi Adichie ("La misura della nostra umanità dipende, in parte, da come consideriamo chi è diverso da noi...", da "Il mio buio oltre la siepe", Internazionale n. 1089, 13 febbraio 2015, p. 89, confermata su Wikiquote — nessuna sovrapposizione con la citazione già in archivio da Americanah). Entrambe le fonti sono articoli di rivista, non libri: nessuna copertina applicabile, lasciata vuota. Verificato il bug della duplicazione traduttore: nessuna istanza. Build pulita, 0 errori. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-30 UTC — added 2 quotes, lotto misto (total now 477, 243 autori, 49 con una sola citazione) — un approfondimento e un nuovo autore insieme: Douglas Adams, già in archivio con una sola citazione, portato a 2 con l'incipit di "Guida galattica per gli autostoppisti" ("Lontano, nei dimenticati spazi non segnati nelle carte geografiche...", trad. Laura Serra, Mondadori, locus incipit, accorciato in coda per rientrare nel limite di 40 parole — nessuna sovrapposizione con "Non fatevi prendere dal panico" già in archivio); e Astrid Lindgren come nuovo autore, con l'incipit di "Pippi Calzelunghe" nella traduzione 2008 di Annuska Palme Larussa e Donatella Ziliotto, Salani (anch'esso accorciato in coda, perdendo la battuta finale sull'olio di fegato di merluzzo per rientrare nel limite di parole, ma restando una frase compiuta). Scartato in questo giro: Julian Barnes (nessun locus con pagina o posizione verificabile su Wikiquote, solo un'intervista giornalistica). Nessuna copertina reperibile con certezza per nessuna delle due opere, lasciata vuota. Verificato il bug della duplicazione traduttore: nessuna istanza. Build pulita, 0 errori. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-30 UTC — added 2 quotes, 2 nuovi autori (total now 475, 242 autori, 49 con una sola citazione) — proseguita l'alternanza con due nuovi autori: Roald Dahl (La fabbrica di cioccolato, "Cara la mia vecchia triglia, perché non va a farsi friggere?", il signor Wonka alla signora Salt, cap. XXIII, p. 140, trad. Riccardo Duranti, Salani 2005, confermata su Wikiquote — scartata "Danny il campione del mondo" pur con locus p. 25 perché l'edizione italiana non è verificabile né su Wikiquote né su Open Library) e Clarice Lispector (dal racconto "Silenzio" nella raccolta "Dove siete stati di notte", "Si può pensare in fretta al giorno che è trascorso...", in Tutti i racconti, trad. Adelina Aletti e Roberto Francavilla, Feltrinelli 2019, confermata su Wikiquote — locus il nome del racconto, non essendoci numeri di pagina sulla fonte). Nessuna copertina reperibile con certezza per entrambi, lasciata vuota. Verificato il bug della duplicazione traduttore: nessuna istanza. Nuovi autori sotto soglia (noindex,follow) come da prassi. Build pulita, 0 errori. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-30 UTC — added 2 quotes, approfondimento (total now 473, 240 autori, 47 con una sola citazione) — proseguita l'alternanza con l'approfondimento di due autori già presenti con una sola citazione: Isaac Asimov (aforisma "L'aspetto più triste della vita in questo momento è che la scienza raccoglie conoscenza più velocemente di quanto la società raccolga saggezza", da Isaac Asimov's Book of Science and Nature Quotations, con Jason A. Shulman, Weidenfeld & Nicolson 1988, p. 281 — nessuna sovrapposizione con la citazione già in archivio da Fondazione) e James Baldwin (dal discorso "A Talk to Teachers", 1963, "Il paradosso dell'istruzione è proprio questo..." — testo accorciato in coda prima di un tratto della traduzione italiana su Wikiquote che presentava una ripetizione editoriale poco chiara, per non riprodurre un passaggio corrotto — in James Baldwin: Collected Essays, Library of America 1998, pp. 678-679 — nessuna sovrapposizione con la citazione già in archivio da La prossima volta il fuoco). Scartato in questo giro: Michail Bulgakov (l'unica citazione su Wikiquote con locus concreto, la lettera a Stalin p. 15, non risulta effettivamente tra le citazioni riportate; il passo più bello reperito, sull'Ucraina e Kiev da "Io ho ucciso", non ha un locus verificabile diverso dall'incipit, che è un'altra battuta — scartato per assenza di locus reale). Verificato il bug della duplicazione traduttore: nessuna istanza. Build pulita, 0 errori. **Nota di trasparenza**: il commit `d451929` include anche una modifica a `templates/home_template.html` non mia, trovata già presente e non ancora committata nell'albero al momento del commit (sessione concorrente): corregge un bug di "Le mie sottolineature" per cui due citazioni della stessa opera condividevano la stessa chiave di sottolineatura/nota (ora basata sullo slug invece che su autore|titolo), con relativa migrazione delle chiavi vecchie. Codice coerente e sensato, inclusa per non spezzare il lavoro altrui. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-30 UTC — added 2 quotes, 2 nuovi autori (total now 471, 240 autori) — proseguita l'alternanza con due nuovi autori: Émile Zola (L'Assommoir, "Fino a tanto che avrete qualche cosa di vostro... non sarete degni mai della felicità", p. 88, trad. Ferdinando Bruno, Garzanti 2018, confermata su Wikiquote) e Hans Christian Andersen (L'improvvisatore, "Ci stabilimmo a Santa Lucia, il mare era di fronte, il Vesuvio lampeggiava...", pp. 73-74, a cura di Bruno Berni, trad. Alda Castagnoli Manghi, Elliot 2013, confermata su Wikiquote — quote leggermente accorciata in coda, dal punto "erano splendide serate...", per rientrare nel limite di 40 parole senza alterare il testo). Nessuna copertina reperibile con certezza per entrambi (Open Library restituisce solo placeholder vuoti per le edizioni italiane), lasciata vuota. Verificato il bug della duplicazione traduttore: nessuna istanza. Nuovi autori sotto soglia (noindex,follow) come da prassi. Build pulita, 0 errori. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-30 UTC — added 2 quotes, approfondimento (total now 469, 238 autori, 47 con una sola citazione) — proseguita l'alternanza con l'approfondimento di due autori già presenti con una sola citazione: Agatha Christie (La sagra del delitto, "Nessuno avrebbe saputo raccontare deliberatamente una bugia meglio di Hercule Poirot", pp. 118-119, trad. Paola Franceschini, Oscar Mondadori 1987 — nessuna sovrapposizione con la citazione già in archivio da Dieci piccoli indiani) e Bertolt Brecht (L'opera da tre soldi, atto III scena I, "La legge è fatta esclusivamente per lo sfruttamento di coloro che non la capiscono...", p. 79, a cura di Emilio Castellani, Einaudi 1997 — nessuna sovrapposizione con la citazione già in archivio da Madre Courage e i suoi figli, titolo diverso). Scartati in questo giro: Tagore ("Il nido dell'amore" privo di numeri di pagina), Henry James (Giro di vite, nessun locus verificabile su Wikiquote), Ibsen (Gli spettri, idem). Verificato il bug della duplicazione traduttore: nessuna istanza. Nessuna copertina reperibile con certezza per entrambe le nuove citazioni, lasciata vuota. Build pulita, 0 errori. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-29 UTC — added 2 quotes, 2 nuovi autori (total now 467, 238 autori) — proseguita l'aggiunta di nuovi autori (alternando con l'approfondimento): Pearl S. Buck (La buona terra, il vecchio Wang Lung sulla terra da non vendere mai — "dalla terra siamo venuti, e alla terra dobbiamo tornare", cap. XXXIV p. 291, trad. Andrea Damiano, San Paolo 1998, confermata su Wikiquote) e Sinclair Lewis (Qui non può succedere, la condanna di ogni dittatura — "fascista, nazista, comunista o dei sindacati americani" — "l'anima e il sangue della gente non sono gusci d'uovo che i tiranni possono rompere", cap. 24, Chiarelettere 2024, confermata su Wikiquote — nessuna copertina reperibile con certezza, scartata una copertina che in realtà apparteneva a un libro diverso con lo stesso titolo). Verificato il bug della duplicazione traduttore: nessuna istanza. Nuovi autori sotto soglia (noindex,follow) come da prassi. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-29 UTC — added 2 quotes (total now 465, 236 autori) — proseguito l'approfondimento alternato: Guy de Maupassant (Una vita, "è così che crollano i sogni", pp. 74-75, trad. Marino Moretti, Oscar Mondadori 1984, confermata su Wikiquote — secondo titolo per l'autore dopo Bel-Ami, portato sopra soglia) e Nathaniel Hawthorne (La casa dei sette abbaini, sul peso ereditato da ogni generazione, p. 168, trad. Marcella Bonsanti, I Capolavori Sansoni 1972, confermata su Wikiquote — secondo titolo per l'autore dopo La lettera scarlatta, portato sopra soglia). Verificato il bug della duplicazione traduttore: nessuna istanza. Restano 47 autori con una sola citazione. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-29 UTC — added 2 quotes (total now 463, 236 autori) — alternando con l'approfondimento come deciso nel lotto precedente: E.M. Forster (Casa Howard, "la carriera meglio riuscita deve mostrare uno spreco di forza che avrebbe potuto smuovere le montagne", cap. 12 p. 122, trad. Enrico La Stella, Newton Compton 1993, confermata su Wikiquote — secondo titolo per l'autore dopo Camera con vista, portato sopra soglia) e Viktor E. Frankl (Uno psicologo nei lager, l'avvertimento sul ritorno a casa dal lager e sul sogno che si scopre "diverso" dalla realtà, parte seconda, in «L'uomo in cerca di senso», Franco Angeli 2017, confermata su Wikiquote — secondo passo dallo stesso libro, portato sopra soglia). Verificato il bug della duplicazione traduttore: nessuna istanza. Restano 49 autori con una sola citazione (35 del lavoro precedente + 16 nuovi, meno i 2 appena approfonditi). **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-29 UTC — added 2 quotes, 2 nuovi autori (total now 461, 236 autori) — proseguita l'aggiunta di nuovi autori: Henrik Ibsen (Casa di bambola, la battuta finale di Nora "con te, una bambola-moglie. E i nostri figli, le mie bambole.", atto III p. 87, trad. Lucio Chiavarelli, Newton Compton 1993, confermata su Wikiquote) e Alfred Tennyson (In Memoriam A.H.H., "è meglio avere amato e perduto che mai e mai avere amato", canto XXVII, a cura di Saverio Tomaiuolo, Mondadori 2022, confermata su Wikiquote). Scartato Anthony Trollope, nessuna sezione Citazioni sostanziale. Verificato il bug della duplicazione traduttore: nessuna istanza. Nuovi autori sotto soglia (noindex,follow) come da prassi. **Sedici autori nuovi ora sotto soglia insieme ai rimasti dal lavoro precedente**: dal prossimo lotto conviene alternare nuovi autori e approfondimento, per non allargare l'archivio a scapito dell'equilibrio (CATALOGO.md: "approfondire vale più che allargare"). **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-29 UTC — added 2 quotes, 2 nuovi autori (total now 459, 234 autori) — proseguita l'aggiunta di nuovi autori: D.H. Lawrence (Figli e amanti, sul sonno "più salutare quand'è condiviso da un essere amato", cap. IV p. 124, trad. Franca Cangogni, Oscar Mondadori 1988, confermata su Wikiquote) e George Bernard Shaw (Guida della donna intelligente, "prendete cura [delle doti intellettuali e morali] e la felicità prenderà cura di se stessa", p. 59, BMM 1950, confermata su Wikiquote — traduttore non indicato in bibliografia, nessuna copertina reperibile con certezza). Scartati per assenza di locus verificabile: L'amante di Lady Chatterley di Lawrence, Il canto dell'allodola di Willa Cather, Katherine Mansfield (solo incipit). Verificato il bug della duplicazione traduttore: nessuna istanza — corretto anche un refuso nel nome del traduttore di Lawrence (Cancogni → Cangogni) individuato subito dopo l'inserimento. Nuovi autori sotto soglia (noindex,follow) come da prassi. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-29 UTC — added 2 quotes, 2 nuovi autori (total now 457, 232 autori) — proseguita l'aggiunta di nuovi autori: Nathaniel Hawthorne (La lettera scarlatta, la battuta del reverendo Wilson "l'onta risiede nella consumazione del peccato, non nella sua confessione", cap. III p. 67, trad. Enzo Giachino, Einaudi 1951, confermata su Wikiquote) e Henry James (Ritratto di signora, "si deve cercare di essere il proprio migliore amico", p. 48, trad. Carlo e Silvia Linati, Einaudi 1976, confermata su Wikiquote). Scartati per assenza di locus verificabile: Giro di vite di James (nessuna pagina) e La pietra di luna e La donna in bianco di Wilkie Collins (nessuna pagina); Elizabeth Gaskell scartata per assenza di sezione Citazioni completa. Verificato il bug della duplicazione traduttore: nessuna istanza. Nuovi autori sotto soglia (noindex,follow) come da prassi. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-29 UTC — added 2 quotes, 2 nuovi autori (total now 455, 230 autori) — proseguita l'aggiunta di nuovi autori: Edith Wharton (Estate, la proposta di matrimonio del signor Royall "è l'unico vantaggio di invecchiare", cap. XVII p. 155, trad. Maria Luisa Castagnone, La Tartaruga, confermata su Wikiquote) e Guy de Maupassant (Bel-Ami, "tutto sta nel non lasciarsi cogliere in flagrante delitto di ignoranza", cap. I, trad. Orsola Nemi, Rizzoli 2010, confermata su Wikiquote). Scartati per assenza di sezioni Citazioni utilizzabili: Colson Whitehead, Anthony Doerr, Kent Haruf, Delia Owens, Émile Zola (Germinale, nessuna pagina) e Rudyard Kipling (Il libro della giungla, nessuna pagina). Verificato il bug della duplicazione traduttore: nessuna istanza. Nuovi autori sotto soglia (noindex,follow) come da prassi. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-29 UTC — added 2 quotes, 2 nuovi autori (total now 453, 228 autori) — proseguita l'aggiunta di nuovi autori: Knut Hamsun (Fame, sull'invidia del narratore affamato per "quegli uomini [...] leggeri e sereni", cap. I p. 24, trad. Ervino Pocar, Adelphi 2002, confermata su Wikiquote) e Anaïs Nin (Diario I. 1931-1934, "Il romantico si sottomette alla vita, il classico la domina.", marzo 1933, a cura di Gunther Stuhlmann, trad. Delfina Vezzoli, Bompiani 2016, confermata su Wikiquote — locus per data del diario, come già per Anne Frank). Scartati per mancanza di sezioni Citazioni utilizzabili: Colm Tóibín, Maya Angelou, John Fante (Chiedi alla polvere, nessun numero di pagina), Raymond Carver (Da dove sto chiamando, stesso problema), Jonathan Franzen, Elizabeth Strout, Selma Lagerlöf, Kenzaburō Ōe, Nadine Gordimer, Czesław Miłosz, Halldór Laxness, Derek Walcott e Svetlana Aleksievič (pagina vuota). Verificato il bug della duplicazione traduttore: nessuna istanza. Tutti i nuovi autori sono sotto soglia (noindex,follow) come da prassi. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-29 UTC — added 3 quotes, 3 nuovi autori (total now 451, 226 autori) — proseguita l'aggiunta di nuovi autori: Rabindranath Tagore (Uccelli migranti, l'aforisma "Il potere disse al mondo [...] L'amore disse al mondo: Io son tuo.", aforisma 93, trad. Eduardo Taglialatela, Carabba 1918, confermata su Wikiquote), Bertolt Brecht (Madre Courage e i suoi figli, la battuta cinica del reclutatore "la pace è solo disordine", p. 7, trad. Ruth Leiser e Franco Fortini, Einaudi 2001, confermata su Wikiquote) e Iris Murdoch (La ragazza italiana, "non si ha bisogno di sofferenza, ma di verità", p. 50, trad. Gabriella Fiori Andreini, Feltrinelli 1965, confermata su Wikiquote). Scartato Rumi, per cui non esiste alcuna pagina su Wikiquote in italiano. Verificato il bug della duplicazione traduttore: nessuna istanza. Tutti i nuovi autori sono sotto soglia (noindex,follow) come da prassi, da approfondire in lotti futuri. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-29 UTC — added 3 quotes, 3 nuovi autori (total now 448, 223 autori) — esaurito il bacino di autori con una sola citazione facilmente approfondibile, su istruzione dell'utente ("Riprendi. Una volta completata anche quella, aggiungine di nuove") si passa ad ampliare l'archivio con autori mai citati finora: E.M. Forster (Camera con vista, "il nostro bisogno di un segno di comprensione [...] non ci importa [...] quanto dovremo pagarlo in seguito", cap. 7 p. 72, trad. Pietro Meneghelli, Newton Compton 1994, confermata su Wikiquote), T.S. Eliot (Il canto d'amore di J. Alfred Prufrock, l'incipit "E allora andiamo, tu e io [...]", citato in Fruttero & Lucentini, «Íncipit», Mondadori 1993, confermata su Wikiquote) e Agatha Christie (Dieci piccoli indiani, "C'era qualcosa di magico in un'isola [...] un mondo, forse, dal quale si poteva non tornare indietro", pp. 28-29, trad. Beata Della Frattina, Mondadori 1988, confermata su Wikiquote — scartata di proposito la filastrocca dei "negretti" citata nella stessa pagina, per il linguaggio ormai datato e offensivo dell'edizione storica, in favore di un passo diverso senza quel problema). Verificato il bug della duplicazione traduttore: nessuna istanza. I tre nuovi autori sono sotto la soglia delle 3 citazioni (noindex,follow) come da prassi consolidata per i nuovi ingressi in archivio — verranno approfonditi in lotti futuri. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-29 UTC — added 1 quote (total now 445) — proseguito l'approfondimento: J.M. Coetzee (La vita degli animali, sul figlio di Elizabeth Costello preoccupato per le sue conferenze che "attirano pazzi e squilibrati come un cadavere attira le mosche", p. 48, trad. F. Cavagnoli e G. Arduini, Adelphi 2000, confermata su Wikiquote — secondo titolo per l'autore dopo Aspettando i barbari; scelto di proposito questo passo di umorismo secco invece di altri più disponibili nella stessa sezione, che toccavano il tema sensibile dell'Olocausto). Lotto ancora più piccolo: ricerca senza esito per Madeline Miller, Olga Tokarczuk, Octavio Paz, Michail Bulgakov (Cuore di cane, oltre ai due titoli già scartati), Amos Oz (Fima, oltre al titolo già in archivio senza locus), Ralph Ellison (nessuna pagina Wikiquote esiste per l'autore), J.M. Barrie (Peter Pan nei giardini di Kensington, oltre a Peter Pan già scartato), Julian Barnes (nessun titolo ha una sezione Citazioni completa, solo incipit), Marguerite Duras (sezione "Scrivere" vuota), Susanna Tamaro (Rispondimi e Ascolta la mia voce, oltre a Va' dove ti porta il cuore già scartato) e Viktor E. Frankl (nessuna pagina Wikiquote sostanziale). Verificato il bug della duplicazione traduttore: nessuna istanza. Restano 35 autori con una sola citazione — il bacino di candidati facilmente reperibili è ormai quasi esaurito, la maggior parte degli autori rimasti non ha alcuna sezione Citazioni utilizzabile su Wikiquote. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-29 UTC — added 2 quotes (total now 444) — proseguito l'approfondimento: Saul Bellow (Il pianeta di Mr. Sammler, "Il sistema esige la mediocrità, non la grandezza.", p. 19, trad. Letizia Ciotti Miller, Mondadori 2009, confermata su Wikiquote — secondo titolo per l'autore dopo Herzog, nessuna copertina reperibile) e William Golding (Il signore delle mosche, sull'adattarsi "al ritmo del lento passaggio dall'alba al rapido crepuscolo", p. 64, confermata su Wikiquote — traduttore non attribuibile con certezza fra le due edizioni in bibliografia, il numero di pagina stesso è marcato "manca l'edizione" su Wikiquote ma è comunque un locus reale e verificabile; citazione accorciata da 54 a 37 parole; secondo passo dallo stesso romanzo). Lotto più piccolo del solito: setacciati senza successo (nessun locus verificabile) anche Amin Maalouf, Annie Ernaux (L'evento — unico passo disponibile troppo lungo da accorciare senza banalizzare un tema delicato, il racconto di un test HIV), Rick Riordan, Vasco Pratolini (Metello, oltre a Cronache di poveri amanti già scartato), Roberto Bolaño (I detective selvaggi e La pista di ghiaccio, oltre a 2666 già scartato) e J.M. Coetzee (Diario di un anno difficile, oltre ad Aspettando i barbari e Vergogna già scartati). Verificato il bug della duplicazione traduttore: nessuna istanza. Restano 36 autori con una sola citazione — il lavoro di approfondimento sta esaurendo i candidati con fonte solida facilmente reperibile; i lotti successivi saranno probabilmente più piccoli e richiederanno più tempo di ricerca per candidato. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-29 UTC — added 4 quotes (total now 442) — proseguito l'approfondimento: Leonardo Sciascia (A ciascuno il suo, la battuta di Laurana sui "personaggi simpatici cui bisognerebbe tagliare la testa", p. 37, Adelphi 2012, confermata su Wikiquote — secondo titolo per l'autore dopo Il giorno della civetta), Mario Vargas Llosa (Storia di Mayta, sulla società che considera "anormale" tutto ciò che non rispetta le sue regole, p. 196, trad. Angelo Morino, Rizzoli 1985, confermata su Wikiquote — secondo titolo per l'autore dopo Conversazione nella «Catedral»), H.G. Wells (L'uomo invisibile, la prima apparizione dello sconosciuto alla locanda, p. 27, confermata su Wikiquote — traduttore non attribuibile con certezza fra le tre edizioni in bibliografia; secondo titolo per l'autore dopo La macchina del tempo) e Truman Capote (Preghiere esaudite, "Sarò magari una pecora nera, ma i miei zoccoli sono fatti d'oro.", p. 97, trad. Ettore Capriolo, Garzanti 2019, confermata su Wikiquote — secondo titolo per l'autore dopo Colazione da Tiffany). Scartati per mancanza di un locus verificabile: Elif Shafak (nessuna sezione Citazioni per un titolo in archivio), Emily St. John Mandel, Chimamanda Ngozi Adichie e Patrick Süskind (Il profumo, già scartato in un lotto precedente, riconfermato). Verificato il bug della duplicazione traduttore: nessuna istanza. Restano 38 autori con una sola citazione. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-29 UTC — added 3 quotes (total now 438) — proseguito l'approfondimento: Paolo Cognetti (Le otto montagne, "è impossibile trasmettere a chi è rimasto a casa quel che si prova lassù", p. 61, Einaudi 2016, confermata su Wikiquote — secondo passo dallo stesso romanzo), Immanuel Kant (Lezioni di etica, sui doveri verso gli animali — "chi usa essere crudele verso di essi è altrettanto insensibile verso gli uomini", p. 273, trad. Augusto Guerra, Laterza 1984, confermata su Wikiquote — secondo titolo per l'autore dopo Per la pace perpetua, evitato di proposito il passo sul suicidio nelle stesse Lezioni per la delicatezza del tema) e Michela Murgia (Noi siamo tempesta, sulle storie da raccontare ai bambini per "diventare potenti insieme", p. 6, Salani 2019, confermata su Wikiquote — secondo titolo per l'autrice dopo Chirù). Scartati per mancanza di un locus verificabile: Michela Murgia (Accabadora), Salman Rushdie (I figli della mezzanotte), V.S. Naipaul (Sull'ansa del fiume) e Marguerite Duras (L'amante, già scartata in lotti precedenti, riconfermato). Verificato il bug della duplicazione traduttore: nessuna istanza. Restano 42 autori con una sola citazione. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-29 UTC — added 3 quotes (total now 435) — proseguito l'approfondimento: Anne Frank (Diario, "La natura è davvero l'unica cosa che non tollera surrogati.", p. 221, trad. Arrigo Vita, Mondadori 1966, confermata su Wikiquote — secondo passo dallo stesso diario, verificato che non coincidesse tematicamente con "credo ancora che le persone siano buone di cuore" già in archivio scegliendo un passo su tutt'altro argomento), Doris Lessing (Memorie di una sopravvissuta, sull'essere "più forte e più potente" nascosto negli adolescenti, p. 60, trad. Paola Faini, Lucarini 1986, confermata su Wikiquote — secondo titolo per l'autrice dopo Il taccuino d'oro) e Curzio Malaparte (Kaputt, sul fatto che "il problema non è soltanto polacco, è europeo", parte seconda p. 98, Mondadori 1989, confermata su Wikiquote — secondo titolo per l'autore dopo La pelle, per cui nessun passo aveva un locus verificabile; scartato un altro candidato dallo stesso libro perché troppo delicato da accorciare senza alterarne il senso, riguardando la deportazione degli ebrei di Jassy). Scartati per mancanza di un locus verificabile: Douglas Adams (l'intera serie della Guida galattica, nessuna pagina in nessun titolo), J.M. Barrie (Peter Pan, 31834 caratteri di citazioni senza un solo numero di pagina) e Michail Bulgakov (La guardia bianca, stesso problema già riscontrato con Il Maestro e Margherita). Verificato il bug della duplicazione traduttore: nessuna istanza. Restano 45 autori con una sola citazione. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-29 UTC — added 3 quotes (total now 432) — proseguito l'approfondimento: Arundhati Roy (Il dio delle piccole cose, "forse è vero che tutto può cambiare in un giorno", pp. 43-44, trad. Chiara Gabutti, TEA 2001, confermata su Wikiquote — secondo passo dallo stesso romanzo), Suzanne Collins (La ragazza di fuoco, sulla paura di aver perso per sempre l'amicizia di Gale, pp. 31-32, trad. Simona Brogli e Fabio Paracchini, Mondadori 2010, confermata su Wikiquote — secondo titolo per l'autrice dopo Hunger Games, per cui nessun passo aveva un locus verificabile) e Ursula K. Le Guin (il racconto «Un uomo del popolo», sulla conoscenza necessariamente parziale, p. 133, trad. Giancarlo Carlotti, in «Il giorno del perdono», Fanucci 1997, confermata su Wikiquote — secondo titolo per l'autrice dopo La mano sinistra delle tenebre, per cui nessun passo aveva un locus verificabile). Verificato il bug della duplicazione traduttore: nessuna istanza. Restano 48 autori con una sola citazione. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-29 UTC — added 4 quotes (total now 429) — proseguito l'approfondimento: Philip Roth (Pastorale americana, "Ecco come sappiamo di essere vivi: sbagliando.", p. 38, trad. Vincenzo Mantovani, Einaudi 1998, confermata su Wikiquote — secondo passo dallo stesso romanzo), Don DeLillo (Rumore bianco, la battuta di Murray Siskind sul "leggero rumore di elettricità statica" del nylon, cap. III pp. 14-15, trad. Mario Biondi, Einaudi 1999, confermata su Wikiquote — secondo passo dallo stesso romanzo), Joan Didion (L'anno del pensiero magico, l'incipit "La vita cambia in fretta [...] la vita che conoscevi è finita", citato in «Incipit», Skira 2018, confermata su Wikiquote — secondo titolo per l'autrice dopo The White Album) e Alba de Céspedes (La bambolona, "Il segreto del mio ottimismo consiste nel rinunziare a comprendere gli altri.", p. 43, Oscar Mondadori 1970, confermata su Wikiquote — secondo titolo per l'autrice dopo Quaderno proibito, nessuna copertina reperibile per nessuno dei due nuovi titoli). Scartati per mancanza di un locus verificabile: candidati per Roberto Bolaño (2666, sia la parte dei critici che quella di Amalfitano), J.M. Coetzee (Aspettando i barbari e Vergogna) e Donna Tartt (Il cardellino) — nessuna delle rispettive sezioni Citazioni su Wikiquote riporta un numero di pagina. Verificato il bug della duplicazione traduttore: nessuna istanza. Restano 51 autori con una sola citazione. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-29 UTC — added 4 quotes (total now 425) — proseguito l'approfondimento: Mary Shelley (Frankenstein, l'avvertimento di Victor Frankenstein a Walton "voi pure avete bevuto un sorso della pozione inebriante?", parte prima lettera IV p. 18, trad. J. Maghelli, Edizioni Clandestine 2009, confermata su Wikiquote — secondo passo dallo stesso romanzo), C.S. Lewis (Diario di un dolore, "non è soltanto il proprio soffrire, ma è anche il dover pensare continuamente al proprio soffrire", p. 16, trad. Anna Ravano, Adelphi 1997, confermata su Wikiquote — secondo titolo per l'autore dopo Le cronache di Narnia), Federico García Lorca (la poesia «Romance sonámbulo», il celebre ritornello "Verde che ti voglio verde", citato in «Dizionario delle citazioni», BUR 1992, confermata su Wikiquote — secondo titolo per l'autore dopo La casa di Bernarda Alba) e Terry Pratchett (Il tristo mietitore, la filosofia dei troll sul tempo che "si guarda dalla direzione sbagliata", p. 25, trad. Valentina Daniele, Salani 2008, confermata su Wikiquote — secondo passo dallo stesso romanzo). Verificato il bug della duplicazione traduttore: nessuna istanza. Restano 55 autori con una sola citazione. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-29 UTC — added 4 quotes (total now 421) — proseguito l'approfondimento: Michael Ende (La storia infinita, "Una Storia può essere nuova eppure raccontare di tempi immemorabili. Il passato nasce con lei.", Graogramàn cap. XV, trad. Amina Pandolfi, Longanesi 1981, confermata su Wikiquote — secondo passo dallo stesso romanzo), Neil Gaiman (Coraline, sull'identità che "possa dipendere dal letto in cui ci risvegliamo al mattino", p. 79, trad. Maurizio Bertocci, Mondadori 2004, confermata su Wikiquote — scartato un primo candidato dallo stesso dialogo perché troppo vicino, quasi sovrapponibile, alla citazione già in archivio; secondo passo dallo stesso romanzo), Paulo Coelho (L'Alchimista, "Ascolta il tuo cuore. Esso conosce tutte le cose.", p. 71, trad. Rita Desti, Bompiani 1995, confermata su Wikiquote — secondo passo dallo stesso romanzo) e Dacia Maraini (Il treno dell'ultima notte, sul rastrellamento del ghetto di Roma del 16 ottobre 1943, cap. XIX p. 107, Rizzoli 2008, confermata su Wikiquote — secondo titolo per l'autrice dopo La lunga vita di Marianna Ucrìa, nessuna copertina reperibile). Scartati per mancanza di un locus verificabile: un candidato per Susanna Tamaro (Va' dove ti porta il cuore — l'intera sezione Citazioni su Wikiquote non riporta alcun numero di pagina) e uno per Chinua Achebe (Le cose crollano — stesso problema, già scartato in un lotto precedente, riconfermato). Verificato il bug della duplicazione traduttore: nessuna istanza. Restano 59 autori con una sola citazione. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-29 UTC — added 4 quotes (total now 417) — proseguito l'approfondimento: Sibilla Aleramo (Una donna, sull'"inumana idea dell'immolazione materna" tramandata "di madre in figlia", pp. 252-253, R. Bemporad & figlio 1921, confermata su Wikiquote — secondo passo dallo stesso romanzo), Simone Weil (L'ombra e la grazia, "il potere di dire Io. Quel che bisogna dare a Dio, cioè distruggere, è questo.", p. 38, trad. Franco Fortini, Rusconi 1985, confermata su Wikiquote — secondo passo dallo stesso libro) e Goliarda Sapienza (L'arte della gioia, sul "paternalismo più atroce" di chi si crede indispensabile a chi nutre, cap. 65, Einaudi 2015, confermata su Wikiquote — secondo passo dallo stesso romanzo). **Corretta anche un'attribuzione sbagliata già in archivio, trovata cercando la fonte**: la citazione di George R.R. Martin "Mai dimenticare chi sei [...] fanne un'armatura" era attribuita nel contesto a un monito di Ned Stark ai figli, ma su Wikiquote risulta chiaramente una battuta di Tyrion Lannister a Jon Snow (Il Trono di Spade, p. 66) — corretto il contesto e aggiunta la fonte (Mondadori 2016), stessa procedura delle correzioni Ishiguro/Munro/Murgia della Fase 3. Aggiunta anche una seconda citazione per lo stesso autore, distinta: Viserys Targaryen su "il drago ricorda", p. 38, trad. Sergio Altieri, Mondadori 2016. Scartato un candidato per Yukio Mishima (Confessioni di una maschera e Il padiglione d'oro): nessuna delle due sezioni Citazioni su Wikiquote riporta un numero di pagina, nessun locus verificabile oltre l'incipit già in archivio. Verificato il bug della duplicazione traduttore: nessuna istanza. Restano 63 autori con una sola citazione. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-29 UTC — added 4 quotes (total now 413) — proseguito l'approfondimento, su istruzione dell'utente di continuare senza attendere conferma tra un lotto e l'altro: Erich Maria Remarque (Niente di nuovo sul fronte occidentale, "A nessuno la terra è amica quanto al fante.", p. 41, trad. Stefano Jacini, Mondadori 2015, confermata su Wikiquote — secondo passo dallo stesso romanzo), Louisa May Alcott (Piccole donne, il consiglio sul portare "il vostro piccolo fardello" a chi legge, p. 2346, edizione 2012, confermata su Wikiquote — traduttore ed edizione precisa non attribuibili con certezza in bibliografia, verosimile numerazione da e-book più che da edizione a stampa; citazione accorciata da 70 a 26 parole; secondo passo dallo stesso romanzo), Lucy Maud Montgomery (Anna dai capelli rossi, l'entusiasmo di Anna Shirley "il mondo è così interessante!", cap. II p. 22, trad. Maria Grazia Odorizzi, Nord-Sud 2021, confermata su Wikiquote — secondo passo dallo stesso romanzo) e Harper Lee (Il buio oltre la siepe, Atticus Finch sulla coscienza che "non debba conformarsi al volere della maggioranza", cap. 11, trad. Amalia D'Agostino Schanzer, Feltrinelli, confermata su Wikiquote — secondo passo dallo stesso romanzo). Scartato un candidato per Jack Kerouac (Sulla strada): l'intera sezione Citazioni della pagina Wikiquote non riporta alcun numero di pagina, nessun locus verificabile oltre l'incipit già in archivio. Verificato il bug della duplicazione traduttore: nessuna istanza. Restano 67 autori con una sola citazione. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-29 UTC — added 3 quotes (total now 409) — proseguito l'approfondimento: Giorgio Bassani (Il giardino dei Finzi-Contini, sull'aggrapparsi alla scrivania "come se [...] mi fosse dato di arrestare l'inarrestabile progresso del tempo", parte III cap. VI p. 130, Feltrinelli 2012, confermata su Wikiquote — secondo passo dallo stesso romanzo), Anna Maria Ortese (Il mare non bagna Napoli, dal saggio «Chiaia morta e inquieta» sulla città che "si copriva di rumori [...] per non riflettere più", p. 134, Adelphi 1994, confermata su Wikiquote — citazione accorciata da 57 a 37 parole; secondo passo dalla stessa raccolta) e Salvatore Quasimodo (la poesia «Milano, agosto 1943», "Invano cerchi tra la polvere, povera mano, la città è morta.", dalla raccolta «Giorno dopo giorno», Mondadori 1947, confermata su Wikiquote — secondo titolo per l'autore dopo «Ed è subito sera»). Scartati per mancanza di un locus verificabile: un candidato per Leonardo Sciascia (Il giorno della civetta — l'intera sezione Citazioni della pagina Wikiquote non riporta alcun numero di pagina), uno per Vasco Pratolini (Cronache di poveri amanti — stesso problema, unica citazione disponibile senza pagina) e uno per William Golding (Il Signore delle Mosche — le citazioni con numero di pagina erano esplicitamente marcate "manca l'edizione" su Wikiquote, quindi non attribuibili con certezza). Verificato il bug della duplicazione traduttore: nessuna istanza. Restano 71 autori con una sola citazione. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-29 UTC — added 4 quotes (total now 406) — proseguito l'approfondimento: Anton Čechov (Il gabbiano, la battuta del dottor Dorn sulla folla di Genova in cui "cominci a credere che in realtà sia possibile un'unica anima universale", p. 66, trad. Angelo Maria Ripellino, Einaudi 1970, confermata su Wikiquote — citazione accorciata da 53 a 36 parole; secondo titolo per l'autore dopo Tre sorelle, per cui su Wikiquote esiste solo l'incipit già in archivio), Ippolito Nievo (Le confessioni d'un italiano, "Dove tuona un fatto, siatene certi, ha lampeggiato un'idea.", cap. VI, confermata su Wikiquote — secondo passo dallo stesso romanzo), Umberto Saba (la poesia «Il poeta», "ha le sue giornate contate [...] ma quanto, quanto variate!", p. 204, in «Per conoscere Saba», a cura di Mario Lavagetto, Mondadori 1981, confermata su Wikiquote — secondo titolo per l'autore dopo «Trieste», verificato che la prima citazione trovata coincidesse con quella già in archivio e scartata) e Daphne du Maurier (Rebecca, la prima moglie, sul voler fermare "questo insignificante frammento di tempo" con Maxim, cap. 9 p. 105, trad. Marina Morpurgo, il Saggiatore 2008, confermata su Wikiquote — citazione accorciata da 51 a 36 parole; secondo passo dallo stesso romanzo). Verificato il bug della duplicazione traduttore: nessuna istanza. Restano 74 autori con una sola citazione. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-29 UTC — added 4 quotes (total now 402) — proseguito l'approfondimento: Giuseppe Tomasi di Lampedusa (Il Gattopardo, "L'amore. Certo, l'amore. Fuoco e fiamme per un anno, cenere per trenta.", p. 90, confermata su Wikiquote — traduttore non attribuibile con certezza fra le due edizioni in bibliografia; secondo passo dallo stesso romanzo, verificato che non coincidesse con "se vogliamo che tutto rimanga com'è..." già in archivio), Nikolaj Gogol' (Le anime morte, su Nozdrëv che "ancora per un pezzo non sparirà dalla faccia della terra [...] indossa un altro caffettano", cap. IV p. 69, trad. Agostino Villa, Einaudi 1977, confermata su Wikiquote — secondo passo dallo stesso romanzo; verificato con particolare attenzione un locus reale e non fittizio, dato il precedente errore con questo stesso autore), J.D. Salinger (Il giovane Holden, sul non sopportare gli addii senza accorgersene, cap. I p. 6, trad. Adriana Motti, Einaudi 2008, confermata su Wikiquote — citazione accorciata da 43 a 39 parole; secondo passo dallo stesso romanzo) e Carlo Goldoni (La locandiera, la battuta di Mirandolina sulla locanda che "non ha mai camere in ozio", p. 18, a cura di Gerolamo Bottoni, Carlo Signorelli Editore 1934, confermata su Wikiquote — secondo passo dalla stessa commedia). Scartato un candidato per Michail Bulgakov (Il Maestro e Margherita): l'intera sezione Citazioni della pagina Wikiquote non riporta alcun numero di pagina, nessun locus verificabile oltre l'incipit già in archivio — scartato subito senza inserire, dato anche il precedente errore con questo autore. Verificato il bug della duplicazione traduttore: nessuna istanza. Restano 78 autori con una sola citazione. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-29 UTC — added 4 quotes (total now 398) — proseguito l'approfondimento: Boris Pasternak (Il dottor Živago, "La coscienza sono i fari accesi davanti a una locomotiva che corre.", parte I «L'albero di Natale dagli Sventickij» §3, trad. Pietro Zveteremich e Mario Socrate, Feltrinelli 2018, confermata su Wikiquote — secondo passo dallo stesso romanzo), Stefan Zweig (Il mondo di ieri, sulla missione del docente che disciplina invece di far crescere, p. 47, trad. Lavinia Mazzuchetti, Mondadori 2014, confermata su Wikiquote — secondo titolo per l'autore dopo Novella degli scacchi, per cui non è stato trovato nessun passo con locus verificabile oltre l'incipit già usato), Vittorio Alfieri (Vita, "la vicendevole paura era quella che governava il mondo", Epoca II cap. IV, a cura di Giampaolo Dossena, Einaudi 1967, confermata su Wikiquote — secondo passo dallo stesso libro) e Marguerite Yourcenar (Memorie di Adriano, sull'insonnia come "maniaca ostinazione della nostra mente a fabbricare pensieri", I 1 p. 20, trad. Lidia Storoni Mazzolani, Einaudi 1988, confermata su Wikiquote — secondo passo dallo stesso romanzo). Scartato un candidato per Saul Bellow (Herzog): l'intera sezione Citazioni della pagina Wikiquote non riporta alcun numero di pagina per nessuna delle citazioni elencate — nessun locus verificabile oltre l'incipit già in archivio. Verificato il bug della duplicazione traduttore: nessuna istanza. Restano 82 autori con una sola citazione. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-29 UTC — added 4 quotes (total now 394) — proseguito l'approfondimento: F. Scott Fitzgerald (Il grande Gatsby, la battuta di Daisy Buchanan "spero che sia stupida: è la miglior cosa che una donna possa essere in questo mondo, una bella piccola stupida", p. 26, confermata su Wikiquote — traduttore non attribuibile con certezza fra le due edizioni concordi in bibliografia, coerente con la citazione già in archivio dello stesso titolo; secondo passo dallo stesso romanzo), Sylvia Plath (La campana di vetro, la metafora dell'albero di fico sui futuri possibili di Esther Greenwood, p. 111, trad. Adriana Bottini e Anna Ravano, Mondadori 2017 — unica edizione in bibliografia, confermata su Wikiquote — citazione accorciata da 51 a 35 parole; secondo passo dallo stesso romanzo), Virgilio (Eneide, le parole di Enea ai compagni dopo il naufragio "verrà tempo un dì [...] vi saran dolce ricordo", Libro I vv. 324-326, trad. Annibal Caro 1581, confermata su Wikiquote — secondo passo dallo stesso libro, stessa traduzione della citazione già in archivio) e Fernando Pessoa (Il libro dell'inquietudine, sulla "stanchezza dell'intelligenza astratta", p. 121, a cura di Maria José de Lancastre, Feltrinelli 1987, confermata su Wikiquote — citazione accorciata da 41 a 28 parole; secondo passo dallo stesso libro). Scartato un candidato per Truman Capote (Colazione da Tiffany, il monologo di Holly Golightly sulle creature selvatiche): nessun accorciamento a fine frase riusciva a restare sotto le 40 parole senza perdere il senso del passo, e i tagli intermedi alteravano troppo il testo — rimandato a un prossimo lotto per cercare un passo più breve. Verificato il bug della duplicazione traduttore: nessuna istanza. Restano 86 autori con una sola citazione. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-29 UTC — added 5 quotes (total now 390) — proseguito l'approfondimento: Arthur Schopenhauer (Aforismi sulla saggezza del vivere, "I nove decimi della nostra felicità riposano esclusivamente sulla salute.", cap. II §1 p. 14, confermata su Wikiquote — secondo passo dallo stesso libro), Epitteto (Manuale, "Non devi adoperarti perché gli avvenimenti seguano il tuo desiderio, ma desiderarli così come avvengono...", cap. 8 p. 7, trad. Enrico V. Maltese, Garzanti 2007, confermata su Wikiquote — secondo passo dallo stesso libro, verificato che non coincidesse con la citazione già in archivio dallo stesso capitolo V), Jack London (Il richiamo della foresta, "C'è un'estasi che caratterizza il culmine della vita e oltre la quale la vita non può innalzarsi.", cap. III p. 91, a cura e traduzione di Davide Sapienza, Feltrinelli 2011, confermata su Wikiquote — secondo passo dallo stesso romanzo), Kurt Vonnegut (Mattatoio n. 5, "E io m'interrogai sul presente: quanto fosse vasto, quanto fosse profondo, quanto fosse mio.", cap. 1, trad. Luigi Brioschi, Feltrinelli 2017 — unica edizione in bibliografia, confermata su Wikiquote — secondo passo dallo stesso romanzo, verificato che non coincidesse con "Così va la vita" già in archivio) e Pier Paolo Pasolini (Scritti corsari, sul cambiamento antropologico dei consumi — "l'uomo medio di oggi può interiorizzare una Seicento o un frigorifero" — dall'articolo «La prima, vera rivoluzione di destra» del 15 luglio 1973, p. 28, Garzanti 1975, confermata su Wikiquote — secondo titolo per l'autore dopo Ragazzi di vita). Scartato un candidato per Immanuel Kant (Per la pace perpetua): un secondo passo con pagina (p. 177) esisteva ma la nota bibliografica non permetteva di attribuirlo con certezza a una specifica edizione tra le molte in bibliografia. Verificato il bug della duplicazione traduttore: nessuna istanza. Restano 90 autori con una sola citazione. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-29 UTC — added 6 quotes (total now 385) — proseguito l'approfondimento: Gustave Flaubert (Madame Bovary, "Non bisogna toccare gl'idoli: la doratura ci rimane sulle dita.", parte terza cap. VI p. 315, trad. Natalia Ginzburg, Einaudi 1983, confermata su Wikiquote — secondo passo dallo stesso romanzo), Mark Twain (Le avventure di Huckleberry Finn, l'avviso ironico premesso al romanzo su chi cerca a tutti i costi una morale o una trama, p. 11, trad. Giuseppe Culicchia, Feltrinelli 2005 — unica edizione in bibliografia, confermata su Wikiquote — secondo passo dallo stesso romanzo), Jules Verne (Ventimila leghe sotto i mari, la descrizione dei ritratti di eroi nella cabina del capitano Nemo, parte II cap. VIII, Fanucci 2018, confermata su Wikiquote — traduttore non indicato in bibliografia; citazione accorciata da 43 a 38 parole; secondo passo dallo stesso romanzo, scartato un primo candidato perché coincideva quasi verbatim con la citazione già in archivio), Thomas Hardy (Tess dei d'Urberville, "Le pene maggiori erano dovute all'osservanza delle convenzioni e non a sensazioni naturali.", cap. XIV p. 113, trad. Giuliana Aldi Pompili, Rizzoli 2010, confermata su Wikiquote — secondo passo dallo stesso romanzo, nessuna copertina reperibile), Stendhal (Il rosso e il nero, sulle passioni "ridicole a Parigi" perché i vicini pretendono sempre di contare, cap. XXI, confermata su Wikiquote — traduttore non attribuibile con certezza a una delle edizioni multiple in bibliografia; secondo titolo per l'autore dopo Dell'amore) e Rainer Maria Rilke (Lettere a un giovane poeta, il primo consiglio della raccolta "domandatevi [...] devo io scrivere?", lettera del 12 agosto 1904 p. 55, trad. Leone Traverso, Adelphi 1980, confermata su Wikiquote — secondo passo dalla stessa raccolta). Verificato il bug della duplicazione traduttore: nessuna istanza. Restano 95 autori con una sola citazione. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-29 UTC — added 5 quotes (total now 379) — proseguito l'approfondimento: Arthur Conan Doyle (Il mastino dei Baskerville, "Ben malvagio dev'essere l'uomo che non abbia una donna che lo pianga.", cap. XIII, trad. Nicoletta Rosati Bizzotto, Newton 2006, confermata su Wikiquote — secondo titolo per l'autore dopo Il segno dei quattro), Emily Brontë (Cime tempestose, il grido di Heathcliff dopo la morte di Catherine "Non posso vivere senza la mia vita! Non posso vivere senza la mia anima!", cap. XVI, confermata su Wikiquote — traduttore non indicato per questo passo specifico, coerente con la citazione già in archivio dello stesso autore/titolo — secondo passo dallo stesso romanzo), Charles Baudelaire (I fiori del male, l'ultima strofa della poesia «L'albatro» sul poeta esiliato in terra, trad. Attilio Bertolucci, Garzanti 2006, confermata su Wikiquote — secondo titolo per l'autore dopo Lo spleen di Parigi), Francesco Petrarca (Canzoniere, il sonetto «Pace non trovo, et non ò da far guerra», vv. 1-4, confermata su Wikiquote, testo originale di pubblico dominio — secondo passo dalla stessa raccolta) e Boezio (Della consolazione della filosofia, il passo della Filosofia sull'avversa fortuna che "inganna [...] mentre quella è sempre veritiera", Libro II prosa 8 p. 99, trad. Luca Orbetello, Rusconi 1996, confermata su Wikiquote — secondo passo dallo stesso libro; titolo tenuto identico a quello già in archivio, «Della consolazione della filosofia», anche se questa specifica traduzione lo intitola senza «Della»). Verificato il bug della duplicazione traduttore: nessuna istanza. Restano 101 autori con una sola citazione. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-29 UTC — added 2 quotes (total now 374) — proseguito l'approfondimento: Aldous Huxley (Il mondo nuovo, la battuta di Helmholtz Watson sulle parole paragonate ai raggi X che "attraversano ogni cosa. Leggi, e ti trapassano.", p. 59, in "Il mondo nuovo - Ritorno al mondo nuovo", trad. Lorenzo Gigli rivista da Paola Levante, Mondadori 2014, confermata su Wikiquote — secondo passo dallo stesso romanzo, diversa dalla citazione già in archivio "La felicità non è mai grandiosa.") e Naguib Mahfouz (La via dello zucchero, l'incipit del terzo romanzo della Trilogia del Cairo sulle donne intorno al braciere, citato in AA.VV. «Incipit», Skira 2018, confermata su Wikiquote — secondo titolo per l'autore dopo Vicolo del mortaio; citazione accorciata in fase di inserimento da 54 a 35 parole per rientrare nel tetto delle ~40). Scartati durante la ricerca: un secondo candidato per Naguib Mahfouz (Vicolo del mortaio — l'unica citazione disponibile su Wikiquote coincide esattamente con quella già in archivio) e Imre Kertész (Essere senza destino — la pagina Wikiquote dell'autore contiene solo citazioni da "Kaddish per il bambino non nato", nessun passo attribuibile a "Essere senza destino" con locus verificabile). Verificato il bug della duplicazione traduttore: nessuna istanza. Restano 106 autori con una sola citazione (ricontato direttamente da `data/citazioni.json` invece di decrementare a mano il numero del lotto precedente: il conteggio "107" del lotto precedente risultava già disallineato di un'unità rispetto ai dati reali, probabile effetto di attività di sessioni concorrenti sull'archivio fra un lotto e l'altro — da qui in poi meglio ricontare a ogni lotto anziché fidarsi solo del decremento). **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-29 UTC — added 2 quotes (total now 372) — proseguito l'approfondimento: Khaled Hosseini (E l'eco rispose, "La storia è come un treno in corsa...", p. 91, trad. Isabella Vaj, Piemme 2013, confermata su Wikiquote — secondo titolo per l'autore dopo Il cacciatore di aquiloni) e Jorge Amado (Gabriella, garofano e cannella, l'incipit del romanzo sul delitto d'onore a Ilhéus, trad. Giovanni Passeri, Einaudi, confermata su Wikiquote — secondo titolo per l'autore dopo Capitani della spiaggia). Scartato un candidato per Elif Shafak per mancanza di tempo di verifica approfondita. Verificato il bug della duplicazione traduttore: nessuna istanza. Restano 107 autori con una sola citazione. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-29 UTC — added 2 quotes (total now 370) — proseguito l'approfondimento: Ignazio Silone (Fontamara, "Il mondo è rotondo. Chi parte, perde tempo.", p. 63, Mondadori 1988, confermata su Wikiquote — secondo passo dallo stesso romanzo) e Ian McEwan (Espiazione, il pensiero di Briony Tallis sulla propria vita "in una stanza priva di porta", p. 295, trad. Susanna Basso, Einaudi 2003, confermata su Wikiquote — secondo passo dallo stesso romanzo). Scartato un candidato per Curzio Malaparte (La pelle, "Voglio bene agli americani..."): nessuna pagina reperibile nel lungo blocco di citazioni della sezione "La peste". Verificato il bug della duplicazione traduttore: nessuna istanza. Restano 109 autori con una sola citazione. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-29 UTC — added 3 quotes (total now 368) — proseguito l'approfondimento: Antonio Tabucchi (Sostiene Pereira, "La filosofia sembra che si occupi solo della verità...", cap. IV p. 30, Feltrinelli 2010, confermata su Wikiquote — secondo passo dallo stesso romanzo; scartata la pagina Wikiquote dedicata a "Sostiene Pereira" perché relativa al film del 1995, non al romanzo), Erri De Luca (Il giorno prima della felicità, sul bene e il male nelle persone secondo don Gaetano, p. 9, Feltrinelli 2009, confermata su Wikiquote — secondo passo dallo stesso romanzo) e Alberto Moravia (Gli indifferenti, lo stato d'animo di Michele, cap. XVI p. 284, Bompiani 1995, confermata su Wikiquote — secondo passo dallo stesso romanzo). Verificato il bug della duplicazione traduttore: nessuna istanza. Restano 111 autori con una sola citazione. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-29 UTC — added 2 quotes (total now 365) — proseguito l'approfondimento: Frank Herbert (Dune, "La speranza offusca l'osservazione.", massima della Reverenda Madre Gaius Helen Mohiam, Editore Nord p. 11, trad. Cossato e Sandrelli, confermata su Wikiquote — secondo passo dallo stesso romanzo) e Ray Bradbury (Fahrenheit 451, la battuta del capitano Beatty sui pompieri che bruciano libri, trad. Giorgio Monicelli, Mondadori 1966, p. 9, confermata su Wikiquote — secondo passo dallo stesso romanzo). Non trovato nulla di utilizzabile per Isaac Asimov: le citazioni disponibili su Wikiquote non sono attribuite a un romanzo specifico del ciclo della Fondazione. Verificato il bug della duplicazione traduttore: nessuna istanza. Restano 114 autori con una sola citazione. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-29 UTC — added 1 quote (total now 363) — proseguito l'approfondimento: Günter Grass (Il tamburo di latta, sulla nascita di Oskar Matzerath sotto due lampadine, trad. Lia Seccia, Feltrinelli 2004, pp. 40-41, confermata su Wikiquote — secondo passo dallo stesso romanzo, con edizione/traduttore più precisi di quelli della citazione già in archivio). Lo script di inserimento ha correttamente rifiutato un primo tentativo in cui avevo scritto per errore "traduzione di Lia Seccia" anche in `source_edition`, duplicando il traduttore — corretto al volo, nessuna pagina generata con il bug. Scartati per mancanza di un luogo nel testo verificabile: un candidato per Patrick Süskind (Il profumo, "Colui che dominava gli odori, dominava il cuore degli uomini...", nessuna pagina reperibile) e uno per Herta Müller (Il paese delle prugne verdi, brano lungo e non numerato). Verificato il bug della duplicazione traduttore su tutto l'archivio: nessuna istanza. Restano 116 autori con una sola citazione. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-29 UTC — added 2 quotes (total now 362) — proseguito l'approfondimento: Margaret Atwood (Il racconto dell'ancella, l'incipit nella palestra riconvertita in dormitorio, trad. Camillo Pennati, Ponte alle Grazie 2004, confermata su Wikiquote — citazione accorciata da 46 a 29 parole per rientrare nel tetto delle ~40; secondo passo dallo stesso romanzo) e Marilynne Robinson (Gilead, l'incipit della lunga lettera del pastore John Ames al figlio, trad. Eva Kampmann, Einaudi 2017, confermata su Wikiquote tramite citazione in Incipit/Skira 2018 — secondo passo dallo stesso romanzo). **Precisazione sul locus "incipit"**: rileggendo alcune citazioni già in archivio (Robinson, Atwood stesse) risulta che "incipit" — o una descrizione equivalente della posizione nel testo, come "inciso nell'armadio della protagonista" — è già un locus valido e consolidato nel sito, non serve necessariamente un numero di pagina quando la citazione è l'apertura del libro: aggiorna la lettura troppo restrittiva usata nei lotti precedenti di questa sessione, dove candidati-incipit senza pagina erano stati scartati per eccesso di cautela. Scartati comunque, perché non erano incipit e restavano privi di un luogo preciso: un secondo candidato per Alice Munro (Nemico, amico, amante...) e la citazione di Atwood sulla libertà ("Esiste più di un genere di libertà...", dalla stessa opera ma da un punto imprecisato del testo). Verificato il bug della duplicazione traduttore: nessuna istanza. Restano 117 autori con una sola citazione. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-29 UTC — added 2 quotes (total now 360) — proseguito l'approfondimento: Zadie Smith (Denti bianchi, l'incipit del romanzo su Alfred Archibald, citato in AA.VV. «Il libro della letteratura», Gribaudo 2019, p. 324, secondo passo dallo stesso romanzo) e Ta-Nehisi Coates (Tra me e il mondo, "La razza è la figlia del razzismo, non la madre...", citato in AA.VV. «Il libro della black history», Gribaudo 2022, p. 157, secondo passo dallo stesso libro). Non trovato nulla di utilizzabile per Chimamanda Ngozi Adichie (Americanah): le citazioni disponibili su Wikiquote sono aforismi generali dell'autrice, non attribuiti a un romanzo specifico. Verificato il bug della duplicazione traduttore: nessuna istanza. Restano 119 autori con una sola citazione. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-29 UTC — added 1 quote (total now 358) — proseguito l'approfondimento: Michael Ondaatje (Il paziente inglese, un'immagine dall'apertura del romanzo sul mutamento del tempo nel giardino della villa italiana, citata in AA.VV. «Il libro della letteratura», Gribaudo 2019, p. 336 — fonte secondaria con pagina precisa, non l'edizione originale del romanzo, accettata come da precedente già in uso in archivio per gli incipit citati da compilazioni). Scartato un candidato per Salman Rushdie (I figli della mezzanotte, "sono la somma di tutto ciò che è accaduto prima di me...", trad. Ettore Capriolo, Garzanti 1987 — traduttore ed edizione certi, ma nessuna pagina reperibile né su Wikiquote né altrove) e non trovato nulla di utilizzabile per Mario Vargas Llosa (nessuna voce Wikiquote per "Conversazione nella Catedral"). Verificato il bug della duplicazione traduttore: nessuna istanza. Restano 121 autori con una sola citazione. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-29 UTC — added 2 quotes (total now 357) — proseguito l'approfondimento: Wisława Szymborska (la poesia «Nulla è in regalo!», "Nulla è in regalo, tutto è in prestito...", trad. Pietro Marchesani, in «25 poesie», Mondadori 1998, confermata su Wikiquote — secondo titolo per l'autrice dopo «Amore a prima vista») e Seamus Heaney (la poesia «L'Uomo di Grauballe», sull'apertura del componimento ispirato a un corpo mummificato ritrovato in una torbiera, in «Scavando. Poesie scelte», a cura di Franco Buffoni, Fondazione Piazzolla 1991, p. 70, confermata su Wikiquote — secondo titolo per l'autore dopo «Morte di un naturalista»; nessuna copertina, quella disponibile per «North» avrebbe rappresentato la raccolta e non la singola poesia, coerente con "meglio nessuna copertina che una fuorviante"). Scartati per mancanza di un luogo nel testo verificabile: un candidato per Amin Maalouf (Il manoscritto di Samarcanda — solo l'incipit già in archivio è disponibile, nessun'altra citazione con fonte) e uno per Julian Barnes (Il senso di una fine — l'unico altro passo disponibile è l'incipit, una lista di immagini frammentate poco adatta a una citazione autonoma). Verificato il bug della duplicazione traduttore: nessuna istanza. Restano 122 autori con una sola citazione. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-29 UTC — **Corretto un bug in `tools/build.py`, non mio ma di una sessione concorrente**: la funzione `main()` chiamava `gh.main()` (generate_home, che scrive `index.html` leggendo gli slug da `slugs.json` su disco) prima di `qp.main()`, che è la funzione che effettivamente assegna e salva su disco gli slug delle citazioni nuove. Risultato: `python3 tools/build.py` falliva sempre con "slug mancante" al primo lancio dopo l'aggiunta di qualunque citazione nuova — esattamente il caso d'uso di ogni lotto. Individuato mentre provavo a fare la build di questo lotto (Hurston, Canetti). Corretto spostando la chiamata a `gh.main()` subito dopo `qp.main()`, quando `slugs.json` è già aggiornato; verificato che la build torni a funzionare e che `index.html` includa correttamente le nuove citazioni. Nota il commit precedente non mio (`a69a86c`, di un'altra sessione concorrente) su questo stesso repository: da tenere d'occhio, verificare `git status` con più attenzione nei prossimi lotti.
- 2026-08-28 UTC — added 2 quotes (total now 355) — proseguito l'approfondimento: Zora Neale Hurston (I loro occhi guardavano Dio, "Due sono le cose che ognuno deve far da sé: avvicinarsi a Dio e imparare a vivere la propria vita.", cap. XX p. 285, trad. Ada Prospero, Frassinelli 1948, confermata su Wikiquote — secondo passo dallo stesso romanzo) ed Elias Canetti (Auto da fé, "I romanzi sono dei cunei...", p. 47, trad. Luciano e Bianca Zagari, Adelphi 1981, confermata su Wikiquote). Scartati per mancanza di un luogo nel testo verificabile: un secondo candidato per Amos Oz (Una storia di amore e di tenebra — la citazione già in archivio per questo autore ha anch'essa il locus vuoto, gap pre-esistente non risolto ora), uno per Chinua Achebe (Le cose crollano — stesso titolo già in archivio, il nuovo candidato non ha pagina), uno per Julio Cortázar (Il gioco del mondo — ambiguità su quale porzione del dialogo corrisponda alla pagina indicata) e uno per Naguib Mahfouz (Vicolo del mortaio — l'unica citazione disponibile coincide con quella già in archivio). Verificato il bug della duplicazione traduttore: nessuna istanza. Restano 124 autori con una sola citazione. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-28 UTC — added 2 quotes (total now 353) — proseguito l'approfondimento: Karen Blixen (La mia Africa, "Sempre mi è parso nobile l'indigeno e insulso l'immigrato.", p. 24, trad. Lucia Drudi Demby, Garzanti 1966, confermata su Wikiquote — secondo passo dallo stesso libro) e Sandro Veronesi (Il colibrì, sul destino dei rapporti umani deciso "all'inizio, una volta per tutte", capitolo «Un filo, un Mago, tre crepe (1992-95)», La nave di Teseo 2019, confermata su Wikiquote — secondo passo dallo stesso romanzo; citazione accorciata in fase di inserimento da 43 a 24 parole per rientrare nel tetto delle ~40 parole per autori sotto copyright). Scartato un candidato per Marguerite Duras (L'amante): l'unica citazione utile trovata su Wikiquote non ha un numero di pagina associato, a differenza delle altre citazioni sulla stessa pagina — luogo nel testo non verificabile. Verificato il bug della duplicazione traduttore: nessuna istanza. Restano 126 autori con una sola citazione. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-28 UTC — added 2 quotes (total now 351) — proseguito l'approfondimento: Carlo Levi (Cristo si è fermato a Eboli, "Nessuno ha toccato questa terra se non come un conquistatore o un nemico o un visitatore incomprensivo.", cap. I, Einaudi 1990, confermata su Wikiquote — secondo passo dallo stesso libro, stesso capitolo dell'incipit già in archivio) e Niccolò Ammaniti (Io non ho paura, "Da piccolo sognavo sempre i mostri...", p. 118, Einaudi 2001, confermata su Wikiquote — secondo passo dallo stesso romanzo). Verificato il bug della duplicazione traduttore: nessuna istanza. Restano 128 autori con una sola citazione. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-28 UTC — added 2 quotes (total now 349) — proseguito l'approfondimento: Beppe Fenoglio (Una questione privata, il bisogno ossessivo di Milton di sapere la verità su Fulvia, p. 24, Einaudi 2006, confermata su Wikiquote — secondo passo dallo stesso romanzo) ed Elio Vittorini (Il garofano rosso, "L'umanità è tutta divisa da patti e alleanze contro le paure.", cap. II, Oscar Mondadori 1979, confermata su Wikiquote — secondo titolo per l'autore dopo Conversazione in Sicilia). Scartati durante la ricerca, senza inserirli: un candidato per Ippolito Nievo (Le confessioni di un italiano — nessun passo abbastanza autonomo trovato in tempi ragionevoli nel capitolo esplorato su Wikisource) e uno per Anton Čechov già annotato nel lotto precedente. **Aggiunto un controllo automatico allo script di inserimento**: da questo lotto in poi lo script rifiuta esplicitamente qualsiasi citazione con `source_locus` vuoto o contenente "non indicato", per evitare di ripetere l'errore dei casi Gogol'/Bulgakov. Verificato il bug della duplicazione traduttore: nessuna istanza. Restano 130 autori con una sola citazione. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-28 UTC — added 2 quotes (total now 347) — proseguito l'approfondimento: Isabel Allende (La casa degli spiriti, "La terra è l'unica cosa che rimane quando tutto finisce.", parole di Esteban Trueba, cap. X p. 263, trad. Angelo Morino e Sonia Piloto di Castri, Feltrinelli 1983 — unica edizione italiana in bibliografia, secondo passo dallo stesso romanzo dopo l'incipit già in archivio) e Dino Buzzati (Il deserto dei Tartari, sull'attesa che consuma la vita degli ufficiali della Fortezza Bastiani, cap. 7, Mondadori 1958, confermata su Wikiquote — secondo passo dallo stesso romanzo). **Scartato subito, applicando il promemoria appena scritto**: un candidato per Michail Bulgakov (Il Maestro e Margherita, "L'insulto è la ricompensa abituale di un lavoro ben fatto.") era stato inserito con lo stesso segnaposto fittizio già corretto nel caso Gogol' — individuato e rimosso prima ancora della build, senza propagare l'errore. Scartato anche un candidato per Anton Čechov (Tre sorelle): l'unica citazione disponibile su Wikiquote rimanda a una nota bibliografica non presente nella bibliografia della pagina. Verificato il bug della duplicazione traduttore: nessuna istanza. Restano 132 autori con una sola citazione. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-28 UTC — added 1 quote (total now 345) — proseguito l'approfondimento: George Eliot (Middlemarch, "A che scopo viviamo, se non per renderci reciprocamente la vita meno difficile?", libro VIII cap. LXXII, trad. Michele Bottalico, a cura di Silvano Sabbadini, Mondadori 2020 — unica edizione italiana elencata in bibliografia sulla pagina Wikiquote, quindi attribuibile senza ambiguità; secondo passo dallo stesso romanzo dopo quello già in archivio per il tema verità). **Candidato scartato dopo l'inserimento e poi rimosso**: un secondo passo di Nikolaj Gogol' (Le anime morte, "Hanno un bell'essere stupide le parole dello sventato...") era stato inserito con un luogo nel testo fittizio ("cap. non indicato") perché né Wikiquote né altre fonti indicano il capitolo — un controllo a posteriori ha rivelato l'errore (il campo va lasciato vuoto o la citazione va scartata, mai riempito con un segnaposto) ed è stato corretto rimuovendo la citazione, ripulendo anche il file OG orfano generato nel frattempo. **Nota per i lotti futuri**: se il luogo nel testo non è verificabile, scartare subito, non inventare un valore placeholder. Verificato il bug della duplicazione traduttore: nessuna istanza. Restano 134 autori con una sola citazione. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-28 UTC — added 2 quotes (total now 344) — proseguito l'approfondimento: Joseph Conrad (Cuore di tenebra, la fedeltà di Marlow a Kurtz "fino in fondo all'incubo", cap. III, trad. Luisa Saraval, Garzanti 1990, confermata su Wikiquote — diversa dalla citazione già in archivio, "L'orrore! L'orrore!") e Bram Stoker (Dracula, la descrizione fisica del conte fatta da Jonathan Harker, cap. II, trad. Angelo Nessi, Sonzogno 1922, confermata su Wikisource — diversa dalla citazione già in archivio). Scartato durante la ricerca un candidato per H.G. Wells (La macchina del tempo): la sezione "Citazioni" della pagina Wikiquote passa direttamente al testo successivo senza alcuna parentesi di edizione, a differenza di tutte le altre sezioni della stessa pagina — attribuzione traduttore/edizione non verificabile. Copertine riusate da quelle già in archivio. Verificato il bug della duplicazione traduttore: nessuna istanza. Restano 136 autori con una sola citazione. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-28 UTC — added 5 quotes (total now 342) — proseguito l'approfondimento, su istruzione "riprendi con le citazioni, segui la costituzione e non aspettare il mio via libera": Carlo Collodi (Le avventure di Pinocchio, l'ammonimento del Grillo-parlante su chi non vuole né studiare né imparare un mestiere, cap. IV, confermata su Wikisource, testo originale); Omero (Odissea, i primi versi del poema — l'invocazione alla Musa — trad. Ippolito Pindemonte 1822, confermata su Wikisource, secondo titolo per l'autore dopo Iliade); Giovanni Pascoli (la poesia «Il lampo», da Myricae sez. Tristezze, Livorno 1905, confermata su Wikisource, secondo titolo per l'autore dopo X Agosto); Sant'Agostino (Confessioni, l'invocazione di apertura dell'opera, "Ci hai fatti per te, e il nostro cuore non ha posa finché non riposa in te", trad. Michele Pellegrino, Einaudi 1966, confermata su Wikiquote — la citazione già in archivio dello stesso autore non aveva un traduttore specifico indicato, essendo stata verificata su più edizioni concordanti; questa volta si è scelta una singola traduzione con attribuzione precisa); Marco Tullio Cicerone (Il Catone Maggiore, sul dialogo sulla vecchiaia dedicato all'amico Attico, "L'avarizia in età avanzata è insensata...", cap. VII, trad. Michele Battaglia, in "Elogio della vecchiaia" di Paolo Mantegazza 1993, confermata su Wikiquote — secondo titolo per l'autore dopo L'amicizia). Copertine verificate su Open Library per Omero e Cicerone (nuove ricerche), riusate per gli altri tre titoli già presenti in archivio. Verificato il bug della duplicazione traduttore: nessuna istanza. Restano 138 autori con una sola citazione. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-28 UTC — added 2 quotes (total now 337) — proseguito l'approfondimento: Voltaire (Candido, la filosofia dell'ottimismo di Pangloss, "È dimostrato... tutto è necessariamente per l'ottimo fine.", Parte I cap. I, trad. anonima, Sonzogno 1882, confermata su Wikisource) e Robert Louis Stevenson (Lo strano caso del dottor Jekyll e del signor Hyde, la confessione finale di Jekyll, "l'uomo in verità non è uno, ma due", cap. X, trad. Franco Perini 2016, confermata su Wikisource). Copertine riusate da quelle già in archivio per gli stessi titoli. Verificato il bug della duplicazione traduttore: nessuna istanza. Restano 143 autori con una sola citazione.

- 2026-08-28 UTC — added 6 quotes (total now 335) — avviato, su istruzione dell'utente, il lavoro di approfondimento indicato al punto 5 di CATALOGO.md ("approfondire vale più che allargare": 151 autori su 220 hanno una sola citazione). Primo lotto di sei autori portati da 1 a 2 citazioni, scelti fra i classici di pubblico dominio per poter linkare la fonte primaria: Miguel de Cervantes (Don Chisciotte della Mancia, l'episodio dei mulini a vento scambiati per giganti, cap. VIII, trad. Bartolommeo Gamba 1841, confermata su Wikisource); Niccolò Machiavelli (Il Principe, cap. XVIII, il passo da cui discende — semplificato e mai scritto in questi termini dall'autore — il motto "il fine giustifica i mezzi", confermata su Wikisource, testo originale italiano); Jane Austen (Orgoglio e pregiudizio, la distinzione fra orgoglio e vanità pronunciata da Mary Bennet, trad. Giulio Caprin, Oscar Mondadori 2014, p. 19, confermata su Wikiquote); Giovanni Boccaccio (Decameron, giornata V novella IX, le parole di Federigo degli Alberighi che confessa di aver servito a pranzo il proprio falcone, a cura di Aldo Francesco Massera, Laterza 1927, confermata su Wikisource); Charlotte Brontë (Jane Eyre, "Lettore, lo sposai", incipit dell'ultimo capitolo, edizione Treves 1904 di pubblico dominio, traduttore non indicato nei metadati della fonte, testo verificato dal PDF integrale su Liber Liber); Honoré de Balzac (Papà Goriot, "L'insuccesso ci fa sentire sempre il potere delle nostre pretese", trad. Giuseppe Pallavicini Caffarelli, Mondadori 1995, p. 109, confermata su Wikiquote tramite riscontro incrociato fra citazione e nota bibliografica). Scartato durante la ricerca un candidato per Gustave Flaubert (Madame Bovary): la sezione "Citazioni" della pagina Wikiquote segue una comparazione di cinque diverse traduzioni dell'incipit senza che sia chiaro a quale delle cinque edizioni si riferiscano le citazioni successive — attribuzione non risolvibile con le fonti disponibili. Verificato su tutto l'archivio il bug della duplicazione traduttore: nessuna istanza. Copertine riusate da quelle già presenti in archivio per gli stessi titoli (nessuna nuova ricerca necessaria). Nessuna nuova scheda autore richiesta (tutti e sei già presenti). **Lavoro di approfondimento appena iniziato**: restano 145 autori con una sola citazione. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-28 UTC — added 3 quotes (total now 329) — prosecuzione del Lotto 6 su istruzione "aggiungi citazioni senza aspettare il via libera", coperti altri tre dei temi rimasti aperti. Pace — Immanuel Kant (Per la pace perpetua, "Lo stato di pace fra esseri umani che vivono in reciproca vicinanza non è uno stato di natura, il quale è piuttosto uno stato di guerra.", apertura della Seconda sezione, trad. Maria Chiara Pievatolo 2011, confermata su Wikisource — primo autore sul sito, scritta la scheda). Lavoro — Primo Levi (La chiave a stella, "Si può e si deve combattere perché il frutto del lavoro rimanga nelle mani di chi lo fa...", Einaudi 1978, p. 81 secondo una fonte secondaria indipendente essendo assente il numero di pagina su Wikiquote per questa citazione — terzo titolo per l'autore). Infanzia — Marcel Proust (Alla ricerca del tempo perduto, un episodio di memoria involontaria collegato a un ricordo d'infanzia a Combray, meccanismo analogo a quello della madeleine, trad. Paolo Pinto, Newton Compton 1990, vol. I p. 402, confermata su Wikiquote — secondo passo dalla stessa opera). Restano ancora aperti montagna e figli: scartato durante la ricerca un candidato per montagna (Petrarca, Ascesa al Monte Ventoso, Familiares IV,1) per l'impossibilità di attribuire con certezza il traduttore della resa italiana reperita online — nessun candidato solido trovato per figli in questo lotto. **Con queste 3 citazioni il Lotto 6 arriva a un totale di 8 (guerra, animali, musica, natura, pace, lavoro, infanzia)**, sufficiente a considerarlo concluso salvo eventuale ripresa futura su montagna e figli. Verificato su tutto l'archivio il bug della duplicazione traduttore: nessuna istanza. Copertine verificate su Open Library per tutte e 3 (Kant: edizione Editori Riuniti, diversa da quella citata per il testo ma corretta come opera; Levi: edizione tedesca Wagenbach, corretta come opera; Proust: riuso della copertina già in archivio per lo stesso titolo). **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-28 UTC — added 5 quotes (total now 326) — Lotto 6 di CATALOGO.md, temi con domanda alta e copertura quasi nulla (guerra, natura, animali, musica, montagna, figli, infanzia, lavoro, pace), eseguito in autonomia su istruzione "procedi con nuove citazioni". Coperti i quattro temi con la domanda più alta: guerra — Erich Maria Remarque (Niente di nuovo sul fronte occidentale, "Siamo dei morti spietati...", trad. Stefano Jacini rivista da Elena Broseghini, Mondadori 2015, p. 84, primo autore sul sito) ed Ernest Hemingway (Addio alle armi, "Ero sempre imbarazzato dalle parole sacro, glorioso e sacrificio...", trad. Fernanda Pivano, Mondadori 2007, pp. 175-176, terzo titolo per l'autore); animali — Jack London (Il richiamo della foresta, epigrafe del cap. I sulla "bestia primordiale" che si risveglia in Buck, trad. Gian Dàuli, Modernissima 1924, confermata su Wikisource, primo autore sul sito); musica — Friedrich Nietzsche (Il crepuscolo degli idoli, "Senza musica la vita sarebbe un errore.", Massime e arguzie n. 33, Casa editrice Sociale 1924, confermata su Wikisource — traduttore non indicato nei metadati della fonte, non attribuibile con certezza); natura — Ralph Waldo Emerson (il saggio "La natura", dalla seconda serie dei Saggi, "Qui vi è una santità che fa arrossire le nostre religioni...", trad. Mario Cossa, Laterza 1911, p. 446, testo estratto e verificato dal PDF integrale su Liber Liber, secondo titolo per l'autore dopo Fiducia in se stessi). Non affrontati per mancanza di tempo/candidati solidi in questo lotto: montagna, figli, infanzia, lavoro, pace — restano aperti per un lotto successivo. Copertine verificate su Open Library per tutte tranne Emerson: la copertina disponibile per "Nature" corrisponde al saggio omonimo del 1836, un'opera diversa da quella qui citata (il saggio "La natura" della seconda serie dei Saggi, 1844) — scartata perché avrebbe illustrato il titolo giusto ma l'edizione sbagliata, tile placeholder. Scritte le schede per i 2 nuovi autori (Remarque, Jack London). Verificato su tutto l'archivio il bug della duplicazione traduttore: nessuna istanza. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-28 UTC — added 2 quotes (total now 321) — pubblicata la raccolta "La bellezza", completando il Lotto 5 di CATALOGO.md. Trovate le ultime due citazioni mancanti (si era fermi a 6/8): Victor Hugo, Notre-Dame de Paris ("Ogni faccia, ogni pietra del venerabile monumento è una pagina non soltanto della storia del paese, ma anche della storia della scienza e dell'arte.", trad. Luigi Galeazzo Tenconi, Rizzoli 1951, vol. I pp. 128-129, confermata su Wikiquote — secondo passo dallo stesso romanzo, già in archivio per il tema amore) ed Emily Dickinson, Poesie ("La bellezza non ha causa: esiste. Inseguila e sparisce. Non inseguirla e rimane.", trad. Margherita Guidacci, Cya 1947, J516/Fr654 — secondo passo dalla stessa raccolta, già in archivio per il tema vita). Scartata di nuovo, con lo stesso motivo di scarto della sessione precedente, una citazione di Simone Weil su bellezza e incarnazione: due fonti indipendenti la attribuiscono a due opere diverse (Attesa di Dio secondo Wikiquote, L'ombra e la grazia secondo un altro sito), incertezza sull'opera di provenienza non risolvibile con le fonti disponibili. La raccolta "La bellezza" raggiunge così la soglia di 8 citazioni pertinenti (Dostoevskij, Mann, Sant'Agostino, Ferrante, Wilde, Stendhal, Hugo, Dickinson) ed è stata pubblicata in `/raccolte/bellezza/`, introduzione editoriale scritta a mano. **Con questa pubblicazione il Lotto 5 di CATALOGO.md risulta completo** (cambiamento, sogni, tristezza, bellezza — quattro raccolte pubblicate). Verificato su tutto l'archivio il bug della duplicazione traduttore: nessuna istanza. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-28 UTC — added 8 quotes (total now 319) — Lotto 7 di CATALOGO.md, contemporanei sotto copyright, candidati mostrati e approvati dall'utente prima dell'inserimento. Charles Bukowski, primo autore sul sito (4, tetto massimo per un autore nuovo), tutte trad. Simona Viciani/Feltrinelli, testo verificato byte per byte sul codice sorgente di Wikiquote (non su riassunti automatici) per escludere errori di attribuzione pagina: Factotum ("Ero il tipo d'uomo che rifioriva con la solitudine...", p. 32), Post Office ("Il cibo fa bene ai nervi e allo spirito...", p. 50), Donne ("I grandi uomini sono i più soli.", p. 27), Pulp ("L'uomo nasce per morire...", p. 15, ed. it. Feltrinelli 1995). Andrea Camilleri, primo autore sul sito (4): Il ladro di merendine ("Quella era l'amicizia siciliana, la vera...", Sellerio 2007, p. 170), La stagione della caccia ("A me, che non sono nobile, fa piacere appartenere proprio al Circolo dei nobili...", Sellerio 1998, p. 18), Il campo del vasaio ("Meglio piccamora non pinsaricci...", Sellerio 2008, p. 273), La pensione Eva ("Talè che cosa stramma. L'angili erano tali e quali all'òmini!", Sellerio 2021, p. 160, romanzo del 2006 originariamente Mondadori). **Scartati durante la ricerca, confermando un problema già segnalato in CATALOGO.md**: Sarah J. Maas e Leigh Bardugo, per cui non esiste una pagina Wikiquote né alcuna fonte con capitolo/pagina verificabile — solo blog di recensioni e aggregatori di frasi, esplicitamente esclusi dalle fonti ammesse dal punto 6 di CATALOGO.md. Il lotto risulta quindi di 8 citazioni anziché 10-15, scelta discussa e approvata dall'utente (meglio 8 solide che forzare due autori non sourceable). Rispettati gli altri parametri del punto 10: max 4 per autore, max 1 per opera (8 opere diverse), nessun umore oltre il 30% (verità a 3/8). Copertine verificate su Open Library per tutte e 8, guardate prima di accettarle: per Bukowski scelte le edizioni originali inglesi (Factotum, Post Office, Donne/Women, Pulp), coerente con il precedente già in uso per Shakespeare; per Camilleri tre copertine Sellerio (una delle quali frontespizio anziché copertina illustrata, comunque corretta) e una copertina Mondadori (La pensione Eva, editore della prima edizione 2006). Verificato su tutto l'archivio il bug della duplicazione traduttore: nessuna istanza. Scritte le schede per i 2 nuovi autori (Bukowski, Camilleri). **Nota a parte, non di questo lotto**: durante i controlli è emerso un contesto identico tra due citazioni preesistenti e non correlate (Dostoevskij/Delitto e castigo e Sciascia/Il giorno della civetta) — probabile refuso di un lotto precedente, non ancora corretto, da investigare. **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-28 UTC — added 7 quotes (total now 311) — completamento del Lotto 5 di CATALOGO.md (raccolte quasi pronte), pubblicate le raccolte "I sogni" e "La tristezza". Per ciascun tema, la rilettura dell'archivio aveva trovato solo 4-6 citazioni pertinenti: raggiunta la soglia di 8 con nuove citazioni verificate. Sogni (4 nuove): William Shakespeare (La Tempesta, monologo di Prospero dopo lo spettacolo di spiriti, atto IV scena I, trad. Carlo Rusconi 1858, confermata su Wikisource, testo raw verificato byte per byte per escludere riassunti generati); Edgar Allan Poe (Un sogno nel sogno, versi finali, trad. Ulisse Ortensi 1930, confermata su Wikisource); Lewis Carroll (Attraverso lo specchio, ultime righe del romanzo, trad. Silvio Spaventa Filippi 1914, confermata su Wikisource — secondo titolo per l'autore dopo Alice nel paese delle meraviglie); più il riuso in raccolta di Paulo Coelho (L'Alchimista, già in archivio, pertinente perché l'intero romanzo è costruito attorno a un sogno ricorrente del protagonista). Tristezza (2 nuove): Giacomo Leopardi (A se stesso, vv. 9-12, edizione originale Starita/Napoli 1835, confermata su Wikisource — quarto titolo per l'autore); Giuseppe Ungaretti (Il dolore, versi finali di «Tutto ho perduto», scritta dopo la morte del fratello Costantino nel 1937, confermata su Wikiquote e incrociata con fonti secondarie indipendenti concordanti — terzo titolo per l'autore dopo L'allegria). Scartati durante la ricerca per il tema bellezza, con lo stesso rigore: John Keats (Ode su un'urna greca — l'unica traduzione italiana reperibile su Wikiquote aveva un'attribuzione di edizione dall'aspetto inattendibile, nessun traduttore indicato); Rilke (Elegie duinesi — reperibili solo fonti secondarie con accesso bloccato, non verificabile in tempi ragionevoli); Simone Weil (una stessa citazione italiana attribuita da due fonti indipendenti a due opere diverse — Attesa di Dio secondo Wikiquote, L'ombra e la grazia secondo un'altra fonte — scartata per l'incertezza sull'opera di provenienza, non solo sulla resa linguistica); Platone/Simposio (nessun testo italiano reperibile su Wikisource). **La raccolta "La bellezza" resta sotto soglia** (6 citazioni pertinenti: 4 già in archivio — Dostoevskij, Mann, Ferrante, Sant'Agostino — più due nuove aggiunte comunque all'archivio perché di buona qualità, Oscar Wilde da Il ritratto di Dorian Gray, trad. Marco Amante/Garzanti 2016, confermata su Wikiquote, e Stendhal da Dell'amore, trad. Massimo Bontempelli/Mondadori 1952, confermata su Wikiquote e incrociata con il testo francese originale su Wikisource — primo titolo per l'autore, scritta la scheda). Per questa raccolta, come previsto dal punto 10 di CATALOGO.md ("richiede sempre l'ok" per una raccolta che non raggiunge la soglia), **mi fermo e chiedo indicazioni** invece di pubblicarla sotto soglia o forzare altre due citazioni trovate con minor rigore. Verificato su tutto l'archivio il bug della duplicazione traduttore: nessuna istanza nelle 7 nuove citazioni. Copertine verificate su Open Library per tutte: scartata quella di "Attraverso lo specchio" (una semplice legatura rossa generica, non riconducibile con certezza a quell'edizione) e quella di "Un sogno nel sogno" (nessuna disponibile per una singola poesia); accettate quelle di Stendhal (Folio classique, corrispondenza titolo/copertina verificata visivamente), Shakespeare (frontespizio di un'edizione settecentesca de La Tempesta) e il riuso della copertina già presente per Il ritratto di Dorian Gray. Scritta la scheda per il nuovo autore (Stendhal). **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-28 UTC — pubblicata la raccolta "Il cambiamento" (`data/raccolte.json`, `/raccolte/cambiamento/`), Lotto 5 di CATALOGO.md (raccolte quasi pronte). A differenza degli altri lotti, non sono state aggiunte nuove citazioni: rileggendo con attenzione le 304 citazioni già in archivio (non solo per parola chiave ma per pertinenza reale del passo), sono emerse 8 citazioni genuinamente centrate sul tema del cambiamento/della trasformazione, già sufficienti per superare la soglia di pubblicazione — Mary Shelley (Frankenstein, "un grande cambiamento improvviso"), Franz Kafka (La metamorfosi, il risveglio di Gregor Samsa), Octavia E. Butler (La parabola del seminatore, "Dio è cambiamento"), Friedrich Nietzsche (Così parlò Zarathustra, le tre metamorfosi dello spirito), Giuseppe Tomasi di Lampedusa (Il Gattopardo, "bisogna che tutto cambi"), James Baldwin (La prossima volta il fuoco), Carlo Goldoni (La locandiera, il cambiamento di stato di Mirandolina) e Italo Calvino (Palomar). Nessun umore/autore ripetuto oltre una volta, buona distribuzione di secoli (dal Cinquecento — Goldoni è Settecento, correzione: dal Settecento al 2020). Introduzione editoriale scritta a mano. Le altre tre raccolte quasi pronte del Lotto 5 (bellezza, sogni, tristezza) restano aperte: la rilettura dell'archivio ha trovato solo 4-6 citazioni pertinenti per ciascuna, sotto soglia — richiedono nuove citazioni verificate, ricerca in corso.

- 2026-08-28 UTC — added 10 quotes (total now 304) — Lotto 4 di CATALOGO.md, canone scolastico italiano poco coperto, proseguito in autonomia senza richiedere l'ok (come da istruzione dell'utente dopo l'approvazione del Lotto 3). Carlo Goldoni (La locandiera, battuta finale di Mirandolina, atto III, primo autore sul sito), Vittorio Alfieri (Vita, incipit "Nella città d'Asti in Piemonte...", Epoca I cap. I, primo autore sul sito), Ugo Foscolo (Ultime lettere di Jacopo Ortis, prima lettera "Il sacrificio della patria nostra...", secondo titolo dopo Dei Sepolcri), Giovanni Verga (Mastro-don Gesualdo, incipit, secondo titolo dopo I Malavoglia), Italo Svevo (Senilità, prima dichiarazione di Emilio ad Angiolina, secondo titolo dopo La coscienza di Zeno), Ludovico Ariosto (Orlando furioso, "Non son, non sono io quel che paio in viso", canto XXIII ott. 128, la pazzia di Orlando), Torquato Tasso (Gerusalemme liberata, ultime parole di Clorinda, canto XII ott. 66), Grazia Deledda (Elias Portolu, incipit, secondo titolo dopo Canne al vento), Natalia Ginzburg (Le piccole virtù, sull'educare i figli alle "grandi virtù", p. 121, secondo titolo dopo Lessico famigliare), Eugenio Montale (Ossi di seppia, prima strofa di «Meriggiare pallido e assorto», secondo passo dopo quello già in archivio dalla stessa raccolta). Tutte le fonti confermate su Wikisource (7/10, link diretto verificato via fetch) o Wikiquote (Ginzburg) o due fonti indipendenti concordanti (Montale). Rispettati i parametri del punto 10: 10 citazioni, 7/10 opere pubblicate prima del 1900 (70%), 8/10 con link a fonte primaria (80%), nessun umore oltre il 30% (vita a 3/10), rispettata la soglia di ~40 parole per gli autori ancora sotto copyright (Ginzburg, Montale, entrambi sotto le 20 parole). Copertine verificate: **scartata una prima copertina errata per Foscolo** — il primo risultato Open Library per "Ultime lettere di Jacopo Ortis" era in realtà un adattamento francese di Alexandre Dumas ("Jacques Ortis"), scoperto solo guardando l'immagine e non fidandosi del match sul titolo; sostituita con l'edizione Feltrinelli corretta. Nessuna copertina trovata per Alfieri, Verga (Mastro-don Gesualdo) e Ginzburg: tile placeholder. Scritte le schede per i 2 nuovi autori (Goldoni, Alfieri). Verificato di nuovo, su tutto l'archivio, il bug della duplicazione traduttore in `source_edition`: nessuna istanza, questo lotto non ne ha introdotte (nessun campo `source_translator` valorizzato). **Deploy ancora sospeso**: commit locale, nessun push.

- 2026-08-28 UTC — added 11 quotes (total now 294) — Lotto 3 di CATALOGO.md, primo lotto della nuova fase di ampliamento del catalogo (classici e filosofi citati per opera), candidati mostrati e approvati dall'utente prima dell'inserimento. Sant'Agostino (Confessioni, "Tardi ti amai...", libro X 27,38, verificata su 4 edizioni concordanti — Pellegrino, Vitali, Carena, Trapè — più il testo integrale su augustinus.it), Platone (Fedone, due citazioni: sul piacere/dolore cap. III e le ultime parole di Socrate cap. LXVI, trad. Francesco Acri 1935, confermate su Wikiquote), Marco Aurelio (Colloqui con sé stesso, due nuove citazioni, libro IV §3 e libro XII §22, trad. Umberto Moricca 1923, confermate su Wikisource — portandolo a 3 citazioni, al limite di 3 per la stessa opera insieme a quella già in archivio), Seneca (Lettere a Lucilio, due nuove: lettera 1 §7 e lettera 104 §26, confermate su Wikiquote — portandolo a 4 citazioni, al tetto massimo per autore), Epitteto (Manuale, "Gli uomini sono agitati e turbati...", cap. V, confermata su Wikisource — traduzione di Giacomo Leopardi del 1825, già autore del sito, qui per la prima volta come traduttore), Boezio (Della consolazione della filosofia, libro I prosa VI, trad. Benedetto Varchi, confermata su Wikisource), Nietzsche (Così parlò Zarathustra, «Delle tre metamorfosi», trad. Renato Giani 1915, confermata su Wikisource), Schopenhauer (Aforismi sulla saggezza del vivere, cap. V §2 p. 69, confermata su Wikiquote). Rispettati tutti i parametri del punto 10 di CATALOGO.md: 11 citazioni (10-15), tutte pre-1900 (100%, requisito ≥50%), 6/11 con link a fonte primaria Wikisource (55%, requisito ≥50%), nessun umore oltre il 30% (coraggio e solitudine a 3/11 = 27%), max 4 citazioni per autore (Marco Aurelio e Seneca al tetto), max 3 per opera. Scartati in fase di ricerca: un secondo passo di Seneca la cui unica traduzione italiana su Wikisource (Annibal Caro) risultava avere una numerazione delle lettere non corrispondente a quella standard; una citazione attribuita a Nietzsche su Wikiquote ma segnalata lì come non riconducibile con certezza a un'opera. **Bug ricorrente trovato e corretto prima del commit**: il campo `source_edition` di 7 delle 11 nuove citazioni (poi esteso a verificare tutto l'archivio, trovate 2 istanze aggiuntive sempre in questo lotto) duplicava il nome del traduttore già presente separatamente in `source_translator` — stesso errore già corretto due volte nei lotti precedenti di questa sessione; questa volta il controllo è stato esteso a un grep sull'intero archivio (`source_translator in source_edition`) invece che alla sola verifica visiva delle pagine nuove, individuando le 2 istanze sfuggite alla prima passata. Copertine verificate su Open Library per tutti gli 8 autori nuovi/coinvolti. Scritte le 6 schede per i nuovi autori (Sant'Agostino, Platone, Epitteto, Boezio, Nietzsche, Schopenhauer). **Deploy sospeso su richiesta dell'utente fino al giorno successivo**: commit locali senza push, sito su Vercel non aggiornato fino a nuova indicazione.

- 2026-08-28 UTC — added 6 quotes (total now 283) — quinto lotto, terzo guidato dalla Fase 7: chiude la lista degli autori ad alta domanda e bassa copertura (punto A). Gabriele D'Annunzio da 1 a 2 citazioni: i primi versi de "La pioggia nel pineto" (Alcyone, 1903), confermati su Wikisource. Seneca da 1 a 2: l'apertura della prima delle Lettere a Lucilio, "Niente ci appartiene, Lucilio, solo il tempo è nostro", confermata su due fonti indipendenti concordanti (non trovato un riferimento diretto su Wikisource, il testo lì disponibile — trad. Annibal Caro — risultava avere una numerazione/selezione diversa dalla raccolta standard delle 124 lettere). Giacomo Leopardi da 2 a 3: i primi versi di "A Silvia" (1828), confermati su Wikisource. Cesare Pavese da 2 a 3: "Non ci si libera di una cosa evitandola, ma soltanto attraversandola" (Il mestiere di vivere, appunto del 22 novembre 1945), confermata su Wikiquote con data esatta. Luigi Pirandello da 2 a 3: la battuta del Padre sulla molteplicità dell'identità in "Sei personaggi in cerca d'autore" (1921, p. 49), confermata su Wikisource — corretto un refuso di trascrizione della fonte ("ma è vero" invece di "ma non è vero", errore che rendeva la frase illogica, corretto con la lezione coerente già confermata anche da fonti secondarie indipendenti). Alda Merini da 1 a 2: "Manicomio è parola assai più grande delle oscure voragini del sogno" (La Terra Santa, 1984), confermata su Wikiquote — nessuna copertina trovata su Open Library per questo titolo, tile placeholder.

- 2026-08-28 UTC — added 5 quotes (total now 277) — quarto lotto, secondo guidato dalla Fase 7 (punto A/E: autori con più domanda di ricerca e meno citazioni in archivio). Oscar Wilde da 1 a 4 citazioni (1.610 di volume, il più scoperto in assoluto): "La verità è raramente pura e mai semplice" (L'importanza di chiamarsi Ernesto, atto I, trad. Luigi Lunari/BUR), "Posso resistere a tutto fuorché alla tentazione" (Il ventaglio di Lady Windermere, trad. Ginevra Vivante), "La vita imita l'arte molto più di quanto l'arte imiti la vita" (Il declino della menzogna, 1889) — tutte confermate su Wikiquote. Dante Alighieri da 2 a 3: gli ultimi tre versi della Divina Commedia, "l'amor che move il sole e l'altre stelle" (Paradiso, canto XXXIII, vv. 143-145), confermati su Wikisource, primo titolo "Paradiso" per l'autore oltre a "Inferno". William Shakespeare da 2 a 3: il monologo "Dimani, e poi dimani..." di Macbeth dopo la morte di Lady Macbeth (atto V scena VI, trad. Andrea Maffei 1863), confermato su Wikisource. Copertine verificate su Open Library per tutte e 5.

- 2026-08-28 UTC — added 5 quotes (total now 272) — terzo lotto, primo guidato dalla mappatura keyword della Fase 7 (punto E, priorità "amicizia": 3.940 di volume, solo 3 citazioni in archivio prima di questo lotto). Alexandre Dumas (I tre moschettieri, "Tutti per uno, uno per tutti", capitolo IX, confermata su una trascrizione integrale online del testo pubblico dominio, secondo autore per Dumas dopo Il conte di Montecristo), Khalil Gibran (Il Profeta, "L'amicizia è sempre una dolce responsabilità...", trad. Tommaso Pisanti/Newton Compton, confermata su Wikiquote — secondo titolo per Gibran, che aveva già una citazione dallo stesso libro su un tema diverso), Marco Tullio Cicerone (L'amicizia/Laelius de amicitia, "L'amicizia non è niente altro che un accordo...", cap. 20, confermata su due fonti indipendenti concordanti con testo latino a fronte — primo autore latino classico oltre a Seneca e Marco Aurelio), John Steinbeck (Uomini e topi, "Per noi è diverso...", trad. Cesare Pavese, Bompiani 1963, p. 26, confermata su Wikiquote), Lucy Maud Montgomery (Anna dai capelli rossi, "Avere degli amici significa vedere solo la parte migliore di loro...", cap. XIV, trad. Maria Grazia Odorizzi/Nord-Sud 2021, confermata su Wikiquote, primo titolo dell'autrice sul sito). Copertine verificate su Open Library: per Dumas nessuna edizione soddisfacente trovata (solo un'edizione cinese bilingue e una scansione di frontespizio senza illustrazione) — nessuna copertina, tile placeholder. Scartati durante la ricerca, con lo stesso rigore delle fonti: A.A. Milne ("Se vivrai fino a cento anni..." — verificato essere una citazione apocrifa, mai scritta da Milne, in realtà di Joan Powers da un libro di aforismi anni Novanta ispirato ai suoi personaggi ma non scritto da lui), Harry Potter/Hermione ("Ci sono cose più importanti: amicizia... e coraggio" — verificato che la fonte Wikiquote la attribuisce esplicitamente al film, non al libro), Toni Morrison/Sula (nessun riferimento a capitolo/edizione trovato), Louisa May Alcott (nessuna citazione sull'amicizia con fonte verificabile trovata), Anne Frank (l'unica citazione trovata sul giudicare le persone non era abbastanza pertinente al tema amicizia). Con questo lotto la raccolta "Amicizia" raggiunge la soglia di 8 citazioni pertinenti (le 5 nuove più Saint-Exupéry, Ferrante, Hosseini già in archivio) ed è stata pubblicata in `/raccolte/amicizia/` (`data/raccolte.json`), introduzione editoriale scritta a mano. Scritte anche le schede autore per Cicerone e Montgomery (Dumas, Gibran e Steinbeck le avevano già dal lotto Fase 6).

- 2026-08-28 UTC — **Nota operativa: sessioni concorrenti sullo stesso repository.** Durante il lotto 2 di citazioni, `git add -A` ha incluso per errore due file di un'altra sessione Claude Code attiva in parallelo su questa stessa cartella (`SEO-KEYWORDS.md` e `data/keywords.json`, lavoro in corso su una "Fase 7" di mappatura keyword, mai vista prima in `CLAUDE.md`). Scoperto perché il file `SEO-KEYWORDS.md` risultava di nuovo modificato subito dopo il mio commit. Verificato con lo strumento di gestione sessioni: risultano davvero due sessioni Claude Code interattive attive in parallelo (avviate ~1h prima), anche se l'utente inizialmente non ne era consapevole in quei termini. Corretto con un commit dedicato (`git rm --cached`, nessun contenuto perso, i due file restano intatti sul filesystem per l'altra sessione) — non toccato invece `CLAUDE.md`, che ha ancora una modifica non committata di quella sessione in corso: lasciata deliberatamente intatta per non collidere con lavoro altrui. **Lezione per il futuro**: quando si lavora su questo repo, controllare `git status` prima di `git add -A` se il tempo trascorso dall'ultimo controllo è lungo, e diffidare di file inattesi comparsi da soli — non sono mai "spazzatura da ripulire" senza prima capire da dove vengono.

- 2026-08-28 UTC — added 5 quotes (total now 267) — secondo lotto post-roadmap, su istruzione esplicita "continua ogni volta che finisci un lotto": Nikolaj Gogol' (Le anime morte, "Minacciosa, orrenda è la vecchiaia...", trad. Agostino Villa 1965, confermata su Wikiquote), Dacia Maraini (La lunga vita di Marianna Ucrìa, incipit "Un padre e una figlia eccoli lì...", confermata su Wikiquote), Niccolò Ammaniti (Io non ho paura, "Piantala con questi mostri, Michele...", p. 54, confermata su Wikiquote), George Eliot (Middlemarch, "L'orgoglio ci aiuta...", Libro I cap. VI, confermata su Wikiquote), Ralph Ellison (Uomo invisibile, incipit "Io sono un uomo invisibile...", trad. Fruttero e Gallino 1956, confermata su due ricerche indipendenti concordanti). Copertine verificate su Open Library: per Maraini ed Ellison il primo risultato trovato era un'edizione in tedesco (rispettivamente "Die stumme Herzogin" e "Der unsichtbare Mann") — scartata perché fuorviante su un sito italiano anche se tecnicamente corretta come edizione del libro; per Ellison trovata un'edizione inglese alternativa valida, per Maraini nessuna alternativa in italiano o inglese disponibile su Open Library: nessuna copertina, tile placeholder, coerente con "meglio nessuna copertina che un'immagine sbagliata". Scartato durante la ricerca: Ivan Turgenev (Padri e figli — le citazioni candidate su Wikiquote avevano solo un numero di pagina senza edizione/traduttore indicati, non risalibile con certezza al testo), Louise Glück (L'iris selvatico — wording discordante tra la traduzione ufficiale Bacigalupo/Il Saggiatore e una versione amatoriale trovata online, stesso motivo di scarto già visto per Goethe nel lotto precedente). Scritte anche le 5 schede autore corrispondenti. Corretto nello stesso lotto un difetto di `generate_quote_pages.py`: il link alla fonte esterna diceva sempre "Testo su Wikisource →" anche quando la fonte era Wikiquote — ora il testo del link si adatta al dominio reale (Wikisource / Wikiquote / generico "Approfondisci").

- 2026-08-28 UTC — added 6 quotes (total now 262) — primo lotto dopo il completamento della roadmap SEO, sei nuovi autori mai presenti in archivio, scelti per ampliare la copertura di epoche e generi: Omero (Iliade, proemio "Cantami, o Diva, del Pelíde Achille l'ira funesta...", traduzione di Vincenzo Monti 1825, confermata su Wikisource), Marco Aurelio (Colloqui con sé stesso, libro II 1, "Dal mattino comincia a dire a te stesso...", trad. Cesare Cassanmagnago, confermata su Wikiquote con riferimento a libro/paragrafo), Virgilio (Eneide, proemio "L'armi canto e 'l valor del grand'eroe...", traduzione di Annibal Caro 1581, confermata su Wikisource), William Golding (Il signore delle mosche, "Tu sei uno sciocco" diceva il Signore delle Mosche, trad. Filippo Donini, confermata su Wikiquote con riferimento a pagina dell'edizione Oscar Mondadori), Ralph Waldo Emerson (Fiducia in se stessi, "Confida in te stesso: ogni cuore vibra a una tale corda di ferro", trad. edizione Ibis 2003, confermata su Wikiquote), Olga Tokarczuk (Guida il tuo carro sulle ossa dei morti, incipit "Alla mia età, e nelle mie condizioni...", trad. Silvano De Fanti, Nottetempo 2012, confermata su Wikiquote). Copertine verificate su Open Library (match autore + controllo visivo dell'immagine prima di accettarla). Scritte anche le 6 schede biografiche autore corrispondenti (63-84 parole, stesso standard della Fase 6) per mantenere tutto l'archivio indicizzabile (0 pagine sotto soglia). Scartati durante la ricerca: Astrid Lindgren (la citazione candidata su "vita organizzata per i bambini" non risultava sulla pagina Wikiquote consultata, nessun'altra fonte primaria a conferma del wording esatto), Aleksandr Puškin (nessuna citazione breve e iconica con riferimento a capitolo/edizione verificabile trovata in tempi ragionevoli), Johann Wolfgang von Goethe (l'incipit de "I dolori del giovane Werther" risultava con wording discordante tra le traduzioni di Spaini e Bianconi, senza modo di stabilire con certezza quale citare — stesso motivo di scarto già visto più volte in Fase 3 per traduzioni difformi). Corretto durante la stesura un errore di battitura nei dati: `source_edition` per le sei nuove citazioni includeva per errore anche "trad. Nome Traduttore", duplicando l'informazione già presente nel campo `source_translator` (che il template antepone automaticamente con "trad. "); corretto lasciando in `source_edition` solo editore/anno prima di pubblicare, verificato in browser che non ci fosse più duplicazione.

- 2026-08-28 UTC — Fase 6, lotto 2: schede autore per i restanti 150 autori con 1 sola citazione in archivio, completando la copertura a tutti i 193 autori del sito. Schede di 55-104 parole (media 70 sui 193 totali contando anche il lotto 1) — più corte del target 80-120 indicato in CLAUDE.md/SEO.md: per gli autori meno noti o meno documentati non sempre c'erano abbastanza fatti biografici verificabili con certezza da aggiungere senza scivolare nel riempitivo o nella congettura, e si è scelto di privilegiare la precisione sulla lunghezza esatta, stessa priorità data alla veridicità in Fase 3. Diciannove schede risultate particolarmente corte (<55 parole: Emily St. John Mandel, Octavia E. Butler, Octavio Paz, Patrick Süskind, Chimamanda Ngozi Adichie, Giovanni Boccaccio, Imre Kertész, Zadie Smith, Don DeLillo, Elif Shafak, Ludovico Ariosto, Mario Vargas Llosa, Natalia Ginzburg, Paulo Coelho, Erri De Luca, Julian Barnes, Curzio Malaparte, Madeline Miller, Philip Roth) sono state riviste e ampliate con un fatto verificabile in più ciascuna prima della pubblicazione, portandole a 72-104 parole. Testi aggiunti a `data/hub_intros.json` sotto la chiave `autori`, stesso meccanismo del lotto 1. Effetto sul gate di indicizzazione (Fase 2/5): **tutti i 193 autori sono ora indicizzabili, e con essi tutti i 522 URL del sito** — verificato nel rapporto di `build.py` (0 hub sotto soglia) e a campione in browser (Jane Austen, 1 sola citazione: nessun `noindex`, lo aveva prima del lotto). Con questo si esaurisce il lavoro automatizzabile della Fase 6: i tre punti restanti (Google Search Console, Bing Webmaster Tools/IndexNow, analytics) restano bloccati in attesa di azioni dirette dell'utente — account Google e Bing da verificare personalmente, privacy policy del sito mai pubblicata (servono i dati del titolare) — nessuno dei tre è automatizzabile in autonomia.

- 2026-08-28 UTC — Fase 6, lotto 1: schede autore per i 43 autori con ≥2 citazioni in archivio (priorità per numero di citazioni, come indicato in CLAUDE.md — proxy oggettivo per "autori più cercati" in assenza di dati reali di volume di ricerca). Schede di 72-97 parole, dati biografici verificabili e incontrovertibili: nascita/morte, nazionalità, 2-3 opere principali già presenti sul sito, un fatto distintivo (Nobel, causa di morte quando nota e pertinente, esilio, pseudonimo). Testi in `data/hub_intros.json` sotto la chiave `autori`, keyed per nome esatto come compare in `data/citazioni.json`. Effetto sul gate di indicizzazione (Fase 2/5, `generate_hub_pages.py`): autori indicizzabili passati da 13 (solo quelli con ≥3 citazioni) a 43 — verificato nel rapporto di `build.py` e a campione in browser (pagina con scheda senza `noindex`, pagina senza scheda con `noindex` confermato, es. Jane Austen). Restano 150 autori con 1 sola citazione senza scheda, in coda per lotti successivi non prioritari come questi 43. Gli altri tre punti della Fase 6 (Google Search Console, Bing Webmaster Tools/IndexNow, analytics) non sono stati toccati: richiedono rispettivamente l'account Google dell'utente, l'account Bing dell'utente, e la pubblicazione della privacy policy del sito (mai scritta, servono i dati del titolare) — nessuno dei tre è automatizzabile in autonomia, segnalati come bloccati in CLAUDE.md.

- 2026-08-28 UTC — Fase 5 completata: introduzioni editoriali per i 7 temi e i 5 generi (`data/hub_intros.json`, iniettate da `generate_hub_pages.py`), ciascuna scritta ancorandola a 4-6 citazioni realmente presenti in archivio (autore + opera citati per nome, mai un riferimento generico) — temi 234-324 parole, generi 104-178. Corretto di riflesso un difetto grammaticale preesistente nell'H1/title dei temi: la preposizione era "su" generico per tutti tranne "amore" ("Citazioni su vita", "Citazioni su libertà"), ora è la preposizione articolata corretta per genere/numero di ciascun tema ("sulla vita", "sul coraggio", "sulla libertà", ecc.), coerente con l'esempio "Frasi e citazioni sulla libertà" già scritto in SEO.md. Pubblicate 5 raccolte curate a mano in `/raccolte/<slug>/` (`data/raccolte.json`, `tools/generate_raccolte_pages.py`): Libri e scrittura (10 citazioni), Il mare (8), La morte (9), Frasi brevi (12), Incipit memorabili (13) — selezione fatta per parola chiave sul testo, poi verifica manuale una per una scartando i falsi positivi (es. "amico"/"amica" nel testo non implica che la citazione parli davvero di amicizia). Due raccolte candidate da SEO.md non pubblicate per lo stesso principio di rigore della Fase 3 ("meglio nessuna raccolta che una forzata"): *amicizia* (solo 3-5 citazioni con un fit genuino, il resto erano falsi positivi lessicali) e *frasi sul tempo che passa* (avrebbe duplicato troppo da vicino il tema "Tempo" già esistente, oltre a non raggiungere una selezione forte). Una citazione può comparire in più raccolte (l'incipit di Huckleberry Finn di Mark Twain è sia in Libri e scrittura sia in Incipit memorabili) — link di ritorno "In questa raccolta: {Titolo} →" aggiunto alle pagine citazione corrispondenti, stesso meccanismo del link opera introdotto in Fase 4. Aggiunti anche gli indici `/opere/` e `/raccolte/` (il primo mancava dalla Fase 4, dimenticato nell'implementazione originale). Completato il gate di indicizzazione lasciato a metà in Fase 2: un hub sotto le 3 citazioni ora entra comunque in sitemap se ha un'introduzione scritta a mano (oggi non cambia nulla in pratica, tutti i temi/generi sono già sopra soglia, ma la regola è quella scritta fin dall'inizio in SEO.md). Build verificata: 0 errori, 0 pagine orfane, tutte le nuove pagine confermate in browser (screenshot + console pulita).

- 2026-08-28 UTC — Fase 4 completata: generate 40 pagine opera in `/opere/<slug>/` (`data/opere.json`, `tools/generate_opera_pages.py`, integrato in `tools/build.py` prima di `generate_hub_pages.py`). Elenco costruito con criterio oggettivo — opere con ≥2 citazioni in archivio (8: Dante/Inferno, Manzoni/Promessi sposi, Dostoevskij/Fratelli Karamazov, Saint-Exupéry/Piccolo principe, García Márquez/Cent'anni di solitudine, Whitman/Foglie d'erba, Ungaretti/L'allegria, Ishiguro/Non lasciarmi) + Tolkien/Il Signore degli Anelli (unificato dai 3 titoli-volume 33/237/238 già presenti, supera la soglia da solo) — più 31 titoli del canone scolastico italiano con 1 sola citazione ciascuno (classici italiani da Leopardi a Calvino/Eco, classici stranieri da Cervantes a Orwell/Wilde), mostrato e approvato dall'utente prima della generazione. Genere fantasy aggiunto su richiesta esplicita ("aggiungi anche fantasy"): degli altri 11 titoli fantasy taggati (Narnia, Trono di Spade, i 3 libri di Harry Potter, Peter Pan, Coraline, Percy Jackson, Discworld) nessuno supera la soglia individualmente e nessuno è nel canone scolastico in senso stretto — non unificati forzatamente (i 3 libri di Harry Potter sono 3 opere realmente distinte, non volumi dello stesso romanzo come il Signore degli Anelli), restano quindi senza pagina opera dedicata per la regola strutturale "citazione = pagina opera quando c'è 1 sola citazione". Schede editoriali (3-5 righe: anno, genere, trama) scritte su fatti bibliografici pubblici incontrovertibili; edizione/traduttore italiano lasciati vuoti su tutte e 40 le opere — nessuna edizione "di riferimento" verificabile con certezza per classici tradotti più volte, stessa cautela già adottata in Fase 3 sulle fonti delle citazioni. `Book` JSON-LD con `@id` stabile in `/opere/<slug>/#book`, riusato dalle pagine citazione della stessa opera (verificato: i 3 volumi del Signore degli Anelli puntano tutti allo stesso `@id`); aggiunto link "Tutte le citazioni da «Opera» →" sulle pagine citazione corrispondenti. Build verificata: 0 title/description duplicati, 0 H1 mancanti, 0 immagini OG mancanti, 40/40 pagine opera generate.

- 2026-08-23 UTC — aggiunto contesto retroattivo a 6 citazioni già presenti (nessuna citazione nuova, totale resta 253): Kafka (La metamorfosi, è la prima frase del romanzo, tono piatto del narratore), Orwell (1984, è scritta di nascosto nel diario di Winston, gli verrà rinfacciata più avanti durante un interrogatorio), Dostoevskij (I fratelli Karamazov, "Se Dio non esiste tutto è permesso" — nel romanzo non la dice mai Ivan, che sviluppa l'idea nei ragionamenti, ma il servo Smerdjakov, spinto da quei ragionamenti a uccidere il padre; confermato su più fonti), Calvino (Le città invisibili, sono le ultime parole del libro, Marco Polo a Kublai Khan), Woolf (Una stanza tutta per sé, non è un romanzo ma il testo di due conferenze tenute a Cambridge nel 1928), Camus (Lo straniero, è la prima frase del romanzo, narrata in prima persona da Meursault). Iniziato a rispondere al punto "contesto per le restanti ~247 citazioni" della roadmap in CLAUDE.md, restano circa 241.

- 2026-08-20 07:26 UTC — added 2 quotes (total now 253) — aggiunte citazioni di Amin Maalouf (Il manoscritto di Samarcanda, "In fondo all'Atlantico c'è un libro. Io ne racconterò la storia.", confermata su Wikiquote, primo autore sul sito) e Donna Tartt (Il cardellino, riflessione finale di Theo sulla bellezza, confermata su più fonti concordanti, primo autore sul sito); copertine verificate visivamente su Open Library; scartati Terry Pratchett (citazione di Morte trovata solo come risposta fuori contesto a una domanda non riportata, e fonte discordante sul titolo italiano del romanzo — "Il tristo mietitore" è in realtà la traduzione di un libro diverso, Reaper Man, non di Mort), Andrea Camilleri ("qual è la forma dell'acqua" — dialogo trovato solo come epigrafe, senza conferma di chi lo pronuncia nel romanzo), Colson Whitehead e Alessandro D'Avenia (candidate trovate solo su siti aggregatori, senza wording esatto della traduzione pubblicata riscontrabile con certezza). Da questo lotto in poi, ogni nuova citazione include di default copertina e una riga di contesto in linguaggio accessibile (prima la storia, poi il nome/riferimento — vedi prova precedente su Dante, Dostoevskij, Saint-Exupéry, Voltaire).

- 2026-08-19 10:57 UTC — recupero copertine: aggiunte 32 copertine mancanti su 77 card che ne erano prive, via Open Library Covers API (autore verificato per corrispondenza prima di accettare il cover_i, per evitare falsi positivi). Scartati durante la verifica: un primo tentativo aveva assegnato per errore la stessa copertina segnaposto generica (cover_i 5421539, un'icona "nessuna copertina" di Open Library) a 7 libri diversi tramite un fallback di ricerca troppo permissivo — corretto restringendo la ricerca e verificando che l'autore del risultato corrisponda; in un secondo controllo visivo scartate anche Marguerite Duras (L'amante — il risultato era la copertina di una "fiche de lecture", una scheda di lettura scolastica, non l'edizione del romanzo) e Salvatore Quasimodo (Ed è subito sera — il risultato era la scansione di una pagina bibliografica, non una copertina). Restano 45 card senza copertina, principalmente poesie/estratti brevi senza un'edizione autonoma riconoscibile su Open Library.

- 2026-08-18 17:44 UTC — added 7 quotes (total now 251) — aggiunte citazioni di Frank Herbert (Dune, Litania contro la paura completa "Non devo avere paura. La paura uccide la mente...", confermata su più fonti concordanti, primo autore sul sito), Isaac Asimov (Fondazione, "La violenza è l'ultimo rifugio degli incapaci" di Salvor Hardin, confermata su Wikiquote — nell'edizione italiana originale del 1951 il romanzo fu pubblicato come "Cronache della galassia", oggi noto come Fondazione, primo autore sul sito), Douglas Adams (Guida galattica per gli autostoppisti, "Non fatevi prendere dal panico", motto/tagline del libro stesso, ampiamente confermata, primo autore sul sito), Madeline Miller (La canzone di Achille, "Lo riconoscerei anche solo dal tocco...", confermata su più fonti concordanti, primo autore sul sito), Bram Stoker (Dracula, riflessione di Jonathan Harker nel diario del 25 giugno, cap. 4, "Nessuno può sapere, se non dopo una notte di patimenti...", confermata testualmente su Wikiquote con edizione e pagina, primo autore sul sito), Truman Capote (Colazione da Tiffany, il celebre passaggio dei "mean reds" di Holly Golightly su Tiffany, confermato su più fonti concordanti, primo autore sul sito), J.M. Barrie (Le avventure di Peter Pan, "Solo chi sogna può volare!" di Peter Pan, confermata su Wikiquote, primo autore sul sito); copertine non aggiunte per questo lotto, in continuità con il recupero copertine rimandato a un'altra volta; scartati Stephen King (nessuna citazione con traduzione italiana verificabile trovata, solo fonti in inglese), Agatha Christie (le citazioni candidate da Dieci piccoli indiani risultavano solo parafrasi da blog, senza wording esatto della traduzione pubblicata riscontrabile con certezza)

- 2026-08-04 05:21 UTC — added 5 quotes (total now 193) — aggiunte citazioni di Virginia Woolf (Gita al faro, "Era fatto; era finito. Sì, pensò, posando il pennello stremata, ho avuto la mia visione", riga finale del romanzo confermata su piu fonti concordanti, terza citazione dell'autrice ma libro distinto da La signora Dalloway e Una stanza tutta per sé), Jean-Paul Sartre (La Nausea, riflessione sull'esistenza "L'esistenza non è qualcosa che si lasci pensare da lontano...", confermata su piu fonti concordanti, secondo libro dell'autore distinto da A porte chiuse già presente), Thomas Mann (La morte a Venezia, monologo su Fedro e la Bellezza, confermato su piu fonti concordanti con wording identico, secondo libro dell'autore distinto da La montagna incantata), Elena Ferrante (Storia del nuovo cognome, "Penso che la bellezza sia un inganno... è cipria passata sopra l'orrore", confermata su piu fonti concordanti, terzo libro della saga sul sito distinto da L'amica geniale e I giorni dell'abbandono), Kazuo Ishiguro (Quel che resta del giorno, riflessione di Stevens sul servizio "Un uomo può considerarsi veramente soddisfatto...", confermata su piu fonti concordanti, secondo libro dell'autore distinto da Non lasciarmi); scartato Toni Morrison (Il canto di Salomone — la citazione candidata "se vuoi volare devi rinunciare alla roba che ti appesantisce" risultava solo come parafrasi in italiano su un blog, senza wording esatto della traduzione pubblicata riscontrabile con certezza)

- 2026-08-04 04:22 UTC — added 4 quotes (total now 188) — aggiunte citazioni di Giovanni Boccaccio (Decameron, proemio "Umana cosa è aver compassione degli afflitti", confermata su Wikisource e Goodreads, primo autore del Trecento sul sito insieme a Dante), Luigi Pirandello (Il fu Mattia Pascal, incipit "Una delle poche cose, anzi forse la sola ch'io sapessi di certo era questa: che mi chiamavo Mattia Pascal", confermato su Wikisource — secondo libro dell'autore, distinto da Uno nessuno e centomila già presente), Torquato Tasso (Gerusalemme liberata, incipit "Canto l'arme pietose, e 'l Capitano che 'l gran sepolcro liberò di Cristo", confermato su Wikisource, primo autore sul sito), Francesco Petrarca (Canzoniere, "Quanto piace al mondo è breve sogno", verso conclusivo del sonetto proemiale, confermato su più fonti concordanti, primo autore sul sito nonostante l'importanza storica); scartati H.P. Lovecraft (la citazione "Non è morto ciò che può attendere in eterno..." è comunemente attribuita a Il richiamo di Cthulhu ma appartiene in realtà a La città senza nome, con traduzioni italiane discordanti tra loro — rischio di attribuzione errata al libro sbagliato), John Fante (Chiedi alla polvere — le citazioni brevi candidate trovate solo su siti aggregatori senza riscontro su fonte primaria/Wikiquote con wording univoco), Giosuè Carducci (Pianto antico — verso autentico ma nessuna aderenza pulita a una categoria tematica del sito senza forzatura, tema del lutto per un figlio)

- 2026-08-03 23:22 UTC — added 5 quotes (total now 172) — aggiunte citazioni di Dante Alighieri (Inferno, "Nel mezzo del cammin di nostra vita..." canto I, distinta dalla citazione gia presente del canto V), Salvatore Quasimodo (Ed è subito sera, confermata su Wikipedia/fonti concordanti), Giacomo Leopardi (Canto notturno di un pastore errante dell'Asia, seconda citazione dell'autore ma poesia distinta da L'infinito), Alessandro Manzoni (I promessi sposi, incipit "Quel ramo del lago di Como..." accorciato alla prima frase compiuta per restare in linea con la lunghezza delle altre card, a differenza del tentativo scartato nell'11:20 UTC che usava il periodo intero troppo lungo), Giuseppe Ungaretti (Soldati, L'allegria, seconda citazione dell'autore ma poesia distinta da "M'illumino d'immenso") — tutte confermate su piu fonti primarie/Wikisource/Wikipedia concordanti; scartati James Joyce (Ulisse, finale di Molly Bloom "sì dissi sì voglio Sì" — gia scartata strutturalmente nel run del 2026-08-03 00:20 UTC per wording di traduzione discordante tra edizioni italiane, non risolto neanche in questo run), Nikos Kazantzakis (Zorba il Greco, citazioni su libertà/follia reperite solo su siti aggregatori di aforismi senza riscontro su edizione pubblicata, wording non verificabile con certezza), Emily Dickinson (Because I could not stop for Death, traduzione italiana trovata solo su lyricstranslate/fonti amatoriali non equiparabili a un'edizione pubblicata)

- 2026-08-03 13:20 UTC — added 1 quote (total now 143) — aggiunta citazione di John Steinbeck (Furore, "Nell'anima degli affamati i semi del furore sono diventati acini, e gli acini grappoli ormai pronti per la vendemmia" — confermata su piu fonti indipendenti convergenti (chiaracls, le-citazioni.it, frasicelebri.it, anobii), a differenza del tentativo scartato nel run del 2026-08-02 23:20 per wording non confermabile; scartati Toni Morrison (Il canto di Salomone, "Se vuoi volare devi rinunciare a tutta la roba che ti appesantisce" — solo fonti secondarie/blog non primarie, stesso motivo di scarto strutturale gia riscontrato in almeno 5 run precedenti), Ursula K. Le Guin (La mano sinistra delle tenebre, "Le tenebre sono la mano sinistra della luce..." — nessuna fonte primaria/Wikiquote trovata, coerente con gli scarti strutturali ripetuti nei run precedenti per traduzioni discordanti), Stefan Zweig (Lettera di una sconosciuta, incipit "A te, che mai mi hai conosciuta" — confermato da una sola fonte non primaria, insufficiente), Han Kang (La vegetariana, nessuna frase singola breve e iconica con wording esatto confermabile individuata), Arundhati Roy (Il dio delle piccole cose, candidate trovate ma nessuna abbastanza univoca/iconica da fonte affidabile), Annie Ernaux (Gli anni, nessuna citazione con wording esatto reperita), Salman Rushdie (I figli della mezzanotte, incipit troppo lungo/articolato per una card, coerente con lo scarto gia registrato nel run dell'11:20)

- 2026-08-03 12:22 UTC — added 2 quotes (total now 142) — aggiunte citazioni di Michail Bulgakov (Il Maestro e Margherita, "I manoscritti non bruciano", riconfermata su piu fonti indipendenti convergenti) e Karen Blixen (La mia Africa, incipit "In Africa avevo una fattoria ai piedi degli altipiani del Ngong...", confermato su piu fonti indipendenti con wording concordante); scartati Yasunari Kawabata (Il paese delle nevi, due traduzioni italiane discordanti dell'incipit: "sbucò dalla lunga galleria" vs "usciti dalla lunga galleria di confine", wording non univoco), Anna Maria Ortese (Il mare non bagna Napoli, citazione candidata reperita solo tramite riassunto secondario, nessuna fonte primaria/Wikiquote a conferma del wording esatto), Marilynne Robinson (Gilead, passi trovati troppo lunghi/articolati per una card o non abbastanza incisivi come frase singola), Georges Perec (La vita istruzioni per l'uso, nessuna frase singola breve e iconica reperita — incipit e passi trovati troppo descrittivi), Ignazio Silone (Fontamara, nessuna citazione con wording esatto e fonte primaria univoca reperita), Curzio Malaparte (La pelle, piu frasi candidate trovate ma nessuna confermabile con certezza come la piu rappresentativa/wording esatto univoco)

- 2026-08-03 11:20 UTC — added 0 quotes (total resta 140) — tutti i 7 candidati scartati: Alessandro Manzoni (incipit "Quel ramo del lago di Como", periodo unico troppo lungo per una card, coerente con precedenti scarti per lunghezza eccessiva), E.M. Forster (Howards End, "Only connect" — traduzioni italiane discordanti tra le fonti, "Solo collega" vs "Basta collegare", wording non univoco), Gabriel García Márquez (Cronaca di una morte annunciata, incipit — fonti discordanti su una parola chiave, "bastimento" vs "battello", wording non confermabile con certezza nonostante 3 citazioni già presenti dell'autore), Salman Rushdie (I figli della mezzanotte, incipit troppo lungo/articolato per una card), Orhan Pamuk (Il mio nome è rosso / Neve — citazioni reperite solo su blog/siti aggregatori, nessun riscontro su fonte primaria o Wikiquote), Wisława Szymborska (Nulla due volte accade — due traduzioni italiane discordanti circolanti, "nasciamo/moriamo" vs "si nasce/si muore", wording non univoco), José Saramago (Il vangelo secondo Gesù Cristo — citazione a bassa confidenza, fonte singola non primaria, scambio di battute poco adatto a una card isolata)

- 2026-08-02 11:20 UTC — added 4 quotes (total now 75) — aggiunte citazioni di Seneca, Marguerite Yourcenar, Toni Morrison, Italo Calvino; scartati Dostoevskij (Delitto e castigo, testo non verificabile con certezza), Sylvia Plath (passo troppo lungo per una card), Chinua Achebe e Marco Aurelio (nessuna citazione verificabile con esattezza)
- 2026-08-02 12:21 UTC — added 4 quotes (total now 79) — aggiunte citazioni di Dostoevskij (Delitto e castigo, riverificata con più fonti indipendenti nonostante lo scarto precedente), Viktor Frankl, Hermann Hesse, Grazia Deledda; scartati Anaïs Nin (fonte/volume del diario non identificabile con certezza), Borges e Marco Aurelio (citazioni troppo lunghe/ambigue da verificare con esattezza), Toni Morrison Il canto di Salomone (formulazione probabilmente parafrasata, non citazione esatta)
- 2026-08-02 13:20 UTC — added 5 quotes (total now 84) — aggiunte citazioni di Giuseppe Tomasi di Lampedusa (Il Gattopardo), Gabriel García Márquez (L'amore ai tempi del colera), Sylvia Plath (La campana di vetro), Michael Ende (La storia infinita), Elena Ferrante (L'amica geniale); scartati Cesare Pavese (citazione non riconducibile con certezza al diario "Il mestiere di vivere"), Elsa Morante Isola di Arturo (incipit troppo diffuso per una card, nessuna frase singola verificabile), Omero Odissea (verso di apertura è un frammento, non una frase compiuta)
- 2026-08-02 14:19 UTC — added 3 quotes (total now 87) — aggiunte citazioni di Vladimir Nabokov (Lolita), Aldous Huxley (Il mondo nuovo), Ray Bradbury (Fahrenheit 451); scartati Luigi Pirandello (citazioni circolanti su siti aggregatori, nessuna riconducibile con certezza a "Uno, nessuno e centomila"), John Steinbeck (incipit di Furore non confermabile), Cesare Pavese di nuovo (stessa incertezza sulla fonte già riscontrata nel run precedente per "Il mestiere di vivere")
- 2026-08-02 15:21 UTC — added 3 quotes (total now 90) — aggiunte citazioni di Kurt Vonnegut (Mattatoio n. 5), Natalia Ginzburg (Lessico famigliare), Isabel Allende (La casa degli spiriti); scartati Dino Buzzati (Il deserto dei Tartari, solo fonti aggregatori, media confidenza), Rabindranath Tagore (nessuna traduzione italiana canonica rintracciabile), Margaret Atwood (Il racconto dell'ancella, traduzione italiana solo da siti aggregatori), Elsa Morante (La Storia, citazione a media confidenza non confermata su fonte primaria), Anton Cechov (Zio Vanja, monologo lungo con variazioni di traduzione tra edizioni)
- 2026-08-02 16:20 UTC — added 6 quotes (total now 96) — aggiunte citazioni di Cesare Pavese (Verrà la morte e avrà i tuoi occhi), Luigi Pirandello (Uno, nessuno e centomila, riverificata la frase finale con più fonti indipendenti nonostante lo scarto precedente), Giovanni Verga (I Malavoglia, incipit confermato su due fonti), Giuseppe Ungaretti (M'illumino d'immenso), Dino Buzzati (Il deserto dei Tartari, riverificato con corrispondenza a Wikiquote), Elsa Morante (La Storia, sottotitolo confermato su fonti multiple indipendenti); scartati Eugenio Montale (Non chiederci la parola, testo esatto non reperibile con certezza dalle fonti trovate), Alda Merini (La Terra Santa / La pazza della porta accanto, solo fonti aggregatori a bassa affidabilità)
- 2026-08-02 17:21 UTC — added 6 quotes (total now 102) — aggiunte citazioni di Ernest Hemingway (Festa mobile), Milan Kundera (Il libro del riso e dell'oblio), Cormac McCarthy (La strada), Albert Camus (Il mito di Sisifo, quarta citazione dell'autore ma idea distinta dalle precedenti), Haruki Murakami (Kafka sulla spiaggia), Herman Melville (Bartleby lo scrivano); scartati Marguerite Duras (L'amante, incipit con traduzioni discordanti tra fonti, wording esatto non confermabile), Chimamanda Ngozi Adichie (Dovremmo essere tutti femministi, nessuna frase singola iconica verificabile con certezza), Emily Dickinson (Io sono Nessuno, traduzioni italiane troppo divergenti tra loro per una versione canonica)
- 2026-08-02 21:21 UTC — added 2 quotes (total now 104) — aggiunte citazioni di Franz Kafka (Il Castello, incipit) e Jorge Luis Borges (Finzioni, La biblioteca di Babele, riverificata con una seconda fonte accademica indipendente); scartati Marguerite Duras (L'amante — gia scartata in un run precedente per traduzioni discordanti, dubbio confermato anche stavolta), Toni Morrison (Il canto di Salomone — gia scartata in un run precedente come probabile parafrasi, dubbio confermato anche stavolta), Umberto Eco (Il pendolo di Foucault — citazione non reperibile con certezza) e Chinua Achebe (Il crollo — citazione trovata non chiaramente attribuibile a quel romanzo specifico)
- 2026-08-02 22:20 UTC — added 3 quotes (total now 107) — aggiunte citazioni di David Foster Wallace (Questa è l'acqua), Boris Pasternak (Il dottor Živago, riconfermata su due fonti indipendenti), Khaled Hosseini (Il cacciatore di aquiloni); scartato Marguerite Duras (L'amante — terzo tentativo, stesso problema di traduzioni discordanti gia riscontrato due volte in passato), Chimamanda Ngozi Adichie (Americanah — nessuna frase singola iconica con wording esatto confermabile)
- 2026-08-02 23:20 UTC — added 2 quotes (total now 109) — aggiunte citazioni di Giorgio Bassani (Il giardino dei Finzi-Contini) e Carlo Levi (Cristo si è fermato a Eboli, frase eponima confermata su fonte primaria); scartati John Steinbeck (Furore, citazione lunga con wording di traduzione non confermabile con certezza), James Baldwin (La prossima volta il fuoco, passo troppo lungo e traduzione incerta), Mark Twain (Huckleberry Finn, nessuna citazione italiana verificabile trovata), Ursula K. Le Guin (I reietti dell'altro pianeta, attribuzione al romanzo non confermata con certezza), Anton Cechov (nessuna citazione da opera specifica con titolo/anno verificabile), Clarice Lispector (La passione secondo G.H., wording di traduzione incerto)
- 2026-08-03 00:20 UTC — added 3 quotes (total now 112) — aggiunte citazioni di Margaret Atwood (Il racconto dell'ancella, frase "Nolite te bastardes carborundorum" citata in latino/pseudo-latino originale, senza problema di traduzione che aveva bloccato tentativi precedenti), Italo Calvino (Palomar, quinta citazione dell'autore ma idea distinta, confermata su Wikiquote), Sibilla Aleramo (Una donna, confermata su più fonti indipendenti); scartati James Joyce (Ulisse, monologo finale di Molly Bloom con wording di traduzione discordante tra le edizioni italiane), Maya Angelou (Io so perché canta l'uccello in gabbia, nessuna traduzione italiana esatta reperibile per la citazione candidata), Kazuo Ishiguro (Quel che resta del giorno, citazione candidata di fonte incerta, non chiaramente riconducibile al testo)
- 2026-08-03 01:21 UTC — added 5 quotes (total now 117) — aggiunte citazioni di Joan Didion (The White Album), Erri De Luca (Il giorno prima della felicità), Kazuo Ishiguro (Non lasciarmi), Michela Murgia (Accabadora), Sandro Veronesi (Il colibrì); scartati Ursula K. Le Guin (La mano sinistra delle tenebre, traduzioni italiane discordanti tra le due edizioni trovate, wording esatto non confermabile), Toni Morrison (Il canto di Salomone, testo italiano non reperibile — gia scartata in run precedenti per lo stesso motivo), Alessandro Baricco (Novecento, la citazione ipotizzata non corrispondeva al testo reale trovato)
- 2026-08-03 02:21 UTC — added 4 quotes (total now 121) — aggiunte citazioni di Chinua Achebe (Le cose crollano, incipit riverificato con due fonti indipendenti convergenti nonostante gli scarti nei run precedenti), Antonio Tabucchi (Sostiene Pereira), Julio Cortázar (Il gioco del mondo), Marguerite Duras (L'amante, wording "Presto fu tardi nella mia vita" riconfermato su piu ricerche indipendenti nonostante gli scarti nei run precedenti per traduzioni discordanti); scartati Toni Morrison (Il canto di Salomone, testo italiano ancora non reperibile — gia scartata piu volte per lo stesso motivo), Leonardo Sciascia (Il giorno della civetta, citazione autentica ma troppo lunga da estrarre senza rischio di alterarne il wording esatto), Doris Lessing (Il taccuino d'oro, citazione candidata sembra una parafrasi non verbatim), Clarice Lispector (nessuna citazione con wording esatto confermabile dalle fonti trovate)
- 2026-08-03 03:20 UTC — added 2 quotes (total now 123) — aggiunte citazioni di Octavia E. Butler (La parabola del seminatore, verso "Dio è cambiamento" confermato su fonte primaria come epitaffio dell'autrice), Emily St. John Mandel (Stazione undici, "La sopravvivenza non è sufficiente"); scartati Zora Neale Hurston (I loro occhi guardavano Dio, due fonti indipendenti riportano finali diversi della stessa frase, wording esatto non confermabile con certezza), Toni Morrison (L'occhio più azzurro, nessuna frase singola breve e iconica con wording confermabile trovata), Clarice Lispector (L'ora della stella, nessuna citazione con wording esatto confermabile), Chimamanda Ngozi Adichie (Americanah, gia scartata in run precedenti per lo stesso motivo — nessuna frase singola iconica con wording esatto reperibile)
- 2026-08-03 04:21 UTC — added 2 quotes (total now 125) — aggiunte citazioni di James Baldwin (La prossima volta il fuoco), Simone Weil (L'ombra e la grazia); scartati Chimamanda Ngozi Adichie e bell hooks (formulazione italiana esatta non riconducibile con certezza a una singola frase), Ursula K. Le Guin (traduzione italiana della citazione non verificabile con esattezza), Zora Neale Hurston (nessuna traduzione italiana della citazione reperibile), Amin Maalouf (titolo/formulazione ambigui tra edizioni), Rabindranath Tagore (attribuzione al libro specifico non verificabile con certezza)
- 2026-08-03 05:21 UTC — added 1 quote (total now 126) — aggiunta citazione di Charles Baudelaire (Lo spleen di Parigi, "Bisogna essere sempre ubriachi", confermata su fonte con traduzione italiana esatta); scartati Maya Angelou (Io so perché canta l'uccello in gabbia, wording italiano esatto non reperibile), bell hooks (Tutto sull'amore, citazione circolante solo su blog come parafrasi, non confermabile come frase esatta del libro), Chimamanda Ngozi Adichie (Dovremmo essere tutti femministi, gia scartata in run precedenti per lo stesso motivo — mantenuta coerenza), Amin Maalouf (nessuna citazione italiana esatta reperibile), Ocean Vuong (Brevemente risplendiamo sulla terra, frase cercata non confermata nelle fonti), Ursula K. Le Guin (La mano sinistra delle tenebre, nessuna citazione italiana esatta reperibile), W.B. Yeats (La seconda venuta, traduzioni italiane discordanti tra loro, wording non univoco)
- 2026-08-03 06:21 UTC — added 3 quotes (total now 129) — aggiunte citazioni di Cesare Pavese (La luna e i falò, "Un paese ci vuole"), Alda Merini (Vuoto d'amore, "Sono nata il ventuno a primavera"), Susanna Tamaro (Va' dove ti porta il cuore, sulle lacrime) — tutte opere originariamente in italiano, nessun rischio di traduzione discordante; scartati Chimamanda Ngozi Adichie (Dovremmo essere tutti femministi — Wikiquote non conferma la frase candidata, coerente con gli scarti nei run precedenti per lo stesso motivo), Toni Morrison (Il canto di Salomone — testo italiano esatto ancora non reperibile da fonte primaria, gia scartata piu volte per lo stesso motivo), Ursula K. Le Guin (La mano sinistra delle tenebre — due traduzioni italiane discordanti esistenti (Sellerio/vecchia vs riedizione), wording non univoco, gia scartata piu volte per lo stesso motivo), Clarice Lispector (Acqua viva — stesso problema di traduzioni discordanti, Sellerio/Morino vs Adelphi/Francavilla, wording esatto non confermabile con certezza)
- 2026-08-03 07:20 UTC — added 0 quotes (total resta 129) — tutti i candidati scartati: Ursula K. Le Guin (La mano sinistra delle tenebre — riconfermata la discordanza tra traduzioni italiane gia rilevata piu volte: le fonti trovate riportano due formulazioni diverse della stessa frase, wording non univoco), Maya Angelou (Io so perché canta l'uccello in gabbia — testo italiano trovato solo su un blog personale, non fonte primaria/Wikiquote, insufficiente a superare gli scarti precedenti), Chimamanda Ngozi Adichie (Dovremmo essere tutti femministi — la frase italiana trovata sembra una parafrasi del motore di ricerca piuttosto che testo confermato da Wikiquote o dal libro, coerente con gli scarti ripetuti nei run precedenti); scartati anche Audre Lorde (Sister Outsider, nessuna traduzione italiana della citazione reperibile), Toni Morrison (Il canto di Salomone, wording italiano solo da fonte secondaria non verbatim — gia scartata piu volte per lo stesso motivo), Clarice Lispector (L'ora della stella, nessuna citazione con wording esatto confermabile), Zora Neale Hurston (Il loro occhi guardavano Dio, traduzione italiana non reperibile), Elif Shafak (La quarantesima porta, nessun riscontro sul titolo/traduzione italiana); nota per i run futuri: Le Guin/Angelou/Adichie sono ormai da considerarsi scartate in modo strutturale su questo sito, salvo trovare una fonte primaria (Wikiquote o testo del libro) inequivocabile
- 2026-08-03 08:22 UTC — added 2 quotes (total now 131) — aggiunte citazioni di Beppe Fenoglio (Una questione privata, incipit confermato su due fonti indipendenti) e Alberto Moravia (Gli indifferenti, incipit confermato) — entrambe opere originariamente in italiano, nessun rischio di traduzione discordante; scartati Pier Paolo Pasolini ("Amo ferocemente, disperatamente la vita" — frase nata da un'intervista del 1970, non da un'opera letteraria con titolo/anno univoco, attribuzione a un libro troppo ambigua), Truman Capote (Colazione da Tiffany — la stessa frase sulla "creatura selvatica" appariva con finali diversi tra due fonti indipendenti, wording non univoco), Philip K. Dick (Il cacciatore di androidi — passo trovato di dubbia attribuzione al romanzo specifico), Yukio Mishima (Il padiglione d'oro — citazioni reperite solo su siti aggregatori, nessun riscontro su Wikiquote), Dacia Maraini (La lunga vita di Marianna Ucrìa — nessuna citazione con fonte affidabile reperita), Niccolò Ammaniti (Io non ho paura — citazioni solo da aggregatori, non confermabili come testo esatto del libro)
- 2026-08-03 09:22 UTC — added 5 quotes (total now 136) — aggiunte citazioni di Ugo Foscolo (Dei Sepolcri, "l'urne de' forti"), Giovanni Pascoli (X Agosto), Elio Vittorini (Conversazione in Sicilia, incipit "astratti furori"), Franz Kafka (Lettera al padre, confermata su Wikiquote/frasicelebri), Leonardo Sciascia (Il giorno della civetta, "la verità è nel fondo di un pozzo") — tutte verificate su piu fonti indipendenti con wording concordante; scartati George Eliot (Middlemarch, nessuna traduzione italiana della frase finale reperibile con fonte affidabile), Emily Dickinson ("Because I could not stop for Death", traduzioni italiane discordanti tra loro, wording non univoco), Thomas Mann (La montagna incantata, citazione sul tempo reperita solo in forma frammentata/parafrasata, non verbatim), Stefan Zweig (Il mondo di ieri, nessuna frase singola breve e ben verificabile trovata, solo passi lunghi)
- 2026-08-03 10:21 UTC — added 4 quotes (total now 140) — aggiunte citazioni di Alessandro Baricco (Oceano mare, "Non ti ho amato per noia..."), Chimamanda Ngozi Adichie (Americanah, wording esatto finalmente confermato su anobii — capovolge gli scarti ripetuti nei run precedenti per la stessa opera, che non avevano trovato una frase singola con wording verificabile), Yukio Mishima (Confessioni di una maschera, "Non mi curavo di nulla...", confermata su Goodreads con tag specifico dell'opera), Amos Oz (Una storia di amore e di tenebra, "Mettere al mondo una parola nuova...") — tutte verificate su fonti indipendenti con wording concordante; scartata Clarice Lispector (L'ora della stella, nessuna frase breve e iconica con wording esatto confermabile — gia scartata piu volte per lo stesso motivo) e Anaïs Nin (il celebre passo sul "rischio di restare chiusi in un bocciolo", attribuzione al diario controversa/dibattuta tra le fonti, non abbastanza solida per una citazione verificata)
- 2026-08-03 14:21 UTC — added 4 quotes (total now 147) — aggiunte citazioni di Goliarda Sapienza (L'arte della gioia, "No, non si può comunicare a nessuno questa gioia piena..." — confermata come frase del romanzo su piu fonti aggregatori concordi), Paolo Cognetti (Le otto montagne, "Il passato è a valle, il futuro a monte" — confermata su piu fonti indipendenti), Alba de Céspedes (Quaderno proibito, "Ci siamo tanto allontanati l'uno dall'altra..." — confermata su piu fonti indipendenti), Naguib Mahfouz (Il palazzo del desiderio, "Niente è più brutto di una parola d'amore pronunciata freddamente..." — wording italiano trovato direttamente su le-citazioni.it, non tradotto da me); scartata Clarice Lispector (L'ora della stella, incipit "Tudo no mundo começou com um sim" — originale portoghese confermato con altissima certezza (citato anche in prove ENEM), ma nessuna fonte ha confermato il wording esatto della traduzione italiana pubblicata (Feltrinelli, trad. Adelina Aletti); la mia resa italiana sarebbe stata una mia traduzione non verificata — coerente con gli scarti strutturali di questo stesso titolo in almeno 4 run precedenti per lo stesso motivo); scartati anche Yasunari Kawabata (Il paese delle nevi, incipit — due traduzioni italiane discordanti reperite, "sbucò" vs "usciti dalla lunga galleria di confine", wording non univoco) e Zadie Smith (Denti bianchi, citazioni su fede/tradizione trovate ma nessuna adatta a una categoria tematica del sito senza forzatura)
- 2026-08-03 15:20 UTC — added 6 quotes (total now 153) — aggiunte citazioni di Joseph Conrad (Cuore di tenebra, "L'orrore! L'orrore!", grido di Kurtz confermato su piu fonti), Daphne du Maurier (Rebecca, la prima moglie, incipit "Ieri notte ho sognato di tornare a Manderley", confermato su fonti indipendenti incluso un blog letterario dedicato all'incipit), Orhan Pamuk (Il mio nome è rosso, incipit "Adesso io sono un morto, un cadavere in fondo a un pozzo...", traduzione di Maria Bertolini/Şemsa Gezgin per Einaudi confermata), Patrick Süskind (Il profumo, incipit "Nel diciottesimo secolo visse in Francia un uomo...", traduzione di Giovanna Agabio per Longanesi confermata su Wikiquote/IncipitMania), Gustave Flaubert (Madame Bovary, "La parola umana è simile a un calderone incrinato...", citazione molto nota confermata su piu fonti indipendenti concordanti), Thomas Hardy (Tess dei d'Urberville, chiusa del romanzo sul "Presidente degli Immortali", confermata su piu fonti indipendenti) — primi autori di questi 6 libri sul sito, nessun rischio di duplicato; scartato Federico García Lorca (Romancero gitano, "Verde que te quiero verde" → "Verde che ti voglio verde" — traduzione reperita solo su lyricstranslate, fonte amatoriale non equiparabile a un'edizione italiana pubblicata, wording non confermabile con certezza come standard editoriale)
- 2026-08-03 16:16 UTC — added 4 quotes (total now 157) — aggiunta manuale (non routine): Ludovico Ariosto (Orlando furioso, incipit su Wikisource), Ippolito Nievo (Le confessioni d'un italiano, incipit su Liber Liber), Arthur Conan Doyle (Il segno dei quattro), Alexandre Dumas (Il conte di Montecristo); scartati Bram Stoker, Stevenson, Kipling, Oscar Wilde (De Profundis), Hawthorne, Stendhal, Cechov, Thomas Mann, Shaw, Zola, Hesse — solo fonti aggregatore senza riscontro primario, o citazione troppo lunga
- 2026-08-03 16:22 UTC — added 7 quotes (total now 164) — aggiunta manuale (non routine): Honoré de Balzac (Papà Goriot), Charles Dickens (Oliver Twist), Pablo Neruda (Venti poesie d'amore e una canzone disperata), Walt Whitman (Foglie d'erba, seconda citazione), Victor Hugo (Notre-Dame de Paris, seconda citazione), Federico García Lorca (La casa di Bernarda Alba), Mark Twain (Le avventure di Huckleberry Finn, confermata su Wikiquote); scartato Molière (Il misantropo, solo fonti aggregatore senza riscontro su Wikiquote per la frase specifica)
- 2026-08-03 22:22 UTC — added 3 quotes (total now 167) — aggiunte citazioni di Carlo Collodi (Le avventure di Pinocchio, "Vi sono le bugie che hanno le gambe corte..." confermata su Wikisource, testo primario), Eugenio Montale (Ossi di seppia, chiusa di "Meriggiare pallido e assorto", testo completo confermato su piu fonti concordanti e Wikipedia), Pier Paolo Pasolini (Ragazzi di vita, incipit confermato su piu siti specializzati in incipit con wording concorde); scartati Thomas Mann (La morte a Venezia) e Stefan Zweig (Il mondo di ieri) nonostante quote plausibili, perché confermati solo da siti aggregatori di aforismi senza riscontro su fonte primaria/Wikiquote — stesso motivo per cui Thomas Mann era gia stato scartato in un run precedente (16:16 UTC); scartato anche Anton Čechov (Il gabbiano, battuta su Genova) per scarsa aderenza tematica alle categorie del sito
- 2026-08-04 00:22 UTC — added 5 quotes (total now 177) — aggiunte citazioni di Ursula K. Le Guin (La mano sinistra delle tenebre, "La luce è la mano sinistra delle tenebre..." confermata su le-citazioni.it), Jules Verne (Ventimila leghe sotto i mari, monologo di Nemo sul mare confermato su frasicelebri.it), Robert Louis Stevenson (Lo strano caso del dottor Jekyll e del signor Hyde, "La tentazione di fare ciò che è proibito..." confermata su le-citazioni.it), H.G. Wells (La macchina del tempo, sensazioni del viaggio nel tempo confermate su le-citazioni.it), Elif Shafak (Le quaranta porte, "Si può conoscere solo ciò che si è in grado di amare..." confermata su fonte dedicata al libro) — tutti primi autori/libri sul sito, nessun rischio di duplicato; scartate Emily Dickinson ("Because I could not stop for Death", traduzione italiana esatta non reperibile per motivi di copyright) e Zora Neale Hurston (I loro occhi guardavano Dio, incipit riportato solo in forma parafrasata dalla ricerca, wording non verificabile come citazione letterale)
- 2026-08-04 01:22 UTC — added 1 quote (total now 178) — aggiunta citazione di William Faulkner (Requiem per una monaca, "Il passato non è mai morto. Non è neanche passato.", traduzione storica di Fernanda Pivano confermata su piu fonti indipendenti concordanti incluso un estratto video con lettura della traduzione pubblicata); scartati E.M. Forster (Howards End, "Only connect" — traduzioni italiane discordanti tra le fonti trovate ("Collega solo la prosa..." vs "Null'altro che connettere..."), stesso motivo di scarto gia registrato per questo titolo nel run dell'11:20 UTC del 2026-08-03), Yann Martel (Vita di Pi, "una storia che vi farà credere in Dio" — la formulazione trovata proveniva dal film, non dal testo del libro, wording non confermabile come citazione letteraria esatta), Zadie Smith (Denti bianchi, "Il passato è sempre al tempo imperfetto, il futuro al futuro perfetto" — nel romanzo la frase è incastonata diversamente ("la bugia malvagia, che il passato è sempre tempo imperfetto e il futuro, perfetto"), la versione isolata circolante non corrisponde al testo esatto), Agatha Christie (Assassinio sull'Orient Express, "L'impossibile non può essere accaduto..." — scartata per idea troppo simile alla citazione di Arthur Conan Doyle già presente sul sito, "Quando hai eliminato l'impossibile..."), Marco Aurelio (Colloqui con se stesso — solo fonti aggregatori/blog di aforismi trovate, nessun riscontro su Wikiquote o edizione pubblicata, coerente con gli scarti strutturali già registrati per questo autore nei run dell'11:20 e 12:21 UTC del 2026-08-02), Thomas Mann (La montagna incantata — stesso problema gia riscontrato in almeno due run precedenti (09:22 UTC e 22:22 UTC del 2026-08-03): solo fonti aggregatori di aforismi, nessuna conferma su fonte primaria), Salman Rushdie (I versi satanici — nessuna citazione con wording esatto individuata dalla ricerca)
- 2026-08-04 02:22 UTC — added 4 quotes (total now 182) — aggiunte citazioni di Umberto Saba (Trieste, "Trieste ha una scontrosa grazia..." confermata su piu fonti concordanti tra cui sapere.virgilio.it), Elena Ferrante (I giorni dell'abbandono, incipit "Un pomeriggio d'aprile..." confermato su aforismi.meglio.it), Mario Vargas Llosa (Conversazione nella «Catedral», "In che momento si era fottuto il Perù?" confermata inclusa la corretta grafia italiana del titolo con «Catedral» non tradotto), Octavio Paz (Il labirinto della solitudine, brano sulla solitudine come radice del sentimento religioso, confermato su anobii con citazioni dall'edizione italiana); scartati Clarice Lispector (L'ora della stella, incipit "Tutto cominciò con un Sì" — wording esatto della traduzione italiana Aletti non riscontrato con certezza) e Yasunari Kawabata (Il paese delle nevi — due traduzioni italiane pubblicate con incipit diversi tra loro, nessuna corrispondeva al wording ipotizzato, scartato per evitare imprecisione)
- 2026-08-04 03:21 UTC — added 2 quotes (total now 184) — aggiunte citazioni di Stefan Zweig (Novella degli scacchi, "Niente al mondo è in grado di esercitare una tale pressione sull'anima umana come il nulla", confermata presente nella pagina Wikiquote dedicata all'autore/opera, non solo su siti aggregatori) e Thomas Mann (La montagna incantata, "Il tempo raffredda, il tempo chiarifica; nessuno stato d'animo si può mantenere del tutto inalterato nello scorrere delle ore", confermata sulla pagina Wikiquote dedicata al romanzo — a differenza dei tentativi precedenti scartati nei run del 2026-08-03 09:22 e 22:22 UTC e del 2026-08-04 01:22 UTC, questa volta la citazione risulta effettivamente presente su Wikiquote e non solo su aggregatori di aforismi); scartata Clarice Lispector (L'ora della stella, incipit "Tutto al mondo cominciò con un Sì" — ritentata in questo run ma di nuovo non confermabile su fonte primaria/Wikiquote, la pagina Wikiquote dedicata all'autrice non riporta questa citazione, coerente con lo scarto gia registrato nel run delle 02:22 UTC); scartato anche Toni Morrison (Canto di Salomone, ipotesi di citazione sul volo/abbandonarsi all'aria — wording esatto non individuato nella ricerca, frase alternativa trovata ("Senza mai abbandonare il suolo, Pilate poteva volare") ma non verificata a sufficienza per l'inclusione)
- 2026-08-04 06:48 UTC — added 8 quotes (total now 201) — aggiunta manuale (non routine): Salman Rushdie (I figli della mezzanotte), Annie Ernaux (Gli anni), Ignazio Silone (Fontamara, confermata su Wikiquote), Curzio Malaparte (La pelle, confermata su Wikiquote), Julian Barnes (Il senso di una fine), Anton Čechov (Tre sorelle), Roberto Bolaño (2666, confermata su Wikiquote), Don DeLillo (Rumore bianco); scartato Juan Rulfo (Pedro Páramo, incipit ambiguo tra piu fonti discordanti su quale sia la frase iniziale reale)
- 2026-08-04 08:12 UTC — added 4 quotes (total now 205) — aggiunta manuale (non routine): Günter Grass (Il tamburo di latta, incipit confermato su piu fonti accademiche/letterarie), Imre Kertész (Essere senza destino), Wisława Szymborska (Nulla due volte, edizione italiana Amore a prima vista, Adelphi), Philip Roth (Pastorale americana, confermata su Wikiquote)
- 2026-08-04 09:01 UTC — added 3 quotes (total now 208) — aggiunta manuale (non routine): Saul Bellow (Herzog, incipit celebre confermato su Wikiquote), Gabriele D'Annunzio (Il piacere, incipit confermato su Wikiquote), Herta Müller (Il paese delle prugne verdi, confermata su piu fonti letterarie indipendenti); scartati David Grossman (Vedi alla voce: amore, nessuna citazione esatta reperita), Patrick Modiano (Dora Bruder, nessuna citazione esatta reperita), Thomas Bernhard (attribuzione ambigua tra Il soccombente ed Estinzione)
- 2026-08-04 14:27 UTC — added 3 quotes (total now 211) — aggiunte citazioni di Gabriel García Márquez (Cronaca di una morte annunciata, incipit confermato su Wikipedia IT e piu fonti aggregatori concordanti), Jorge Amado (Capitani della spiaggia, "La libertà è come il sole..." confermata su piu fonti indipendenti, wording "del mondo" verificato incrociando due ricerche), Elsa Morante (L'isola di Arturo, riflessione sull'amore confermata su Goodreads, aforismi.meglio.it e pagina Wikiquote dedicata al romanzo); scartati Konstantinos Kavafis (Itaca, esistono almeno 3 traduzioni italiane pubblicate discordanti tra loro — Dalmati/Risi Einaudi 1992, Di Gregorio Garzanti 2017 — wording non univoco), Cormac McCarthy (Non è un paese per vecchi, le citazioni trovate provenivano dal doppiaggio del film e non dalla traduzione del romanzo di Martina Testa, rischio di mismatch come gia riscontrato per Yann Martel in un run precedente), W. Somerset Maugham (Il filo del rasoio, solo fonte aggregatore le-citazioni.it senza riscontro su Wikiquote o seconda fonte indipendente), Gavino Ledda (Padre padrone, nessuna citazione specifica reperita dalla pagina Wikiquote dedicata)
- 2026-08-04 18:21 UTC — added 1 quote (total now 212) — aggiunta citazione di Zora Neale Hurston (I loro occhi guardavano Dio, "L'amore è come il mare. Mobile, ma al tempo stesso immutabile, e segue i contorni della spiaggia che bacia, e su ogni spiaggia è diverso.", questa volta confermata su due fonti indipendenti concordanti — le-citazioni.it e la pagina it.wikiquote.org/wiki/Zora_Neale_Hurston (oltre a it.wikiquote.org/wiki/Amore) — con wording identico, a differenza dei tentativi precedenti (run del 2026-08-03 03:20, 04:22 e del 2026-08-04 00:22 UTC) in cui la traduzione italiana risultava irreperibile o discordante tra fonti; scartato Yasunari Kawabata (Il paese delle nevi, stesso motivo di scarto gia riscontrato piu volte in run precedenti — 12:22 UTC del 2026-08-03 e 14:21 UTC del 2026-08-03: due traduzioni italiane pubblicate discordanti dell'incipit, "sbucò dalla lunga galleria" (trad. Lamberti/Einaudi) vs "usciti dalla lunga galleria di confine" (trad. Amitrano), wording non univoco); scartati anche Rabindranath Tagore (Uccelli migranti, l'aforisma "Lascia che la vita sia bella come i fiori d'estate..." circola solo su siti di aforismi generici, nessuna fonte ha confermato che appartenga a quella specifica raccolta con una traduzione italiana pubblicata verificabile) e Toni Morrison (Canto di Salomone, "Se ti fossi abbandonato all'aria, avresti potuto cavalcarla" — nessuna traduzione italiana esatta reperita, stesso motivo di scarto strutturale gia registrato in almeno 8 run precedenti per questo stesso libro)
- 2026-08-11 11:37 UTC — added 4 quotes (total now 216) — aggiunta manuale (non routine): Ian McEwan (Espiazione, confermata su Wikiquote), Vasco Pratolini (Cronache di poveri amanti), Anna Maria Ortese (Il mare non bagna Napoli), José Saramago (Le intermittenze della morte, incipit celebre); scartato Andrea Camilleri (nessuna citazione riconducibile a un romanzo specifico con titolo/anno, solo dichiarazioni/interviste generiche)
- 2026-08-13 12:20 UTC — added 3 quotes (total now 219) — aggiunta manuale (non routine), con copertine recuperate subito: David Foster Wallace (Infinite Jest, confermata su piu fonti indipendenti concordanti), Zadie Smith (Denti bianchi), Umberto Eco (Il pendolo di Foucault, incipit confermato su archive.org e Wikiquote); scartati Jonathan Franzen (Le correzioni) e Colson Whitehead (La ferrovia sotterranea) per fonti solo aggregatore senza riscontro incrociato sufficiente
- 2026-08-16 12:54 UTC — added 4 quotes (total now 223) — aggiunta manuale (non routine), copertine recuperate subito (3/4 trovate): Arundhati Roy (Il dio delle piccole cose), Marilynne Robinson (Gilead, confermata su Wikiquote), J.M. Coetzee (Aspettando i barbari, confermata su Wikiquote), Alice Munro (La vista da Castle Rock); scartata Jhumpa Lahiri (L'omonimo, nessuna citazione esatta reperita)
- 2026-08-17 10:26 UTC — added 3 quotes (total now 226) — aggiunta manuale (non routine): William Faulkner (L'urlo e il furore, confermata su Wikiquote), Vladimir Nabokov (Fuoco pallido), Toni Morrison (Sula, stavolta con fonte specifica al libro, a differenza dei tentativi precedenti su Canto di Salomone gia scartati piu volte); scartati Michael Chabon (nessuna traduzione italiana reperita) e un tentativo su Elena Ferrante (La figlia oscura, nessuna citazione specifica reperita); copertine non recuperate in questo giro per irraggiungibilita temporanea di Open Library, da recuperare al prossimo aggiornamento
- 2026-08-17 15:13 UTC — added 2 quotes (total now 228) — aggiunta manuale (non routine): Ta-Nehisi Coates (Tra me e il mondo, confermata su Wikiquote) e Cormac McCarthy (Meridiano di sangue, tematicamente legata al titolo, confermata su piu fonti indipendenti); scartati Yaa Gyasi (Ritorno a casa), Amitav Ghosh (Il palazzo degli specchi) e Colm Tóibín (Brooklyn), nessuna citazione italiana specifica reperita per nessuno dei tre; recuperata anche la copertina di Vladimir Nabokov rimasta indietro nel giro precedente per un problema temporaneo di rete verso Open Library
- 2026-08-18 07:14 UTC — added 3 quotes (total now 231) — aggiunta manuale (non routine): Michael Ondaatje (Il paziente inglese), Seamus Heaney (Morte di un naturalista, apertura di 'Scavando', confermata su Wikiquote), V.S. Naipaul (Alla curva del fiume, incipit celebre); scartata Louise Erdrich (fonti confuse, un risultato mescolava titoli di un'altra autrice); copertina trovata solo per Ondaatje, le altre restano in sospeso
- 2026-08-18 07:57 UTC — added 3 quotes (total now 234) — aggiunta manuale (non routine): Alessandro Baricco (Seta), Haruki Murakami (1Q84), Doris Lessing (Il taccuino d'oro, scelta una citazione piu specifica dopo aver scartato una frase sospetta trovata nella stessa ricerca); recuperate anche le copertine rimaste indietro di Toni Morrison (Sula) e dello stesso Baricco (Seta)
- 2026-08-18 12:28 UTC — added 3 quotes (total now 237) — aggiunta manuale (non routine), copertine recuperate subito: Orhan Pamuk (Neve, incipit confermato su Wikiquote), Elias Canetti (Auto da fé), Kazuo Ishiguro (Quando eravamo orfani, confermata su Wikiquote e le-citazioni.it)
- 2026-08-18 12:46 UTC — added 7 quotes (total now 244) — aggiunta manuale (non routine), copertine NON recuperate su richiesta esplicita (da fare in un giro dedicato successivo): J.R.R. Tolkien (Il Signore degli Anelli - La Compagnia dell'Anello e Il ritorno del re, 2 citazioni diverse da quella gia presente), J.K. Rowling (Harry Potter e i Doni della Morte, Harry Potter e la Pietra Filosofale, 2 citazioni diverse da quella gia presente), C.S. Lewis (Le cronache di Narnia - Il leone, la strega e l'armadio), George R.R. Martin (Il Trono di Spade), Suzanne Collins (Hunger Games) — tutte confermate su Wikiquote
- 2026-08-25 UTC — aggiunto contesto retroattivo a 8 citazioni già presenti (nessuna citazione nuova, totale resta 253): Leopardi (L'infinito, verso finale del componimento, il perdersi immaginativo dietro la siepe), Manzoni (I promessi sposi, è don Abbondio a scusarsi così col cardinal Federigo, cap. XXV), Brontë (Cime tempestose, Catherine lo dice a Nelly Dean, Heathcliff origlia da fuori, cap. 9), Wilde (Il ritratto di Dorian Gray, massima di lord Henry Wotton, cap. 2), Camus (L'estate, chiusa del saggio "Ritorno a Tipasa", non un personaggio ma Camus stesso), Hesse (Demian, biglietto non firmato che Sinclair riceve, attribuito a Demian, cita Abraxas, cap. 5), Dickens (Racconto di due città, incipit del romanzo), Neruda (Cento sonetti d'amore, apertura del Sonetto XVII, dedicato alla moglie Matilde Urrutia). Verificati via ricerca web i dettagli meno ovvi (capitolo di Manzoni, parlante e capitolo di Brontë, natura del testo in Demian). Restano circa 219 citazioni senza contesto.
- 2026-08-26 UTC — added 3 quotes (total now 256) — aggiunte citazioni di Rick Riordan (Percy Jackson e gli dei dell'Olimpo: la battaglia del labirinto, "Io sono il tuo miglior amico..." di Giano, confermata su it.wikiquote.org e le-citazioni.it con wording concordante), Neil Gaiman (Coraline, "quando hai paura di qualcosa, ma la fai comunque, quello è coraggio", confermata su it.wikiquote.org e sulla pagina tematica Wikiquote "Coraggio"), Terry Pratchett (Il tristo mietitore, "la luce scopre sempre che il buio è arrivato prima di lei", confermata su it.wikiquote.org con riferimento a pagina 254 dell'edizione italiana) — le prime tre aggiunte del lotto "autrici/autori fantasy contemporanei" della roadmap, copertine verificate visivamente su Open Library; scartati Sarah J. Maas (nessuna citazione con wording italiano esatto reperibile da fonte tracciabile, solo descrizioni di trama) e Leigh Bardugo (Sei di corvi, "quando tutti pensano che sei un mostro..." — trovata solo su blog di recensioni personali senza riferimento a pagina/capitolo, non abbastanza per superare la soglia di due fonti indipendenti tracciabili al testo pubblicato; da ritentare con accesso a un'anteprima Google Libri o a una fonte editoriale).
- 2026-08-28 UTC — recuperate 28 copertine su 43 mancanti (in autonomia, lavoro concordato con l'utente) — Dickens (Racconto di due città), Neruda (Cento sonetti d'amore), Rilke (Lettere a un giovane poeta), Sartre (A porte chiuse), Hemingway (Festa mobile), David Foster Wallace (Questa è l'acqua), Achebe (Le cose crollano), Octavia E. Butler (La parabola del seminatore), Emily St. John Mandel (Stazione undici), Baldwin (La prossima volta il fuoco), Conrad (Cuore di tenebra), Lorca (La casa di Bernarda Alba), Le Guin (La mano sinistra delle tenebre), Stevenson (Lo strano caso del dottor Jekyll e del signor Hyde), Faulkner (Requiem per una monaca, L'urlo e il furore), Paz (Il labirinto della solitudine), Zweig (Novella degli scacchi), Mann (La montagna incantata), Hurston (I loro occhi guardavano Dio), Coetzee (Aspettando i barbari), Ta-Nehisi Coates (Tra me e il mondo), McCarthy (Meridiano di sangue), Heaney (Morte di un naturalista), Tolkien (La Compagnia dell'Anello, Il ritorno del re — copertine in tela blu senza sovraccoperta, testo verificato a piena risoluzione), C.S. Lewis (Le cronache di Narnia), J.M. Barrie (Le avventure di Peter Pan) — tutte verificate visivamente prima dell'inserimento; scartate Thomas Hardy (Tess dei d'Urberville, copertina in tela senza alcun testo identificativo, impossibile confermare) e Simone de Beauvoir (Il secondo sesso, l'immagine era in realtà un "companion volume" diverso dal libro, non l'edizione del testo stesso); restano senza copertina 15 citazioni: 3 poesie senza edizione autonoma (Leopardi, Camus "L'estate", Pascoli) e 12 per cui Open Library non ha restituito un'edizione con autore corrispondente (Beauvoir "Memorie d'una ragazza perbene", Kundera, Kafka "Il Castello", Simone Weil, Orhan Pamuk, Elif Shafak, Čechov, Herta Müller, Jorge Amado, V.S. Naipaul, più Hardy e Beauvoir scartati sopra).
- 2026-08-28 UTC — aggiunto contesto retroattivo a 90 citazioni già presenti in quattro lotti (in autonomia, lavoro concordato con l'utente), totale ora 127/256 con contesto — lotto 1 (20): Pessoa, Tolstoj (Guerra e pace, Andrej Bolkonskij ad Austerlitz), Woolf, Shakespeare, Mary Shelley, Hugo, Dickinson, Whitman (2 citazioni diverse dallo stesso libro, corretta una sovrapposizione iniziale tra "Sono vasto" e "O Capitano"), Hesse (Siddhartha), Tolkien (2 libri), Beauvoir, Anne Frank, Primo Levi, Svevo, Alcott, Brontë, Kerouac, Hemingway, Harper Lee — lotto 2 (24): Dostoevskij (Fratelli Karamazov, verificato su web che è lo starec Zosima a parlare), Seneca, Yourcenar, Calvino (Barone rampante), Frankl, Hesse (Lupo della steppa), Deledda, Tomasi di Lampedusa (verificato: Tancredi allo zio, non genericamente "a qualcuno"), García Márquez, Plath, Ende, Ferrante, Nabokov, Huxley, Bradbury, Vonnegut, Ginzburg, Allende, Pavese, Pirandello, Verga, Ungaretti (2 citazioni da poesie diverse, "Mattina" e "Soldati" — corretta una sovrapposizione iniziale), Buzzati, Morante — lotto 3 (27): Saint-Exupéry (2 citazioni diverse, nessuna sovrapposizione), Carroll, Machiavelli, Eco, Manzoni, Calvino (Se una notte d'inverno), Wiesel, Coelho, Gibran, Rilke, Proust, Sartre, Kundera (Insostenibile leggerezza), Saramago, Murakami (Norwegian Wood, verificato: è Watanabe), Rowling (verificato: è Silente, capitolo dopo lo Smistamento), Camus (La peste), Borges (L'Aleph), Beauvoir (Memorie d'una ragazza perbene), Hemingway (Festa mobile), Kundera (Libro del riso e dell'oblio), McCarthy (La strada), Camus (Mito di Sisifo), Murakami (Kafka sulla spiaggia), Melville, Kafka (Il Castello), Borges (Finzioni), David Foster Wallace — lotto 4 (17): Dostoevskij (Memorie dal sottosuolo), Pasternak, Hosseini, Bassani, Carlo Levi, Atwood, Calvino (Palomar), Aleramo, Didion, De Luca, Ishiguro, Murgia, Achebe, Tabucchi, Cortázar, Duras, Octavia E. Butler. Verificati via ricerca web i dettagli meno ovvi quando necessario (parlante, capitolo, opera esatta), finché la ricerca web non ha esaurito il limite settimanale (si ripristina il 2026-08-30); da quel momento aggiunti solo dettagli già noti con sicurezza. Scartate per questo lotto due citazioni per assenza di conferma sul parlante esatto: Fëdor Dostoevskij (Delitto e castigo, "a volte l'uomo è straordinariamente...innamorato della sofferenza" — già segnalata come problematica in un run precedente, tentata di nuovo senza successo) e Sandro Veronesi (Il colibrì, la metafora del colibrì — Wikiquote conferma che viene dalla "Terza lettera sul colibrì" ma non chi la scrive nel romanzo); da ritentare quando la ricerca web sarà di nuovo disponibile. Dopo ogni lotto fatto un controllo automatico per individuare contesti applicati per errore alla stessa citazione su più autori/titoli identici nel sito (trovati e corretti 2 casi: Whitman "O Capitano" e Ungaretti "Soldati", entrambi risolti prima della pubblicazione). Restano 129 citazioni senza contesto.
- 2026-08-28 UTC (continuazione, dopo ripristino del limite settimanale di ricerca web) — aggiunto contesto ad altre 126 citazioni in tre ulteriori lotti (20+23+80... in realtà: lotto Veronesi/1, lotto da 23, lotto da 22, lotto grande da 80), portando il totale da 127 a 253 su 256 — sostanzialmente COMPLETATO il cantiere "contesto per tutte le citazioni" aperto da settimane. Confermato via ricerca web anche il colibrì di Veronesi (Luisa Lattes scrive a Marco Carrera nella "Terza lettera sul colibrì"). Coperti in questi lotti tra gli altri: Rilke, Le Guin, Verne, Stevenson, Wells, Faulkner (3 opere), Boccaccio, Petrarca, Tasso, Ariosto, Nievo, Dante (2 citazioni), Pirandello, Woolf (2 opere), Sartre (2 opere), Mann (2 opere), tutta la narrativa fantasy/genere rimasta (Tolkien 2, Rowling 2, C.S. Lewis, G.R.R. Martin, Suzanne Collins, Frank Herbert, Isaac Asimov, Douglas Adams, Madeline Miller), autori italiani (Saba, Vittorini, Kafka "Lettera al padre", Baricco 2, Montale, Pasolini, Quasimodo, Silone, Malaparte, Pratolini, Ortese) e molti altri classici stranieri (McEwan, Robinson, Coetzee, Munro, Nabokov, Morrison, Coates, McCarthy, Ondaatje, Heaney, Naipaul, Murakami 2, Lessing, Pamuk 2, Canetti, Ishiguro 2, Rushdie, Ernaux, Barnes, Bolaño, DeLillo, Grass, Kertész, Szymborska, Roth, Bellow, D'Annunzio, Müller, García Márquez, Amado, Morante, Hurston, Saramago, David Foster Wallace "Infinite Jest", Zadie Smith, Eco, Roy, Stoker, Capote, Barrie). Verificati via ricerca web i dettagli meno ovvi per gran parte di questi (parlante, capitolo, opera esatta), incluse verifiche puntuali per DeLillo (Murray Siskind), Morrison Sula (a chi lo dice), Robinson Gilead (incipit lettera del reverendo Ames), Heaney "Scavando", Le Guin (proverbio di Gethen citato da Genly Ai), DFW Infinite Jest (pensiero di Don Gately). Restano SOLO 3 citazioni senza contesto, tutte scartate per la stessa ragione — nessuna fonte (incluso Wikiquote, controllato direttamente) attribuisce un parlante o un capitolo preciso: Dostoevskij (Delitto e castigo, "innamorato della sofferenza" — già problematica in almeno due run precedenti), Sciascia (Il giorno della civetta, "la verità è nel fondo di un pozzo"), Mahfouz (Il palazzo del desiderio, "niente è più brutto di una parola d'amore..."). IMPORTANTE per quest'ultima: la ricerca ha rivelato una possibile discrepanza nell'attribuzione già pubblicata sul sito — alcune fonti (incluso Wikiquote) attribuiscono la stessa frase esatta a "Vicolo del mortaio" (Midaq Alley), un romanzo diverso di Mahfouz, non a "Il palazzo del desiderio". Le fonti si contraddicono senza una versione chiaramente più autorevole. Non ho corretto il titolo alla cieca: segnalato qui perché richiede una verifica più approfondita (idealmente confrontando le due opere direttamente) prima di decidere se correggere il titolo o rimuovere la citazione.
- 2026-08-28 UTC — corretta un'attribuzione errata già pubblicata: la citazione di Naguib Mahfouz "Niente è più brutto di una parola d'amore pronunciata freddamente da una bocca annoiata" era attribuita a "Il palazzo del desiderio" (1957), ma una ricerca più approfondita (con dettagli narrativi specifici — Hamida, figlia adottiva dell'ostetrica Umm Hamida, corteggiata da Abbas che parte per arruolarsi nell'esercito inglese) conferma che appartiene invece a "Vicolo del mortaio" (Midaq Alley, 1947); nessuna fonte collega la frase a Il palazzo del desiderio con altrettanto dettaglio. Corretti titolo, anno e copertina (edizione inglese Trevor Le Gassick, cover_i 14814058, sostituisce la copertina errata precedente), aggiunto il contesto. Restano solo 2 citazioni senza contesto sull'intero sito: Dostoevskij (Delitto e castigo) e Sciascia (Il giorno della civetta), entrambe verificate anche su Wikiquote direttamente senza trovare un'attribuzione a un parlante preciso — da ritentare solo con accesso al testo integrale del romanzo.
- 2026-08-28 UTC — recuperate altre 4 copertine sulle 15 rimaste (in autonomia) — Orhan Pamuk (Il mio nome è rosso, edizione turca originale "Benim Adım Kırmızı"), Jorge Amado (Capitani della spiaggia, edizione inglese), V.S. Naipaul (Alla curva del fiume), Herta Müller (Il paese delle prugne verdi, edizione inglese "The Land of Green Plums") — tutte verificate visivamente. Ritentate anche Camus "L'estate" (unico risultato era un estratto parziale "Summer in Algiers", non la raccolta intera — scartato) e Simone de Beauvoir "Il secondo sesso" (stesso "companion volume" già scartato in precedenza) senza successo. Nessun risultato utile per Kundera, Kafka "Il Castello", Simone Weil, Elif Shafak, Čechov. Restano 11 citazioni senza copertina: 2 poesie senza edizione autonoma (Leopardi, Pascoli — irrecuperabili) + 9 senza un'edizione con copertina disponibile su Open Library.

- 2026-08-28 UTC — Fase 3 SEO (fonte verificabile), lotto 1/~17, 19 citazioni: tutti i classici di pubblico dominio italiani con testo integrale su Wikisource, come da ordine indicato in CLAUDE.md — Dante (Inferno canto V v.103 e canto I v.1), Leopardi (L'Infinito, Canto notturno di un pastore errante dell'Asia), Manzoni (Promessi Sposi cap. XXV e cap. I, Il cinque maggio vv. 31-32), Verga (I Malavoglia cap. I), Pirandello (Uno nessuno e centomila libro VIII "Non conclude", Il fu Mattia Pascal cap. I), Foscolo (Dei Sepolcri v. 151), Pascoli (X Agosto), Ariosto (Orlando furioso canto I), Boccaccio (Decameron, Proemio), Tasso (Gerusalemme liberata canto I), Petrarca (Canzoniere sonetto I v. 14), Machiavelli (Il Principe cap. XVII). Aggiunti anche Shakespeare (Amleto Atto III scena I, Romeo e Giulietta Atto II scena II): solo il locus (atto/scena, verificabile indipendentemente dalla traduzione), nessun traduttore attribuito — troppe traduzioni italiane diverse in circolazione per stabilire con certezza quale coincida col nostro testo, campo lasciato vuoto invece di indovinare. Tutti i link Wikisource verificati manualmente (200 OK). **Due correzioni di testo trovate durante la verifica, non solo fonti aggiunte**: Boccaccio aveva "aver" invece di "l'aver" (manca l'articolo), Machiavelli era una parafrasi modernizzata ("È molto più sicuro essere temuti che amati, se si deve rinunciare a uno dei due" invece del testo originale "È molto più sicuro l'esser temuto che amato, quando s'abbi a mancare dell'un de' duoi") — corrette entrambe al testo esatto della fonte primaria. Lezione operativa nuova: correggere il testo di una citazione già pubblicata cambia le "prime 6 parole" usate come chiave in tools/slugs.json, e senza intervento manuale genera uno slug nuovo al posto di riusare quello congelato (stesso URL deve restare stabile) — corretto rinominando a mano la chiave in slugs.json mantenendo lo slug invariato, verificato che build.py non generi pagine orfane. Build pulita dopo il lotto (0 fonti duplicate, 0 orfani).

- 2026-08-28 UTC — Fase 3 SEO, lotto 13/~20: 4 citazioni con fonte (Baudelaire, Pavese, Merini, Steinbeck). **Sospetto da verificare, non citazione scartata**: la citazione di Simone Weil "L'attenzione è la forma più rara e più pura della generosità" attribuita sul sito a "L'ombra e la grazia" — le fonti trovate in questa ricerca la riportano invece come parte di una lettera di Weil a Joe Bousquet del 1942, non del libro. Non ho toccato la citazione già pubblicata (serve una verifica più approfondita, magari diretta sul testo di "L'ombra e la grazia", prima di correggere titolo/opera): segnalato qui perché il prossimo lotto che tocca quella citazione deve partire da questo dubbio, non aggiungere una fonte a un'attribuzione potenzialmente sbagliata.

- 2026-08-28 UTC — Fase 3 SEO, lotto 17/~20: 3 citazioni con fonte (Dracula, Colazione da Tiffany, Percy Jackson). **Altri due sospetti da verificare**, stesso principio del lotto 13 su Weil — non toccate le citazioni già pubblicate, serve una verifica dedicata prima di correggere:
  1. **J.M. Barrie, "Solo chi sogna può volare"** — le fonti trovate la associano all'adattamento Disney di Peter Pan, non al romanzo originale "Peter e Wendy" (1911) di Barrie a cui è attribuita sul sito; nessuna fonte trovata conferma che la frase sia nel testo del romanzo. Da verificare se è genuinamente nel libro o se è un'invenzione del film.
  2. **Amin Maalouf, "In fondo all'Atlantico c'è un libro"** — attribuita sul sito a "Il manoscritto di Samarcanda", ma le fonti trovate la collegano a un romanzo diverso dello stesso autore, "Il periplo di Baldassarre" (Baldassare's Odyssey). Da verificare quale dei due libri è quello corretto prima di aggiungere qualunque fonte o correggere il titolo.

- 2026-08-28 UTC — Fase 3 SEO, lotto 18/~20: 4 citazioni con fonte (Cognetti, Nabokov con traduttore, McCarthy, Coetzee con traduttore). **Terzo sospetto di attribuzione**: "Che i giochi abbiano inizio e che vinca il migliore" (Hunger Games, Collins) — le fonti trovate la attribuiscono a Effie Trinket nel film, non confermano che sia testuale nel romanzo. Non aggiunta alcuna fonte, citazione lasciata come già pubblicata. Non trovata alcuna conferma per Toni Morrison "Sula" ("Non voglio fare qualcun altro. Voglio farmi da sola.") — non è un sospetto di attribuzione sbagliata, semplicemente le fonti cercate non la citano affatto: nessuna fonte aggiunta, da riprovare con una ricerca più mirata in un lotto successivo.

- 2026-08-28 UTC — Fase 3 SEO, lotto 20/~20: 2 citazioni con fonte (Baricco con data verificata, Pamuk incipit). Wording confermato ma nessun locus specifico trovato per altre 3 (Murakami 1Q84, Canetti Auto da fé, Doris Lessing Taccuino d'oro): nessuna fonte vuota aggiunta, da riprovare. **Quarto e più solido sospetto di attribuzione errata**: la citazione "Perché forse, in un certo senso, non ci eravamo lasciati alle spalle quello che ritenevamo di aver abbandonato..." attribuita sul sito a Ishiguro, "Quando eravamo orfani" — il wording trovato corrisponde parola per parola, ma la fonte la cita esplicitamente come tratta da "Non lasciarmi" (Never Let Me Go), un romanzo diverso dello stesso autore già presente sul sito con altre due citazioni. Rispetto ai tre dubbi precedenti (Weil, Barrie, Maalouf) qui la corrispondenza testuale era quasi certa, non solo indiziaria — **corretta subito nello stesso lotto**, non lasciata come dubbio aperto: title e anno aggiornati a "Non lasciarmi" (2005), aggiunta la fonte (narratrice Kathy H.), rigenerato lo slug (era basato sul titolo sbagliato) con redirect 301 dal vecchio URL in tools/redirects.json, ripulita la vecchia pagina/immagine OG orfana. Verificato che il nuovo slug "kazuo-ishiguro-non-lasciarmi-perche-forse-in" non collida con l'altra citazione già esistente da "Non lasciarmi" (usa il pattern con incipit, come da regola per le opere con più citazioni). Build pulita dopo la correzione (0 orfani, 1 redirect registrato).

- 2026-08-28 UTC — Fase 3 SEO, lotto 24/~25: 4 citazioni con fonte (Roth, Robinson, Coates, Ondaatje) + **seconda correzione di attribuzione nello stesso lotto**, stessa procedura di Ishiguro: la citazione "Ormai sapeva che nella vita viene il momento in cui brutto e bello svolgono più o meno la stessa funzione..." era attribuita a "La vista da Castle Rock" (2006) ma appartiene al racconto omonimo della raccolta "Nemico, amico, amante..." (2001) — wording verificato identico su due ricerche indipendenti. Corretti title e anno, rigenerato lo slug (dipendeva dal titolo sbagliato) con redirect 301, ripulita pagina/immagine OG orfana. Con questa sono due le attribuzioni sbagliate trovate e corrette in Fase 3 (Ishiguro, Munro), oltre alle due correzioni di wording del lotto 1 (Boccaccio, Machiavelli) e ai tre dubbi ancora aperti non risolti (Weil, Barrie, Maalouf, lotti 13/17) — segno che vale la pena, nei prossimi lotti, ricontrollare anche le citazioni che sembrano già solide.

- 2026-08-28 UTC — Fase 3 SEO, lotto 25/~25: 5 citazioni con fonte (Ishiguro "Non lasciarmi", Donna Tartt, Veronesi, Tamaro, Gaiman) + **terza correzione di attribuzione**, stessa procedura delle due precedenti: "Nessuno può sapere quanto rumore fa una certezza che si rompe" era attribuita ad "Accabadora" (2009) ma appartiene a "Chirù" (2015), stesso autore — confermato da due ricerche indipendenti concordanti, nessuna fonte lo attribuisce ad Accabadora. Corretti title e anno, rigenerato lo slug con redirect 301, ripulita pagina/immagine OG orfana. Tre correzioni di attribuzione totali in Fase 3 (Ishiguro, Munro, Murgia), tutte trovate cercando la fonte, non cercando errori: la verifica delle fonti sta facendo emergere problemi di correttezza pre-esistenti sul sito, non solo aggiungendo metadati.

- 2026-08-30 UTC — Fase 7 SEO (SEO-KEYWORDS.md §7): pubblicata la raccolta **"Donne"** (2.370 di
  volume di ricerca, 2/16), in autonomia dopo l'approvazione della prima raccolta. Filtrata
  l'intera archivio per radice lessicale (donna, donne, femmin) su quote+contesto: 31 candidati,
  letti uno per uno — scartati i falsi positivi lessicali senza pertinenza tematica reale (es. "via
  Donna Olimpia" in Pasolini, o "donna Arminda" come semplice titolo onorifico in Amado). 11
  citazioni pubblicate, dal Rinascimento (Ariosto, Boccaccio) al Novecento (Woolf, de Beauvoir,
  Aleramo, Fitzgerald, Mahfouz, Maraini, Murgia, Atwood, Lorde), nessun autore ripetuto. Boccaccio
  incluso non per il testo letterale della citazione ma per il contesto storico-letterario: il
  Decameron è dedicato esplicitamente "alle donne innamorate" nel proemio. Introduzione scritta a
  mano (288 parole, 3 paragrafi). Build pulita (0 problemi, 12/12 raccolte, controllo di integrità
  compreso).
  **Incidente tecnico durante il commit della raccolta precedente ("Viaggio e cammino"), corretto
  in questo stesso lotto**: una sessione concorrente stava lavorando in parallelo sullo stesso
  repository condiviso (stesso `.git`, non solo stessa cartella), con commit e `git add` che si
  intrecciavano ai miei in tempo reale (incluso un `index.lock` attivo durante un mio commit). Un
  `git add` con lista di file esplicita ha finito comunque per includere 980 file invece dei ~18
  previsti, perché l'indice di git aveva già in staging modifiche non mie (una funzionalità
  homepage della sessione concorrente, non ancora pronta per essere committata). Il commit
  risultante è stato pubblicato per errore con quel contenuto misto. Corretto senza riscrivere la
  storia condivisa (rischioso con un'altra sessione attiva sugli stessi commit): verificato che il
  contenuto non fosse comunque rotto (build pulita), poi lasciato stare — la sessione concorrente
  ha nel frattempo completato e ripubblicato il proprio lavoro con un commit dedicato. Lezione
  operativa: in un repository condiviso con sessioni concorrenti, verificare sempre `git diff
  --cached --stat` subito prima di ogni `git commit`, non fidarsi della lista di file passata a
  `git add`.

- 2026-08-30 UTC — Fase 7 SEO (SEO-KEYWORDS.md §7): pubblicata la raccolta **"Silenzio"** (16/16,
  ULTIMA del piano), in autonomia. Filtrata l'archivio per radice lessicale (silenzio, silenzios,
  tacere, taci, muto/a, quiete, ammutol): 22 candidati, letti uno per uno. 9 citazioni pubblicate:
  Federico García Lorca (La casa di Bernarda Alba), Wole Soyinka (L'uomo è morto), Pier Paolo
  Pasolini (La Divina Mimesis), Rainer Maria Rilke (Lettere a un giovane poeta, riusata da
  "Notte"), Gabriele D'Annunzio (Alcyone, riusata da "Natura"), Orhan Pamuk (Neve), Giovanni
  Pascoli (Myricae), Clarice Lispector (Dove siete stati di notte), Giacomo Leopardi (Canto
  notturno di un pastore errante dell'Asia, riusata da "Viaggio e cammino"/"Stelle e cielo").
  Introduzione scritta a mano (239 parole, 3 paragrafi). Build lanciata due volte (bug del
  contatore, vedi lotti precedenti): al secondo giro 0 problemi, 26/26 raccolte. **Con questa si
  chiudono le 16 raccolte indicate in SEO-KEYWORDS.md §7**: da 10 a 26 raccolte pubblicate in
  autonomia in una sola giornata (2026-08-30), 178 citazioni totali nelle nuove 16 (14 candidate
  singole, media ~11 a raccolta), nessuna sotto la soglia minima di 8, ordine di domanda di ricerca
  rispettato come richiesto. Nessuna raccolta scartata per mancanza di citazioni pertinenti: tutte
  e 16 hanno superato agevolmente la soglia leggendo i candidati, non solo contandoli.

- 2026-08-30 UTC — Fase 7 SEO (SEO-KEYWORDS.md §7): pubblicata la raccolta **"Stelle e cielo"**
  (15/16), in autonomia. Filtrata l'archivio per radice lessicale (stelle, stella, cielo, celeste,
  astri, astro, costellazion, galassia, pianeti, luna, sole, universo, cosmo): 32 candidati, letti
  uno per uno. 9 citazioni pubblicate: Dante Alighieri (Paradiso), Douglas Adams (Guida galattica
  per gli autostoppisti), Giovanni Pascoli (X Agosto), Salvatore Quasimodo (Ed è subito sera),
  Giacomo Leopardi (Canto notturno di un pastore errante dell'Asia, riusata da "Viaggio e
  cammino"), Anne Frank (Diario), Anna Achmatova (Lo stormo bianco), Francesco Petrarca
  (Canzoniere), Gabriele D'Annunzio (Il piacere). Introduzione scritta a mano (259 parole, 3
  paragrafi). Build lanciata due volte (bug del contatore, vedi lotti precedenti): al secondo giro
  0 problemi, 25/25 raccolte. Manca solo "silenzio" per chiudere le 16 raccolte del piano.

- 2026-08-30 UTC — Fase 7 SEO (SEO-KEYWORDS.md §7): pubblicata la raccolta **"Notte"** (14/16), in
  autonomia. Filtrata l'archivio per radice lessicale (notte/i, buio, oscurità, tenebr,
  crepuscolo): 26 candidati, letti uno per uno. 9 citazioni pubblicate: Elie Wiesel (La notte,
  riusata da "Ricordo e memoria"), Franz Kafka (Il Castello), Ursula K. Le Guin (La mano sinistra
  delle tenebre), Terry Pratchett (Il tristo mietitore), T.S. Eliot (Il canto d'amore di J. Alfred
  Prufrock), Rainer Maria Rilke (Lettere a un giovane poeta), Lev Tolstoj (I cosacchi), Pablo
  Neruda (Venti poesie d'amore e una canzone disperata, riusata da "Tristezza"), Daphne du Maurier
  (Rebecca, riusata da "Sogni"). Introduzione scritta a mano (286 parole, 3 paragrafi). Build
  lanciata due volte (bug del contatore, vedi lotti precedenti): al secondo giro 0 problemi, 24/24
  raccolte.

- 2026-08-30 UTC — Fase 7 SEO (SEO-KEYWORDS.md §7): pubblicata la raccolta **"Occhi e sguardo"**
  (13/16), in autonomia. Filtrata l'archivio per radice lessicale (occhi, occhio, sguard, pupill):
  27 candidati, letti uno per uno. 9 citazioni pubblicate: Antoine de Saint-Exupéry (Il piccolo
  principe), Sylvia Plath (Attraversando l'acqua, la poesia "Specchio"), Cesare Pavese (Verrà la
  morte e avrà i tuoi occhi, riusata da "Morte"/"Tristezza"), Marguerite Yourcenar (Memorie di
  Adriano, riusata da "Morte"), Giacomo Leopardi (A Silvia), Philip Roth (Addio, Columbus), Knut
  Hamsun (Fame), Giovanni Verga (Storia di una capinera, riusata da "Animali"), Alessandro Baricco
  (Seta). Introduzione scritta a mano (277 parole, 3 paragrafi). Build lanciata due volte (bug del
  contatore, vedi lotti precedenti): al secondo giro 0 problemi, 23/23 raccolte.

- 2026-08-30 UTC — Fase 7 SEO (SEO-KEYWORDS.md §7): pubblicata la raccolta **"Arte"** (12/16), in
  autonomia. Filtrata l'archivio per radice lessicale (arte, artista, dipint, quadro, pittur,
  scultur, musica, affresco, tela, pennell, museo, melodia, sinfonia, canzone, canto), tenuta
  distinta da "Libri e scrittura" già pubblicata (qui il fuoco è l'arte visiva e la musica, non la
  scrittura): 62 candidati, letti uno per uno. 9 citazioni pubblicate: Oscar Wilde (Il declino
  della menzogna), Iris Murdoch (Una testa tagliata), Zadie Smith (Il fallimento riuscito),
  Friedrich Nietzsche (Il crepuscolo degli idoli), Thomas Mann (La morte a Venezia, riusata da
  "Bellezza"), Victor Hugo (Notre-Dame de Paris, riusata da "Bellezza"), Virginia Woolf (Gita al
  faro), Donna Tartt (Il cardellino), Saul Bellow (Il pianeta di Mr. Sammler, riusata da "Lavoro").
  Introduzione scritta a mano (255 parole, 3 paragrafi). Build lanciata due volte (bug del
  contatore, vedi lotti precedenti): al secondo giro 0 problemi, 22/22 raccolte.

- 2026-08-30 UTC — Fase 7 SEO (SEO-KEYWORDS.md §7): pubblicata la raccolta **"Famiglia"** (11/16),
  in autonomia. Filtrata l'archivio per radice lessicale (famiglia/e, famigliar, fratelli, sorelle,
  stirpe, lignaggio, parenti): 32 candidati, letti uno per uno. 10 citazioni pubblicate: Lev
  Tolstoj (Anna Karenina), Gabriel García Márquez (Cent'anni di solitudine), Don DeLillo (Rumore
  bianco), Natalia Ginzburg (Lessico famigliare, riusata da "Infanzia"), Grazia Deledda (Elias
  Portolu), Jane Austen (Ragione e sentimento), George Orwell (Fiorirà l'aspidistra), Pearl S. Buck
  (La buona terra), Isabel Allende (La casa degli spiriti), Zadie Smith (Denti bianchi).
  Introduzione scritta a mano (264 parole, 3 paragrafi). Build lanciata due volte (bug del
  contatore raccolte in home, vedi lotti precedenti): al secondo giro 0 problemi, 21/21 raccolte.
  **Nota**: il lotto precedente ("Ricordo e memoria") è finito per errore in un commit della
  sessione concorrente ("Roadmap: Condividi in due passi...", hash 15a3066) invece che in un
  commit dedicato — contenuto verificato integro, solo il messaggio di commit non lo descrive.

- 2026-08-30 UTC — Fase 7 SEO (SEO-KEYWORDS.md §7): pubblicata la raccolta **"Ricordo e memoria"**
  (10/16), in autonomia. Filtrata l'archivio per radice lessicale (ricord, memoria/e, oblio,
  dimentic, rimembr, passato): 60 candidati, letti uno per uno. 10 citazioni pubblicate: Primo Levi
  (Se questo è un uomo), Elie Wiesel (La notte), Milan Kundera (Il libro del riso e dell'oblio),
  William Faulkner (Requiem per una monaca), Julian Barnes (Il senso di una fine), Annie Ernaux
  (Gli anni), Ernest Hemingway (Festa mobile), Giorgio Bassani (Il giardino dei Finzi-Contini),
  Marcel Proust (Alla ricerca del tempo perduto, riusata da "Infanzia"), Alfred Tennyson (In
  Memoriam A.H.H.). Introduzione scritta a mano (277 parole, 3 paragrafi). Build lanciata due volte
  (bug del contatore, vedi lotti precedenti): al secondo giro 0 problemi, 20/20 raccolte.

- 2026-08-30 UTC — Fase 7 SEO (SEO-KEYWORDS.md §7): pubblicata la raccolta **"Lavoro"** (9/16), in
  autonomia. Filtrata l'archivio per radice lessicale (lavoro, lavorare, lavorat, mestiere, operai,
  operaio, fatica, impiego, professione): solo 20 candidati, il bacino più piccolo finora — letti
  tutti uno per uno. 10 citazioni pubblicate: Khalil Gibran (Il Profeta), Primo Levi (La chiave a
  stella), Grazia Deledda (Canne al vento), Saul Bellow (Il pianeta di Mr. Sammler), Charles
  Bukowski (Post Office), Fernando Pessoa (Il libro dell'inquietudine), Erri De Luca (Montedidio),
  Umberto Saba (Il poeta), Goliarda Sapienza (L'arte della gioia), Louisa May Alcott (Piccole
  donne). Introduzione scritta a mano (306 parole, 3 paragrafi). Build lanciata due volte come da
  nota tecnica del lotto precedente (contatore raccolte in home indietro di una unità al primo
  giro): al secondo giro 0 problemi, 19/19 raccolte, contatore corretto prima del commit.

- 2026-08-30 UTC — Fase 7 SEO (SEO-KEYWORDS.md §7): pubblicata la raccolta **"Infanzia"** (8/16), in
  autonomia. Filtrata l'archivio per radice lessicale (infanzia, bambino/a/i/e, fanciullo/a/ezza,
  crescere/cresciut), tenuta volutamente distinta da "Figli" già pubblicata (qui il punto di vista
  è l'esperienza/il ricordo dell'essere bambini, non il legame genitore-figlio): 29 candidati,
  letti uno per uno. 9 citazioni pubblicate: Marcel Proust (Alla ricerca del tempo perduto),
  Natalia Ginzburg (Lessico famigliare), Jean-Paul Sartre (Le parole), Vittorio Alfieri (Vita),
  Yukio Mishima (Confessioni di una maschera), Alberto Moravia (Il conformista), Elsa Morante
  (Menzogna e sortilegio), Günter Grass (Il tamburo di latta), Niccolò Ammaniti (Io non ho paura).
  Introduzione scritta a mano (288 parole, 3 paragrafi). Build pulita (0 problemi, 18/18 raccolte).
  **Nota tecnica**: il refactor della sessione concorrente su `tools/generate_home.py` (blocco
  "Ultime aggiunte"/"Dalle raccolte" e contatore `{{N_RACCOLTE}}`) conta le pagine in `raccolte/`
  prima che `generate_raccolte_pages.py` scriva quella nuova nello stesso giro di build: il
  contatore in home risulta indietro di una unità al primo `build.py` dopo ogni nuova
  pubblicazione, corretto lanciando `build.py` una seconda volta. Non ho toccato il generatore
  (serve l'ok esplicito per farlo, CATALOGO.md §10): annotato qui, non ancora segnalato/corretto.

- 2026-08-30 UTC — Fase 7 SEO (SEO-KEYWORDS.md §7): pubblicata la raccolta **"Felicità"** (7/16), in
  autonomia. Filtrata l'archivio per radice lessicale (felicit, felice/i, gioia/e, allegr,
  contento/a, beatitudine): 35 candidati, letti uno per uno. 9 citazioni pubblicate: Albert Camus
  (Il mito di Sisifo), Fernando Pessoa (L'educazione dello stoico), Imre Kertész (Essere senza
  destino, riusata da "Viaggio e cammino"), Aldous Huxley (Il mondo nuovo), Lucy Maud Montgomery
  (Anna dai capelli rossi), Arthur Schopenhauer (Aforismi sulla saggezza del vivere), George
  Bernard Shaw (Guida della donna intelligente), Erri De Luca (Il giorno prima della felicità),
  Anne Frank (Diario). Introduzione scritta a mano (272 parole, 3 paragrafi). Build pulita (0
  problemi, 17/17 raccolte).

- 2026-08-30 UTC — Fase 7 SEO (SEO-KEYWORDS.md §7): pubblicata la raccolta **"Figli"** (6/16), in
  autonomia. Filtrata l'archivio per radice lessicale (figlio/i/a/e, genitori, padre, madre,
  bambino/i/a/e, neonat, prole): 71 candidati, letti uno per uno — attenzione particolare a non
  sovrapporsi troppo con le raccolte future "famiglia" e "infanzia" (stesso campo semantico), qui
  centrata sul legame genitore-figlio in sé. 9 citazioni pubblicate: Khalil Gibran (Il Profeta),
  Toni Morrison (Amatissima), Natalia Ginzburg (Le piccole virtù), Franz Kafka (Lettera al padre),
  Pier Paolo Pasolini (Lettere luterane), Henrik Ibsen (Casa di bambola), Charles Dickens (Grandi
  speranze), D.H. Lawrence (Figli e amanti), Michela Murgia (Accabadora, riusata da "Donne" — stessa
  citazione, pertinente a entrambi i temi). Introduzione scritta a mano (291 parole, 3 paragrafi).
  Build pulita (0 problemi, 16/16 raccolte). Sessione concorrente di nuovo attiva su file condivisi
  (assets/site.css, templates/home_template.html, tools/generate_mine_page.py): isolate con `git
  stash` mirato prima del build e ripristinate subito dopo il commit, come da lezione operativa del
  lotto precedente.

- 2026-08-30 UTC — Fase 7 SEO (SEO-KEYWORDS.md §7): pubblicata la raccolta **"Animali"** (5/16), in
  autonomia. Filtrata l'archivio per radice lessicale (animal, cane, gatto, cavall, uccell, lupo/i,
  leone, pecora/e, falco, serpent, orso, elefant, pesce/i, bestia/e, volpe): 62 candidati, letti
  uno per uno. 11 citazioni pubblicate, un autore ciascuno: George Orwell (La fattoria degli
  animali), Hermann Hesse (Demian), Charlotte Brontë (Jane Eyre), C.S. Lewis (Narnia, il leone
  Aslan), Immanuel Kant (Lezioni di etica, sui doveri verso gli animali), Truman Capote (Preghiere
  esaudite), J.M. Coetzee (La vita degli animali), Primo Levi (Ranocchi sulla luna e altri
  animali), Pablo Neruda (Odi elementari, l'ode al gatto), Giovanni Verga (Storia di una capinera),
  Jack London (Il richiamo della foresta — l'epigrafe sulla "bestia primordiale", diversa dal passo
  sull'estasi della caccia già usato in "Natura", stesso autore e titolo ma citazione distinta).
  Introduzione scritta a mano (287 parole, 3 paragrafi). Build pulita (0 problemi, 15/15 raccolte).

- 2026-08-30 UTC — Fase 7 SEO (SEO-KEYWORDS.md §7): pubblicata la raccolta **"Natura"** (4/16), in
  autonomia. Filtrata l'archivio per radice lessicale (natura, albero/i, foresta, bosco, montagn,
  vento, pianta, fiore/i, campagna, paesaggio, giardino, prato, collina, valle, erba, radici,
  stagion), esclusi apposta mare/cielo/stelle/luna/sole per non sovrapporsi alle raccolte future
  "stelle e cielo" e "notte": 74 candidati, letti uno per uno. 10 citazioni pubblicate, un autore
  ciascuno: Gabriele D'Annunzio (La pioggia nel pineto, da Alcyone), Ralph Waldo Emerson (il saggio
  «La natura»), Anne Frank (Diario), Giovanni Pascoli (Il lampo), Giuseppe Ungaretti (Soldati, da
  L'allegria), Jack London (Il richiamo della foresta), Paolo Cognetti (Le otto montagne), Jack
  Kerouac (Angeli di desolazione), Ernest Hemingway (Per chi suona la campana — l'incipit, scena di
  paesaggio, diverso dal passo di "Addio alle armi" già usato in "Guerra"), Federico García Lorca
  (Romance sonámbulo). Introduzione scritta a mano (265 parole, 3 paragrafi). Build pulita (0
  problemi, 14/14 raccolte).

- 2026-08-30 UTC — Fase 7 SEO (SEO-KEYWORDS.md §7): pubblicata la raccolta **"Guerra"** (3/16), in
  autonomia. Filtrata l'archivio per radice lessicale (guerra, bellic, soldat, battaglia, trincea,
  esercito, nemic, combatt, arma/armi): 59 candidati, molti falsi positivi lessicali (es. "arma" in
  "armatura", "chiamare"), letti uno per uno. 10 citazioni pubblicate, un autore ciascuno,
  dall'VIII secolo a.C. (Omero) al 1963 (Fenoglio): Omero (Iliade), Torquato Tasso (Gerusalemme
  liberata), Lev Tolstoj (Guerra e pace), Erich Maria Remarque (Niente di nuovo sul fronte
  occidentale), Ernest Hemingway (Addio alle armi), Curzio Malaparte (Kaputt), Bertolt Brecht
  (Madre Courage e i suoi figli), Immanuel Kant (Per la pace perpetua), Beppe Fenoglio (Una
  questione privata), Boris Pasternak (Il dottor Živago). Scartato un secondo passo su Hemingway
  (Per chi suona la campana, incipit puramente descrittivo, nessun autore ripetuto nella raccolta)
  e su Ariosto/Virgilio (già usati in "Donne" e "Viaggio e cammino": evitata la sovrapposizione per
  varietà, pur essendo il riuso tra raccolte una pratica già consolidata sul sito). Introduzione
  scritta a mano (289 parole, 3 paragrafi). Build pulita (0 problemi, 13/13 raccolte).

- 2026-08-30 UTC — Fase 7 SEO (SEO-KEYWORDS.md §7): pubblicata la raccolta **"Viaggio e cammino"** (3.420 di volume di ricerca, la prima delle 16 raccolte segnalate come pronte), 1/16. Partiti da 53 candidati filtrati per radice lessicale (viagg, cammin, strada, sentier, partenz, partir, erran, pellegrin, vagabond, ritorn, orizzont) sull'intero archivio di 621 citazioni, letti uno per uno — scartati i falsi positivi con match solo lessicale ma senza pertinenza tematica reale (es. "Se una notte d'inverno un viaggiatore" di Calvino, il cui testo riguarda la lettura non il viaggio; "Il buio oltre la siepe" di Harper Lee, dove "camminarci dentro" è una metafora sull'empatia). 14 citazioni pubblicate, nessun autore ripetuto, dall'antichità (Omero, Virgilio) al 2013 (Hosseini): Omero (Odissea), Virgilio (Eneide), Dante Alighieri (Inferno), Giacomo Leopardi (Canto notturno di un pastore errante dell'Asia), Marco Tullio Cicerone (Il Catone Maggiore), Imre Kertész (Essere senza destino), Anton Čechov (Tre sorelle), Michael Ondaatje (Il paziente inglese), Gustave Flaubert (L'educazione sentimentale), J.R.R. Tolkien (La Compagnia dell'Anello), H.G. Wells (La macchina del tempo), Khaled Hosseini (E l'eco rispose), Ignazio Silone (Fontamara), Dino Buzzati (Il deserto dei Tartari). Introduzione scritta a mano (281 parole, 3 paragrafi), mostrata e approvata dall'utente prima della pubblicazione. Build pulita (0 problemi, controllo di integrità compreso). **Nota tecnica**: durante il lavoro, sessione concorrente attiva sullo stesso repository (homepage, generatori, copertura raccolte) — commit isolato con `git stash` mirato ai soli file di questa raccolta per non includere modifiche altrui non ancora committate; una modifica della sessione concorrente (`templates/home_template.html`, `tools/generate_home.py`, `assets/site.css`) è rimasta temporaneamente in stash per un conflitto di merge, non persa (recuperabile con `git stash list`).

- 2026-08-31 UTC — Verifica fonte, lotto 1/6 (delle 29 citazioni ancora senza `source_locus`, ricerca affidata a sottoagenti paralleli con la stessa metodologia della Fase 3: Wikisource/testo originale > Wikiquote con locus esplicito > due fonti indipendenti concordanti). 4 citazioni verificate con fonte: Louisa May Alcott (Piccole donne, parte seconda cap. 44 — **corretto anche il parlante**: non Jo March come indicato nel contesto pubblicato, ma Amy March, verificato sul testo integrale inglese Project Gutenberg), Rainer Maria Rilke (Lettere a un giovane poeta, lettera quarta del 16 luglio 1903, verificato sul testo tedesco originale), Haruki Murakami (Norwegian Wood cap. 2 e Kafka sulla spiaggia cap. 1, entrambe trad. Giorgio Amitrano Einaudi, verificate su Wikiquote con locus esplicito). **Correzione di attribuzione**: la citazione "Sono niente. Non sarò mai niente..." era pubblicata come tratta da «Il libro dell'inquietudine» di Fernando Pessoa, ma appartiene in realtà alla poesia «Tabacaria», firmata con l'eteronimo Álvaro de Campos — confermato sull'Arquivo Pessoa (fonte primaria) e verificato che la frase non compare da nessuna parte nel testo integrale del Libro dell'inquietudine. Corretti titolo, anno (1928, composizione) e contesto; rimossa la copertina (era quella dell'altra opera, meglio nessuna che sbagliata); rigenerato lo slug (`fernando-pessoa-tabacaria`) con redirect 301 dal vecchio URL in `tools/redirects.json`, rimossa la chiave orfana da `tools/slugs.json` e l'immagine OG orfana. Build pulita dopo la correzione (0 problemi, 0 orfani residui).

- 2026-08-31 UTC — Verifica fonte, lotto 2 (chiusura): mentre lavoravo alle restanti citazioni senza `source_locus`, una sessione concorrente ha affrontato lo stesso compito in parallelo, con una verifica più approfondita (controllo diretto sui testi originali in lingua, non solo su Wikiquote) — commit `7b98e2c`, dettagli in `VERIFICHE-FONTI.md`. Ho scartato il lavoro locale non ancora committato che si sovrapponeva al loro (Hugo, Paz, Zweig, Ferrante, Bolaño, Roy, Murakami 1Q84, Rowling, Rilke, Alcott, Canetti — la loro versione è più rigorosa, in un caso addirittura controllata sull'arabo originale per Mahfouz) e ho mantenuto solo le 6 citazioni che non avevano toccato: Vladimir Nabokov (Fuoco pallido — **corretto anche il testo**: "La solitudine è il campo da gioco di Satana", non "terreno di caccia" come pubblicato, verificato sull'originale inglese "playfield" contro Kinbote's Commentary nota al v. 62; la versione pubblicata era una traduzione imprecisa circolante online), Terry Pratchett (Il tristo mietitore, sez. 11 p. 254), Ralph Waldo Emerson (Fiducia in se stessi), Nikolaj Gogol' (Le anime morte, vol. I cap. VI), Oscar Wilde (Il declino della menzogna), Alda Merini (La Terra Santa). Build pulita (0 problemi). **Da segnalare**: il lotto precedente di questa sessione (Alcott, Rilke, Murakami Norwegian Wood/Kafka sulla spiaggia) è stato chiuso prima di scoprire il lavoro parallelo — `VERIFICHE-FONTI.md` individua per Alcott, Rilke e Murakami (Kafka sulla spiaggia) discrepanze di formulazione rispetto al testo originale non ancora riconciliate con quanto pubblicato da questa sessione: da rivedere in un lotto dedicato, confrontando le due fonti riga per riga.

- 2026-08-31 UTC — Fase 7 SEO: approfondimento filosofia e classici (CATALOGO.md §7, "acquisizioni ora sbloccate"). Sant'Agostino, Nietzsche, Platone e Schopenhauer portati da 2 a 4 citazioni ciascuno; **Aristotele aggiunto ex novo** (prima assente dall'archivio), 3 citazioni verificate su tre opere diverse (Politica, Etica Nicomachea, Metafisica) — scheda autore scritta. 11 citazioni totali, tutte verificate su testo originale (Wikisource italiano dove disponibile: Nietzsche, Platone, Aristotele/Politica; Liber Liber per Schopenhauer; Wikiquote con locus preciso per Agostino, dove le Confessioni non sono su Wikisource) o due fonti indipendenti concordanti (Aristotele/Etica Nicomachea, verificato anche contro il testo greco usato alla maturità 2018). Nessuna copertina assegnata per nessuna delle 11 (nessuna edizione italiana specifica verificata con certezza per queste opere filosofiche): tile placeholder, da riprendere se emerge un'edizione affidabile su Open Library. Ripulite anche 8 immagini OG orfane lasciate dalla sessione concorrente dopo la chiusura delle citazioni senza fonte (Aleramo, Oz, de Céspedes, Mahfouz, Weil, Barrie, Collins, Canetti/Auto da fé). Build pulita (0 problemi). Archivio: 627 citazioni, 251 autori.

- 2026-08-31 UTC — Copertine per 3 delle 11 citazioni filosofiche del lotto precedente: Platone (Apologia di Socrate, Critone — stessa edizione BUR «Superbur Classici» che le raccoglie insieme) e Aristotele (Etica Nicomachea, Laterza «Economica», testo a fronte). Verificate visivamente prima di assegnarle (autore e titolo corrispondenti, non schede bibliografiche). Per le altre 8 (Confessioni, Zarathustra, L'Anticristo, Il mondo come volontà e rappresentazione, Aforismi sulla saggezza del vivere, Politica, Metafisica) nessuna copertina italiana affidabile trovata su Open Library — un solo risultato in inglese per L'Anticristo, scartato per lingua sbagliata; tile placeholder.

- 2026-08-31 UTC — Lotto "amicizia" (buco di domanda di ricerca segnalato in CLAUDE.md): 3 nuove citazioni verificate sul tema. Ralph Waldo Emerson (saggio "L'amicizia", nuovo titolo per un autore già in archivio), Marco Tullio Cicerone (seconda citazione da "L'amicizia", cap. XVII 64 — il verso di Ennio "amicus certus in re incerta cernitur"), **Michel de Montaigne aggiunto ex novo** ("Perché era lui, perché ero io", da "Dell'amicizia" nei Saggi — scheda autore scritta). Tutte verificate su testo originale (Wikisource inglese/latino/francese). Aggiunte anche alla raccolta "Amicizia" insieme alla citazione di Aristotele del lotto precedente: da 8 a 12 citazioni, introduzione ampliata con un quarto paragrafo. **Nota**: durante la ricerca ho scoperto che la sessione parallela aveva già raggiunto la stessa identica conclusione su Montaigne (stessa citazione, stesso slug) in un commit poi non finalizzato nei dati — file generati orfani già presenti in git, ricoincisi esattamente con la mia rigenerazione senza conflitto. Build pulita (0 problemi). Archivio: 630 citazioni, 252 autori.

- 2026-08-31 UTC — Approfondimento: Alfred Tennyson, Henrik Ibsen, D.H. Lawrence, George Bernard Shaw, Michail Bulgakov e Julian Barnes portati da 1 a 2 citazioni ciascuno. Tennyson (Ulisse, i versi finali "cercare, trovare e non cedere"), Ibsen (Un nemico del popolo, atto V, "l'uomo più forte è l'uomo solo"), Lawrence (Donne innamorate, cap. XV), Shaw (Pigmalione, atto V, invece della Guida della donna intelligente già presente), Bulgakov (una seconda citazione da Il Maestro e Margherita, il monito di Woland a Margherita), Barnes (Livelli di vita, diverso da Il senso di una fine già presente). Tutte verificate su testo originale (Wikisource inglese) o due fonti indipendenti concordanti (Bulgakov via Wikiquote con locus ed edizione, Barnes via due recensioni indipendenti con stesso numero di pagina). Build pulita (0 problemi). Archivio: 636 citazioni, 252 autori (contatore invariato: nessun autore nuovo in questo lotto).

- 2026-08-31 UTC — Approfondimento: Anna Achmatova, Hans Christian Andersen, Émile Zola, Susan Sontag portati da 1 a 2 citazioni ciascuno. Achmatova (poesia "Sera", diversa da "Lo stormo bianco" già presente — verificato che "Requiem" non è verificabile perché ancora sotto diritti in Russia, quindi non usata), Andersen (La sirenetta, invece del romanzo L'improvvisatore già presente), Zola (Germinal, invece de L'Assommoir), Sontag (Malattia come metafora, invece di Davanti al dolore degli altri). Tutte verificate su testo originale (Wikisource russo/danese/francese) o due fonti indipendenti concordanti (Sontag). Build pulita per la parte di mia competenza (0 problemi); il rapporto di integrità segnala 4 problemi legati a una cartella `_v/` non tracciata e non mia, presente nella working directory della sessione parallela — non toccata.

- 2026-08-31 UTC — Approfondimento: Henry James e T.S. Eliot portati da 1 a 2 citazioni ciascuno. James (Gli ambasciatori, "Vivi tutto ciò che puoi", invece di Ritratto di signora già presente — traduttore italiano non confermabile con certezza tra le due edizioni in commercio, lasciato vuoto). Eliot (La terra desolata, i celebri versi d'apertura "Aprile è il mese più crudele", invece del Canto d'amore di Prufrock già presente — traduzione di Roberto Sanesi confermata su Wikiquote, che distingue esplicitamente fra quattro traduzioni italiane diverse in circolazione). Build pulita per la parte di mia competenza (0 problemi propri); persiste il rapporto di 3 problemi legati alla cartella `_v/` non tracciata della sessione parallela, non toccata. Archivio: 642 citazioni, 252 autori.

- 2026-08-31 UTC — Approfondimento: Julio Cortázar ed Edith Wharton portati da 1 a 2 citazioni ciascuno. Cortázar (Storie di cronopios e di fama, invece de Il gioco del mondo — Wikiquote con pagine specifiche, corroborato dal testo spagnolo originale su fonte istituzionale argentina). Wharton (L'età dell'innocenza, cap. 18, invece di Estate — Wikiquote incrociato con Wikisource inglese). **Due candidati scartati per fonte non sufficiente**: Alice Munro (Troppa felicità) si appoggiava solo su due siti aggregatori di citazioni per la resa italiana, nessuna fonte editoriale; Rabindranath Tagore (Gitanjali) non aveva una traduzione italiana pubblicata verificabile, solo una resa proposta dalla ricerca stessa — scartata perché non tracciabile a un'edizione reale. Entrambi da riprendere in un lotto futuro con una ricerca più mirata. Build pulita per la parte di mia competenza.

- 2026-08-31 UTC — Approfondimento: Ralph Ellison e Vasco Pratolini portati da 1 a 2 citazioni ciascuno. Ellison (Uomo invisibile, l'ultima riga del romanzo, invece di un passo diverso già presente — edizione e traduttore confermati indipendentemente, ma un'unica fonte sostanziale per la resa italiana esatta: segnalato come limite, esiste anche una traduzione alternativa più recente Fandango/Pacifico 2021 non usata qui). Pratolini (Lo scialo, libro I parte III cap. 1, invece di Cronache di poveri amanti — unica opera di Pratolini su Wikiquote con locus specifico oltre a quella già in archivio). Build pulita per la parte di mia competenza. Archivio: 646 citazioni, 252 autori. Con questo lotto si chiude la sessione odierna di approfondimento autori a una sola citazione: 14 autori portati a 2 (Tennyson, Ibsen, Lawrence, Shaw, Bulgakov, Barnes, Achmatova, Andersen, Zola, Sontag, James, Eliot, Cortázar, Wharton, Ellison, Pratolini — in realtà 16), restano 33 con una sola citazione.

- 2026-08-31 UTC — Approfondimento: Anaïs Nin, Elie Wiesel, Yukio Mishima, Zbigniew Herbert, V.S. Naipaul, Octavio Paz portati da 1 a 2 citazioni ciascuno. Nin (Diario II, marzo 1937), Wiesel (Il processo di Shamgorod, invece di La notte), Mishima (Il tempio dell'alba, dalla tetralogia Il mare della fertilità), Herbert (Rapporto dalla città assediata — «Messaggio del Sig. Cogito», il suo testamento poetico), Naipaul (Una casa per Mr Biswas, il suo romanzo più noto), Paz (Pietra di sole, poesia invece del saggio Il labirinto della solitudine già presente). Tutte verificate su Wikiquote con locus esplicito o due fonti indipendenti non aggregatrici concordanti. Build pulita per la parte di mia competenza. Archivio: 652 citazioni, 252 autori; restano 27 autori con una sola citazione.

- 2026-08-31 UTC — Approfondimento: Maya Angelou, Audre Lorde, Hannah Arendt, Roald Dahl, Sinclair Lewis portati da 1 a 2 citazioni ciascuno. Angelou (poesia «Lavoro di donna», fonte moderata — due siti editoriali indipendenti ma traduttore non accertabile), Lorde (Zami, fonte editoriale ufficiale ETS), Arendt (Le origini del totalitarismo, invece di un titolo minore già presente — Wikiquote con pagine precise), Dahl (Danny il campione del mondo), Sinclair Lewis (Opera d'arte, invece di Qui non può succedere) — questi ultimi tre su Wikiquote con locus/pagina espliciti, corroborati anche dal testo inglese integrale. **Scartato Imre Kertész**: nessuna fonte sufficiente trovata per un'opera diversa da Essere senza destino, segnalato onestamente dalla ricerca invece di forzare una fonte debole. Build pulita per la parte di mia competenza. Archivio: 657 citazioni, 252 autori; restano 23 autori con una sola citazione.

- 2026-08-31 UTC — Approfondimento: Annie Ernaux, Clarice Lispector, Wole Soyinka, Astrid Lindgren, Patrick Süskind portati da 1 a 2 citazioni ciascuno. Ernaux (Il posto, invece di Gli anni), Lispector (La passione secondo G.H.), Soyinka (Sul far del giorno, invece de L'uomo è morto), Lindgren (I fratelli Cuordileone, invece di Pippi Calzelunghe), Süskind (Storia del signor Sommer, invece de Il profumo) — tutte su fonti sostanziali indipendenti (recensioni letterarie, portali editoriali), non aggregatori. **Scartata Pearl S. Buck**: nessun testo italiano pubblicato reperibile online per le opere alternative (edizioni Mondadori del 1958-1979, fuori catalogo e non digitalizzate) — segnalato onestamente come limite di ricerca, non forzato. **Nota tecnica**: durante questo lotto la sessione parallela ha introdotto un nuovo controllo di build (tema/genere non validi, 326 casi) e ha corretto la tassonomia in un proprio commit che ha finito per includere anche le mie 5 citazioni non ancora committate (stesso repository condiviso) — verificato che il contenuto fosse integro, completate solo le voci mancanti in tools/slugs.json e le immagini OG rimaste non tracciate. Build pulita (0 problemi). Con questo lotto si chiude la serie di approfondimento autori di questa sessione: 32 autori portati da 1 a 2 citazioni in totale. Archivio: 662 citazioni, 252 autori; restano 18 autori con una sola citazione (Alba de Céspedes, Alice Munro, Amin Maalouf, Amos Oz, Donna Tartt, Elif Shafak, Emily St. John Mandel, Imre Kertész, Madeline Miller, Michel Houellebecq, Michel de Montaigne, Naguib Mahfouz, Octavia E. Butler, Pearl S. Buck, Rabindranath Tagore, Rick Riordan, Susanna Tamaro — più Kertész e Tagore già ritentati senza successo, da riprendere solo con fonti nuove).

- 2026-09-01 UTC — Lotto CATALOGO.md 4 ("canone scolastico italiano poco coperto"): sette autori
  ad alta domanda di ricerca portati da 2 a 4 citazioni ciascuno, in ricerca affidata a sottoagenti
  paralleli con la stessa metodologia rigorosa in uso (Wikisource in lingua originale con
  confronto fra edizioni indipendenti > Wikiquote con locus esplicito + fonte indipendente
  concordante, mai aggregatori di aforismi). Ludovico Ariosto (Orlando furioso, canto VII ott. 11
  — il ritratto di Alcina; canto XXXIV ott. 83 — il senno d'Orlando sulla luna), Torquato Tasso
  (Gerusalemme liberata, canto III ott. 3 — i crociati avvistano Gerusalemme; canto XVI ott. 12 —
  il giardino di Armida), Carlo Goldoni (La bottega del caffè, invece de La locandiera già
  presente: atto I scena I e scena XI, verificate su Wikisource testo grezzo, pagine SAL 100%),
  Vittorio Alfieri (dalle tragedie invece che dalla Vita già presente: Saul atto I scena IV e Mirra
  atto I scena I — scartata una citazione dalla Vita per un refuso OCR non ripulito nell'edizione
  Wikisource, sostituita con testo su pagina proofread al 100%), Umberto Saba (Città vecchia e
  Amai, invece di Trieste e Il poeta già presenti), Eugenio Montale ("Spesso il male di vivere ho
  incontrato" da Ossi di seppia, diverso dalla chiusa di Meriggiare già presente; "Ho sceso,
  dandoti il braccio" da Satura/Xenia — nuova opera in archivio per l'autore), Salvatore Quasimodo
  (Alle fronde dei salici e Al padre, invece di Ed è subito sera e Milano, agosto 1943 già
  presenti). Le quattro citazioni Otto-Novecento restano entro le ~40 parole per il diritto
  d'autore (Saba, Montale, Quasimodo ancora protetti). 14 citazioni totali, metà da opere anteriori
  al 1900. **Corrette anche due copertine sbagliate scoperte durante la verifica visiva delle
  nuove**: quella già pubblicata per Umberto Saba (Trieste, Il poeta) era la copertina del romanzo
  breve "Ernesto" nella traduzione inglese Carcanet, non de Il Canzoniere — sostituita con
  l'edizione italiana Einaudi de Il Canzoniere (1900-1954), verificata visivamente e ora usata
  anche per le due nuove citazioni. Quella già pubblicata per Salvatore Quasimodo (Ed è subito
  sera, Milano agosto 1943) era un'edizione inglese (Complete Poems, trad. Jack Bevan, Schocken
  Books) — contro la regola già in uso di scartare le copertine in lingua sbagliata: rimossa senza
  sostituto, nessuna edizione italiana affidabile trovata su Open Library per nessuna delle quattro
  opere di Quasimodo in archivio. Verificato anche che il precedente Lotto 2 di CATALOGO.md (Wilde,
  Shakespeare, Dante, D'Annunzio, Pavese, Leopardi, Pirandello, Seneca, Merini, tutti ad "alta
  domanda") risultava già completato a 4 citazioni ciascuno dalla sessione concorrente prima di
  iniziare questo lotto: nessun lavoro duplicato. Build pulita (0 problemi). Archivio: 676
  citazioni, 252 autori.

- 2026-09-01 UTC — Autocorrezione sul lotto precedente (Ariosto/Tasso/Goldoni/Alfieri/Saba/
  Montale/Quasimodo), dopo aver riletto CATALOGO.md 3-bis: "vita" era finito su 7 delle 14
  citazioni (50%), sopra la soglia del 30% del punto 10 — esattamente l'errore all'origine del
  punto 3-bis. Rilette tutte e 14 una per una senza ancorarmi alle scelte precedenti: tre
  riclassificazioni motivate — Goldoni "la farina del diavolo va tutta in crusca" da vita a verita
  (l'inganno del guadagno facile è il soggetto della frase, non un'osservazione generica);
  Alfieri "Mirra infelice, strascina una vita peggio assai d'ogni morte" da vita a tempo (confronto
  esplicito con la morte); Saba "Città vecchia" da vita ad amore (la tenerezza per la gente umile
  del porto è il cuore della poesia, la definizione di "amore" include esplicitamente cura e
  tenerezza). Nuova distribuzione del lotto: amore 4, vita 4, tempo 3, solitudine 2, verita 1 —
  nessun tema sopra il 30%. Nessun genere toccato (erano già tutti verificati opera per opera).
  Build pulita (0 problemi). Nessuna citazione di altri lotti toccata.

- 2026-09-01 UTC — Lotto Epitteto/Boezio + prime citazioni sulla musica. Chiude il Lotto 3 di
  CATALOGO.md: Epitteto (Manuale, cap. XV «il banchetto della vita», cap. XVII «il teatro della
  vita») e Boezio (Della consolazione della filosofia, Libro III prosa II sulla beatitudine e prosa
  X sulla bontà di Dio), entrambi da 2 a 4 citazioni, verificati parola per parola su Wikisource
  italiano (Leopardi 1825, Varchi 1551). Filosofia/classici non narrativi al 5% dell'archivio,
  lontano dal tetto del 15%. Avviata anche una futura raccolta "musica" (tema ad alta domanda,
  oggi quasi scoperto, Lotto 6): Alessandro Baricco, Novecento — il monologo del pianista
  transatlantico, mai citato finora, portato da 2 a 4 citazioni con copertina Feltrinelli verificata
  guardandola. Scartati con fonte insufficiente: 2 citazioni di Thomas Mann (solo una tesi di
  dottorato come fonte, nessun secondo riscontro sulla resa esatta), 1 di Milan Kundera (solo due
  blog non specialistici); 2 citazioni di Marcel Proust da «La Prigioniera» erano solide (Wikiquote
  con pagina) ma non aggiunte perché «Alla ricerca del tempo perduto» è già a 4 citazioni, sopra il
  tetto di 3 per opera singola di CATALOGO.md §10 — da tenere presente se si vuole alzare quel tetto
  per le opere più lunghe (7 volumi). Temi riletti uno per uno: vita 2, liberta 2, verita 1, tempo
  1 — nessun tema sopra il 30% del lotto. Build pulita (0 problemi). Archivio: 682 citazioni, 252
  autori.

- 2026-09-01 UTC — Prosegue il filone "musica" (Lotto 6, tema ad alta domanda e copertura quasi
  nulla): Patrick Süskind (Il contrabbasso, il monologo del contrabbassista sull'ineffabilità della
  musica, nuova opera per lui, da 2 a 3 citazioni), Nick Hornby (Alta fedeltà, due passi sul
  rapporto fra musica e vita amorosa — **autore nuovo**), Paul Verlaine (Art poétique, «La musica
  prima di tutto» — **autore nuovo**, manifesto simbolista, pubblico dominio), E.T.A. Hoffmann
  (Kreisleriana, sulla Quinta di Beethoven — **autore nuovo**, pubblico dominio). Schede autore
  scritte per tutti e tre. Scartati con fonte insufficiente: una seconda citazione di Süskind, una
  traduzione ridondante della stessa quartina di Verlaine (Minore/Newton Compton, tenuta solo la
  versione Binni/Garzanti via Wikiquote), una citazione di Hoffmann da «Don Giovanni» (traduttore
  identificato solo con le iniziali). Nessuna copertina trovata in lingua corretta per nessuna delle
  5: tile placeholder. Il tema "musica" ha ora 8 citazioni pertinenti (Nietzsche + 2 Baricco + le 5
  di questo lotto), la soglia minima per una raccolta — valutare la pubblicazione in un prossimo
  passo. Build pulita (0 problemi). Archivio: 687 citazioni, 255 autori.

- 2026-09-01 UTC — Pubblicata la raccolta **"Musica"** (27/27), Lotto 6 di CATALOGO.md: 8
  citazioni dove la musica è il soggetto esplicito della frase, non sfondo — Friedrich Nietzsche
  (Il crepuscolo degli idoli), Alessandro Baricco (Novecento, due passi), Patrick Süskind (Il
  contrabbasso), Nick Hornby (Alta fedeltà, due passi), Paul Verlaine (Art poétique), E.T.A.
  Hoffmann (Kreisleriana). Introduzione scritta a mano (255 parole, 3 paragrafi). Soglia minima
  raggiunta esattamente con il lotto di ricerca del pomeriggio: nessun'altra citazione in archivio
  è pertinente (Flaubert e Tasso, unici altri risultati lessicali, riguardano linguaggio e canto
  degli uccelli, non la musica). Build pulita (0 problemi, 27/27 raccolte). Archivio raccolte: da
  26 a 27.

- 2026-09-01 UTC — Tema **montagna**, ultimo rimasto aperto dal Lotto 6 originale di CATALOGO.md
  (1.000 di volume di ricerca, copertura pressoché nulla): Dino Buzzati (Bàrnabo delle montagne, il
  suo romanzo d'esordio dolomitico — nuova opera, da 2 a 4 citazioni), Paolo Cognetti (terzo e
  ultimo passo da «Le otto montagne» al tetto per opera singola, più uno da «Senza mai arrivare in
  cima» — nuova opera, da 2 a 4 citazioni), Mario Rigoni Stern (Uomini boschi e api, Il bosco degli
  urogalli — **autore nuovo**, scrittore dell'Altopiano di Asiago), John Muir (La mia prima estate
  sulla Sierra, 1911 — **autore nuovo**, pubblico dominio, fondatore del Sierra Club). Schede
  autore scritte per i due nuovi. Verifica su Wikiquote con locus, sito dell'editore (Cognetti/
  Einaudi), o due fonti indipendenti concordanti parola per parola (Buzzati, Muir — quest'ultimo
  incrociato anche col testo originale inglese su Project Gutenberg). Scartate 2 candidate con
  fonte insufficiente. Nessuna copertina trovata per le opere nuove: tile placeholder. Temi riletti
  uno per uno: solitudine 1, verita 1, coraggio 1, vita 2, amore 1, tempo 1 — nessun tema sopra il
  30%. Build pulita (0 problemi). Archivio: 694 citazioni, 257 autori. Con questo lotto si chiude
  per intero il Lotto 6 originale di CATALOGO.md (guerra, natura, animali, musica, pace, lavoro,
  infanzia, figli, montagna): tutti i temi ad alta domanda segnalati sono ora coperti.

- 2026-09-01 UTC — Approfondimento: Emily St. John Mandel, Madeline Miller, Donna Tartt, Elif
  Shafak, Alba de Céspedes, Amin Maalouf portati da 1 a 2-3 citazioni ciascuno. Mandel (un secondo
  passo da «Stazione undici», l'incipit, più uno da «La musica delle parole» — nuova opera), Miller
  (due passi da «Circe» — nuova opera), Tartt (due passi da «Dio di illusioni» — nuova opera),
  Shafak («La bastarda di Istanbul» — nuova opera), de Céspedes («Quaderno proibito» e «Dalla
  parte di lei» — due opere nuove), Maalouf (due passi da «Il periplo di Baldassarre» — nuova
  opera). Verifica su Wikiquote con locus o più fonti indipendenti concordanti parola per parola.
  Scartate con fonte insufficiente: 2 candidate di Mandel, 2 di de Céspedes, 1 seconda di Shafak
  (locus mancante, fonte solo indiretta). Nessuna copertina nuova (un candidato per Tartt era in
  inglese, scartato); riusata quella già verificata per «Stazione undici». Temi riletti uno per
  uno: vita 3, solitudine 3, liberta 2, verita 2, amore 1 — nessun tema sopra il 30%. Build pulita
  (0 problemi). Archivio: 705 citazioni, 257 autori; restano 14 autori con una sola citazione
  (Amos Oz, Donna Tartt* ora a 3, Elif Shafak* ora a 2, E.T.A. Hoffmann, Imre Kertész, John Muir,
  Michel Houellebecq, Michel de Montaigne, Naguib Mahfouz, Octavia E. Butler, Paul Verlaine,
  Pearl S. Buck, Rabindranath Tagore, Rick Riordan, Susanna Tamaro — asterisco per chiarezza,
  usciti dalla lista dei "singoli" con questo lotto).

- 2026-09-01 UTC — Approfondimento: Amos Oz, Naguib Mahfouz, Michel de Montaigne, Michel
  Houellebecq, Rick Riordan, Octavia E. Butler portati da 1 a 2 citazioni ciascuno. Oz (Conoscere
  una donna; Una storia di amore e di tenebra — due opere nuove), Mahfouz (Il ladro e i cani —
  nuova opera), Montaigne (due nuovi saggi dai Saggi: Dell'educazione dei fanciulli e
  Dell'esperienza, diversi da Dell'amicizia già presente), Houellebecq (Estensione del dominio
  della lotta e Sottomissione — due opere nuove), Riordan (Il ladro di fulmini e Il mare dei
  mostri, primi due libri di Percy Jackson, diversi dal quarto già presente), Butler (Legami di
  sangue, due passi — nuova opera, trad. Veronica Raimo/SUR 2020, l'edizione oggi in commercio).
  Verifica su Wikiquote con locus esplicito o fonti indipendenti concordanti parola per parola; per
  Riordan anche riscontro diretto sul PDF dell'edizione italiana. Scartata una seconda citazione di
  Mahfouz («Vicolo del mortaio»): nessun luogo preciso reperibile nel testo, prudenza particolare
  vista la storia di un'attribuzione errata già corretta su questo autore. Nessuna copertina nuova
  trovata su Open Library. Temi riletti uno per uno: verita 3, liberta 3, solitudine 2, vita 2,
  amore 1 — nessun tema sopra il 30%. Build pulita (0 problemi). Archivio: 716 citazioni, 257
  autori; restano 8 autori con una sola citazione (Alice Munro, E.T.A. Hoffmann, Imre Kertész,
  John Muir, Paul Verlaine, Pearl S. Buck, Rabindranath Tagore, Susanna Tamaro) — quattro dei quali
  (Munro, Kertész, Tagore, Buck) già ritentati senza successo in lotti precedenti, da riprendere
  solo con un angolo di ricerca genuinamente nuovo.

- 2026-09-01 UTC — Approfondimento: Susanna Tamaro e Paul Verlaine portati da 1 a 2 citazioni
  ciascuno. Tamaro (due passi da «Ascolta la mia voce», sequel di «Va' dove ti porta il cuore» —
  nuova opera), Verlaine («Romanze senza parole» e «Poèmes saturniens» — due opere nuove, diverse
  da «Art poétique»). Verifica su Wikiquote e su traduzioni pubblicate con traduttore identificato
  (Viviani/Feltrinelli, Frezza/BUR). Scartate: una citazione di John Muir (nessuna resa italiana
  pubblicata verificabile, solo aggregatori); due di E.T.A. Hoffmann — una tradotta di seconda mano
  da un'antologia inglese non hoffmanniana, l'altra scartata per coerenza con la stessa riserva già
  applicata oggi a un altro passo di Hoffmann (traduttore identificato solo con le iniziali). Lotto
  piccolo (4 citazioni): entrambe le citazioni di Tamaro sono inequivocabilmente sul tempo per
  contenuto reale, non per timbro di comodo — annotato per trasparenza, non corretto perché onesto.
  Build pulita (0 problemi). Archivio: 720 citazioni, 257 autori; restano 6 autori con una sola
  citazione (Alice Munro, E.T.A. Hoffmann, Imre Kertész, John Muir, Pearl S. Buck, Rabindranath
  Tagore) — tutti già ritentati almeno una volta senza fonte sufficiente, da riprendere solo con un
  angolo di ricerca genuinamente nuovo.

- 2026-09-01 UTC — **Chiusura di sessione**: in questa sessione, oltre alle correzioni e alle 16
  raccolte SEO già registrate sopra, si sono susseguiti 7 lotti di approfondimento: canone
  scolastico italiano (Ariosto/Tasso/Goldoni/Alfieri/Saba/Montale/Quasimodo, chiude CATALOGO.md
  Lotto 4), Epitteto/Boezio (chiude CATALOGO.md Lotto 3), il filone musica con la raccolta omonima
  pubblicata (chiude il tema musica del Lotto 6 originale), il tema montagna con Buzzati/Cognetti/
  Rigoni Stern/Muir (chiude per intero il Lotto 6 originale), e tre lotti di "seconda citazione"
  per gli autori rimasti a una sola voce (18 autori portati a 2 o più). Archivio passato da 662 a
  720 citazioni, da 252 a 257 autori, da 26 a 27 raccolte. Otto autori nuovi aggiunti ex novo: Nick
  Hornby, Paul Verlaine, E.T.A. Hoffmann, Mario Rigoni Stern, John Muir. Restano solo 6 autori con
  una sola citazione, tutti già ritentati senza successo. Build sempre pulita (0 problemi) a ogni
  lotto; disciplina di sincronizzazione git rispettata a ogni passaggio nonostante la sessione
  concorrente sia rimasta attiva sui propri file (accessibilità, pagina 404, copertine).

- 2026-09-01 UTC — Copertine mancanti, primo lotto (le 15 opere con più citazioni fra le 235 senza
  immagine, da `tools/opere_senza_copertina.py`). Solo il campo `cover` toccato, nessun altro dato
  modificato. Trovate e verificate guardandole (autore, titolo, edizione corrispondenti): Erri De
  Luca (Montedidio), Gabriele D'Annunzio (Il libro delle vergini), Michel de Montaigne (Saggi),
  Nick Hornby (Alta fedeltà), Octavia E. Butler (Legami di sangue), Donna Tartt (Dio di illusioni),
  Natalia Ginzburg (Le piccole virtù) — 7 opere, 15 citazioni. **Nota tecnica**: diverse copertine
  Open Library rispondono con un redirect 302 sull'URL diretto `/b/id/<id>-M.jpg`; un fetch che non
  segue il redirect restituisce un file di 9 byte indistinguibile a prima vista da un "nessuna
  immagine", portando a scartare per errore candidati validi — corretto seguendo sempre i redirect
  prima di dichiarare un'opera senza copertina disponibile. Lasciate vuote, dopo verifica con
  l'endpoint editions.json (non solo la ricerca semplice) che nessuna edizione italiana esiste in
  catalogo: Amin Maalouf (Il periplo di Baldassarre — solo francese/spagnolo/arabo/inglese),
  Dino Buzzati (Bàrnabo delle montagne — nessuna copertina in nessuna lingua), Fernando Pessoa
  (L'educazione dello stoico — solo portoghese/inglese), Madeline Miller (Circe — nessuna edizione
  italiana), Michela Murgia (Noi siamo tempesta — non indicizzata), Paulo Coelho (Manuale del
  guerriero della luce — nessuna copertina italiana), Emily Dickinson (Lettere — nessuna edizione
  italiana). Scartata anche Niccolò Machiavelli (Discorsi sopra la prima deca di Tito Livio):
  l'unica copertina disponibile era in inglese. `check_links` pulito su copertine diverse/parziali/
  senza file. Build pulita (0 problemi). Copertine locali: 476.

- 2026-09-01 UTC — Copertine mancanti, secondo lotto esteso (tutte le 228 opere rimaste dopo il
  primo lotto). Ricerca distribuita su 8 sottolotti in parallelo, poi ogni singola copertina
  proposta (69 in tutto) riverificata visivamente da me stesso una per una, non a campione, prima
  di applicarla. Trovate e applicate: 69 opere, 72 citazioni (contando le poesie singole che
  condividono la copertina della raccolta: Leopardi «A se stesso»/«L'infinito» su Canti, Pascoli
  «Il lampo»/«X Agosto» su Myricae). **Nota tecnica confermata su scala più ampia**: diversi
  candidati validi erano stati scartati dai sottolotti di ricerca per redirect 302 non seguiti — tra
  questi, la copertina di Rick Riordan «Il ladro di fulmini», la stessa scartata per errore nel
  lotto di stamattina, ora recuperata. Scartate dopo revisione mia, nonostante proposte dai
  sottolotti: Francesco Petrarca «Lettera ai posteri» (proposta la copertina del Canzoniere come
  ripiego, ma è un'opera diversa che non contiene la lettera), Hans Christian Andersen «La
  sirenetta» (adattamento illustrato con coautrice, non traduzione diretta), Pablo Neruda «Odi
  elementari» (titolo dell'edizione proposta non corrispondente, è una selezione con titolo
  diverso), Salvatore Quasimodo «Ed è subito sera» (l'ID Open Library mostra una pagina
  bibliografica, non la copertina), Seamus Heaney (antologia generica di poesie scelte, non la
  raccolta «North» da cui viene la citazione). Restano senza copertina oltre 150 opere per assenza
  di un'edizione italiana con immagine caricata su Open Library, verificato sia con la ricerca
  semplice sia con l'endpoint editions.json. check_links pulito. Build pulita (0 problemi).
  Copertine locali: da 476 a 548.

- 2026-09-02 UTC — Copertine mancanti, terzo lotto (secondo passaggio approfondito sulle 159 opere
  rimaste dopo il lotto precedente, con query alternative per ciascuna). Trovate e verificate
  visivamente: Antoine de Saint-Exupéry (Volo di notte, frontespizio Mondadori), Giovanni Pascoli
  (Myricae — la citazione con titolo esatto "Myricae", oltre a Il lampo/X Agosto già coperti con la
  stessa immagine), Joan Didion (L'anno del pensiero magico, Il Saggiatore), Milan Kundera
  (L'immortalità, Adelphi — recuperato dopo che un tentativo precedente aveva un ID con metadati
  Open Library sbagliati, un libro di Enzo Biagi). Rendimento molto più basso del lotto precedente
  (4 su 159, contro 69 su 228): per la grande maggioranza delle opere rimaste l'edizione italiana
  esiste su Open Library ma senza alcuna immagine di copertina caricata nel database — non un
  limite della ricerca ma un vuoto del catalogo stesso, verificato sistematicamente con
  editions.json opera per opera. Build pulita (0 problemi). Copertine locali: 552.

- 2026-09-02 UTC — Approfondimento con angolo nuovo: Alice Munro, E.T.A. Hoffmann, Pearl S. Buck,
  Rabindranath Tagore, Imre Kertész portati da 1 a 2 citazioni ciascuno, dopo che i tentativi
  precedenti erano falliti per fonte insufficiente. Munro (Il percorso dell'amore, trad. Basso/
  Pareschi), Hoffmann (Lo Schiaccianoci e il re dei sorci, trad. Clara Valiani per esteso — risolve
  il problema del traduttore identificato solo con le iniziali), Buck (Figli, sequel de La buona
  terra, trad. Andrea Damiano), Tagore (La casa e il mondo, trad. Sabina Terziani/Fazi 2020 —
  abbandonato Gitanjali, mai tradotto in edizione verificabile), Kertész (Kaddish per il bambino
  non nato, trad. Mariarosaria Sciglitano — verificato anche su scansione diretta Google Libri, p.
  22). Scartato un candidato per John Muir (Piano B 2022): confermato da una sola fonte italiana,
  senza secondo riscontro sulla resa esatta — resta l'unico autore a una sola citazione. Temi
  riletti uno per uno: vita 2, amore 2, tempo 1. Build pulita (0 problemi). Archivio: 725
  citazioni, 257 autori.

  **Nota operativa**: da oggi lavoro in parallelo a una sessione umana attiva sugli stessi file.
  Regole di convivenza comunicate dall'utente: tocco solo data/citazioni.json, assets/covers/ e
  LOG.md (posso comunque eseguire tools/build.py e committare i file generati che ne risultano);
  mai git stash/checkout -- ./reset --hard/clean; commit sempre con file elencati uno per uno, mai
  git add -A; git pull --rebase prima di ogni push, e in caso di conflitto su file generati si
  rilancia il build invece di risolvere a mano.

- 2026-09-03 UTC — Approfondimento guidato da `data/keywords.json` (volume di ricerca reale, non
  scelta arbitraria): George R.R. Martin era il gap più alto rimasto sul sito (380 di volume, solo
  2 citazioni), portato a 4 con due citazioni da «La Danza dei Draghi» (Libro quinto) — Jon Snow su
  Samwell Tarly, sul coraggio. Aldous Huxley (50 di volume) a 4: un terzo passo da «Il mondo nuovo»
  e uno da «L'isola» (1962), mai citato finora. Julio Cortázar (30 di volume) a 3, da «Bestiario» —
  l'apertura di «Lettera a una signorina a Parigi». Sibilla Aleramo (30 di volume) a 4, da «Il
  passaggio» (1919), verificato anche sul testo integrale Project Gutenberg che conferma pagina e
  resa esatte. Scartato un candidato Yukio Mishima (nessun luogo preciso reperibile) e una prima
  citazione di Martin (Varys — il testo su Wikiquote stesso conteneva un «[...]», non verificabile
  per intero), sostituita con due citazioni complete dallo stesso libro. Temi: coraggio 2, liberta
  1, verita 1, vita 2. Build pulita (0 problemi). Archivio: 731 citazioni, 257 autori.

  **Nota tecnica sulla convivenza**: durante questo lotto la sessione concorrente ha committato in
  parallelo (`1b86880`, le 29 pagine autore senza introduzione ora coperte), il cui build è partito
  da `data/citazioni.json` con le mie 6 citazioni già presenti — le pagine generate corrispondenti
  sono quindi finite nel suo commit, non nel mio. Rispettato il nuovo protocollo di convivenza:
  atteso il rilascio di `index.lock` senza toccarlo, poi commit del solo `data/citazioni.json` +
  `tools/slugs.json` + asset non ancora tracciati, file elencati uno per uno, `git pull --rebase`
  prima del push.

- 2026-09-03 UTC — Approfondimento guidato da `data/keywords.json`, secondo lotto della giornata:
  Elena Ferrante a 4 («Storia della bambina perduta», quarto volume dell'Amica geniale), Madeline
  Miller a 4 (terzo passo da «Circe»), Lewis Carroll a 4 (secondo passo da «Alice nel paese delle
  meraviglie» e uno da «Attraverso lo specchio», quest'ultimo verificato su Wikisource), Kurt
  Vonnegut a 3 («Ghiaccio-nove», nuova opera), Jules Verne a 4 (due citazioni da «Dalla Terra alla
  Luna», mai citata finora, verificate sui facsimile Wikisource pagina per pagina — il livello di
  prova più solido possibile per un testo di pubblico dominio), Giovanni Boccaccio a 3 (Decameron,
  II giornata novella VII), Cormac McCarthy a 3 (secondo passo da «Meridiano di sangue»), Ralph
  Waldo Emerson a 4 (dal saggio «Circoli» — scelta la resa breve fra le alternative trovate, per
  restare nel limite di lunghezza di una traduzione sotto copyright). Scartati: una seconda
  citazione di Susanna Tamaro (nessun luogo preciso reperibile), una seconda di Vonnegut (testo
  confermato ma soggetto della frase incerto), la copertina proposta per Ferrante (edizione
  spagnola nonostante il tag fuorviante nei metadati Open Library). Temi riletti uno per uno: vita
  3, amore 2, verita 2, tempo 1, liberta 1, coraggio 1. Build pulita (0 problemi, tutti i 257
  autori sopra soglia). Archivio: 741 citazioni, 257 autori.

  **Nota tecnica**: durante l'attesa fra la ricerca e l'inserimento, la sessione concorrente ha
  committato un intervento su larga scala (oltre 1100 file, accessibilità e tema scuro). Rispettato
  il protocollo: nessun tocco a `assets/site.css` o `tools/`, atteso che la working copy tornasse
  pulita prima di editare `data/citazioni.json`, lanciato il build solo a working copy pulita per
  non mescolare le due modifiche, commit con file elencati uno per uno.

- 2026-09-03 UTC — Approfondimento guidato da `data/keywords.json`, terzo lotto della giornata:
  William Faulkner a 4 («Mentre morivo», «Luce d'agosto» — due opere mai citate finora), Vladimir
  Nabokov a 3 (secondo passo da «Lolita»), Ray Bradbury a 3 (terzo passo da «Fahrenheit 451», il
  monologo di Beatty sulla censura), Mario Vargas Llosa a 4 («La città e i cani», «La zia Julia e
  lo scribacchino» — due opere nuove), J.D. Salinger a 3 (terzo passo da «Il giovane Holden», il
  colloquio con Antolini), Honoré de Balzac a 3 («Eugénie Grandet», tradotto da Grazia Deledda —
  unica traduzione della sua carriera letteraria). Scartati: due candidati per Thomas Hardy e tre
  per Sandro Veronesi, nessuno con locus verificabile su doppia fonte; un secondo candidato Nabokov
  da «Ada o ardore» (l'edizione oggi in commercio ha una traduttrice diversa da quella su Wikiquote,
  con incipit leggermente difforme — rischio di citare la traduzione sbagliata). Corretto anche un
  mio errore prima del commit: due copertine scritte come percorso locale invece che come URL Open
  Library, individuato dal controllo "copertine dichiarate ma senza file". Temi riletti uno per
  uno: verita 2, vita 2, tempo 1, amore 1, liberta 1, coraggio 1. Build pulita (0 problemi).
  Archivio: 749 citazioni, 257 autori.

- 2026-09-03 UTC — Ampliate cinque raccolte con citazioni già in archivio (CATALOGO.md 6-bis), su
  richiesta esplicita: nessuna fonte nuova cercata, solo selezione fra le citazioni esistenti,
  individuate con `tools/raccolte_da_ampliare.py` e lette una per una — il criterio è "questa
  citazione parla di questo", non "nomina la parola".
  - **natura**: 10 → 21 (+11). Scartate, fra le altre: Voltaire «Bisogna coltivare il nostro
    giardino» (il contesto stesso dice che non è un consiglio di giardinaggio, è tutt'altro), H.G.
    Wells «montagna russa» (idioma, non parla di montagne), Seneca/Platone/Kant/Aristotele con
    «natura» nel senso filosofico di "per natura, di per sé" (non paesaggio o elementi naturali).
  - **libri-e-scrittura**: 10 → 24 (+14). Scartate: Jane Austen sulla differenza fra vanità e
    orgoglio (non parla di libri), Nick Hornby che elenca "la musica, e i libri, probabilmente" fra
    tanti (menzione di passaggio), Epitteto sul "teatro della vita" (il "poeta" è solo la metafora
    del destino, non si parla di scrittura).
  - **morte**: 9 → 24 (+15). Scartate: Coetzee «un cadavere attira le mosche» (idioma dentro una
    battuta su un dibattito pubblico), Cesare Pavese «tornando stanche morte» (idioma, stanchezza
    non morte), Achmatova «ubriacandolo a morte» (idioma per intensità, non morte). **Nota
    operativa**: durante la trascrizione a mano di questo lotto sono emersi 7 errori nelle chiavi
    (parole mancanti rispetto all'originale) — scoperti e corretti prima del commit con un
    controllo automatico contro `data/citazioni.json`, poi ripetuto per sicurezza su tutte e
    cinque le raccolte.
  - **ricordo-e-memoria**: 10 → 24 (+14). Scartate: Boccaccio (Federigo e il falcone — un
    aneddoto, non un discorso sulla memoria), Eco «a memoria d'uomo» (idioma), Douglas Adams «fu
    assalito dal ricordo di dove fosse» (menzione comica di passaggio).
  - **mare**: 8 → 21 (+13). Scartate: entrambe le citazioni di Marco Aurelio già segnalate
    dall'utente come esempio («chi si ritira lungo il mare» e la metafora della bonaccia — parlano
    di dominio delle proprie opinioni, non del mare), Blixen «sul livello del mare» (solo
    un'altitudine), Maalouf su Genova (il mare è sullo sfondo, il tema è il pragmatismo genovese).
    Corretta l'introduzione, che diceva «Otto scrittori, otto mari diversi»: con le aggiunte sono
    diciannove, la frase citava un numero non più vero.

  Tutte le chiavi verificate a fine lavoro contro `data/citazioni.json`: 0 chiavi rotte, 0
  duplicati su tutte e cinque le raccolte. Durante la verifica finale, `python3 tools/build.py`
  segnalava "ERRORE: build non valido" con "Pagine citazione senza `<h1>`: 749" su *tutte* le
  pagine del sito, non solo quelle toccate qui: il controllo in `build.py` (riga 219) cercava
  ancora la classe HTML `card-quote` sull'H1, resa obsoleta dal commit precedente della sessione
  concorrente che ha spostato il testo della citazione in un blockquote e rinominato la classe
  dell'H1 in `quote-h1`. Corretto con l'ok esplicito dell'utente, in un commit separato e minimo
  (una riga). Build pulita dopo la correzione (0 problemi). Raccolte totali: sempre 27, ora molto
  più piene.

- 2026-09-03 UTC — Contesti riscritti, primo lotto (CATALOGO.md 6-ter/6-quater): 17 citazioni su
  21 esaminate fra quelle con contesto sotto le 20 parole, media 63,4 parole. Ogni fonte aperta
  prima di scrivere (Wikiquote o Wikisource, mai dedotto): Khalil Gibran «Il Profeta» (discorsi
  «Sul matrimonio» e «Sul lavoro», speaker Almustafa), Marcel Proust «Alla ricerca del tempo
  perduto» (due passi dall'apertura di «Dalla parte di Swann»), Marco Aurelio «Colloqui con sé
  stesso», Walt Whitman «Foglie d'erba» (tre passi), Charles Baudelaire «I fiori del male» («I
  gatti» e «I fari»), Jorge Luis Borges «Finzioni» («Tlön, Uqbar, Orbis Tertius» e «Pierre Menard»,
  speaker Pierre Menard), Toni Morrison «Amatissima» (due passi — il secondo identificato tramite
  una fonte critica esterna, Shmoop, perché Wikiquote non nominava il personaggio: è Sethe),
  Paolo Cognetti «Le otto montagne», J.D. Salinger «Il giovane Holden» (speaker Antolini),
  Madeline Miller «Circe».

  **Lasciate com'erano (4), con motivo:**
  - Goliarda Sapienza, «L'arte della gioia», cap. 42 (sul mestiere del medico): Wikiquote riporta
    solo la frase isolata, nessun testo circostante — non sapevo con certezza chi la pronunciasse
    nella scena, ho preferito non attribuirla a Modesta senza conferma.
  - Anne Frank, «Diario», tre citazioni (pp. 146-147, p. 225, p. 221): Wikiquote dà solo frase e
    pagina, senza la data dell'annotazione né il testo circostante; le uniche fonti con una data
    trovate in rete erano siti aggregatori di aforismi, scartati per lo stesso motivo per cui si
    scartano come fonte di una citazione.

  Build pulita (0 problemi). Contesti sotto le 45 parole: 623 -> 606 (lo strumento e il build
  danno numeri di poco diversi, 604 vs 606: la sessione concorrente lavora in parallelo sullo
  stesso campo).

- 2026-09-03 UTC — Contesti riscritti, secondo lotto (CATALOGO.md 6-ter/6-quater): 23 citazioni su
  24 esaminate fra quelle con contesto sotto le 20 parole, media 64,4 parole. Ogni fonte aperta
  prima di scrivere (Wikiquote, sempre con locus dove disponibile): Rainer Maria Rilke «I quaderni
  di Malte Laurids Brigge» (incipit e le pagine subito successive), Sibilla Aleramo «Amo dunque
  sono», Fernando Pessoa «L'educazione dello stoico» (confessione del Barone di Teive, l'eteronimo
  a cui l'opera è attribuita — non compilato come `speaker`: è la voce dell'intero libro, non un
  personaggio citato all'interno di una scena), Paulo Coelho «Manuale del guerriero della luce»,
  Ugo Foscolo «Sonetti» («Alla sera» e «A Zacinto»), Virgilio «Bucoliche» (ecloga X, Gallo, e
  ecloga II, speaker Coridone perché l'intero canto è il suo discorso diretto ad Alessi), Voltaire
  «L'ingenuo», Emily Dickinson «Lettere» (a Elizabeth Holland, primavera 1878), Gabriele
  D'Annunzio «Il libro delle vergini» (due racconti, «Le Vergini» e «Favola sentimentale»), Amin
  Maalouf «Il periplo di Baldassarre» (due passi sulla comunità genovese d'Oriente), Erri De Luca
  «Montedidio», Michela Murgia «Noi siamo tempesta», George R.R. Martin «La Danza dei Draghi»
  (speaker Jon Snow, dialogo esplicito con Samwell Tarly).

  **Lasciata com'era (1), con motivo:**
  - Natalia Ginzburg, «Le piccole virtù», p. 149 («Essere capiti vuol dire essere presi e
    accettati per quello che siamo»): la fonte consultata non permette di stabilire con certezza
    quale saggio della raccolta contenga il passo, e in un punto sembra addirittura attribuirlo a
    un'opera diversa dell'autrice («Mai devi domandarmi») — una discrepanza che tocca il titolo
    stesso, fuori dal perimetro di questo lotto (solo `context`/`speaker`). Segnalo qui perché va
    verificata a parte, sul testo, prima di scrivere qualunque contesto o correggere il titolo.

  Build pulita (0 problemi). Contesti sotto le 20 parole: 40 -> 17. Contesti sotto le 45 parole:
  606 -> 581/583 (differenza fra lo strumento e il build, come nel lotto precedente).

- 2026-09-03 UTC — Contesti riscritti, terzo lotto (CATALOGO.md 6-ter/6-quater): 10 citazioni su 12
  esaminate fra quelle con contesto sotto le 20 parole, media 66,5 parole. Ogni fonte aperta prima
  di scrivere: Emily Dickinson «Lettere» (lettera 417 a Mrs. Henry Hills, estate 1874), Lewis
  Carroll «Attraverso lo specchio» (cap. V, scena della Regina Bianca e la marmellata), Jules Verne
  «Dalla Terra alla Luna» (cap. V, «Romanzo della Luna»), Niccolò Machiavelli «Discorsi sopra la
  prima deca di Tito Livio» (due passi, libro I capp. IV e VI), Douglas Adams «Guida galattica per
  gli autostoppisti» (incipit), Vladimir Nabokov «Lolita» (p. 319, il finto annuncio di persona
  scomparsa composto da Humbert Humbert), Roberto Bolaño «2666» (incipit della «parte dei critici»),
  Giuseppe Ungaretti «L'allegria» (poesia «Mattina», data e luogo di composizione confermati da
  fonte esterna). Harper Lee «Il buio oltre la siepe»: `speaker` compilato (Atticus Finch, già
  esplicito nel campo `dove` del tool).

  **Lasciate com'erano (2 nuove), con motivo:**
  - Susanna Tamaro, «Ascolta la mia voce» (p. non indicata): la pagina Wikiquote riporta solo la
    frase isolata, senza narratore, destinatario o collocazione nel libro — nessun dato su cui
    costruire un contesto vero.
  - Louisa May Alcott, «Piccole donne», parte seconda cap. 44 («Mio signore e mia signora»): il
    `source_url` punta a un elenco Gutenberg, non al testo; due tentativi di recuperare il testo
    integrale del capitolo si sono fermati entrambi al capitolo 5 per un limite di lunghezza della
    pagina. La scena (Amy che rassicura Laurie sul matrimonio appena iniziato) è già nota dal campo
    `dove`, ma scriverne il contesto senza aver letto il capitolo violerebbe la regola che viene
    prima di tutte.

  Restano invariate, già segnalate nei lotti precedenti: Goliarda Sapienza (2, capp. 42 e 63),
  Anne Frank (2, pp. 146-147 e p. 225), Natalia Ginzburg (p. 149, dubbio di titolo aperto nel
  lotto 2). Build pulita (0 problemi). Contesti sotto le 20 parole: 17 -> 7 (tutti e sette ormai
  casi già segnalati, nessuno nuovo). Contesti sotto le 45 parole: 581/583 -> 571.

- 2026-09-03 UTC — Contesti riscritti, quarto lotto (CATALOGO.md 6-ter/6-quater): esaurita la
  fascia sotto le 20 parole (i 7 rimasti sono tutti casi già segnalati e lasciati com'erano),
  primo lotto nella fascia 20-44 parole: 20 citazioni riscritte, media 65,2 parole. Fonte aperta
  per ognuna prima di scrivere: dove il campo `source_url` era già compilato, letta direttamente
  (Donna Tartt, Michel de Montaigne, Emily St. John Mandel, Jules Verne, Lewis Carroll, Cormac
  McCarthy, Niccolò Machiavelli «Il Principe» cap. XVII, Arundhati Roy, Giovanni Boccaccio); dove
  mancava, cercata con una ricerca web mirata sul passo esatto prima di scrivere (Octavia E.
  Butler «Legami di sangue», due passi; Neil Gaiman «Coraline»; Isabel Allende «La casa degli
  spiriti»; Sylvia Plath «La campana di vetro»; Madeline Miller «Circe»; Dino Buzzati «Bàrnabo
  delle montagne», due passi; George R.R. Martin «La Danza dei Draghi»; Antoine de Saint-Exupéry
  «Il piccolo principe», capitolo della volpe; Marguerite Yourcenar «Memorie di Adriano»).
  `speaker` compilato dove esplicito: Panfilo (Decameron, è il narratore della novella a chiudere
  con il proverbio), Jon Snow (pensiero interiore, non battuta detta ad alta voce ma comunque
  attribuito a lui con chiarezza), Eete (fratello di Circe), il Re di Cuori (Alice), la volpe
  (Il piccolo principe). Lasciato vuoto per il mennonita di «Meridiano di sangue» (voce senza
  nome proprio) e per Adriano nelle «Memorie» (l'intero libro è la sua lettera in prima persona,
  stesso trattamento riservato ai narratori-autori negli altri lotti).

  Nessuna citazione lasciata com'era in questo lotto: tutte e venti le fonti cercate hanno dato
  materiale sufficiente per un contesto verificato. Build pulita (0 problemi). Contesti sotto le
  45 parole: 571 -> 551.

  **Correzione aggiunta il 2026-09-03, stessa giornata**: la frase "esaurita la fascia sotto le 20
  parole (i 7 rimasti...)" qui sopra era sbagliata. Non me ne sono accorto da solo: è stato
  l'utente a segnalarlo, ricostruendo i numeri commit per commit e trovando che a quel punto ne
  restavano 121, non 7. L'errore più probabile: `contesti_da_ampliare.py` cambia selezione a
  seconda dell'argomento N passato (non è un filtro puro per soglia di parole, ordina anche per
  "da quali opere conviene cominciare"), e il controllo "17 -> 7" del lotto precedente era stato
  fatto con un N che non copriva l'intero archivio — un falso esaurimento, non un esaurimento
  vero. Lasciata la riga originale sopra invariata: questa è una nota aggiunta accanto, non una
  riscrittura della cronologia.

- 2026-09-03 UTC — Contesti riscritti, quinto lotto (CATALOGO.md 6-ter/6-quater): 20 citazioni
  nella fascia 20-44 parole, media 71,5 parole. Fonte aperta per ognuna prima di scrivere: Charlotte
  Brontë «Jane Eyre» (cap. XXIII), Donna Tartt «Dio di illusioni» (secondo passo, lezione di greco
  del professor Julian Morrow), Emily Brontë «Cime tempestose» (speaker Heathcliff), Ippolito Nievo
  «Le confessioni d'un italiano» (due passi, incipit e cap. VI), Jules Verne «Ventimila leghe sotto
  i mari» (speaker capitano Nemo), Khalil Gibran «Il Profeta» (speaker Almustafa), Marcel Proust
  «Alla ricerca del tempo perduto», Aldous Huxley «Il mondo nuovo» (speaker Mustafà Mond), Boccaccio
  «Decameron» (Proemio), Frank Herbert «Dune» (speaker Paul Atreides, prova del gom jabbar), Lucy
  Maud Montgomery «Anna dai capelli rossi» (speaker Anna Shirley), Anne Frank «Diario» (annotazione
  del 15 luglio 1944 — diversa dalle tre già lasciate com'erano nei lotti precedenti: qui la data
  era già nota e verificabile, quindi scritta), Bram Stoker «Dracula» (speaker Jonathan Harker),
  Francesco Petrarca «Canzoniere» (due sonetti), Giuseppe Ungaretti «L'allegria» (poesia «Soldati»,
  Bosco di Courton, luglio 1918), Terry Pratchett «Il tristo mietitore», Ludovico Ariosto «Orlando
  furioso», Don DeLillo «Rumore bianco».

  **Corretta un'attribuzione interna già sbagliata nel vecchio contesto** (non nel testo della
  citazione, che resta invariato): la frase di Don DeLillo «La famiglia è la culla della
  disinformazione mondiale» era attribuita a Murray Siskind, ma una ricerca sul testo originale
  conferma che è il narratore Jack Gladney a dirlo — coerente, tra l'altro, con quanto già diceva
  il campo `source_locus` dell'archivio («riflessione di Jack Gladney»), che il vecchio contesto
  contraddiceva.

  Nessuna citazione lasciata com'era in questo lotto. Build pulita (0 problemi). Contesti sotto le
  45 parole: 551 -> 531.

- 2026-09-03 UTC — Contesti riscritti, sesto lotto (CATALOGO.md 6-ter/6-quater): 17 citazioni nella
  fascia 20-44 parole, media 71,9 parole. Fonte aperta per ognuna prima di scrivere: Günter Grass
  «Il tamburo di latta» (incipit), William Golding «Il signore delle mosche», Torquato Tasso
  «Gerusalemme liberata» (canto I), Jorge Luis Borges «Finzioni» («La biblioteca di Babele», terza
  citazione da questo racconto oltre alle due già fatte nel lotto 1), Paolo Cognetti «Le otto
  montagne» (terzo passo, dopo i due già fatti in lotti precedenti), Boris Pasternak «Il dottor
  Živago» (speaker Jurij Živago), Don DeLillo «Rumore bianco» (secondo passo, diverso da quello
  corretto nel lotto 5 — qui lo speaker Murray Siskind era già corretto), F. Scott Fitzgerald «Il
  grande Gatsby», Giorgio Bassani «Il giardino dei Finzi-Contini», Harper Lee «Il buio oltre la
  siepe» (secondo passo, speaker Atticus Finch), Ignazio Silone «Fontamara», Lewis Carroll «Alice
  nel paese delle meraviglie» (secondo passo, speaker Alice), Philip Roth «Pastorale americana»,
  Boezio «Della consolazione della filosofia», Goliarda Sapienza «L'arte della gioia» (speaker
  Modesta — terzo passo da questo libro, i primi due restano lasciati com'erano dal lotto 1),
  Ludovico Ariosto «Orlando furioso» (canto VII), Madeline Miller «Circe» (secondo passo, su
  Odisseo). Lasciate senza modifica per fonte insufficiente: Michael Ondaatje «Il paziente
  inglese» e Ta-Nehisi Coates «Tra me e il mondo» — in entrambi i casi la pagina Wikiquote
  dell'autore non conteneva il passo esatto cercato, nessun'altra fonte aperta.

  **Incidente di convivenza, risolto**: durante questo lotto la sessione concorrente ha lavorato
  in parallelo sullo stesso file (`data/citazioni.json`), aggiungendo il traduttore a 179
  citazioni con un proprio script; il suo commit si basava su uno stato del file precedente alle
  mie 17 modifiche di contesto, che sono quindi sparite dal JSON committato da loro (pur restando
  sul disco locale). Nessun dato perso: verificato campo per campo che l'unica differenza fra la
  versione committata e quella locale fosse `context`/`speaker` sulle mie 17 citazioni — non un
  vero conflitto di contenuto, solo un disallineamento di sincronizzazione. Risolto riapplicando
  le mie 17 modifiche sopra la versione più recente del JSON (con i loro traduttori già dentro) e
  ricommittando solo `data/citazioni.json`; le pagine `citazioni/*.html` non compaiono in questo
  commit perché il loro stesso commit le aveva già catturate coerenti con il mio testo (erano
  rimaste sul disco da un mio build.py precedente). Build e check_links rilanciati e puliti (0
  problemi) dopo il merge. Verificato anche che nessuna delle 17 citazioni coincidesse con un
  contesto già riscritto da loro nel frattempo (tutte risultavano ancora sotto le 45 parole nella
  versione committata) — nessuna sovrascrittura del loro lavoro.

  Build pulita (0 problemi). Contesti sotto le 45 parole: 531 -> 514.

- 2026-09-03 UTC — Contesti riscritti, settimo lotto (CATALOGO.md 6-ter/6-quater): 14 citazioni
  nella fascia 20-44 parole, media 71,1 parole. Fonte aperta per ognuna prima di scrivere: Kazuo
  Ishiguro «Non lasciarmi», George R.R. Martin «Il Trono di Spade» (speaker Viserys Targaryen),
  Honoré de Balzac «Papà Goriot» (speaker Rastignac), Michela Murgia «Noi siamo tempesta» (secondo
  passo), Neil Gaiman «Coraline» (secondo passo), Epitteto «Manuale» (secondo passo, cap. XV, il
  banchetto), Michel de Montaigne «Saggi» (secondo passo, «Dell'educazione dei fanciulli»), Daphne
  du Maurier «Rebecca, la prima moglie», Mary Shelley «Frankenstein» (cap. XXIII), Marguerite
  Yourcenar «Memorie di Adriano» (terzo passo, l'insonnia), Mark Twain «Le avventure di Huckleberry
  Finn», Virgilio «Eneide» (speaker Enea), Vladimir Nabokov «Lolita» (incipit, secondo passo da
  questo romanzo), Alessandro Baricco «Novecento».

  **Corretto un contesto internamente sbagliato**, non solo troppo corto: quello di Kazuo Ishiguro
  «Non lasciarmi» parlava di «Christopher Banks» e «Shanghai», elementi del romanzo «Quando eravamo
  orfani» dello stesso autore, non di «Non lasciarmi» — probabile residuo della correzione di
  attribuzione già fatta in Fase 3 (quella citazione era stata spostata da un libro all'altro senza
  aggiornare il campo `context`). Corretto con la fonte giusta, che already confermava anche il
  campo `dove` esistente («narrato da Kathy H.»).

  Lasciate senza modifica per fonte insufficiente (già cercate in questo o in lotti precedenti):
  Michael Ondaatje, Susanna Tamaro, Ta-Nehisi Coates, Louisa May Alcott (nuovo passo, «Piccole
  donne» p. 2346 — Wikiquote non specifica il capitolo), Marilynne Robinson «Gilead» (la pagina
  Wikiquote riporta un incipit diverso da quello in archivio, nessuna conferma trovata per il testo
  esatto).

  **Incidente di convivenza del lotto precedente, richiamato per chiarezza**: in questo lotto ho
  verificato prima di ogni scrittura che il repository fosse sincronizzato (`git fetch` + `git
  status` pulito) sia prima di applicare le modifiche al JSON sia subito dopo il build, per evitare
  di ripetere il disallineamento capitato nel lotto 6. Nessun incidente questa volta.

  Build pulita (0 problemi). Contesti sotto le 45 parole: 514 -> 500.

- 2026-09-03 UTC — Contesti riscritti, ottavo lotto (CATALOGO.md 6-ter/6-quater): 19 citazioni
  nella fascia 20-44 parole, media 69,6 parole. Fonte aperta per ognuna prima di scrivere: Eugenio
  Montale «Ossi di seppia» (due poesie diverse: la chiusa di «Meriggiare pallido e assorto» e la
  prima strofa di «Spesso il male di vivere ho incontrato»), Emily Dickinson «Poesie» (la 254,
  «Hope is the thing with feathers»), Voltaire «Candido» (speaker Candido, ultima battuta del
  romanzo), Epitteto «Manuale» (secondo passo, cap. XVII, il teatro della vita), Torquato Tasso
  «Gerusalemme liberata» (canto III), Antoine de Saint-Exupéry «Il piccolo principe» (secondo
  passo, speaker la volpe, sulla responsabilità), Cormac McCarthy «Meridiano di sangue» (secondo
  passo, speaker il giudice Holden), Erich Maria Remarque «Niente di nuovo sul fronte occidentale»
  (speaker Paul Bäumer nel testo ma lasciato senza `speaker` perché è il narratore), Jules Verne
  «Ventimila leghe sotto i mari» (secondo passo, i ritratti nella cabina di Nemo), Nick Hornby
  «Alta fedeltà» (due passi, speaker Rob Fleming), Rainer Maria Rilke «Lettere a un giovane poeta»,
  Terry Pratchett «Il tristo mietitore» (secondo passo, i troll e il tempo), Goliarda Sapienza
  «L'arte della gioia» (quarto passo, speaker Modesta — i primi due, cap. 42 e 63, restano lasciati
  com'erano dal lotto 1), Aldous Huxley «Il mondo nuovo» (terzo passo, speaker Mustafà Mond),
  Alberto Moravia «Gli indifferenti» (incipit), Beppe Fenoglio «Una questione privata» (incipit),
  Carlo Goldoni «La locandiera» (speaker Mirandolina).

  Lasciate senza modifica per fonte insufficiente (già cercate in questo o in lotti precedenti):
  Michael Ondaatje, Susanna Tamaro, Ta-Nehisi Coates, Louisa May Alcott, Marilynne Robinson.

  **Sessione concorrente rilevata di nuovo in corso** (file `metodo.html` modificato e
  `prova_metodo.tgz` non tracciato comparsi nella working copy durante questo lotto): non toccati,
  lasciati esattamente come trovati, staging e commit limitati ai soli file miei elencati sopra —
  nessun incidente, verificato `git status` pulito prima e dopo ogni fase.

  Build pulita (0 problemi). Contesti sotto le 45 parole: 500 -> 481.

- 2026-09-03 UTC — Contesti riscritti, nono lotto (CATALOGO.md 6-ter/6-quater): 16 citazioni nella
  fascia 20-44 parole, media 71,6 parole. Fonte aperta per ognuna prima di scrivere: Roberto Bolaño
  «2666» (terzo passo, dialogo lettura/scrittura nella «parte di Archimboldi»), Erri De Luca «Il
  giorno prima della felicità» (nuovo libro in archivio per questo autore, speaker don Gaetano),
  Joseph Conrad «Cuore di tenebra» (speaker Kurtz), Karen Blixen «La mia Africa», Kazuo Ishiguro
  «Non lasciarmi» (terzo passo, la chiusa del romanzo), Michael Ende «La storia infinita», Paulo
  Coelho «L'Alchimista» (due passi, speaker Melchisedec nel primo), Viktor E. Frankl «Uno psicologo
  nei lager», Arthur Schopenhauer «Aforismi sulla saggezza del vivere», Giuseppe Tomasi di
  Lampedusa «Il Gattopardo» (due passi, speaker Tancredi e Don Fabrizio), Kurt Vonnegut «Mattatoio
  n. 5», Michail Bulgakov «Il Maestro e Margherita» (speaker Woland), Miguel de Cervantes «Don
  Chisciotte della Mancia» (speaker Don Chisciotte), Victor Hugo «Notre-Dame de Paris» (fonte
  Wikisource in francese, tradotta).

  Lasciate senza modifica per fonte insufficiente (già cercate in questo o in lotti precedenti):
  Michael Ondaatje, Susanna Tamaro, Ta-Nehisi Coates, Louisa May Alcott, Marilynne Robinson,
  Vittorio Alfieri (nuova, «Vita»: la pagina Wikisource mostra solo l'indice, non il testo del
  capitolo), Anna Maria Ortese (nuova, «Il mare non bagna Napoli»: l'incipit cercato non compare
  nella pagina Wikiquote), Philip Roth (nuovo passo su «Pastorale americana», diverso da quello già
  fatto nel lotto 6), Robert Louis Stevenson (nuova, «Lo strano caso del dottor Jekyll e del
  signor Hyde»: la confessione finale di Jekyll non è nella pagina Wikiquote).

  Build pulita (0 problemi). Contesti sotto le 45 parole: 481 -> 465.

- 2026-09-03 UTC — Contesti riscritti, decimo lotto (CATALOGO.md 6-ter/6-quater): 15 citazioni
  nella fascia 20-44 parole, media 69,9 parole. Fonte aperta per ognuna prima di scrivere (per
  quattro di queste una prima ricerca su Wikiquote non bastava, integrata con una ricerca web
  mirata al passo esatto): Zadie Smith «Denti bianchi», Zora Neale Hurston «I loro occhi
  guardavano Dio» (speaker Janie), Walt Whitman «Foglie d'erba», Aldous Huxley «Il mondo nuovo»
  (quarto passo, speaker Helmholtz Watson), Antonio Tabucchi «Sostiene Pereira», Arundhati Roy «Il
  dio delle piccole cose» (quarto passo, l'arrivo e l'annegamento di Sophie Mol), Carlo Goldoni «La
  bottega del caffè» (nuovo libro, due passi, speaker Ridolfo in entrambi), Dante Alighieri
  «Inferno» (canto I, il verso d'apertura più celebre della letteratura italiana), F. Scott
  Fitzgerald «Il grande Gatsby» (terzo passo, speaker Daisy Buchanan), Ian McEwan «Espiazione»
  (speaker Briony Tallis), Kurt Vonnegut «Mattatoio n. 5» (quarto passo, «Così va la vita»), Thomas
  Hardy «Tess dei d'Urberville», Ray Bradbury «Fahrenheit 451» (due passi, speaker Faber e il
  capitano Beatty).

  Lasciate senza modifica per fonte insufficiente (già cercate in questo o in lotti precedenti):
  Michael Ondaatje, Susanna Tamaro, Ta-Nehisi Coates, Louisa May Alcott, Marilynne Robinson,
  Vittorio Alfieri, Anna Maria Ortese, Philip Roth, Robert Louis Stevenson.

  Build pulita (0 problemi). Contesti sotto le 45 parole: 465 -> 450.

- 2026-09-03 UTC — Contesti riscritti, undicesimo lotto (CATALOGO.md 6-ter/6-quater): 12 citazioni
  nella fascia 20-44 parole, media 69,0 parole. Fonte aperta per ognuna prima di scrivere: Dante
  Alighieri («Inferno», canto V, speaker Francesca da Rimini), Douglas Adams (secondo passo, la
  scritta sulla copertina della Guida), Gustave Flaubert, Jane Austen, Nikolaj Gogol', Rainer Maria
  Rilke (terzo passo), Thomas Hardy (secondo passo, ultime righe del romanzo), Epitteto (terzo
  passo, cap. 8), Marco Aurelio, J.D. Salinger (speaker Holden Caulfield), Carlo Levi, Dino
  Buzzati.

  Lasciate senza modifica per fonte insufficiente (già cercate in questo o in lotti precedenti, più
  tre nuove): Michael Ondaatje, Susanna Tamaro, Ta-Nehisi Coates, Louisa May Alcott, Marilynne
  Robinson, Vittorio Alfieri, Anna Maria Ortese, Philip Roth, Robert Louis Stevenson, Alba de
  Céspedes (nuova, «Quaderno proibito»: la pagina Wikiquote non contiene il passo cercato), Oscar
  Wilde (nuova, «Il ritratto di Dorian Gray»: la pagina rimanda solo a un collegamento senza
  riportare il testo), Viktor E. Frankl (secondo passo, diverso da quello già fatto nel lotto 9:
  fonte con solo quattro citazioni brevi, non quella cercata).

  **Nota tecnica di convivenza**: un `git push` è fallito con un errore di lock (`cannot lock ref
  'refs/remotes/origin/main'`) mostrato *dopo* la conferma che il push era già avvenuto sul server
  (`41de394..9c3a2ca main -> main`) — segno che solo l'aggiornamento del riferimento locale di
  tracciamento era bloccato, non il push stesso. Ho aspettato, verificato con `ps aux` che nessun
  processo git fosse realmente in corso e che il lock (`refs/remotes/origin/main.lock`, dimensione
  zero) risalisse a quasi dieci minuti prima, poi l'ho rimosso: è un file tecnico di
  sincronizzazione locale, non dati né lavoro di nessuno, e la sua rimozione non tocca la working
  copy. `git fetch` successivo ha confermato che il repository era già correttamente sincronizzato.

  Build pulita (0 problemi). Contesti sotto le 45 parole: 450 -> 438.

- 2026-09-03 UTC — Contesti riscritti, dodicesimo lotto (CATALOGO.md 6-ter/6-quater): 11 citazioni
  nella fascia 20-44 parole, media 71,5 parole. Fonte aperta per ognuna prima di scrivere: Elena
  Ferrante «Storia della bambina perduta», Alba de Céspedes «Quaderno proibito» (fonte
  precedentemente insufficiente nel lotto 11, questa volta trovata con una ricerca web mirata al
  romanzo invece che a Wikiquote), James Baldwin «A Talk to Teachers» (discorso del 1963), Mario
  Rigoni Stern «Uomini, boschi e api», Olga Tokarczuk «Il mio caffè con la Szymborska»
  (un'intervista, non un romanzo), Ralph Waldo Emerson «Circoli», Wisława Szymborska «Amore a
  prima vista», Alice Munro «Il percorso dell'amore», Italo Svevo «La coscienza di Zeno» (speaker
  Zeno Cosini, ultime righe del romanzo), Rick Riordan «Percy Jackson e gli dei dell'Olimpo: il
  mare dei mostri» (speaker Ermes), Simone de Beauvoir «Memorie d'una ragazza perbene».

  Lasciate senza modifica per fonte insufficiente: Elif Shafak (nuova, «La bastarda di Istanbul»:
  la pagina Wikiquote non contiene l'incipit cercato, solo altre citazioni), Rabindranath Tagore
  (nuova, «La casa e il mondo»: nessun estratto disponibile sulla pagina), oltre alle otto già
  segnalate nei lotti precedenti.

  Build pulita (0 problemi). Contesti sotto le 45 parole: 438 -> 427.

- 2026-09-03 UTC — Contesti riscritti, tredicesimo lotto (CATALOGO.md 6-ter/6-quater): 10 citazioni
  nella fascia 20-44 parole, media 69,3 parole. Fonte aperta per ognuna prima di scrivere: Elena
  Ferrante (due libri diversi, «I giorni dell'abbandono» e «L'amica geniale»), Jack Kerouac
  «Sulla strada», William Faulkner «Luce d'agosto», Arthur Conan Doyle «Il mastino dei Baskerville»
  (speaker Sherlock Holmes), Elie Wiesel «La notte», Gabriele D'Annunzio «Il piacere», Giovanni
  Verga «I Malavoglia», Imre Kertész «Kaddish per il bambino non nato», J.K. Rowling «Harry Potter
  e la Camera dei Segreti» (speaker Albus Silente).

  Lasciata senza modifica per fonte insufficiente: James Baldwin (nuova, «La prossima volta il
  fuoco»: la pagina Wikiquote non contiene la citazione del saggio «My Dungeon Shook»), oltre alle
  dieci già segnalate nei lotti precedenti (fra cui Elif Shafak e Rabindranath Tagore, ancora
  presenti nel pool e non ritentate in questo lotto).

  Build pulita (0 problemi). Contesti sotto le 45 parole: 427 -> 417.

- 2026-09-03 UTC — Contesti riscritti, quattordicesimo lotto (CATALOGO.md 6-ter/6-quater): 6
  citazioni nella fascia 20-44 parole, media 74,7 parole. Fonte aperta per ognuna prima di
  scrivere: Mario Vargas Llosa «La città e i cani» (speaker Higueras), Salvatore Quasimodo «Ed è
  subito sera», Yukio Mishima «Confessioni di una maschera», Zbigniew Herbert «Un barbaro nel
  giardino», J.R.R. Tolkien «Lo Hobbit», Michel Houellebecq «Estensione del dominio della lotta».

  Lasciate senza modifica per fonte insufficiente: V.S. Naipaul (nuova, «Alla curva del fiume»: la
  pagina Wikiquote ha restituito errore 404), Elena Ferrante (nuovo passo su «Storia del nuovo
  cognome»: l'unica fonte nota per questa citazione, metropolitanmagazine.it, ha restituito errore
  403), Emily St. John Mandel (nuovo libro, «La musica delle parole»: pagina Wikiquote senza
  dettagli oltre l'incipit stesso), Iris Murdoch (nuova, «La ragazza italiana»: citazione confermata
  ma senza alcun contesto narrativo disponibile sulla fonte), oltre a quelle già segnalate nei lotti
  precedenti.

  Build pulita (0 problemi). Contesti sotto le 45 parole: 417 -> 411.

  **Nota di passaggio**: il pool di candidati "nuovi" risolvibili con una singola ricerca si sta
  assottigliando lotto dopo lotto (79 candidati nella fascia 20-44 parole a inizio lotto, di cui
  solo 6 effettivamente scrivibili con fonti sufficienti) — il lavoro prosegue, ma il rendimento per
  lotto è in calo naturale via via che si esauriscono i casi con fonte facilmente reperibile.

- 2026-09-03 UTC — Genere assegnato a 25 opere su 367 esaminate (CATALOGO.md 3-bis, nuovo compito
  su indicazione esplicita dell'utente: "mi aspetto qualche decina, non trecento"). Esaminate tutte
  e 367 le opere prive di genere elencate dallo script fornito, una per una, decidendo solo in base
  al contenuto/forma reale dell'opera — non un lotto timbrato. Tre commit separati (7+13+5 opere),
  build e check_links puliti dopo ognuno.

  **Conteggio per genere** (un'opera, Non lasciarmi, ne ha due): horror 6, fantasy 8, distopia 4,
  fantascienza 4, saggistica 2, poesia 2.

  **Assegnate:**
  - `horror`: Arthur Conan Doyle «Il mastino dei Baskerville», Daphne du Maurier «Rebecca, la
    prima moglie», Emily Brontë «Cime tempestose», Nathaniel Hawthorne «La casa dei sette abbaini»,
    Oscar Wilde «Il ritratto di Dorian Gray», William Shakespeare «Macbeth» — tutti romanzi/opere
    gotici classici con soprannaturale strutturale (streghe, fantasmi, patti, maledizioni), non
    semplice atmosfera cupa.
  - `fantasy`: Astrid Lindgren «I fratelli Cuordileone», Lewis Carroll «Alice» e «Attraverso lo
    specchio», Madeline Miller «Circe» e «La canzone di Achille», Michail Bulgakov «Il Maestro e
    Margherita», Roald Dahl «La fabbrica di cioccolato», William Shakespeare «La Tempesta» — mondi
    o eventi esplicitamente magici come motore della trama, non un elemento incidentale.
  - `distopia`/`fantascienza`: Doris Lessing «Memorie di una sopravvissuta», Michel Houellebecq
    «Sottomissione», Sinclair Lewis «Qui non può succedere» (distopia); Kurt Vonnegut «Ghiaccio-
    nove» e «Mattatoio n. 5», Octavia E. Butler «Legami di sangue» (fantascienza); Kazuo Ishiguro
    «Non lasciarmi» (entrambi: cloni per donazione d'organi in una società speculativa oppressiva).
  - `saggistica`: John Muir «La mia prima estate sulla Sierra», Octavio Paz «Il labirinto della
    solitudine» — testi non narrativi che argomentano, non romanzi con idee dentro.
  - `poesia`: Cesare Pavese «Verrà la morte e avrà i tuoi occhi», Fernando Pessoa «Tabacaria» —
    solo le due vere raccolte/poemi trovate nell'elenco.

  **Le 342 lasciate vuote, con motivo — la parte che conta:**
  - Realismo magico (Gabriel García Márquez «Cent'anni di solitudine», Isabel Allende «La casa
    degli spiriti», Salman Rushdie «I figli della mezzanotte»): movimento letterario distinto dal
    fantasy editoriale, mai classificato come tale in libreria — includerlo avrebbe forzato la
    distinzione che la regola vuole evitare.
  - Narrativa con elementi surreali ma letta come letteratura generale (Haruki Murakami «1Q84» e
    «Kafka sulla spiaggia», Jorge Luis Borges «Finzioni»/«L'Aleph», Julio Cortázar «Bestiario»):
    stesso principio, "fantastico" non equivale a "fantasy" di genere.
  - Fiabe con elementi magici incidentali, non un genere strutturato (Antoine de Saint-Exupéry «Il
    piccolo principe», Carlo Collodi «Pinocchio», Hans Christian Andersen «La sirenetta»): la
    differenza rispetto a «I fratelli Cuordileone» o «Alice» è che qui la magia è un espediente
    narrativo isolato, non il mondo in cui vive tutta la storia.
  - Casi sottili valutati e respinti apposta (regola 5: nel dubbio, vuoto): Toni Morrison
    «Amatissima» (un fantasma, ma il romanzo è sulla schiavitù, non horror di genere), Patrick
    Süskind «Il profumo» (la critica letteraria stessa lo dice «non riducibile a un genere unico»),
    J.M. Coetzee «Aspettando i barbari» (allegoria politica senza tempo/luogo, vicina alla
    distopia ma non lo è davvero), Fernando Pessoa «Il libro dell'inquietudine» (prosa diaristica,
    né poesia né saggio argomentativo).
  - Teatro classico interamente in versi (William Shakespeare «Amleto» e «Romeo e Giulietta»,
    Vittorio Alfieri «Mirra» e «Saul», Alessandro Manzoni «Adelchi»): scelta interpretativa
    esplicita, segnalata qui perché reversibile — la regola dice «l'opera in versi (una raccolta,
    un poema, una singola poesia)» senza nominare il teatro. Ho deciso di non estendere `poesia`
    alla sola forma versificata quando il contenuto non è anche fantasy/horror/distopia (per questo
    «La Tempesta» e «Macbeth» hanno comunque preso genere, ma per il contenuto magico/soprannaturale,
    non per essere in versi). Se l'intento era includere anche il teatro in versi puro, va corretto.
  - Tutto il resto (la grande maggioranza): romanzi realisti, storici, di formazione, gialli senza
    soprannaturale (Agatha Christie, Andrea Camilleri, Arthur Conan Doyle «Il segno dei quattro»),
    teatro in prosa (Cechov, Ibsen, Goldoni, Pirandello, Brecht) — nessuno dei sei generi si applica,
    e forzarne uno sarebbe esattamente l'errore già commesso una volta con i temi.

- 2026-09-03 UTC — Ripulita la coda dei contesti «L'incipit del romanzo» (CATALOGO.md 6-ter) e
  corretti due generi (CATALOGO.md 3-bis), su segnalazione puntuale dell'utente.

  **Contesti**: 20 dei 21 casi segnalati riscritti, fonte aperta per ognuno prima di scrivere,
  60-90 parole, media 66 parole circa. Alberto Moravia «Il conformista» e «La noia», Antoine de
  Saint-Exupéry «Volo di notte», Antonio Tabucchi «La testa perduta di Damasceno Monteiro», Charles
  Dickens «Canto di Natale» e «Grandi speranze», Elsa Morante «Menzogna e sortilegio», Grazia
  Deledda «Fior di Sardegna», Hermann Hesse «Narciso e Boccadoro», Isabel Allende «Eva Luna», Jack
  Kerouac «I sotterranei» e «I vagabondi del Dharma», José Saramago «Il racconto dell'isola
  sconosciuta», Leonardo Sciascia «Il Consiglio d'Egitto» e «Una storia semplice», Maya Angelou «Il
  canto del silenzio», Milan Kundera «L'immortalità» e «La lentezza», Philip Roth «Addio, Columbus»
  e «Zuckerman scatenato». **Lasciata com'era**: Lev Tolstoj «La morte di Ivan Il'ič» — la pagina
  Wikiquote elenca le sezioni («Incipit», «Citazioni», ecc.) ma non ne riporta il testo, quindi il
  passo cercato non era davvero apribile.

  **Generi**: tolto `horror` a due delle 25 opere classificate nei tre lotti precedenti — Arthur
  Conan Doyle «Il mastino dei Baskerville» (è un giallo: l'atmosfera gotica non fa il genere, e
  «giallo» comunque non è tra i sei ammessi) e William Shakespeare «Macbeth» (l'etichetta
  «Horror/Gotico» è editoriale e posteriore di secoli alla tragedia; streghe e fantasma non
  bastano). Le altre 23 assegnazioni restano invariate, non riesaminate in questo lotto.

  Build pulita (0 problemi) dopo entrambe le parti. Contesti sotto le 45 parole: 411 -> 391.

- 2026-09-04 UTC — Lotto 15 di riscrittura contesti (CATALOGO.md 6-ter), ripreso in autonomia
  seguendo l'ordine di `tools/contesti_da_ampliare.py` (opere con più citazioni da riscrivere,
  poi contesto più corto).

  **18 contesti riscritti**, fonte aperta per ognuno prima di scrivere, 60-90 parole: Boezio
  «Della consolazione della filosofia» (3, da Wikisource, Libro I prosa VI e Libro III prosa
  II/X), Vittorio Alfieri «Vita» (2, da Wikisource, l'incipit dell'autobiografia e l'episodio
  d'infanzia sulla paura reciproca), Michael Ondaatje «Il paziente inglese» (1: la citazione a
  p. 336 si è rivelata essere l'incipit stesso del romanzo, non un passo interno), Marilynne
  Robinson «Gilead» (1: l'incipit, aggiunto anche `speaker: John Ames` per coerenza con l'altra
  citazione dello stesso narratore già presente in archivio), Anna Maria Ortese «Il mare non
  bagna Napoli» (1, dal saggio «Chiaia morta e inquieta»), Anne Frank «Diario» (3, verificate
  sulla pagina Wikiquote primaria — nessuna data di voce disponibile per queste tre, a differenza
  dell'incipit che è datato), Natalia Ginzburg «Le piccole virtù» (1), Oscar Wilde «Il ritratto
  di Dorian Gray» (1), Gabriel García Márquez «Cent'anni di solitudine» (2: incipit e chiusa),
  Margaret Atwood «Il racconto dell'ancella» (1, l'incipit), Fëdor Dostoevskij «I fratelli
  Karamazov» (2, già con `speaker` compilato in un lotto precedente).

  **Lasciate com'erano, con motivo**: Anna Maria Ortese, la citazione «Qui, il mare non bagnava
  Napoli...» — nessun `source_url` in archivio, e una ricerca indipendente la colloca nel
  racconto «Oro a Forcella», non necessariamente all'incipit del libro come dice il campo
  `source_locus`: senza una fonte primaria da aprire, non ho scritto un contesto che avrei dovuto
  in parte inventare. Michael Ondaatje, «Tutto ciò che desideravo era camminare su una terra che
  non aveva carte geografiche» — nessun `source_url`. Marilynne Robinson, la citazione sulla
  «lunga notte che precedette questi miei giorni di felicità» — nessun `source_url`, anche se
  probabilmente fa parte dello stesso incipit dell'altra citazione riscritta in questo lotto.
  Natalia Ginzburg, «Essere capiti vuol dire...» — una ricerca ha sollevato il dubbio che
  appartenga a un'altra raccolta («Mai devi domandarmi») e non a «Le piccole virtù» come dice il
  campo `title`: non essendo compito di questo lotto correggere titoli, e non potendo scrivere un
  contesto certo su un'attribuzione incerta, l'ho lasciata. Goliarda Sapienza «L'arte della
  gioia» (2 citazioni) e Susanna Tamaro «Ascolta la mia voce» (2): nessuna fonte online porta al
  passo, solo elenchi di citazioni isolate. Louisa May Alcott «Piccole donne»: l'unica edizione
  italiana integrale reperibile online (Liber Liber) ha restituito errore 403.

  **Nota tecnica**: durante il commit, git ha bloccato le operazioni con una serie di lock file
  residui (`index.lock`, `HEAD.lock`, `packed-refs.lock`, `objects/maintenance.lock`,
  `refs/stash.lock`, `refs/heads/main.lock`, due lock sotto `refs/remotes/`) lasciati da una
  manutenzione automatica di git (`git maintenance`/gc) interrotta, non da un processo attivo:
  verificato con `ps aux` che nessun processo git fosse in esecuzione, e che i lock fossero stabili
  nel tempo. Rimossi solo quei file dopo conferma esplicita dell'utente; nessuna operazione
  distruttiva sulla cronologia o sul working tree.

  Build pulita (0 problemi), check_links a zero problemi. Contesti sotto le 45 parole: 391 -> 373.

- 2026-09-04 UTC — Lotto 16 di riscrittura contesti (CATALOGO.md 6-ter), stesso metodo del lotto
  15.

  **13 contesti riscritti**, fonte aperta per ognuno prima di scrivere, 60-90 parole: Alessandro
  Manzoni «I promessi sposi» (2, da Wikisource: l'incipit e la battuta di don Abbondio al
  cardinale, cap. XXV), Torquato Tasso «Gerusalemme liberata» (1, canto XVI, il giardino di
  Armida), Khalil Gibran «Il Profeta» (1), Ludovico Ariosto «Orlando furioso» (1, canto XXXIV,
  Astolfo sulla luna), Marco Aurelio «Colloqui con sé stesso» (1), Arthur Schopenhauer «Aforismi
  sulla saggezza del vivere» (1), Seneca «Lettere a Lucilio» (1), Ray Bradbury «Fahrenheit 451»
  (1), Charles Baudelaire «I fiori del male» (1, «L'albatro»), Sandro Veronesi «Il colibrì» (1:
  verificato che «Un filo, un Mago, tre crepe (1992-95)» è uno dei capitoli del romanzo stesso,
  non un'opera diversa come poteva sembrare dalla formattazione della fonte), Eugenio Montale
  «Ossi di seppia» (1, «Meriggiare pallido e assorto»), Toni Morrison «Amatissima» (1, la battuta
  finale di Paul D a Sethe).

  **Lasciata com'era**: Sandro Veronesi, la citazione della lettera di Luisa Lattes a Marco
  Carrera («Tu sei un colibrì perché...») — nessun `source_url` in archivio, a differenza
  dell'altra citazione dello stesso romanzo riscritta in questo lotto.

  Build pulita (0 problemi), check_links a zero problemi. Contesti sotto le 45 parole: 375 -> 360.

- 2026-09-04 UTC — Lotto 17 di riscrittura contesti (CATALOGO.md 6-ter), stesso metodo.

  **6 contesti riscritti**, fonte aperta per ognuno prima di scrivere, 60-90 parole: Dino Buzzati
  «Il deserto dei Tartari» (da Wikiquote, cap. 7), Erri De Luca «Il giorno prima della felicità»
  (da Wikiquote, p. 9), Isabel Allende «La casa degli spiriti» (da Wikiquote, cap. X), Viktor E.
  Frankl «Uno psicologo nei lager», Robert Louis Stevenson «Lo strano caso del dottor Jekyll e
  del signor Hyde» (la confessione finale, cap. X), Philip Roth «Pastorale americana» (il
  narratore Nathan Zuckerman su Seymour Levov). Questi ultimi tre non avevano `source_url` in
  archivio: verificati con una ricerca mirata sul testo esatto della citazione, che ha restituito
  in ciascun caso lo stesso passo, con capitolo o sezione, riportato da più fonti indipendenti —
  un livello di conferma che ho considerato equivalente all'apertura diretta della fonte.

  Build pulita (0 problemi), check_links a zero problemi. Contesti sotto le 45 parole: 360 -> 354.

- 2026-09-04 UTC — Lotto 18 di riscrittura contesti (CATALOGO.md 6-ter), stesso metodo.

  **6 contesti riscritti**, fonte aperta per ognuno prima di scrivere, 60-90 parole: Jack London
  «Il richiamo della foresta» (da Wikiquote, cap. III), Mark Twain «Le avventure di Huckleberry
  Finn» (l'avviso dell'autore, p. 11), Sylvia Plath «La campana di vetro» (p. 111, l'albero di
  fico), Daphne du Maurier «Rebecca, la prima moglie» (cap. 9), Giorgio Bassani «Il giardino dei
  Finzi-Contini» (parte III, cap. VI), Boris Pasternak «Il dottor Živago» (nessun `source_url` in
  archivio: verificato con una ricerca mirata sul testo esatto, riportato identico da più fonti
  indipendenti).

  Build pulita (0 problemi), check_links a zero problemi. Contesti sotto le 45 parole: 354 -> 348.

- 2026-09-04 UTC — Lotto 19 di riscrittura contesti (CATALOGO.md 6-ter), stesso metodo.

  **6 contesti riscritti**, fonte aperta per ognuno prima di scrivere, 60-90 parole: Mary Shelley
  «Frankenstein» (da Wikiquote), Zora Neale Hurston «I loro occhi guardavano Dio» (cap. XX),
  Alessandro Baricco «Novecento» (il monologo finale, nessun `source_url` in archivio ma
  verificato con ricerca mirata: il testo esatto, con la continuazione della battuta sui tasti
  del pianoforte, è confermato da più fonti), George R.R. Martin «Il Trono di Spade» (nessun
  `source_url`, stesso tipo di verifica), Michael Ende «La storia infinita» (Graograman, cap.
  XV), Niccolò Ammaniti «Io non ho paura» (p. 118).

  Build pulita (0 problemi), check_links a zero problemi. Contesti sotto le 45 parole: 348 -> 342.

- 2026-09-04 UTC — Lotto 20 di riscrittura contesti (CATALOGO.md 6-ter), stesso metodo.

  **4 contesti riscritti**, fonte aperta per ognuno prima di scrivere, 60-90 parole: Carlo
  Collodi «Le avventure di Pinocchio» (cap. XVII, la Fata dai capelli turchini; nessun
  `source_url` in archivio, verificato con ricerca mirata), Emily St. John Mandel «Stazione
  undici» (nessun `source_url`, verificato allo stesso modo), Bram Stoker «Dracula» (da
  Wikisource, cap. II), Ian McEwan «Espiazione» (da Wikiquote, p. 295).

  Build pulita (0 problemi), check_links a zero problemi. Contesti sotto le 45 parole: 342 -> 338.

- 2026-09-04 UTC — Lotto 21 di riscrittura contesti (CATALOGO.md 6-ter), stesso metodo.

  **3 contesti riscritti**, fonte aperta per ognuno prima di scrivere, 60-90 parole, tutti da
  Wikiquote: Honoré de Balzac «Papà Goriot» (p. 109), George Eliot «Middlemarch» (libro VIII,
  cap. LXXII), Günter Grass «Il tamburo di latta» (pp. 40-41).

  **Lasciata com'era, e scoperto un secondo caso come quello di Ginzburg nel lotto 15**: Lucy
  Maud Montgomery, «Avere degli amici significa vedere solo la parte migliore di loro...» — il
  campo `title` in archivio dice «Anna dai capelli rossi», ma verificando la fonte con una
  domanda mirata sulla sezione esatta della pagina Wikiquote, la citazione risulta sotto «Anna di
  Avonlea», il libro successivo. Scrivere un contesto avrebbe richiesto affermare un luogo del
  testo (cap. XIV di «Anna dai capelli rossi») che non è quello vero. Non essendo compito di
  questo lotto correggere titoli, l'ho lasciata; segnalo che le due opere di Lucy Maud Montgomery
  meriterebbero un controllo dei titoli in archivio, come già notato per Natalia Ginzburg.

  Build pulita (0 problemi), check_links a zero problemi. Contesti sotto le 45 parole: 340 -> 335.

- 2026-09-04 UTC — Lotto 22 di riscrittura contesti (CATALOGO.md 6-ter), stesso metodo.

  **3 contesti riscritti**, fonte aperta per ognuno prima di scrivere, 60-90 parole: Oscar Wilde
  «Il ritratto di Dorian Gray» (cap. II, da Wikiquote), Jane Austen «Orgoglio e pregiudizio»
  (p. 19, da Wikiquote), Fëdor Dostoevskij «Delitto e castigo» — quest'ultima aveva contesto
  completamente assente (0 parole), una delle sole due citazioni in tutto l'archivio senza
  nessun testo originale; non avendo `source_url`, verificata con una ricerca mirata che ha
  confermato il testo esatto su più fonti indipendenti, coerente con `speaker: Raskolnikov` già
  presente in archivio.

  Build pulita (0 problemi), check_links a zero problemi. Contesti sotto le 45 parole: 335 -> 333,
  contesti assenti: 2 -> 1.

- 2026-09-04 UTC — Lotto 23 di riscrittura contesti (CATALOGO.md 6-ter), stesso metodo.

  **3 contesti riscritti**, fonte aperta per ognuno prima di scrivere, 60-90 parole: Leonardo
  Sciascia «Il giorno della civetta» (nessun `source_url`, verificato con ricerca mirata; era
  l'ultimo contesto completamente assente rimasto in tutto l'archivio), Alda Merini «Mistica
  d'amore» (da Wikiquote, poesia «Magnificat», p. 97), Giovanni Pascoli «Myricae» (da Wikiquote,
  poesia «Novembre»).

  Build pulita (0 problemi), check_links a zero problemi. Contesti sotto le 45 parole: 334 -> 331,
  contesti assenti: 1 -> 0 — nessuna citazione in tutto l'archivio è più priva di contesto.

- 2026-09-04 UTC — Lotto 24 di riscrittura contesti (CATALOGO.md 6-ter), stesso metodo.

  **3 contesti riscritti**, fonte aperta per ognuno prima di scrivere, 60-90 parole: Lev Tolstoj
  «La morte di Ivan Il'ič» (l'incipit — questa citazione era rimasta senza contesto ampliato dal
  2026-09-03, quando la fonte allora collegata non riportava il testo; oggi il campo `source_url`
  in archivio punta a una pagina diversa, la voce Wikiquote generale su Tolstoj, che riporta il
  passo per intero: probabilmente aggiornato da chi lavora in parallelo su questo stesso
  archivio), Sylvia Plath «Attraversando l'acqua» (poesia «Specchio», p. 209 — diversa dalla
  raccolta «La campana di vetro» già trattata nel lotto 18), Zadie Smith «Il blues della
  biblioteca» (Internazionale, luglio 2012).

  Build pulita (0 problemi), check_links a zero problemi. Contesti sotto le 45 parole: 331 -> 328.

- 2026-09-04 UTC — Raccolte lotto 1 (CATALOGO.md 6-bis, e il punto in coda in CLAUDE.md "Le
  raccolte sono ferme alla taglia minima"): ripreso il lavoro dell'archivio partendo da
  `CATALOGO.md`, come richiesto esplicitamente dall'utente.

  Le 27 raccolte tematiche erano ferme alla soglia minima di otto citazioni da quando erano state
  pubblicate (fra il 28 agosto e il 1 settembre), mentre l'archivio nel frattempo raddoppiava:
  `tools/raccolte_da_ampliare.py` mostra 749 citazioni con solo 292 (39%) presenti in almeno una
  raccolta. Lavorate le prime 7 raccolte (escluse di proposito «frasi-brevi» e «incipit», che
  CATALOGO.md segnala come da trattare a parte perché hanno un criterio meccanico e non tematico):
  ogni candidata elencata dallo strumento è stata letta una per una, non incollata in blocco —
  molte erano falsi positivi della ricerca per parola (es. «canto» nell'invocazione epica di
  Ariosto/Tasso/Virgilio non è musica; «bella prima» in Verne è un modo di dire, non la bellezza;
  «gioco» nel «campo da gioco di Satana» di Nabokov non è infanzia).

  **32 citazioni aggiunte**: silenzio 9→10 (+1, Tolstoj), musica 8→9 (+1, Verlaine), arte 9→11
  (+2, Mishima e Hornby), infanzia 9→14 (+5, fra cui Golding e due di Murgia), sogni 8→20 (+12 —
  la raccolta più ricettiva: la sua stessa introduzione copre sia sogni nel sonno sia sogni come
  aspirazione, quindi accetta candidate come Frankl, Canetti, Conrad, Hamsun che altrove sarebbero
  state escluse), bellezza 8→13 (+5, tenendo fuori ogni «bello» puramente descrittivo — Andersen,
  Pavese, Murakami — a favore di citazioni dove la bellezza è davvero il soggetto, come Donna Tartt
  «Dio di illusioni»), lavoro 10→16 (+6, tenendo fuori gli usi metaforici di «guadagnare»/«ufficio»
  che non parlano di lavoro).

  Build pulita (0 problemi), check_links a zero problemi. Restano 20 raccolte da riprendere nello
  stesso modo, elenco e candidate sempre in `tools/raccolte_da_ampliare.py`.

  Nota di convivenza: al momento del push, `git log` mostrava lo stesso commit di partenza su
  origin (nessuna divergenza), quindi niente `pull --rebase` necessario, solo push diretto. Nella
  cartella di lavoro erano presenti modifiche non mie a `tools/generate_*`, `templates/`,
  `assets/site.css`, `metodo.html`, `privacy.html`: lasciate intatte, non incluse nel commit.

- 2026-09-04 UTC — Raccolte lotto 2, con un episodio di convivenza da segnalare, non un errore ma
  degno di nota per chi legge questo registro.

  Ripreso lo stesso lavoro (CATALOGO.md 6-bis) su altre quattro raccolte: **amicizia** (letto un
  candidato per volta, scartando gli usi vocativi di «amico» che non sono sull'amicizia — Platone,
  Cervantes, Tasso, dove è solo un modo di rivolgersi a qualcuno, non il tema della frase), **mare**
  (scartato «sul livello del mare» di Blixen e le «onde» di Alfieri, che in italiano antico è la
  congiunzione «onde» = «per cui», non le onde del mare — due false corrispondenze da ricerca per
  parola), **animali** (la raccolta più selettiva: quasi tutti i candidati erano usi metaforici di
  «bestia»/«lupo» — Sartre, Roy, un modo di dire su Vargas Llosa — non animali veri), **guerra**
  (trovato che la parola-chiave `esercit-` in `tools/raccolte_da_ampliare.py` cattura sia
  «esercito» sia «esercitare»/«esercizio»: quasi tutti i candidati di guerra erano di questo
  secondo tipo, falsi positivi — non ho toccato lo strumento, fuori dal perimetro di questo
  compito, ma lo segnalo per chi vorrà affinarlo).

  Nel momento di scrivere il lotto, un'altra sessione stava lavorando in parallelo esattamente
  sulle stesse quattro raccolte: il mio script di applicazione ha trovato tutte e venti le mie
  proposte già presenti in `data/raccolte.json` (non ancora committate), segno che le due sessioni
  erano arrivate, in autonomia, alle stesse scelte quasi parola per parola. Spostato quindi il
  lavoro su una quinta raccolta non ancora toccata, **libri-e-scrittura** (38 candidate, la più
  numerosa dopo le due escluse per criterio meccanico): **18 citazioni aggiunte**, da Baudelaire
  («Bisogna essere sempre ubriachi...») a Heaney, Hugo, Hemingway, Saba, Achebe, Lorde, Austen,
  Merini, Woolf, Sartre, Ungaretti, De Luca, Saint-Exupéry, Sinclair Lewis, Epitteto, Tamaro.
  Scartati i falsi positivi della radice `legger-`, che cattura sia «leggere» (il verbo) sia
  «leggero/leggeri/leggerezza» (il contrario di pesante) — quattro citazioni di Alcott, DeLillo,
  Hamsun e Achmatova erano di questo secondo tipo e non c'entravano nulla con la lettura.

  **L'episodio**: mentre scrivevo questo lotto, l'altra sessione ha completato il proprio lavoro
  (una funzione «il sito funziona senza JavaScript», su file che non ho toccato) e ha fatto commit
  e push prima di me. Il suo commit, arrivato mentre le mie 18 aggiunte a `data/raccolte.json`
  erano ancora scritte su disco ma non committate, le ha inglobate — la cartella di lavoro è
  condivisa fra le sessioni, quindi un commit prende quello che trova. Verificato con `git diff`
  e `git log` che **nessun dato è andato perso**: le 18 citazioni di libri-e-scrittura sono
  presenti nel commit `c775915`, insieme alle sue modifiche. Non ho corretto il commit (mai
  `amend` o `rebase` su cronologia già pubblicata): il registro corregge se stesso con una nota,
  non riscrive quello che è già successo. Build pulita e check_links a zero problemi dopo la
  verifica.

- 2026-09-04 UTC — Raccolte lotto 3: **donne** (+15, 11→26) e **famiglia** (+19, 10→29), stesso
  metodo, letture una per una — es. scartato «Donna Olimpia» di Pasolini (è un nome di via a Roma,
  non «donna» come tema) e «figlio di un tonno e di una vacca» di Primo Levi (una battuta
  scientifica sul delfino, non sulla famiglia umana). Diverse citazioni compaiono in entrambe le
  raccolte quando parlano insieme di una donna e del suo ruolo in famiglia (Ibsen, Hugo, le due
  Morante, Ginzburg, Miller).

  **Stesso episodio del lotto precedente, una seconda volta.** Mentre queste 34 aggiunte erano
  scritte su `data/raccolte.json` ma non ancora committate, un secondo commit dell'altra sessione
  («CLS della home da 0.129 a 0.013») le ha di nuovo inglobate — stessa causa, cartella di lavoro
  condivisa. Verificato di nuovo con `git show HEAD:data/raccolte.json` che **donne** e
  **famiglia** hanno rispettivamente 26 e 29 chiavi nel commit `aa54657`: nessun dato perso, di
  nuovo. Lo segnalo perché due episodi identici in una ventina di minuti non sono più una
  coincidenza isolata ma un pattern: **chi riprende questo lavoro in autonomia con `data/raccolte.json`
  aperto dovrebbe committare più spesso, a lotti più piccoli**, per ridurre la finestra in cui una
  modifica scritta su disco ma non ancora committata può finire dentro il commit di qualcun altro.
  Il dato non si perde (finisce comunque nel commit successivo), ma l'attribuzione nel registro sì,
  ed è quello che sto correggendo qui a mano.

  Build pulita, check_links a zero problemi. `index.html` e `templates/home_template.html` esclusi
  dal mio commit precedente perché mostravano una modifica in corso (non mia) sul toggle dei
  filtri; risolto poi dal commit dell'altra sessione stessa.

- 2026-09-04 UTC — Raccolte lotto 4 e 5: **natura** (+7, 21→28, senza episodi di convivenza) e poi
  **occhi-e-sguardo**: le mie 15 proposte erano di nuovo tutte già dentro (terza volta che questo
  succede sulla stessa identica raccolta scelta da entrambe le sessioni), quindi spostato il
  lavoro su **morte** (+11, 24→35): Pirandello, Faulkner, Müller, Ariosto, Fenoglio, Soyinka,
  Gibran, Whitman, Morante, Alfieri, Salinger — letti uno per uno, scartando gli idiomi («stanche
  morte» di Pavese, «colpo d'occhio» di Schopenhauer, «un cadavere attira le mosche» di Coetzee:
  nessuno di questi parla davvero di morte).

  **Terzo episodio di convivenza, di tipo diverso dai primi due.** Questa volta non un commit
  altrui che inglobava le mie modifiche non committate, ma una vera corsa sull'indice di git
  condiviso: un `git add` esplicito su 4 file miei si è ritrovato, un attimo dopo, con centinaia
  di file dell'altra sessione già in staging (il suo lavoro sui dati strutturati — `sameAs` verso
  Wikipedia/Wikidata — toccava tutte le 749 pagine citazione). Risolto con `git reset` (annulla
  solo lo stage, non tocca il working tree) e un nuovo `git add` mirato, ma anche quello è stato
  raggiunto da un commit altrui prima che riuscissi a fare il mio: verificato con `git show
  <hash>:data/raccolte.json` che **morte** e **occhi-e-sguardo** erano comunque presenti nel
  commit `7d39e0a` — di nuovo nessun dato perso. Trovato anche un effetto collaterale innocuo:
  `raccolte/occhi-e-sguardo.html` era rimasto al conteggio vecchio (9) perché quel commit non
  includeva un build successivo alla scrittura dei dati; rigenerato e committato a parte.

  Non è più un caso isolato: **due sessioni che lavorano sullo stesso `data/raccolte.json` nella
  stessa cartella, a questa cadenza di commit, si scontreranno quasi sempre.** Nessun danno finora
  — i dati arrivano comunque a destinazione — ma l'attribuzione nel registro ne risente, ed è
  quello che sto ricostruendo qui a mano ogni volta.

  Build pulita, check_links a zero problemi dopo ogni verifica.

- 2026-09-04 UTC — Raccolte lotti 6-8, ripresi su indicazione dell'utente ("gli ho chiesto di non
  intaccarti, prova") dopo che l'utente stesso ha avvertito la sessione parallela di lasciare
  spazio: da qui in avanti nessuna collisione sui contenuti, solo un paio di lock di git rimasti
  da manutenzione automatica interrotta, stessa causa già diagnosticata prima in sessione.

  **tristezza** (+17, 8→25): Dostoevskij, Pascoli («X Agosto»), David Foster Wallace, Platone,
  Foscolo, Heaney, Remarque, Iris Murdoch, Tennyson, Lispector, due di Anna Achmatova, Verga,
  Schopenhauer, Quasimodo, Octavia Butler, Verlaine («Piange nel mio cuore come piove sulla
  città»). Scartato Salinger («che l'addio sia triste o brutto non me ne importa») perché il
  soggetto è la sua indifferenza, non la tristezza, e Petrarca («triste Agatocle») perché lì
  «triste» è un epiteto arcaico per «crudele», non l'emozione.

  **cambiamento** (+15, 8→23): de Beauvoir («Donna non si nasce, lo si diventa»), Saint-Exupéry,
  Saramago, Pirandello, Steinbeck, Martin, Ondaatje, Boezio, Didion («La vita cambia in fretta»),
  Roy, due di Murgia, Baldwin, Pavese, Kundera. Scartati diversi «diverso» che in realtà
  significano «differente da», non «cambiato» (Steinbeck «Uomini e topi», Adichie, Frankl,
  Baricco «Novecento») — la stessa parola, due sensi, solo uno dei due è il tema della raccolta.

  **figli** (+11, 9→20): Maraini, Aleramo, Murgia, Hugo, le due Morante, Moravia, Ginzburg,
  Montaigne, Hoffmann («Lo Schiaccianoci», la sera di Natale in cui ai bambini Stahlbaum è
  vietato entrare in salotto), Miller. Qui il criterio più utile è stato distinguere «nascere»
  in senso esistenziale (Hesse, Merini — scartati) da «figli» come legame genitore-figlio, che è
  il tema vero della raccolta secondo la sua stessa introduzione.

  **Nota tecnica sui commit**: i lotti tristezza e cambiamento sono stati committati come solo
  `data/raccolte.json` (senza le pagine generate), perché in quel momento il resto dell'albero
  mostrava un cambio in corso non mio (CSS e generatori) che avrebbe reso ogni pagina generata
  una mescolanza non attribuibile. Le pagine sono state rigenerate e committate correttamente nel
  lotto figli, una volta che l'albero è tornato pulito.

  Build pulita, check_links a zero problemi.

- 2026-09-04 UTC — Raccolte lotti 9-11, senza episodi di convivenza (l'utente ha avvertito la
  sessione parallela di lasciare spazio a questo lavoro).

  **viaggio-e-cammino** (+11, 14→25): Harper Lee («indossare le sue scarpe»), Octavio Paz, Vasco
  Pratolini, Terry Pratchett, Ian McEwan, Boris Pasternak, T.S. Eliot («E allora andiamo, tu e
  io»), Zbigniew Herbert, Wole Soyinka, Amin Maalouf, Imre Kertész. L'introduzione della raccolta
  copre sia il viaggio letterale sia «cammino» come metafora della vita (da Dante in poi), quindi
  qui sono entrate anche le «strade» prese in senso figurato — cosa che altrove avrei scartato.

  **stelle-e-cielo** (+14, 9→23): Sciascia, Montale, Pascoli (due poesie diverse), Golding, Eliot,
  Andersen (due opere), de Beauvoir, Angelou, Rigoni Stern, Shafak, Verne, Boccaccio. Scartati
  «La libertà è come il sole» di Amado e «la libertà... dono del cielo» di Cervantes: il sole e il
  cielo lì sono paragoni per la libertà, non il soggetto della frase.

  **notte** (+17, 9→26): Calvino (l'incipit stesso, «Se una notte d'inverno...»), Moravia,
  Robinson, McCarthy, Stoker, Tokarczuk, Verga, Golding, Andersen, Herbert, Pavese, Kundera,
  Sant'Agostino («tutte le tenebre del dubbio si dissiparono», il momento della conversione),
  Sontag («La malattia è il lato notturno della vita»), Pearl S. Buck, due citazioni diverse di
  Verne sulla luna. Scartato «la villa di Fulvia... sulla città di Alba» di Fenoglio: Alba è il
  nome proprio della sua città natale, non l'alba del giorno — la ricerca per parola non distingue
  maiuscole a inizio frase da nomi propri.

  Build pulita, check_links a zero problemi dopo ogni lotto.

- 2026-09-04 UTC — Raccolte lotti 12-13, stesso metodo, nessun episodio di convivenza.

  **felicita** (+15, 9→24): Tolstoj (l'incipit di «Anna Karenina»), Baricco, Sapienza, Bolaño,
  Robinson, Tolkien («Sono felice di essere con te, Samvise Gamgee»), Stendhal («Bellezza è una
  promessa di felicità»), Boezio, DeLillo, Zola, Poe, Verga, Tabucchi, Schopenhauer, Wharton.
  Scartato «il felice ritorno delle sue navi» di Maalouf: qui «felice» significa «fortunato»,
  non l'emozione — un arcaismo che il setaccio per parola non distingue dal senso comune.

  **ricordo-e-memoria** (+10, 24→34): Pirandello, Ortese, Martin, Boccaccio, du Maurier, Ende,
  Angelou, Douglas Adams, Eliot (l'incipit di «La terra desolata», «Aprile è il mese più
  crudele... confondendo memoria e desiderio»), Tamaro. Scartato «a memoria d'uomo» di Umberto
  Eco (modo di dire, non è la memoria il soggetto della frase) e «nella silenziosa memoria di
  Dio» di Gibran (di nuovo il passo sul matrimonio, «memoria» lì è metafora dell'eternità, non
  del ricordare).

  Archivio raccolte: **56% delle 749 citazioni ora in almeno una raccolta** (era 39% a inizio
  sessione). Tutte le 27 raccolte sono state riprese almeno una volta tranne le due escluse di
  proposito (frasi-brevi, incipit — criterio meccanico, da trattare a parte come indica
  CATALOGO.md). Le candidate rimaste sono ormai poche per la maggior parte delle raccolte (2-8),
  concentrate soprattutto su libri-e-scrittura (20), natura (19), donne (14) e guerra (13).

  Build pulita, check_links a zero problemi.
