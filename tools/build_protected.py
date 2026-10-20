"""Proposta non integrata: check/build in sola staging, audit della base pubblica.

Nessuna modalita' applica, committa, pubblica, approva o promuove una baseline.
"""
import argparse
import datetime
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

import protection_gate as gate

ROOT = Path(__file__).resolve().parent.parent


def reference(root):
    pages, _, _ = gate.site_state(root)
    match = re.search(r'var giorni = (\{[^\n]+\});', (Path(root) / 'index.html').read_text())
    gate.need(match is not None, 'Ancora calendario assente: nessuna data inventata')
    keys = json.loads(match.group(1).replace('<\\/', '</'))
    anchor = datetime.datetime.strptime(min(keys), '%Y%m%d').date() + datetime.timedelta(days=1)
    return {'home_date': anchor.isoformat(), 'related': {
        Path(p).stem: page.related for p, page in pages.items()
        if p.startswith('citazioni/') and not p.endswith('/index.html')}}


def run_worker(site, ref, worker, log_path):
    p = subprocess.run([sys.executable, '-I', str(worker), str(site), str(ref)],
                       cwd=site, capture_output=True, text=True,
                       env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
    Path(log_path).write_text(p.stdout + p.stderr)
    gate.need(p.returncode == 0, 'Build in staging fallita: ' + str(log_path))


def protected_build(root, base, manifest, *, trusted_state=gate.TRUSTED_STATE):
    checker = gate.Gate(root, trusted_state=trusted_state)
    checker.trusted_engine()  # non esegue un gate/generatore modificato dal lotto
    plan = checker.plan(base, manifest, phase='inputs')
    gate.need(not plan['global'], 'Lotto globale: solo revisione da codice fidato, nessuna esecuzione del codice candidato')
    with tempfile.TemporaryDirectory(prefix='sottolineature-bounded-') as tmp:
        tmp = Path(tmp)
        base_root, stage = tmp / 'reference', tmp / 'site'
        gate.export(root, base, base_root)
        shutil.copytree(base_root, stage)
        ref = tmp / 'reference.json'
        ref.write_text(json.dumps(reference(base_root)))
        # Sono eseguiti esclusivamente i generatori/il worker dallo stato fidato.
        for name in checker.trusted_tree:
            if name.startswith(('tools/', 'templates/')):
                target = stage / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(gate.git(root, 'show', checker.trusted + ':' + name, binary=True))
        for name in plan['manifest']['sources']:
            (stage / name).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(Path(root) / name, stage / name)
        for name in plan['manifest']['derived']:
            if gate.classification(name, checker.trusted_tree) == 'asset':
                (stage / name).parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(Path(root) / name, stage / name)
        for name in plan['manifest']['pages']['modified']:
            if name in {'metodo.html', 'privacy.html', 'affiliazioni.html', 'note-legali.html'}:
                shutil.copyfile(Path(root) / name, stage / name)
        for name in checker.trusted_tree:
            if name == gate.APPROVALS or name.startswith('protection/manifests/'):
                target = stage / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(gate.git(root, 'show', checker.trusted + ':' + name, binary=True))
        if manifest:
            (stage / manifest).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(Path(root) / manifest, stage / manifest)
        run_worker(stage, ref, stage / 'tools/protection_worker.py', tmp / 'build.log')
        result = checker.plan(base, manifest, observed_root=stage)
        result['counts'] = gate.seo_check(base_root, stage, plan['manifest'])
        gate.need(gate.filesystem(root) == plan['snapshot'], 'Lavoro concorrente: arresto, nessun file applicato')
        return {k: v for k, v in result.items() if k not in {'snapshot', 'manifest'}}


def audit_reference(root, base, report_dir):
    """Diagnostica della proposta, NON autorizzazione del lotto ne' bootstrap."""
    gate.need(base == gate.TRUSTED_STATE, 'Audit limitato al full SHA pubblico fissato dal proprietario')
    gate.full_commit(root, base)
    original = gate.filesystem(root)
    tracked = gate.tree(root, base)
    delta = gate.changed(tracked, original)
    gate.need(not delta['removed'] and set(delta['modified']) <= {'CLAUDE.md', 'LOG.md'} and
              set(delta['new']) <= gate.PROPOSAL_FILES,
              'Audit diagnostico: trovate variazioni oltre i soli nuovi file di protezione/registri')
    report_dir = Path(report_dir).resolve()
    gate.need(report_dir.is_relative_to(Path(root).resolve() / 'archivio'), 'Rapporti solo in archivio, mai tra gli output pubblici')
    gate.need(not report_dir.exists(), 'Non sovrascrivere un rapporto precedente')
    report_dir.mkdir(parents=True)
    summaries = []
    with tempfile.TemporaryDirectory(prefix='sottolineature-public-proof-') as tmp:
        tmp = Path(tmp)
        baseline = tmp / 'baseline'
        gate.export(root, base, baseline)
        baseline_files = gate.filesystem(baseline)
        ref = tmp / 'reference.json'
        frozen = reference(baseline)
        ref.write_text(json.dumps(frozen))
        for number in (1, 2):
            stage = tmp / ('build-' + str(number))
            shutil.copytree(baseline, stage)
            run_worker(stage, ref, Path(root) / 'tools/protection_worker.py', report_dir / ('build-' + str(number) + '.log'))
            result = gate.changed(baseline_files, gate.filesystem(stage))
            gate.need(not any(result.values()), 'Build non byte-identica alla base pubblica: ' + str(result))
            counts = gate.seo_check(baseline, stage, gate.empty_manifest(base))
            data = json.loads((stage / 'data/affiliazioni.json').read_text())
            quotes = json.loads((stage / 'data/citazioni.json').read_text())
            gate.need(len(quotes) == 883 and len(data['edizioni']) == 135 and
                      data['amazon_it_tracking_id'] == 'sottolineature-21', 'Conteggi/Tracking ID pubblici cambiati')
            summaries.append({'run': number, 'changes': result, 'counts': counts,
                              'quotes': len(quotes), 'editions': len(data['edizioni']),
                              'tracking_id': data['amazon_it_tracking_id']})
        gate.need(summaries[0]['counts'] == summaries[1]['counts'], 'Build non deterministiche')
        hashes = {p: x['sha256'] for p, x in baseline_files.items()}
        output_digest = gate.sha(json.dumps(hashes, sort_keys=True, separators=(',', ':')).encode())
    gate.need(gate.filesystem(root) == original, 'La diagnostica ha rilevato lavoro concorrente')
    report = {'base': base, 'branch': gate.git(root, 'branch', '--show-current'),
              'authority_granted': False, 'bootstrap_approval_present': False,
              'deterministic': True, 'all_tracked_file_hashes_digest': output_digest,
              'frozen_related_quotes': len(frozen['related']), 'runs': summaries,
              'modified_files': delta, 'applied': False, 'published': False}
    (report_dir / 'proof.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    return report


def main(root=ROOT, trusted_state=gate.TRUSTED_STATE):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['check', 'build', 'audit-reference'])
    parser.add_argument('--base', required=True)
    parser.add_argument('--manifest')
    parser.add_argument('--report-dir')
    args = parser.parse_args()
    try:
        if args.command == 'audit-reference':
            gate.need(args.report_dir is not None and args.manifest is None, 'Audit senza manifest e con rapporto separato')
            result = audit_reference(root, args.base, args.report_dir)
        elif args.command == 'build':
            result = protected_build(root, args.base, args.manifest, trusted_state=trusted_state)
        else:
            checker = gate.Gate(root, trusted_state=trusted_state)
            checker.trusted_engine()
            result = checker.verify(args.base, args.manifest)
            result = {k: v for k, v in result.items() if k not in {'snapshot', 'manifest'}}
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (gate.Rejected, OSError, ValueError, KeyError, TypeError) as error:
        raise SystemExit('PROTEZIONE: BLOCCATO — ' + str(error))


if __name__ == '__main__':
    main()
