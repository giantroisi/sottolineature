"""Launcher: carica il gate DAL COMMIT FIDATO, mai dal lotto candidato.

La forma autorevole e' eseguire anche questo launcher con git show dal pin
indicato dal proprietario. Il pin non e' un flag, un ref simbolico o una env.
Ora il bootstrap e' intenzionalmente chiuso: ec9287e4 non contiene il gate.
"""
import importlib.util
from pathlib import Path
import re
import subprocess
import sys
import tempfile

TRUSTED_STATE = 'ec9287e4c9038b53c93219168e77bcffbc4f215b'
MODULES = ('protection_gate.py', 'protection_worker.py', 'build_protected.py')


def load_trusted(root, pin=TRUSTED_STATE):
    """pin e' una dipendenza del launcher/test, non e' accettato dalla CLI."""
    root = Path(root).resolve()
    if not isinstance(pin, str) or not re.fullmatch('[0-9a-f]{40}', pin):
        raise ValueError('Pin fidato non valido')
    def git(*args):
        p = subprocess.run(['git', '-C', str(root), *args], capture_output=True)
        if p.returncode:
            raise ValueError('Bootstrap assente/base fidata non valida: serve approvazione separata')
        return p.stdout
    if git('rev-parse', '--verify', pin + '^{commit}').decode().strip() != pin:
        raise ValueError('Pin non commit')
    git('merge-base', '--is-ancestor', pin, 'HEAD')
    # Si raccolgono tutti i blob PRIMA di qualsiasi import del codice locale.
    blobs = {name: git('show', pin + ':tools/' + name) for name in MODULES}
    with tempfile.TemporaryDirectory(prefix='sottolineature-trusted-code-') as tmp:
        for name, data in blobs.items():
            (Path(tmp) / name).write_bytes(data)
        old_path = list(sys.path)
        old_modules = {k: sys.modules.get(k) for k in ('protection_gate', 'protection_worker', 'build_protected')}
        try:
            for name in old_modules:
                sys.modules.pop(name, None)
            sys.path.insert(0, tmp)
            spec = importlib.util.spec_from_file_location('trusted_protected_build', Path(tmp) / 'build_protected.py')
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            module.main(root=root, trusted_state=pin)
        finally:
            sys.path[:] = old_path
            for name, old in old_modules.items():
                if old is None:
                    sys.modules.pop(name, None)
                else:
                    sys.modules[name] = old


if __name__ == '__main__':
    # --root e' solo il checkout da controllare; non sceglie autorita' o baseline.
    try:
        if len(sys.argv) < 3 or sys.argv[1] != '--root':
            raise ValueError('Uso: launcher --root CHECKOUT check|build --base FULL_SHA ...')
        workspace = sys.argv[2]
        sys.argv = [sys.argv[0], *sys.argv[3:]]
        if sys.argv[1:2] == ['audit-reference']:
            raise ValueError('La diagnostica della proposta non e\' un comando autorevole')
        load_trusted(workspace)
    except (ValueError, OSError) as error:
        raise SystemExit('PROTEZIONE: BLOCCATO — ' + str(error))
