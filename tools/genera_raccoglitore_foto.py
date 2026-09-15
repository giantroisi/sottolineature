#!/usr/bin/env python3
"""Scrive la paginetta che raccoglie le foto degli autori dal browser.

Perche' dal browser e non da qui: Wikimedia (wikidata.org, commons.wikimedia.org,
upload.wikimedia.org) e' irraggiungibile sia dalla shell della sessione Claude
sia da quella sul Mac - provate, rispondono tutte `000`. E' la stessa strada gia'
percorsa per le copertine a settembre: la pagina gira nel browser dell'utente,
scarica, verifica e impacchetta tutto in un file solo.

Uso:
    python3 tools/genera_raccoglitore_foto.py
    open archivio/raccogli-foto-autori.html

La pagina scrive in ~/Downloads un `foto-autori.tar` con dentro le immagini e un
`manifest.json` con, per ciascuna: autore, file, impronta SHA-256, licenza,
autore della fotografia, indirizzo del file su Commons. Da li' le riprende la
sessione, che verifica le impronte e le mette in pagina.

Regola di ammissione, e non si deroga: entra solo il file con **licenza libera
dichiarata** (pubblico dominio, CC0, CC BY, CC BY-SA). Fuori tutto il resto:
licenza assente, «fair use», o campo `Restrictions` non vuoto (che su Commons
segnala marchi, diritti d'immagine, vincoli d'uso). Dove non c'e' una foto
pulita l'autore resta senza: un vuoto e' meglio di un credito sbagliato.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USCITA = os.path.join(ROOT, 'archivio', 'raccogli-foto-autori.html')

PAGINA = r"""<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8">
<title>Raccolta foto autori — Sottolineature</title>
<style>
  body { font: 15px/1.6 -apple-system, system-ui, sans-serif; max-width: 62rem;
         margin: 2rem auto; padding: 0 1.5rem; color: #211f1b; background: #f2f0eb; }
  h1 { font-size: 1.4rem; }
  button { font: inherit; padding: 0.7rem 1.4rem; border: 1px solid #33523f;
           background: #33523f; color: #f2f0eb; border-radius: 999px; cursor: pointer; }
  button.secondario { background: none; color: #33523f; }
  button[disabled] { opacity: 0.45; cursor: default; }
  #stato { margin: 1.5rem 0; font-variant-numeric: tabular-nums; }
  table { border-collapse: collapse; width: 100%; font-size: 0.85rem; margin-top: 1.5rem; }
  td, th { text-align: left; padding: 0.35rem 0.6rem; border-bottom: 1px solid #ddd9cf; vertical-align: top; }
  .no { color: #8a4b2a; }
  .si { color: #33523f; }
  code { background: #e8e5dd; padding: 0.1rem 0.3rem; border-radius: 3px; }
</style>
</head>
<body>
<h1>Raccolta delle foto degli autori</h1>
<p>Chiede a Wikidata quale immagine e' associata a ciascun autore, chiede a Wikimedia
Commons la licenza di quell'immagine, <strong>scarta tutto cio' che non ha una licenza
libera dichiarata</strong>, scarica le altre a 600px di lato lungo, ne calcola l'impronta
SHA-256 e impacchetta tutto in un <code>foto-autori.tar</code>.</p>
<p>Non ritaglia e non modifica le immagini: le ridimensiona soltanto. Il ritaglio, dove
serve, lo fa il foglio di stile del sito, che non tocca il file.</p>
<p>
  <button id="prova">Prova con i primi 10</button>
  <button id="tutti" class="secondario">Tutti e __QUANTI__</button>
  <button id="mancanti" class="secondario">Solo i __MANCANTI__ senza ritratto</button>
</p>
<div id="stato">Pronto.</div>
<div id="esito"></div>

<script>
const AUTORI = __ELENCO__;

// Licenze ammesse: pubblico dominio, CC0, CC BY, CC BY-SA (qualunque versione).
// Il campo `License` di Commons e' la forma leggibile a macchina: "pd", "cc0",
// "cc-by-4.0", "cc-by-sa-3.0", "fair use"...
function licenzaAmmessa(m) {
  const lic = ((m.License && m.License.value) || '').toLowerCase().trim();
  if (!lic) return [false, 'licenza non dichiarata'];
  if (lic.indexOf('fair') === 0 || lic.indexOf('non-free') >= 0) return [false, 'non libera: ' + lic];
  const ok = lic === 'cc0' || lic.indexOf('pd') === 0 || lic.indexOf('cc-by') === 0;
  if (!ok) return [false, 'licenza non in elenco: ' + lic];
  // Il campo `Restrictions` di Commons non parla di copyright: avverte che
  // sull'immagine gravano altri diritti. `personality` sono i diritti della
  // persona ritratta - niente pubblicita', niente uso che faccia sembrare
  // un'approvazione - e l'uso editoriale con il credito, che e' il nostro, e'
  // esattamente quello che quel marchio prevede (decisione dell'utente del
  // 2026-09-15). Tutte le altre restrizioni - marchi, insegne, valute, disegni
  // industriali, costumi - restano un no.
  const restr = ((m.Restrictions && m.Restrictions.value) || '').replace(/<[^>]+>/g, ' ').trim();
  if (restr) {
    const voci = restr.split(/[|,;]+/).map(v => v.trim().toLowerCase()).filter(Boolean);
    const vietate = voci.filter(v => v !== 'personality');
    if (vietate.length) return [false, 'restrizioni dichiarate: ' + vietate.join(', ').slice(0, 60)];
  }
  return [true, lic];
}

function testo(html) {
  if (!html) return '';
  const d = document.createElement('div');
  d.innerHTML = html;
  return (d.textContent || '').replace(/\s+/g, ' ').trim();
}

async function api(base, params) {
  const u = new URL(base);
  Object.keys(params).forEach(k => u.searchParams.set(k, params[k]));
  u.searchParams.set('format', 'json');
  u.searchParams.set('origin', '*');
  const r = await fetch(u.toString());
  if (!r.ok) throw new Error(base + ' -> ' + r.status);
  return r.json();
}

async function impronta(buf) {
  const h = await crypto.subtle.digest('SHA-256', buf);
  return Array.from(new Uint8Array(h)).map(b => b.toString(16).padStart(2, '0')).join('');
}

// --- TAR (ustar), scritto a mano: nessuna libreria da caricare ---------------
function blocco(nome, dati) {
  const intestazione = new Uint8Array(512);
  const enc = new TextEncoder();
  const scrivi = (s, off, len) => { const b = enc.encode(s); for (let i = 0; i < Math.min(b.length, len); i++) intestazione[off + i] = b[i]; };
  scrivi(nome, 0, 100);
  scrivi('0000644', 100, 7);
  scrivi('0000000', 108, 7);
  scrivi('0000000', 116, 7);
  scrivi(dati.length.toString(8).padStart(11, '0'), 124, 11);
  scrivi(Math.floor(Date.now() / 1000).toString(8).padStart(11, '0'), 136, 11);
  for (let i = 148; i < 156; i++) intestazione[i] = 32;
  scrivi('0', 156, 1);
  scrivi('ustar', 257, 5);
  scrivi('00', 263, 2);
  let somma = 0;
  for (let i = 0; i < 512; i++) somma += intestazione[i];
  scrivi(somma.toString(8).padStart(6, '0') + '\0 ', 148, 8);
  const coda = new Uint8Array((512 - (dati.length % 512)) % 512);
  return [intestazione, dati, coda];
}

function faiTar(voci) {
  let pezzi = [];
  voci.forEach(v => { pezzi = pezzi.concat(blocco(v.nome, v.dati)); });
  pezzi.push(new Uint8Array(1024));
  return new Blob(pezzi, { type: 'application/x-tar' });
}

const stato = document.getElementById('stato');
const esito = document.getElementById('esito');

async function raccogli(elenco) {
  ['prova', 'tutti', 'mancanti'].forEach(id => { document.getElementById(id).disabled = true; });
  const righe = [];
  const file = [];
  try {
    // 1. Wikidata: qual e' l'immagine di questo autore (proprieta' P18)
    stato.textContent = 'Chiedo a Wikidata le immagini di ' + elenco.length + ' autori...';
    const perQid = {};
    for (let i = 0; i < elenco.length; i += 50) {
      const fetta = elenco.slice(i, i + 50);
      const d = await api('https://www.wikidata.org/w/api.php', {
        action: 'wbgetentities', ids: fetta.map(a => a.qid).join('|'), props: 'claims',
      });
      fetta.forEach(a => {
        const e = d.entities && d.entities[a.qid];
        const c = e && e.claims && e.claims.P18 && e.claims.P18[0];
        const nome = c && c.mainsnak && c.mainsnak.datavalue && c.mainsnak.datavalue.value;
        if (nome) perQid[a.qid] = nome;
      });
      stato.textContent = 'Wikidata: ' + Math.min(i + 50, elenco.length) + '/' + elenco.length;
    }

    // 2. Commons: licenza, autore della foto, indirizzo della miniatura
    const senzaFoto = elenco.filter(a => !perQid[a.qid]);
    const conFoto = elenco.filter(a => perQid[a.qid]);
    const info = {};
    for (let i = 0; i < conFoto.length; i += 50) {
      const fetta = conFoto.slice(i, i + 50);
      const titoli = fetta.map(a => 'File:' + perQid[a.qid]).join('|');
      const d = await api('https://commons.wikimedia.org/w/api.php', {
        action: 'query', titles: titoli, prop: 'imageinfo',
        iiprop: 'url|extmetadata|mime|size', iiurlwidth: '600', iiextmetadatalanguage: 'it',
      });
      const pagine = (d.query && d.query.pages) || {};
      const perTitolo = {};
      Object.keys(pagine).forEach(k => { perTitolo[pagine[k].title] = pagine[k]; });
      fetta.forEach(a => { info[a.qid] = perTitolo['File:' + perQid[a.qid]]; });
      stato.textContent = 'Commons: ' + Math.min(i + 50, conFoto.length) + '/' + conFoto.length;
    }

    senzaFoto.forEach(a => righe.push({ autore: a.autore, ok: false, motivo: 'nessuna immagine su Wikidata' }));

    // 3. scarico solo quelle ammesse, una alla volta, con l'impronta
    let n = 0;
    for (const a of conFoto) {
      n++;
      stato.textContent = 'Scarico ' + n + '/' + conFoto.length + ': ' + a.autore;
      const p = info[a.qid];
      const ii = p && p.imageinfo && p.imageinfo[0];
      if (!ii) { righe.push({ autore: a.autore, ok: false, motivo: 'file non trovato su Commons' }); continue; }
      const m = ii.extmetadata || {};
      const [ammessa, perche] = licenzaAmmessa(m);
      if (!ammessa) { righe.push({ autore: a.autore, ok: false, motivo: perche, file: p.title }); continue; }
      if ((ii.mime || '').indexOf('image/') !== 0 || (ii.mime || '').indexOf('svg') >= 0) {
        righe.push({ autore: a.autore, ok: false, motivo: 'formato non adatto: ' + ii.mime }); continue;
      }
      const url = ii.thumburl || ii.url;
      let buf;
      try {
        const r = await fetch(url);
        if (!r.ok) throw new Error(r.status);
        buf = await r.arrayBuffer();
      } catch (e) {
        righe.push({ autore: a.autore, ok: false, motivo: 'scaricamento fallito: ' + e.message }); continue;
      }
      const sha = await impronta(buf);
      const est = (ii.mime === 'image/png') ? '.png' : '.jpg';
      const nomeFile = a.slug + est;
      file.push({ nome: 'foto/' + nomeFile, dati: new Uint8Array(buf) });
      righe.push({
        autore: a.autore, ok: true, file: nomeFile, sha256: sha, byte: buf.byteLength,
        licenza_codice: ((m.License && m.License.value) || '').toLowerCase(),
        licenza_nome: testo(m.LicenseShortName && m.LicenseShortName.value) || '',
        licenza_url: (m.LicenseUrl && m.LicenseUrl.value) || '',
        fotografo: testo(m.Artist && m.Artist.value) || '',
        credito: testo(m.Credit && m.Credit.value) || '',
        restrizioni: ((m.Restrictions && m.Restrictions.value) || '').replace(/<[^>]+>/g, ' ').trim(),
        pagina_commons: ii.descriptionurl || '',
        file_commons: p.title || '',
        larghezza: ii.thumbwidth || ii.width, altezza: ii.thumbheight || ii.height,
      });
      await new Promise(r => setTimeout(r, 120));
    }

    file.push({ nome: 'manifest.json', dati: new TextEncoder().encode(JSON.stringify(righe, null, 1)) });
    const tar = faiTar(file);
    const a = document.createElement('a');
    a.href = URL.createObjectURL(tar);
    a.download = 'foto-autori.tar';
    a.click();

    const ok = righe.filter(r => r.ok).length;
    stato.innerHTML = '<strong>Fatto.</strong> ' + ok + ' foto ammesse su ' + righe.length +
      ' autori. Il file <code>foto-autori.tar</code> e\' in Download.';
    esito.innerHTML = '<table><tr><th>Autore</th><th>Esito</th><th>Licenza / motivo</th><th>Fotografo</th></tr>' +
      righe.map(r => '<tr><td>' + r.autore + '</td><td class="' + (r.ok ? 'si">ammessa' : 'no">scartata') +
        '</td><td>' + (r.ok ? (r.licenza_nome || r.licenza_codice) : r.motivo) + '</td><td>' +
        (r.fotografo || '') + '</td></tr>').join('') + '</table>';
  } catch (e) {
    stato.innerHTML = '<span class="no">Errore: ' + e.message + '</span>';
  }
  ['prova', 'tutti', 'mancanti'].forEach(id => { document.getElementById(id).disabled = false; });
}

document.getElementById('prova').onclick = () => raccogli(AUTORI.slice(0, 10));
document.getElementById('tutti').onclick = () => raccogli(AUTORI);
document.getElementById('mancanti').onclick = () => raccogli(AUTORI.filter(a => !a.gia));
</script>
</body>
</html>
"""


def main():
    with open(os.path.join(ROOT, 'data', 'autori_sameas.json'), encoding='utf-8') as f:
        sameas = json.load(f)
    with open(os.path.join(ROOT, 'tools', 'slugs.json'), encoding='utf-8') as f:
        slugs = json.load(f).get('authors', {})
    with open(os.path.join(ROOT, 'data', 'citazioni.json'), encoding='utf-8') as f:
        d = json.load(f)
    quotes = d if isinstance(d, list) else d['citazioni']
    in_archivio = []
    visti = set()
    for q in quotes:
        a = q['author']
        if a in visti:
            continue
        visti.add(a)
        wd = (sameas.get(a) or {}).get('wikidata') or ''
        qid = wd.rstrip('/').split('/')[-1] if wd else ''
        slug = slugs.get(a)
        if qid and slug:
            in_archivio.append({'autore': a, 'slug': slug, 'qid': qid})
    # chi il ritratto ce l'ha gia' si segna, cosi' un secondo giro puo' chiedere
    # solo quelli che mancano invece di riscaricare tutto
    try:
        with open(os.path.join(ROOT, 'data', 'autori_foto.json'), encoding='utf-8') as f:
            gia_fatti = set(json.load(f))
    except (IOError, ValueError):
        gia_fatti = set()
    for voce in in_archivio:
        voce['gia'] = voce['autore'] in gia_fatti
    mancanti = sum(1 for v in in_archivio if not v['gia'])
    pagina = PAGINA.replace('__ELENCO__', json.dumps(in_archivio, ensure_ascii=False))
    pagina = pagina.replace('__QUANTI__', str(len(in_archivio)))
    pagina = pagina.replace('__MANCANTI__', str(mancanti))
    os.makedirs(os.path.dirname(USCITA), exist_ok=True)
    with open(USCITA, 'w', encoding='utf-8') as f:
        f.write(pagina)
    print(len(in_archivio), 'autori con identificativo Wikidata e slug')
    print('scritto', USCITA)


if __name__ == '__main__':
    main()
