"""Verifie que chaque campagne a les pages de livret qu'elle declare, et qu'elles s'ouvrent.

    python3 tools/verifier_pages_campagnes.py

Pour chaque `data/campagnes/*.json` : toutes les planches citees (regles, intro, epilogue, vilains, expert) existent dans
`public/stories/<code>/` (et `fr/` si la campagne declare `livret_fr`), s'ouvrent comme image, ne sont pas minuscules ;
aucune planche orpheline. Signale (sans echouer) les campagnes sans couverture ou sans aucune planche : ce sont des boites
portees sans livret (web_of_deceit, galactic_storm pour la couverture). Code de sortie non nul s'il manque une planche citee.
"""
import glob
import json
import os
import sys

from PIL import Image

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLES = ('pages_regles', 'pages_intro', 'pages_expert', 'pages_vilains', 'intro', 'regles', 'epilogue')


def collecter(o, acc):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in CLES and isinstance(v, list):
                acc.extend([x if isinstance(x, str) else x.get('fichier') for x in v])
            else:
                collecter(v, acc)
    elif isinstance(o, list):
        for x in o:
            collecter(x, acc)


def main():
    erreurs, notes, lues = [], [], 0
    for chemin in sorted(glob.glob(os.path.join(RACINE, 'data', 'campagnes', '*.json'))):
        d = json.load(open(chemin, encoding='utf-8'))
        code = d['code']
        pages = []
        collecter(d, pages)
        pages = [p for p in dict.fromkeys(pages) if p]
        base = os.path.join(RACINE, 'public', 'stories', code)
        dossiers = [base] + ([os.path.join(base, 'fr')] if d.get('livret_fr') else [])
        if not pages:
            notes.append(f"{code} : aucune planche declaree (boite sans livret)")
        if not os.path.exists(os.path.join(base, '00-couverture.jpg')):
            notes.append(f"{code} : pas de couverture (repli sur l'illustration d'extension)")
        for dos in dossiers:
            for nom in pages:
                p = os.path.join(dos, nom)
                if not os.path.exists(p):
                    erreurs.append(f"{code} : planche ABSENTE {os.path.relpath(p, RACINE)}")
                    continue
                try:
                    im = Image.open(p)
                    im.load()
                    lues += 1
                    if min(im.size) < 300:
                        erreurs.append(f"{code} : planche minuscule {nom} {im.size}")
                except Exception as e:
                    erreurs.append(f"{code} : planche illisible {nom} ({e})")
        orphelines = [] if not os.path.isdir(base) else [x for x in os.listdir(base) if x.endswith('.jpg') and x != '00-couverture.jpg' and x not in set(pages)]
        if orphelines:
            notes.append(f"{code} : planches non citees {orphelines[:4]}")
    print(f"{lues} planches lues")
    for n in notes:
        print("note :", n)
    for e in erreurs:
        print("ERREUR :", e)
    if not erreurs:
        print("OK : toutes les planches citees existent et s'ouvrent.")
    return 1 if erreurs else 0


if __name__ == '__main__':
    sys.exit(main())
