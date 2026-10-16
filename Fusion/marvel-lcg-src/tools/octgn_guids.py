"""Table GUID OCTGN -> code de carte, pour l'import des fichiers .o8d.

Un .o8d nomme chaque carte par un identifiant OCTGN (un GUID). MarvelCDB le publie
dans le champ `octgn_id` de chaque carte ; on en tire une table, rangee dans
data/octgn_guids.json et lue par le navigateur (public/js/marvelcdb/octgn.js).
Les cartes sans GUID chez MarvelCDB, et celles des modules maison, se retrouvent
par leur nom (voir octgn.js).

    python3 tools/octgn_guids.py
"""
import json, os, urllib.request

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, 'data', 'octgn_guids.json')
SOURCES = ['https://marvelcdb.com/api/public/cards/', 'https://mc4db.merlindumesnil.net/api/public/cards/']


def main():
    table = {}
    for url in SOURCES:
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=90) as r:
                cartes = json.load(r)
        except Exception as e:
            print('source ignoree', url, e)
            continue
        n = 0
        for c in cartes:
            guid = (c.get('octgn_id') or '').lower()
            if guid and c.get('code') and guid not in table:
                table[guid] = c['code']
                n += 1
        print(f'{url} : {n} identifiants ajoutes')
    with open(SORTIE, 'w', encoding='utf-8') as f:
        json.dump(dict(sorted(table.items())), f, ensure_ascii=False, indent=0)
    print(len(table), 'identifiants ->', SORTIE)


if __name__ == '__main__':
    main()
