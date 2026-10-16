"""Telecharge UNE FOIS les scans HD (715 px) des cartes que l'interface agrandit,
pour ne plus dependre de Cerebro / MarvelCDB a l'usage.

Les grands visuels (`/hd/<code>`, public/js/prepare/api.js) ne servent que pour les
heros (face heros et alter ego) et les scenarios (vignette, mechants). On les demande
au moteur lui-meme : il telecharge, garde dans assets/pics-hd/ et le remet de cote.

    python3 tools/telecharger_hd.py [--serveur http://127.0.0.1:2345] [--pause 0.4]

Le moteur doit tourner. Relancable : ce qui est deja sur disque est saute.
"""
import argparse, gzip, json, os, re, sys, time, urllib.parse, urllib.request

OFFICIEL = re.compile(r'^\d{5}[a-z]?$')
RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HD = os.path.join(RACINE, 'assets', 'pics-hd')


def json_de(base, route):
    with urllib.request.urlopen(f'{base}/{route}', timeout=30) as r:
        brut = r.read()
    if brut[:2] == b'\x1f\x8b':  # le moteur compresse ses reponses JSON
        brut = gzip.decompress(brut)
    return json.loads(brut)


def ids_dans(valeur, trouves):
    if isinstance(valeur, str):
        for part in re.split(r'[,\s]+', valeur):
            if OFFICIEL.match(part):
                trouves.add(part)
    elif isinstance(valeur, list):
        for v in valeur:
            ids_dans(v, trouves)
    elif isinstance(valeur, dict):
        for v in valeur.values():
            ids_dans(v, trouves)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--serveur', default='http://127.0.0.1:2345')
    ap.add_argument('--pause', type=float, default=0.4)
    a = ap.parse_args()
    ids = set()
    for nom in json_de(a.serveur, 'list_starter_deck?'):
        nom = re.sub(r'^.*[\\/]|\.[^.]+$', '', nom)
        try:
            ids_dans(json_de(a.serveur, 'get_hero_json?' + urllib.parse.quote(nom)).get('hero'), ids)
        except Exception as e:
            print('deck ignore', nom, e)
    noms = set()
    for route in ('list_scenarios?', 'get_sets_custom_scenario?'):
        try:
            donnees = json_de(a.serveur, route)
        except Exception:
            continue
        ids_dans_noms = []
        def collecter(v):
            if isinstance(v, str):
                ids_dans_noms.append(v)
            elif isinstance(v, list):
                [collecter(x) for x in v]
            elif isinstance(v, dict):
                [collecter(x) for x in v.values()]
        collecter(donnees)
        noms.update(ids_dans_noms)
    for nom in sorted({re.sub(r'^.*[\\/]|\.[^.]+$', '', n) for n in noms}):
        try:
            sc = json_de(a.serveur, 'get_scenario_json?' + urllib.parse.quote(nom))
        except Exception:
            continue
        ids_dans({k: sc.get(k) for k in ('tileImage', 'villainCards', 'villain', 'main_scheme', 'mainScheme') if k in sc}, ids)
    ids |= {i[:-1] + 'b' for i in ids if i.endswith('a')}
    manquants = sorted(i for i in ids if not any(os.path.exists(f'{HD}/{i}{e}') for e in ('.jpg', '.webp', '.png')))
    print(f'{len(ids)} cartes candidates, {len(manquants)} HD a telecharger')
    ok = 0
    for n, i in enumerate(manquants, 1):
        try:
            urllib.request.urlopen(f'{a.serveur}/hd/{i}', timeout=40).read()
        except Exception as e:
            print('echec', i, e)
        if os.path.exists(f'{HD}/{i}.jpg'):
            ok += 1
        if n % 25 == 0:
            print(f'  {n}/{len(manquants)}')
        time.sleep(a.pause)
    print(f'{ok}/{len(manquants)} telechargees')


if __name__ == '__main__':
    sys.exit(main())
