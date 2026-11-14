"""Genere les entrees `data/cards.json` (cle de pack `shadowland`) a partir de transcriptions/toutes-relues.json.

Usage : python3 generer_cards_json.py <debut> <fin>   (numeros imprimes 65NNN inclus) -> brouillons/cards_<debut>_<fin>.json
Regles (verifiees sur les cartes officielles 01097b, 01101, 01107-01109, 01121) :
 - id : 65NNN[A|B] -> slNNN[a|b] ; les cartes recto-verso (complots, vilains, positions) gardent la lettre, les autres non.
 - "N par_joueur" -> "N*" ; escalade "+N par_joueur" -> EscalationThreat "N*" ; TargetThreat/StartingThreat idem.
 - icones rouges en Y = Boost n ; crisis/hazard/acceleration -> Crisis/Hazard/Acceleration ; etoile de boost = texte seul (separe par <hr />).
 - mots-cles en tete de ligne (Guard, Assault...) -> desc[Mot]="1" ET restes dans le texte comme sur les cartes officielles.
 - unique -> nom precede de "* ".
"""
import json, re, sys, os
ici = os.path.dirname(os.path.abspath(__file__))
deb, fin = int(sys.argv[1]), int(sys.argv[2])
d = json.load(open(os.path.join(ici, 'transcriptions/toutes-relues.json')))
TYPES = {'MAIN SCHEME': 'MainScheme', 'SIDE SCHEME': 'SideScheme', 'VILLAIN': 'Villain', 'MINION': 'Minion', 'TREACHERY': 'Treachery',
         'ENVIRONMENT': 'Environment', 'ATTACHMENT': 'Attachment', 'OBLIGATION': 'Obligation', 'ALLY': 'Ally', 'UPGRADE': 'Upgrade'}
MOTS = ['Guard', 'Assault', 'Patrol', 'Surge', 'Peril', 'Steady', 'Toughness', 'Villainous', 'Quickstrike', 'Retaliate', 'Stalwart', 'Incite', 'Hinder', 'Amplify']
SETS = {'SHADOWS IN THE NIGHT': 'Shadows in the Night', 'DARK PROTÉGÉ': 'Dark Protégé', 'NINJA SWARM': 'Ninja Swarm', 'SHADOW LABYRINTH': 'Shadow Labyrinth',
        'DEADLY CONTRAPTIONS': 'Deadly Contraptions', 'HEART OF SHADOW': 'Heart of Shadow', 'BLACK FLOWER': 'Black Flower', 'CREEPING CORRUPTION': 'Creeping Corruption'}
CLES = {'SCH': 'SCH', 'ATK': 'ATK', 'HP': 'HP', 'StartingThreat': 'StartingThreat', 'TargetThreat': 'TargetThreat'}


def val(s):
    s = str(s).strip()
    pj = 'par_joueur' in s
    m = re.match(r'\+?(\d+|∞)', s)
    n = m.group(1) if m else s
    return n + ('*' if pj else '')


def entree(x):
    num = int(x['id_scan'][:5]); face = x['id_scan'][5:].lower()
    t = TYPES[x['type']]
    recto_verso = t in ('MainScheme', 'Villain') or (t in ('Environment', 'Upgrade') and face)
    cid = 'sl%03d%s' % (num - 65000, face if (recto_verso and face) else '')
    desc = {}
    for k, v in (x.get('stats') or {}).items():
        if k == 'escalade':
            desc['EscalationThreat'] = val(v)
        elif k in CLES:
            desc[k] = val(v).replace('★', '') if k in ('ATK', 'SCH') else val(v)
    nb_boost = 0
    if t == 'Minion' and 'cout' in (x.get('stats') or {}): desc['HP'] = str(x['stats']['cout'])     # le cercle de la carte Ninja Swarm / Black Flower : transcrit « cout » = PV (verifie sur sl030 : 2)
    if t == 'Minion' and 'Boost' in (x.get('stats') or {}):
        desc['HP'] = str((x['stats'] or {})['Boost'])
    icones = x.get('icones') or []
    if isinstance(icones, str): icones = [icones]
    for ic in icones:
        # deux formes de transcription : dict {nom, nombre} ou simple chaine (« boost 5 », « hazard », « crisis »...)
        nom = (ic if isinstance(ic, str) else ic['nom']).lower()
        nombre = 1 if isinstance(ic, str) else ic['nombre']
        m = re.match(r'^boost (\d+)$', nom)
        if m: pass         # « boost 5 » des transcriptions de sbires = le cercle en bas a droite de l'illustration = les POINTS DE VIE (verifie sur sl020 : 5, pas 5 icones)
        elif re.match(r'^boost x(\d+)', nom): nb_boost += int(re.match(r'^boost x(\d+)', nom).group(1))
        elif re.search(r'en y x(\d+)', nom): nb_boost += int(re.search(r'en y x(\d+)', nom).group(1))
        elif 'ensemble de rencontre' in nom and 'rouge' in nom:     # « 2 icones d'ensemble de rencontre (Y rouge) » = les icones de BOOST (Y rouges, bas droite)
            mm = re.match(r'^(\d+)', nom); nb_boost += int(mm.group(1)) if mm else 1
        elif 'crisis' in nom: desc['Crisis'] = str(nombre)
        elif 'hazard' in nom: desc['Hazard'] = str(nombre)
        elif 'acceleration' in nom: desc['Acceleration'] = str(nombre)
        elif 'etoile' in nom or 'étoile' in nom or 'star' in nom: pass     # icone de set / etoile de boost ou d'ATK : pas de desc
        elif ' y ' in (' ' + nom + ' ') or 'forme de y' in nom: nb_boost += nombre
    if nb_boost: desc['Boost'] = str(nb_boost)
    texte = x.get('texte') or ''
    for ligne in texte.split('\n'):
        # mots-cles en TETE de ligne, enchaines (« Steady. Toughness. »)
        reste = ligne.strip()
        while True:
            m = re.match(r'^(%s)\b\.?\s*' % '|'.join(MOTS), reste)
            if not m: break
            desc.setdefault(m.group(1), '1')
            reste = reste[m.end():]
    if t in ('MainScheme',) and face == 'a': desc['Stage'] = x['face'][0]
    if t in ('MainScheme',) and face == 'b': desc['Stage'] = x['face'][0]
    texte = re.sub(r'<b>\[star\] ([^<]+)</b>', r'[star] <b>\1</b>', texte)     # forme officielle (01129) : l'etoile HORS de la balise
    texte = re.sub(r'\n?---\n?', '\n', texte)          # la transcription marque la barre des cartes Rencontre par « --- » : on la rend par <hr /> ci-dessous
    # separateur regles / boost a etoile, comme 01121
    texte = re.sub(r'\n(\[star\] <b>Boost</b>)', r'\n<hr />\n\1', texte)
    nom = ('* ' if x.get('unique') else '') + x['titre']
    e = {'card_id': cid, 'type': t, 'name': nom, 'subtitle': x.get('sous_titre') or '', 'desc': desc,
         'traits': x.get('traits') or [], 'set_name': SETS.get(x['set'], x['set'].title()), 'text': texte}
    return e

out = [entree(x) for x in d if deb <= int(x['id_scan'][:5]) <= fin]
os.makedirs(os.path.join(ici, 'brouillons'), exist_ok=True)
p = os.path.join(ici, 'brouillons/cards_%d_%d.json' % (deb, fin))
json.dump(out, open(p, 'w'), ensure_ascii=False, indent=1)
for e in out: print(e['card_id'], e['type'], e['name'], e['desc'], e['traits'])
