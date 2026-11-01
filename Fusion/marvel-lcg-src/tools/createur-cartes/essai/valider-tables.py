"""Valide le pack fabrique par tables-export.mjs contre les listes de reference des outils de la communaute.

    python3 -I valider-tables.py <dossier ou le pack.zip a ete decompresse>

Sources des listes : MCdeck (github.com/lcgtools/MCdeck, mcdeck/octgn.py : OctgnProperties.fields, tailles `size`) pour OCTGN ;
dragncards-mc-plugin (github.com/hone/dragncards-mc-plugin : json/cardTypes.json, json/cardBacks.json, src/dragncards/database.rs) pour DragnCards.
"""
import csv, glob, os, re, sys
import xml.etree.ElementTree as ET

racine = sys.argv[1]
echecs = []
def verifier(nom, ok, detail=""):
    print(("  OK   " if ok else "  RATE ") + nom + ("" if ok else " | " + str(detail)))
    if not ok: echecs.append(nom)

# ---- OCTGN (MCdeck)
TYPES = {'ally', 'alter_ego', 'attachment', 'environment', 'event', 'hero', 'main_scheme', 'minion', 'obligation', 'resource', 'side_scheme', 'support', 'treachery', 'upgrade', 'villain'}
PROPRIETES = {'Type', 'CardNumber', 'Unique', 'Cost', 'Attribute', 'Text', 'Resource_Physical', 'Resource_Mental', 'Resource_Energy', 'Resource_Wild', 'Quote', 'Owner',
              'Attack', 'Thwart', 'Defense', 'Recovery', 'Scheme', 'AttackCost', 'ThwartCost', 'HandSize', 'HP', 'HP_Per_Hero', 'Threat', 'EscalationThreat',
              'EscalationThreatFixed', 'BaseThreat', 'BaseThreatFixed', 'Scheme_Acceleration', 'Scheme_Crisis', 'Scheme_Hazard', 'Scheme_Boost', 'Boost',
              'Position', 'Quantity', 'DefaultSetupPile'}  # les trois derniers : set d'exemple de la communaute (She-Hulk, Merlin)
ENTIERS = {'Cost', 'Resource_Physical', 'Resource_Mental', 'Resource_Energy', 'Resource_Wild', 'Attack', 'Thwart', 'Defense', 'Recovery', 'Scheme', 'AttackCost', 'ThwartCost', 'HandSize', 'HP', 'Threat', 'EscalationThreat', 'BaseThreat', 'Scheme_Acceleration', 'Scheme_Crisis', 'Scheme_Hazard', 'Scheme_Boost', 'Boost'}
TAILLES = {'SchemeCard': {'main_scheme', 'side_scheme'}, 'EncounterCard': {'attachment', 'environment', 'minion', 'obligation', 'treachery'}, 'VillainCard': {'villain'}}

xmls = glob.glob(os.path.join(racine, 'octgn/GameDatabase/*/Sets/*/set.xml'))
verifier('un seul set.xml', len(xmls) == 1, xmls)
t = ET.parse(xmls[0]).getroot()
set_id = t.get('id')
verifier('<set> : name, id, gameId, version', all(t.get(k) for k in ('name', 'id', 'gameId', 'gameVersion', 'version')))
verifier('dossier du set = id du set (OCTGN)', os.path.basename(os.path.dirname(xmls[0])) == set_id)
imgs = glob.glob(os.path.join(racine, 'octgn/ImageDataBase/*/Sets/*/Cards/*'))
verifier('dossier d\'images du meme set', all(f'/Sets/{set_id}/Cards/' in f for f in imgs) and imgs)
verifier('images .jpg / .png seulement', all(f.endswith(('.jpg', '.png')) for f in imgs))
ids = set(); mauvais = []
for c in t.iter('card'):
    cid = c.get('id'); ids.add(cid)
    if not re.fullmatch(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', cid): mauvais.append(('guid', cid))
    props = {}
    for p in list(c.findall('property')) + [q for a in c.findall('alternate') for q in a.findall('property')]:
        n = p.get('name'); props.setdefault(n, []).append(p)
        if n not in PROPRIETES: mauvais.append(('propriete inconnue', n))
        if n in ('Text', 'Quote'):
            if p.get('value') is not None or not (p.text or '').strip(): mauvais.append(('Text/Quote doit etre le texte de l\'element', n))
        elif p.get('value') is None: mauvais.append(('value manquante', n))
        if n in ENTIERS and not re.fullmatch(r'\d+', p.get('value') or ''): mauvais.append(('entier attendu', n, p.get('value')))
    types = [p.get('value') for k, v in props.items() if k == 'Type' for p in v]
    for ty in types:
        if ty not in TYPES and ty != 'fm_hero_setup': mauvais.append(('Type inconnu', ty))
    taille = c.get('size')
    if taille:
        if types[0] not in TAILLES.get(taille, set()): mauvais.append(('size incoherente', taille, types[0]))
    elif types[0] in set().union(*TAILLES.values()): mauvais.append(('size manquante', types[0]))
    if not any(os.path.basename(f) in (cid + '.jpg', cid + '.png') for f in imgs): mauvais.append(('pas d\'image', cid))
    for a in c.findall('alternate'):
        if not any(os.path.basename(f) in (cid + '.b.jpg', cid + '.b.png') for f in imgs): mauvais.append(('pas d\'image b', cid))
verifier('cartes OCTGN conformes (guid, Type, proprietes, entiers, size, images)', not mauvais, mauvais[:6])
verifier('ids de cartes tous differents', len(ids) == len(list(t.iter('card'))))

# ---- DragnCards (plugin)
CARD_TYPES = {'Ally', 'Alter-Ego', 'Event', 'Hero', 'Resource', 'Support', 'Upgrade', 'Attachment', 'Environment', 'Evidence - Means', 'Evidence - Motive', 'Evidence - Opportunity', 'Leader', 'Main Scheme', 'Minion', 'Obligation', 'Player Side Scheme', 'Side Scheme', 'Treachery', 'Villain'}
BACKS = {'encounter', 'player', 'villain', 'multi_sided'}
lignes = list(csv.DictReader(open(os.path.join(racine, 'dragncards/cards.tsv'), encoding='utf-8'), delimiter='\t'))
oblig = ('databaseId', 'name', 'imageUrl', 'cardBack', 'type')
verifier('colonnes obligatoires presentes', all(k in lignes[0] for k in oblig))
verifier('chaque ligne remplit les colonnes obligatoires', all(l[k] for l in lignes for k in oblig))
verifier('type valide (cardTypes du plugin)', all(l['type'] in CARD_TYPES for l in lignes), {l['type'] for l in lignes} - CARD_TYPES)
verifier('cardBack valide (cardBacks du plugin + multi_sided)', all(l['cardBack'] in BACKS for l in lignes))
verifier('imageUrl finit par .jpg / .png', all(re.search(r'\.(jpg|png)$', l['imageUrl']) for l in lignes))
groupes = {}
for l in lignes: groupes.setdefault(l['databaseId'], []).append(l)
verifier('multi_sided : toutes les lignes d\'un databaseId (>=2) et seulement elles', all((len(g) > 1) == all(x['cardBack'] == 'multi_sided' for x in g) and (len(g) == 1 or all(x['cardBack'] == 'multi_sided' for x in g)) for g in groupes.values()))
verifier('databaseId = UUID', all(re.fullmatch(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', k) for k in groupes))
verifier('chaque image du tsv existe', all(os.path.exists(os.path.join(racine, 'dragncards/images', l['imageUrl'].rsplit('/', 1)[-1])) for l in lignes))
verifier('entiers : handSize, hitPoints*, startingThreat*, acceleration*', all(re.fullmatch(r'\d*', l[k]) for l in lignes for k in ('handSize', 'hitPointsFixed', 'hitPointsScaling', 'startingThreatFixed', 'startingThreatScaling', 'accelerationFixed', 'accelerationScaling')))
sys.exit(1 if echecs else 0)
