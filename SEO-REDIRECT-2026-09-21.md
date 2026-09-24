# Redirect: un errore vero e una catena da appiattire

Data: 21 settembre 2026. Verificato sul sito pubblicato e su vercel.json.

Il 20 settembre Search Console ha segnalato su sottolineature un motivo
nuovo di mancata indicizzazione: «Errore di reindirizzamento». Controllati
tutti i 23 redirect di slug in vercel.json: nessun loop, tutti arrivano a
una pagina 200. Ma ci sono due difetti, e il primo è un bug di contenuto.

## 1. Accabadora: una citazione vera nascosta da un redirect vecchio

- Esiste la pagina /citazioni/michela-murgia-accabadora/, generata dalla
  citazione «Fillus de anima. È così che…» (Michela Murgia, Accabadora).
- La pagina è in sitemap-citazioni.xml.
- Ma tools/redirects.json (e quindi vercel.json) contiene ancora:
      /citazioni/michela-murgia-accabadora/ -> /citazioni/michela-murgia-chiru/
- Su Vercel i redirect vengono valutati PRIMA dei file statici: quindi la
  pagina Accabadora è irraggiungibile, e chi la apre — persone e Google —
  finisce su un'altra citazione, di un altro libro (Chirù).

Probabile origine: lo slug «accabadora» era stato reindirizzato quando una
citazione fu riattribuita; poi una citazione nuova da Accabadora ha
ricevuto di nuovo lo stesso slug, e il redirect vecchio se l'è presa.

INTERVENTO:
- togliere da tools/redirects.json la voce
  /citazioni/michela-murgia-accabadora/ -> /citazioni/michela-murgia-chiru/
- rigenerare con build.py (che riscrive vercel.json)

## 2. Pessoa: una catena di due salti

    /citazioni/fernando-pessoa-il-libro-dell-inquietudine/
        -> /citazioni/fernando-pessoa-tabacaria/
        -> /autori/fernando-pessoa/

Nata col commit 3e95a9d7, che ha tolto la citazione da «Tabacaria» e ha
aggiunto il secondo redirect senza aggiornare il primo. Funziona, ma è una
catena: ogni salto in più è scansione sprecata.

INTERVENTO: in tools/redirects.json far puntare il primo direttamente a
/autori/fernando-pessoa/. Il secondo resta.

## 3. Il controllo che impedisce che ricapiti

In tools/build.py, prima di scrivere vercel.json, aggiungere due controlli
che fanno FALLIRE il build (non solo avvisare):

- una sorgente di redirect coincide con una pagina che il build sta
  generando  -> errore, con il nome dello slug
- la destinazione di un redirect è a sua volta sorgente di un altro
  redirect (catena)  -> errore, con la catena completa

Sono esattamente i due casi di sopra: con questi controlli nessuno dei due
sarebbe andato online.

## Verifica

1. build.py chiude con 0 problemi, check_links 0, controlla_jsonld 0.
2. Sul sito pubblicato /citazioni/michela-murgia-accabadora/ risponde 200,
   senza redirect, e mostra la citazione di Accabadora.
3. /citazioni/fernando-pessoa-il-libro-dell-inquietudine/ arriva a
   /autori/fernando-pessoa/ con UN solo salto.
4. Aggiungere a mano, in prova, un redirect la cui sorgente è una pagina
   esistente: il build deve fermarsi. Poi toglierlo.
5. Ricordare: l'HTML generato è tracciato in git e Vercel non fa build.

## Nota

Non è detto che questi due siano gli URL segnalati da Search Console come
«Errore di reindirizzamento»: quel motivo di solito indica un loop o una
catena troppo lunga, e qui non ce ne sono. Gli URL esatti si vedono
aprendo quella riga in Indicizzazione → Pagine. Ma il primo è comunque un
errore vero, e va corretto a prescindere.

---

## Aggiornamento, stessa sera: la causa dell'«Errore di reindirizzamento»

Aperta la riga in Search Console. Gli URL segnalati sono tre, tutti
scansionati il 15 settembre:

    https://sottolineature.it/opere/eugenio-montale-ossi-di-seppia
    https://sottolineature.it/opere/italo-calvino-le-citta-invisibili
    https://sottolineature.it/opere/franz-kafka-la-metamorfosi

**Mancano tutti e tre della barra finale.** Sono gli URL passati per la
richiesta manuale di indicizzazione del 14 settembre, scritti senza «/».
Il sito fa correttamente redirect da /opere/x a /opere/x/, e un URL
inviato per l'indicizzazione che fa redirect viene segnalato così.

**Il sito non ha niente di sbagliato su questo punto.** Le pagine vere,
con la barra, rispondono 200. L'errore è nell'indirizzo inviato, non
nella pagina.

Accabadora e Pessoa NON c'entrano con la segnalazione — restano però
difetti veri e gli interventi 1, 2 e 3 qui sopra valgono lo stesso.

Regola per chi prepara le liste di richieste manuali: su sottolineature
ogni URL finisce con «/». Su oratorna no. Su dietroiltesto sì, e con www.
