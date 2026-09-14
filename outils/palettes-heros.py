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


def cartes_du_catalogue():
    with open(os.path.join(DATA, 'cards.json'), encoding='utf-8') as f:
        brut = json.load(f)
    for pack, liste in brut.items():
        if not isinstance(liste, list):
            continue
        for carte in liste:
            if isinstance(carte, dict) and carte.get('card_id'):
                yield pack, carte


def seau_de(r, g, b):
    """Dans quel groupe ranger ce pixel : une teinte, le clair, ou le sombre."""
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    if l > 0.72 and s < 0.45:
        return 'clair'       # le BLANC, qui fait Captain America et Black Widow
    if l < 0.16:
        return None          # ⚠ LE CADRE SOMBRE EST SUR TOUTES LES CARTES : il ne
                             # caracterise aucun heros. Garde, il evincait le blanc
                             # de Captain America, qui est pourtant bleu BLANC rouge.
    if s < 0.28:
        return None          # un gris terne ne dit rien du heros
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
    total = sum(a[3] for a in seaux.values())
    if not total or lues < 2:
        return None, lues
    tri = sorted(seaux.values(), key=lambda a: -a[3])
    couleurs = [
        [round(a[0] / a[3]), round(a[1] / a[3]), round(a[2] / a[3])]
        for a in tri if a[3] / total >= PART_MINIMALE
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
        couleurs, lues = palette_du_set(par_set.get(set_name, []))
        if not couleurs:
            sans.append((set_name, lues))
            continue
        for face in faces:
            palettes[face] = couleurs

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
