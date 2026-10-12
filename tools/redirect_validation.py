"""Controlli bloccanti sui redirect prima di generare vercel.json."""
from pathlib import Path


IGNORED_DIRS = {'.git', 'archivio', 'assets', 'node_modules', 'templates', 'tools'}


def public_html_routes(root):
    """Restituisce gli URL puliti serviti dai file HTML pubblici del progetto."""
    root = Path(root)
    routes = set()
    for path in root.rglob('*.html'):
        relative = path.relative_to(root)
        if any(part in IGNORED_DIRS or part.startswith('.') for part in relative.parts[:-1]):
            continue
        if relative.name == 'index.html':
            parent = relative.parent.as_posix()
            routes.add('/' if parent == '.' else '/' + parent.strip('/') + '/')
        else:
            routes.add('/' + relative.with_suffix('').as_posix().strip('/') + '/')
    return routes


def redirect_chains(redirects):
    """Elenca catene e cicli, mostrando l'intero percorso coinvolto."""
    destinations = {item['from']: item['to'] for item in redirects}
    chains = []
    for source in destinations:
        path = [source]
        current = source
        seen = {source}
        while current in destinations:
            destination = destinations[current]
            path.append(destination)
            if destination in seen:
                chains.append(path)
                break
            if destination not in destinations:
                if len(path) > 2:
                    chains.append(path)
                break
            seen.add(destination)
            current = destination
    return chains


def validate_redirects(redirects, root):
    """Blocca collisioni con pagine pubbliche e redirect a piu salti."""
    sources = [item['from'] for item in redirects]
    duplicates = sorted({source for source in sources if sources.count(source) > 1})
    collisions = sorted(set(sources) & public_html_routes(root))
    chains = redirect_chains(redirects)

    problems = []
    if duplicates:
        problems.append('sorgenti duplicate: ' + ', '.join(duplicates))
    if collisions:
        problems.append('sorgenti che coincidono con pagine pubbliche: ' + ', '.join(collisions))
    if chains:
        problems.append('redirect a catena: ' + '; '.join(' -> '.join(chain) for chain in chains))
    if problems:
        raise ValueError('Redirect non validi: ' + ' | '.join(problems))

