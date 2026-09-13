"""Construit l'annuaire des PERSONNES du jeu, a partir de data/cards.json.

A quoi ca sert : le releve des illustrations (data/images_cartes.json, page
/releve-images.html) doit dire QUI est dessine sur une carte. « Qui » est une
personne, pas une carte. Sans annuaire, la page devrait proposer 142 heros,
139 alter ego, 241 cartes de vilain et 409 sbires uniques, avec la meme
personne repetee partout : Rhino y figurerait trois fois (une par etape),
Spider-Man cinq fois (l'officiel et quatre versions fan-made), Apocalypse
treize fois.

⚠ LA MEME PERSONNE, MEME EN PLUSIEURS CARTES, EST UNE SEULE ENTREE. C'est tout
l'interet du fichier. Trois consequences, chacune voulue :
  - Spider-Man officiel et un Spider-Man fan-made ne font qu'un. Une carte qui
    montre Peter Parker le montre, peu importe quel paquet on joue.
  - Les etapes d'un vilain (Rhino I/II/III) ne font qu'un.
  - Le heros et son alter ego ne font qu'un : « Spider-Man / Peter Parker ».
    L'image de Peter Parker EST l'image de l'identite de Spider-Man, et le
    texte de Muse dit « l'image de son identite », pas « de sa face heros ».

⚠ LE REGROUPEMENT SE FAIT SUR LE NOM, PAS SUR L'IDENTIFIANT. Les identifiants
ne regroupent rien d'utile : les etapes d'un vilain portent des numeros qui se
suivent sans rien de commun (01094, 01095, 01096), et deux versions de
Spider-Man n'ont aucun chiffre en partage (01001 et su001).

⚠ MAIS POUR UN JOUEUR, LE REGROUPEMENT SE FAIT SUR LE COUPLE HEROS + ALTER EGO,
JAMAIS SUR LE SEUL NOM DE HEROS. Erreur commise puis corrigee le 13/09/2026 :
regrouper sur « Spider-Man » fondait Peter Parker, Miles Morales, Miguel O'Hara
et Elliot Tolliver en UNE personne. Ils partagent un nom de code, pas un visage.
Muse se declencherait alors sur l'image de Peter pendant qu'on joue Miles, ce
qui est faux. Le couple les separe (`spider-man-peter-parker` contre
`spider-man-miles-morales`) tout en fondant bien l'officiel et le fan-made qui
decrivent la MEME personne.

Les adversaires, eux, n'ont pas d'alter ego : ils se regroupent sur le seul nom,
et le catalogue les desambiguise deja la ou il le faut.

⚠ CE FICHIER EST GENERE, PAS ECRIT A LA MAIN. Il est relance quand cards.json
bouge (nouveau heros, nouveau set fan-made) :

    python3 outils/annuaire-identites.py --ecrire
    python3 outils/annuaire-identites.py            # montre sans ecrire

Une face qui n'apparait dans AUCUNE entree est un trou : le moteur ne saura pas
rattacher le joueur qui la controle a une personne. Le mode par defaut les
compte et les affiche, c'est le controle a faire apres chaque regeneration.
"""

import json
import os
import sys
import unicodedata

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARDS = os.path.join(RACINE, 'Fusion', 'marvel-lcg-src', 'data', 'cards.json')
SORTIE = os.path.join(RACINE, 'Fusion', 'marvel-lcg-src', 'data', 'identites.json')

# Les types qui designent quelqu'un qu'on peut reconnaitre sur une image.
# ⚠ Pas les allies : un allie est une personne, mais il y en a 500 et la
# plupart ne sont l'identite de personne. La liste sert a dire « c'est
# l'identite d'un joueur ou l'adversaire d'un scenario », pas « c'est un
# personnage Marvel ».
TYPES_JOUEUR = ('Hero', 'AlterEgo')
TYPES_ADVERSE = ('Villain', 'Minion')


def sans_accent(texte):
    decompose = unicodedata.normalize('NFD', texte)
    return ''.join(c for c in decompose if unicodedata.category(c) != 'Mn')


def cle(nom):
    """Identifiant stable d'une personne, tire de son nom.

    ⚠ STABLE VEUT DIRE : ne change pas quand on regenere, ne change pas quand
    une carte change de numero. Le releve existant pointe dessus ; le jour ou
    cette fonction changerait de resultat, tout le travail deja fait
    designerait des personnes qui n'existent plus.
    """
    base = sans_accent(nom).lower().strip()
    propre = ''.join(c if c.isalnum() else '-' for c in base)
    while '--' in propre:
        propre = propre.replace('--', '-')
    return propre.strip('-')


def lire_cartes():
    with open(CARDS, encoding='utf-8') as f:
        brut = json.load(f)
    for pack, cartes in brut.items():
        # La cle "checksum" est une chaine, pas une liste de cartes.
        if not isinstance(cartes, list):
            continue
        for carte in cartes:
            if isinstance(carte, dict) and carte.get('card_id'):
                yield pack, carte


def nom_propre(carte):
    return str(carte.get('name') or '').lstrip('* ').strip()


def construire():
    # Passe 1 : apparier heros et alter ego. Ils partagent leur numero a la
    # lettre de face pres (01001a / 01001b), sauf SP//dr, seule exception du
    # catalogue, ou la combinaison et sa pilote sont deux cartes distinctes
    # (31001 / 31002). L'exception est traitee plus bas, nommement.
    par_base = {}
    for _, carte in lire_cartes():
        if carte.get('type') not in TYPES_JOUEUR:
            continue
        ident = str(carte['card_id'])
        base = ident[:-1] if ident[-1:].isalpha() else ident
        par_base.setdefault(base, []).append(carte)

    # SP//dr : la seule identite du jeu dont les deux faces sont deux cartes.
    # Le moteur la traite deja a part (game/player/player.py, IsName).
    APPARIEMENT_A_LA_MAIN = {'31002': '31001'}
    for source, cible in APPARIEMENT_A_LA_MAIN.items():
        if source in par_base and cible in par_base:
            par_base[cible] += par_base.pop(source)

    identites = {}

    def ajouter(id_personne, nom, genre, carte):
        entree = identites.setdefault(id_personne, {
            'id': id_personne, 'nom': nom, 'alias': [], 'genre': genre, 'faces': [],
        })
        # ⚠ Un joueur l'emporte sur un adversaire : Venom est jouable ET vilain,
        # et c'est la meme personne. Le genre sert a ranger la liste dans la
        # page, pas a distinguer deux personnes.
        if genre == 'joueur':
            entree['genre'] = 'joueur'
        ident = str(carte['card_id'])
        if ident not in entree['faces']:
            entree['faces'].append(ident)
        return entree

    # Heros et alter ego : une entree par personne, nommee par sa face heros.
    for base in sorted(par_base):
        faces = par_base[base]
        heros = [c for c in faces if c.get('type') == 'Hero']
        alter = [c for c in faces if c.get('type') == 'AlterEgo']
        nom = nom_propre(heros[0]) if heros else nom_propre(faces[0])
        civil = nom_propre(alter[0]) if alter else ''
        # ⚠ Le couple, pas le nom de code seul : voir l'avertissement en tete.
        # Groot s'appelle Groot des deux cotes : inutile de le dire deux fois.
        id_personne = cle(nom + ' ' + civil) if civil and civil != nom else cle(nom)
        entree = None
        for carte in faces:
            entree = ajouter(id_personne, nom, 'joueur', carte)
        if entree is not None and civil and civil != nom and civil not in entree['alias']:
            entree['alias'].append(civil)

    # Vilains et sbires uniques : une entree par nom. Un sbire non unique
    # (« Thug ») n'est personne en particulier, on ne le propose pas.
    for _, carte in lire_cartes():
        if carte.get('type') not in TYPES_ADVERSE:
            continue
        if not str(carte.get('name') or '').startswith('* '):
            continue
        nom = nom_propre(carte)
        if not nom:
            continue
        ajouter(cle(nom), nom, 'adverse', carte)

    return identites


def main():
    identites = construire()
    ecrire = '--ecrire' in sys.argv

    joueurs = [x for x in identites.values() if x['genre'] == 'joueur']
    adverses = [x for x in identites.values() if x['genre'] != 'joueur']
    print(f"{len(identites)} personnes : {len(joueurs)} jouables, {len(adverses)} adverses")

    # Controle : une face de heros ou d'alter ego que l'annuaire ne rattache a
    # personne empecherait le moteur de reconnaitre ce joueur.
    rattachees = {f for x in identites.values() for f in x['faces']}
    orphelines = []
    for _, carte in lire_cartes():
        if carte.get('type') in TYPES_JOUEUR and str(carte['card_id']) not in rattachees:
            orphelines.append((carte['card_id'], nom_propre(carte)))
    if orphelines:
        print(f"⚠ {len(orphelines)} face(s) de heros/alter ego sans personne :")
        for ident, nom in orphelines[:20]:
            print(f"    {ident} {nom}")
    else:
        print("toutes les faces de heros et d'alter ego sont rattachees")

    if not ecrire:
        print("\n(rien ecrit ; relancez avec --ecrire)")
        return 1 if orphelines else 0

    donnees = {
        '_lisez_moi': ("Annuaire des personnes du jeu. GENERE par "
                       "outils/annuaire-identites.py, ne pas editer a la main. "
                       "Sert au releve des illustrations (data/images_cartes.json)."),
        'version': 1,
        'identites': [identites[k] for k in sorted(identites)],
    }
    provisoire = SORTIE + '.tmp'
    with open(provisoire, 'w', encoding='utf-8') as f:
        json.dump(donnees, f, ensure_ascii=False, indent=1)
    os.replace(provisoire, SORTIE)
    print(f"ecrit : {SORTIE}")
    return 1 if orphelines else 0


if __name__ == '__main__':
    sys.exit(main())
