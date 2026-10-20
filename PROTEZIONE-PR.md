# Protezione semplice delle pubblicazioni

Flusso: ramo di lavoro -> pull request verso main -> controllo obbligatorio
"SEO safety" -> merge -> Vercel produzione. Niente push diretto a main,
nessuna App aggiuntiva, chiave privata o finto consenso del proprietario.
La precedente proposta complessa 4df543a2 e' conservata solo localmente e
non fa parte di questa installazione, basata sul main pubblico 29010e3e.

## Controlli automatici

Il job confronta il full SHA base della PR con il suo head: file, hash e mode,
conteggio HTML/URL, datePublished e added, dateModified/lastmod, sitemap,
canonical/robots, configurazione redirect, slug, correlati e blocchi affiliati.
Soglie ordinarie: massimo 25 file e cinque HTML; non sono deroghe per file extra.
Ogni modifica HTML o sitemap richiede protection/change-manifest.json esatto:

```
{"version":1,"base":"FULL_BASE_SHA","reason":"Motivo concreto","files":{
  "percorso": {"before":"SHA256_o_null","after":"SHA256_o_null",
               "before_mode":"100644_o_null","after_mode":"100644_o_null"}
}}
```

Il rapporto del controllo riporta la mappa completa da verificare: non va
allargata per nascondere un output imprevisto. Il manifest non elenca se stesso;
se gia' presente, va aggiornato alla base e ai file della PR corrente. Le date
iniziali/slug non si cambiano. Un semplice aggiornamento di date senza contenuto
reale e' un errore, anche con approvazione. Canonical/robots/sitemap/redirect o
componenti eseguibili condivisi richiedono l'eccezione esplicita qui sotto.

Seguono due build in copie temporanee, calendario e correlati ancorati alla
baseline pubblicata. Ogni byte generato deve coincidere con gli artefatti della
PR; nessun output viene applicato al checkout. Validatori strutturali/link,
sitemap/immagini e JSON-LD e tutta la suite esistente devono passare. Gli errori
di build/test e le invarianti rigide non possono essere approvati via override.

Il guard, il parser e la dipendenza hash-locked sono caricati dalla base main
della PR, non dal nuovo guard proposto. Unica inizializzazione: base esatta
29010e3e, guard ancora assente e soltanto la lista di file tecnici di bootstrap
nel codice, senza HTML/dati/SEO. Questa inizializzazione e' autorizzata dal
proprietario e non approva modifiche future.

## Eccezione trasparente del proprietario

Se il controllo segnala un impatto globale intenzionale, fermarsi, verificare
il rapporto e chiedere al proprietario. Solo lui puo' scrivere nella PR:

```
/seo-override FULL_HEAD_SHA IMPACT_SHA256 Motivo esplicito di almeno dieci caratteri
```

Poi rieseguire il job fallito dalla pagina Actions della PR. Il controllo legge
i commenti, non ne scrive: login giantroisi, tipo User, associazione OWNER,
SHA e digest dell'intero impatto devono coincidere. Nessun flag, label o file
del candidato crea approvazioni. Una modifica successiva invalida il consenso.
ID/URL del commento, motivo, impronta e finding sono registrati nei log e nel
riepilogo della run. Riportarli anche in LOG.md al completamento. Un agente non
e' autorizzato a scrivere per il proprietario un consenso che non ha ricevuto.

## GitHub e Vercel

Main richiede PR, ramo aggiornato e check SEO safety dell'App standard GitHub
Actions (ID verificato 15368), applicato anche agli amministratori; force-push
ed eliminazione disabilitati. Zero approvazioni formali di un secondo reviewer:
il proprietario e' l'unico gestore e non puo' auto-approvare una review GitHub.
L'unione resta una sua azione esplicita o un'azione dell'agente autorizzata per
quel lotto; non e' abilitato l'auto-merge. Leggere le impostazioni effettive prima
di dichiarare attiva la protezione. Se il piano/accesso non lo permette, fermarsi.

Vercel mantiene l'integrazione Git: preview sui rami/PR, produzione soltanto
dal main dopo il merge. Non cambiare domini, canonical, accesso o contenuti.
Non usare la CLI per pubblicare direttamente in produzione aggirando la PR.

Limite esplicito: e' una protezione pratica contro errori e cambiamenti inattesi,
NON un'autorita' crittografica indipendente. Un amministratore puo' modificare
regole, workflow o credenziali; il nome/app standard di un check non distingue
workflow ostili intenzionalmente omonimi. Modificare quei controlli richiede
revisione esplicita del proprietario; non dichiarare impossibili tali bypass.

## IndexNow

Nessun trigger push, preview, build o deploy invia URL. Il solo workflow manuale
su main richiede attore proprietario, SHA esatto, lista JSON di URL e conferma
esplicita (false per default). Prima dell'unica richiesta verifica main corrente,
PR unita su main, deploy Vercel Production concluso con successo e URL realmente
presenti nella sitemap canonica. Il flag generico production_environment di GitHub
non e' affidabile per Vercel: si controllano ambiente Production e autore/stato
vercel[bot]. Qualunque dato ambiguo blocca l'invio. Nessun retry automatico o invio
a GSC; questa installazione e i suoi test non inviano alcun URL.
