#!/usr/bin/env python3
"""Ajoute au createur deux gabarits d'INSERT (feuillets de campagne / regles) : `insert` (format carte, 1500 x 2150) et
`insert-page` (A4, 2100 x 2970). Fabrique les images (papier + bandeau teinte) et complete donnees/types.json.
Usage : python3 tools/createur-cartes/ajouter-inserts.py   (relancable : remplace les deux entrees)."""
import copy, json, os, random
from PIL import Image, ImageDraw, ImageFilter

RACINE = os.path.join(os.path.dirname(__file__), '..', '..', 'public', 'createur-cartes')
TYPES = os.path.join(RACINE, 'donnees', 'types.json')
IMG = os.path.join(RACINE, 'img')

def papier(l, h, dossier):
    os.makedirs(os.path.join(IMG, dossier), exist_ok=True)
    k = l / 1500
    rayon = int(60 * k)
    # fond : papier creme legerement grene, coins arrondis transparents, liseré noir
    random.seed(7)
    bruit = Image.effect_noise((l // 4, h // 4), 14).resize((l, h)).convert('L')
    fond = Image.new('RGB', (l, h), (243, 234, 210))
    fond = Image.blend(fond, Image.merge('RGB', [bruit] * 3).point(lambda v: 200 + v // 6), 0.12)
    masque = Image.new('L', (l, h), 0)
    ImageDraw.Draw(masque).rounded_rectangle((0, 0, l - 1, h - 1), rayon, fill=255)
    cadre = ImageDraw.Draw(fond)
    cadre.rounded_rectangle((0, 0, l - 1, h - 1), rayon, outline=(20, 20, 24), width=int(26 * k))
    cadre.rounded_rectangle((int(46 * k), int(46 * k), l - 1 - int(46 * k), h - 1 - int(46 * k)), int(rayon * .6), outline=(60, 60, 70), width=max(2, int(5 * k)))
    base = fond.convert('RGBA'); base.putalpha(masque)
    base.save(os.path.join(IMG, dossier, 'base.webp'), quality=88)
    # bandeau : une forme pleine (la couleur du role right_color la remplit), biseautee a droite comme les titres du jeu
    b = Image.new('RGBA', (l, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(b)
    x0, x1, y0, y1, c = int(70 * k), l - int(70 * k), int(70 * k), int(260 * k), int(70 * k)
    d.polygon([(x0, y0), (x1 - c, y0), (x1, y0 + c), (x1, y1), (x0 + c, y1), (x0, y1 - c)], fill=(255, 255, 255, 255))
    d.line([(x0, y1 + int(14 * k)), (x1, y1 + int(14 * k))], fill=(255, 255, 255, 255), width=max(4, int(10 * k)))
    b.save(os.path.join(IMG, dossier, 'bandeau.webp'), quality=90)

def spec(modele, ident, etiquette, l, h, dossier, echelle_boites, echelle_police):
    el = {e['cls']: e for e in modele['elements'] if e['cls'] in ('cardtext', 'traits', 'rules', 'quote', 'title', 'c-line')}
    k = echelle_boites
    def poser(e, boite, police=None, **style):
        e = copy.deepcopy(e)
        e['boite'] = [round(v * k) for v in boite]
        e['origine'] = [e['boite'][2] / 2, e['boite'][3] / 2]
        e['parent'] = -1
        if police is not None:
            e['style']['fontSize'] = f"{police * echelle_police:g}px"
        for a, v in style.items(): e['style'][a] = v
        return e
    corps = poser(el['cardtext'], [120, 330, 1260, 1640])
    sortie = [corps]
    for c in ('traits', 'rules', 'quote'):
        e = poser(el[c], {'traits': [120, 330, 1260, 86], 'rules': [120, 440, 1260, 69], 'quote': [120, 1800, 1260, 120]}[c])
        e['parent'] = corps['i']
        if c != 'traits':
            e['style']['fontSize'] = f"{float(e['style']['fontSize'][:-2]) * echelle_police:g}px"
            e['style']['lineHeight'] = f"{float(e['style']['lineHeight'][:-2]) * echelle_police:g}px"
        sortie.append(e)
    titre = poser(el['title'], [120, 84, 1260, 156], color='rgb(255, 255, 255)')
    titre['style']['fontSize'] = f"{102 * (k if k > 1 else 1):g}px"
    titre['style']['lineHeight'] = f"{156 * k:g}px"
    sortie.append(titre)
    sortie.append(poser(el['c-line'], [120, 2060, 1260, 57], color='rgb(40, 40, 46)'))
    for n, e in enumerate(sortie): e['i'] = 1000 + n
    for e in sortie:
        if e['parent'] != -1: e['parent'] = sortie[0]['i']
    return {
        'id': ident, 'etiquette': etiquette, 'famille': 'hero', 'paysage': False, 'largeur': l, 'hauteur': h,
        'calques': [{'role': 'photo'}, {'role': 'base', 'src': f'{dossier}/base.webp'},
                    {'role': 'right_color', 'src': f'{dossier}/bandeau.webp', 'teinte': 'right_color'}, {'role': 'photofront'}],
        'couleursParDefaut': {'right_color': '#2f6db5'},
        'elements': sortie,
    }

def main():
    types = json.load(open(TYPES))
    modele = types['support']
    papier(1500, 2150, 'insert')
    papier(2100, 2970, 'insert-page')
    types['insert'] = spec(modele, 'insert', 'Insert (card size)', 1500, 2150, 'insert', 1, 1)
    types['insert-page'] = spec(modele, 'insert-page', 'Insert (A4 page)', 2100, 2970, 'insert-page', 1.4, 0.85)
    json.dump(types, open(TYPES, 'w'), ensure_ascii=False, separators=(',', ':'))
    print('ok :', ', '.join(k for k in types if k.startswith('insert')))

main()
