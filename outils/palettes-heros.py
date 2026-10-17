"""La palette de chaque heros, tiree du CONTOUR de ses cartes.

    python3 outils/palettes-heros.py            # montre sans ecrire
    python3 outils/palettes-heros.py --ecrire

A quoi ca sert : teinter le fond du plateau aux couleurs du heros qu'on joue.
Constat de l'utilisateur, 14/09/2026 : « sur les faces, le contour des cartes,
il y a deux ou trois couleurs, et c'est systematiquement comme ca pour tous les
heros avec des couleurs differentes ».

⚠ LE CONTOUR, PAS L'ILLUSTRATION. Un premier essai moyennait l'image entiere
d'une carte : il en sortait du brun, parce qu'une moyenne de rouge et de bleu
EST du brun. Ici on lit une bande le long des bords, ou vit le cadre colore, et
on regroupe les pixels par TEINTE au lieu de les moyenner.

⚠ ET ON GARDE LE BLANC. Un filtre sur la saturation seule ecartait le blanc, or
Captain America est bleu BLANC rouge : sans lui, il ne restait que deux tiers du
personnage. Les neutres tres clairs et tres sombres ont donc leur propre seau.

⚠ SUR TOUT LE SET, PAS SUR UNE CARTE. Une carte isolee donne la couleur de SON
illustration ; l'ensemble des cartes signature donne celle du heros. C'est ce
qui rend le resultat stable.

⚠ CE FICHIER EST GENERE, PAS ECRIT A LA MAIN, et relance quand les scans ou le
catalogue changent. Le controle a faire apres : la liste des heros sans palette.
"""

import colorsys
import json
import os
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(RACINE, 'Fusion', 'marvel-lcg-src', 'data')
PICS = os.path.join(RACINE, 'Fusion', 'marvel-lcg-src', 'assets', 'pics')
SORTIE = os.path.join(DATA, 'palettes-heros.json')

# En dessous, la couleur ne veut plus rien dire : c'est du bruit de compression.
PART_MINIMALE = 0.10
COULEURS_GARDEES = 3


# ⚠ LES DEUX CATALOGUES. `cards.json` porte les cartes officielles,
# `cards_custom.json` les sets maison ; le moteur charge les deux, et les
# oublier laissait Stan Lee, Hulk (Rainy) et Rescue (Rainy) sans palette,
# donc sans halo, alors que leurs scans sont bien la.
CATALOGUES = ('cards.json', 'cards_custom.json')


def cartes_du_catalogue():
    for nom in CATALOGUES:
        chemin = os.path.join(DATA, nom)
        if not os.path.exists(chemin):
            continue
        with open(chemin, encoding='utf-8') as f:
            brut = json.load(f)
        for pack, liste in brut.items():
            if not isinstance(liste, list):
                continue
            for carte in liste:
                if isinstance(carte, dict) and carte.get('card_id'):
                    yield pack, carte


# ⚠ LA PART COMMUNE DU NOIR ET DU GRIS, MESUREE SUR LES 133 SETS. Chaque
# carte du jeu porte un liseré sombre et des gris d'ombre : ~21 % de noir et
# ~18 % de gris en mediane, du plus clair (11 % / 1 %) au plus charge (58 % /
# 57 %). Ces parts-la ne disent rien du heros, on les retranche. Ce qui DEPASSE,
# lui, est bien la couleur du cadre : Venom pese 42 % de noir, Magneto 34 % de
# gris. Une premiere version jetait ces deux seaux en bloc, et onze heros
# (Venom, Magneto, Storm, Gamora, Winter Soldier, Black Cat...) ressortaient en
# BLANC QUASI PUR, faute d'autre seau survivant. Leurs cadres sont noir et gris :
# c'est leur vraie couleur, pas un defaut de mesure.
PART_COMMUNE = {'sombre': 0.211, 'terne': 0.183}


def seau_de(r, g, b):
    """Dans quel groupe ranger ce pixel : une teinte, le clair, le gris, le noir."""
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    if l > 0.72 and s < 0.45:
        return 'clair'       # le BLANC, qui fait Captain America et Black Widow
    if l < 0.16:
        return 'sombre'      # le NOIR, qui fait Venom et Gamora
    if s < 0.28:
        return 'terne'       # le GRIS, qui fait Magneto et Storm
    return int(h * 360) // 20


def contour(chemin, seaux):
    """Ajoute les pixels du POURTOUR de cette carte aux seaux communs."""
    from PIL import Image
    try:
        im = Image.open(chemin).convert('RGB')
    except Exception:
        return 0
    L, H = im.size
    px = im.load()
    marge_x = max(2, int(L * 0.045))
    marge_y = max(2, int(H * 0.05))
    points = []
    for x in range(1, marge_x):
        points += [px[x, y] for y in range(int(H * 0.06), int(H * 0.94), 2)]
    for x in range(L - marge_x, L - 1):
        points += [px[x, y] for y in range(int(H * 0.06), int(H * 0.94), 2)]
    for y in range(H - marge_y, H - 1):
        points += [px[x, y] for x in range(int(L * 0.06), int(L * 0.94), 2)]

    retenus = 0
    for r, g, b in points:
        cle = seau_de(r, g, b)
        if cle is None:
            continue
        a = seaux.setdefault(cle, [0, 0, 0, 0])
        a[0] += r
        a[1] += g
        a[2] += b
        a[3] += 1
        retenus += 1
    return retenus


def palette_du_set(cartes):
    seaux = {}
    lues = 0
    for cid in cartes:
        # ⚠ DEUX EXTENSIONS : les cartes officielles sont en .jpg, les fan-made
        # en .png, dans le MEME dossier. Ne chercher que les .jpg laissait
        # 30 sets sans palette, tous fan-made.
        chemin = next((c for c in (os.path.join(PICS, cid + e) for e in ('.jpg', '.png'))
                       if os.path.exists(c)), None)
        if not chemin:
            continue
        if contour(chemin, seaux):
            lues += 1
    brut = sum(a[3] for a in seaux.values())
    if not brut or lues < 2:
        return None, lues
    # Le poids RETENU de chaque seau : sa part, moins la part que porte n'importe
    # quelle carte (voir PART_COMMUNE). Un seau qui ne depasse pas sa ligne de
    # base ne caracterise pas ce heros et disparait.
    pesees = []
    for cle, a in seaux.items():
        part = a[3] / brut - PART_COMMUNE.get(cle, 0.0)
        if part > 0:
            pesees.append((part, a))
    total = sum(p for p, _ in pesees)
    if not total:
        return None, lues
    pesees.sort(key=lambda x: -x[0])
    couleurs = [
        [round(a[0] / a[3]), round(a[1] / a[3]), round(a[2] / a[3])]
        for part, a in pesees if part / total >= PART_MINIMALE
    ][:COULEURS_GARDEES]
    return (couleurs or None), lues


def main():
    ecrire = '--ecrire' in sys.argv

    # Les identites, et le set auquel chacune appartient.
    identites = {}   # set_name -> [card_id des faces d'identite]
    par_set = {}     # set_name -> [card_id des cartes signature]
    for _, carte in cartes_du_catalogue():
        set_name = carte.get('set_name') or ''
        if not set_name:
            continue
        if carte.get('type') in ('Hero', 'AlterEgo'):
            identites.setdefault(set_name, []).append(str(carte['card_id']))
        classe = str((carte.get('desc') or {}).get('Class') or '')
        if 'Hero' in classe.split(';'):
            par_set.setdefault(set_name, []).append(str(carte['card_id']))

    palettes = {}
    sans = []
    for set_name, faces in sorted(identites.items()):
        # ⚠ LES CARTES SIGNATURE D'ABORD, LES FACES D'IDENTITE EN SECOURS. Tout
        # un set donne une couleur stable ; une ou deux cartes donnent celle de
        # LEUR illustration. Mais un set peut n'avoir aucune carte signature
        # (Stan Lee n'est que ses deux faces) : sans ce repli il n'aurait aucun
        # halo, alors que son cadre porte bien ses couleurs.
        cartes = par_set.get(set_name) or faces
        couleurs, lues = palette_du_set(cartes)
        if not couleurs:
            sans.append((set_name, lues))
            continue
        for face in faces:
            palettes[face] = couleurs

    # LES MECHANTS (17/10/2026) : demande de l'utilisateur, « en haut a gauche les couleurs
    # du mechant », comme le coin bas droit porte celles du heros. UN MECHANT = UNE PALETTE :
    # toutes ses phases (1A, 2A, 3A, leurs deux faces) partagent les memes couleurs, pour que le
    # fond ne saute pas quand le mechant passe a la phase suivante. Le groupe est le set du
    # mechant (`set_name`) ; la palette est tiree du contour de TOUTES ses cartes mechant.
    mechants = {}    # set_name -> [card_id des phases]
    for _, carte in cartes_du_catalogue():
        set_name = carte.get('set_name') or ''
        if set_name and carte.get('type') == 'Villain':
            mechants.setdefault(set_name, []).append(str(carte['card_id']))
    sans_mechant = []
    for set_name, phases in sorted(mechants.items()):
        couleurs, lues = palette_du_set(phases)
        if not couleurs:
            sans_mechant.append((set_name, lues))
            continue
        for phase in phases:
            palettes.setdefault(phase, couleurs)
    print(f"{len(mechants)} mechants, {len(mechants) - len(sans_mechant)} avec une palette")
    for nom, lues in sans_mechant[:12]:
        print(f"    mechant sans palette : {nom} ({lues} carte(s) lue(s))")

    print(f"{len(identites)} identites, {len(palettes)} faces avec une palette")
    if sans:
        print(f"⚠ {len(sans)} set(s) sans palette (scans absents ou trop peu nombreux) :")
        for nom, lues in sans[:12]:
            print(f"    {nom} ({lues} carte(s) lue(s))")
        if len(sans) > 12:
            print(f"    ... et {len(sans) - 12} de plus")

    for exemple in ('03001a', '01001a', '10001a', '08001a'):
        if exemple in palettes:
            print(f"  {exemple} -> {palettes[exemple]}")

    if not ecrire:
        print("\n(rien ecrit ; relancez avec --ecrire)")
        return 0

    donnees = {
        '_lisez_moi': ("La palette de chaque heros, tiree du CONTOUR de ses cartes "
                       "signature. GENERE par outils/palettes-heros.py, ne pas editer "
                       "a la main. Sert a teinter le fond du plateau."),
        'version': 1,
        'palettes': palettes,
    }
    provisoire = SORTIE + '.tmp'
    with open(provisoire, 'w', encoding='utf-8') as f:
        json.dump(donnees, f, ensure_ascii=False, indent=1, sort_keys=True)
    os.replace(provisoire, SORTIE)
    print(f"\necrit : {SORTIE}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
