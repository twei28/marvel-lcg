"""Verse dans le releve un lot rendu par une IA (voir .planning/releve-images/).

    python3 outils/importer-releve-images.py lot.json            # verifie seulement
    python3 outils/importer-releve-images.py lot.json --ecrire   # verifie et verse

⚠ RIEN N'EST VERSE SANS CONTROLE. Un relevé faux est PIRE que pas de relevé :
une carte absente du fichier garde l'approximation du jeu, une carte presente
est crue sur parole. Un identifiant invente, une image qui n'existe pas, une
valeur qui n'est pas une liste : tout cela est refuse, et le lot entier est
rejete si une seule ligne cloche. Corriger un lot est facile, retrouver une
ligne fausse noyee dans 4000 ne l'est pas.

⚠ LE FICHIER EXISTANT N'EST JAMAIS ECRASE EN BLOC. On relit, on fusionne cle
par cle, on reecrit atomiquement. Deux lots successifs s'additionnent donc, et
le travail fait a la main dans le jeu n'est pas perdu.

⚠ UNE LISTE VIDE EST UNE REPONSE, PAS UN TROU. « [] » veut dire « regarde, il
n'y a personne dessus » et sera ecrit tel quel. Ne pas relever une carte, c'est
ne pas mettre sa cle du tout.
"""

import json
import os
import re
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(RACINE, 'Fusion', 'marvel-lcg-src', 'data')
RELEVE = os.path.join(DATA, 'images_cartes.json')
IDENTITES = os.path.join(DATA, 'identites.json')
CARTES = os.path.join(DATA, 'cards.json')


def images_connues():
    """Les identifiants d'illustration qui existent vraiment.

    Meme resolution que le moteur et que la page : `pic_id`, puis la carte
    d'origine si c'est une reimpression, puis l'identifiant propre.
    """
    with open(CARTES, encoding='utf-8') as f:
        catalogue = json.load(f)
    connues = set()
    for _, liste in catalogue.items():
        if not isinstance(liste, list):
            continue
        for carte in liste:
            if isinstance(carte, dict) and carte.get('card_id'):
                connues.add(str(carte.get('pic_id') or carte.get('full_link') or carte['card_id']))
    return connues


def personnes_connues():
    with open(IDENTITES, encoding='utf-8') as f:
        return {str(e['id']) for e in json.load(f).get('identites', []) if e.get('id')}


def main():
    arguments = [a for a in sys.argv[1:] if not a.startswith('--')]
    if len(arguments) != 1:
        print(__doc__)
        return 2
    lot_chemin = arguments[0]
    ecrire = '--ecrire' in sys.argv

    with open(lot_chemin, encoding='utf-8') as f:
        lot = json.load(f)
    if not isinstance(lot, dict):
        print("REFUS : le lot doit etre un objet JSON { image: [personnes] }")
        return 1

    images = images_connues()
    personnes = personnes_connues()

    plaintes = []
    propre = {}
    for cle, valeur in lot.items():
        image = str(cle).strip()
        if image not in images:
            plaintes.append(f"{image} : cette illustration n'existe pas dans le catalogue")
            continue
        if not isinstance(valeur, list):
            plaintes.append(f"{image} : la valeur doit etre une liste, recu {type(valeur).__name__}")
            continue
        retenues = []
        for brut in valeur:
            id_personne = str(brut).strip()
            if id_personne not in personnes:
                plaintes.append(f"{image} : personne inconnue « {id_personne} »")
                continue
            if id_personne not in retenues:
                retenues.append(id_personne)
        propre[image] = retenues

    if plaintes:
        print(f"REFUS : {len(plaintes)} probleme(s), rien n'est verse.")
        for ligne in plaintes[:40]:
            print('  ' + ligne)
        if len(plaintes) > 40:
            print(f'  ... et {len(plaintes) - 40} de plus')
        return 1

    # Fusion avec l'existant.
    donnees = {'version': 1, 'cartes': {}}
    if os.path.exists(RELEVE):
        with open(RELEVE, encoding='utf-8') as f:
            lu = json.load(f)
        if isinstance(lu, dict) and isinstance(lu.get('cartes'), dict):
            donnees = lu

    avant = dict(donnees['cartes'])
    nouvelles = [k for k in propre if k not in avant]
    changees = [k for k in propre if k in avant and avant[k] != propre[k]]

    print(f"{len(propre)} illustration(s) dans le lot, toutes valides")
    print(f"  nouvelles : {len(nouvelles)}")
    print(f"  modifiees : {len(changees)}")
    for cle in changees[:10]:
        print(f"    {cle} : {avant[cle]} -> {propre[cle]}")
    vides = sum(1 for v in propre.values() if not v)
    print(f"  dont « personne dessus » : {vides}")

    if not ecrire:
        print("\n(rien ecrit ; relancez avec --ecrire)")
        return 0

    donnees['cartes'].update(propre)
    provisoire = RELEVE + '.tmp'
    with open(provisoire, 'w', encoding='utf-8') as f:
        json.dump(donnees, f, ensure_ascii=False, indent=1, sort_keys=True)
    os.replace(provisoire, RELEVE)
    print(f"\nverse : {len(donnees['cartes'])} illustration(s) relevees au total")
    print("⚠ Le serveur garde le releve en cache : redemarrez-le, ou relevez une")
    print("  carte depuis /releve-images.html, pour qu'il en tienne compte.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
