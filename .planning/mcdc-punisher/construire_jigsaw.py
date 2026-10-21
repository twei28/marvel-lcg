"""Echafaudage du set Jigsaw (lot PU-2) : cards.json, images, encounter set, scenarios, sets_info.
Idempotent. AUCUN script de capacite. Usage : python3 construire_jigsaw.py  (depuis la racine du depot)."""
import copy, importlib.util, json, os, re
from PIL import Image

RACINE = os.getcwd()
JEU = os.path.join(RACINE, 'Fusion/marvel-lcg-src')
SCANS = os.path.join(RACINE, 'paquets-cartes/MC x DC 2026 - campagne Punisher/scans')
PACK = 'punisher_mcdc_2026'
spec = importlib.util.spec_from_file_location('defs', os.path.join(RACINE, '.planning/mcdc-punisher/defs/punisher_cards.py'))
defs = importlib.util.module_from_spec(spec); spec.loader.exec_module(defs)

PAGE = {'pu056a': 111, 'pu056b': 112, 'pu057a': 113, 'pu057b': 114, 'pu058': 115, 'pu059': 117, 'pu060': 119,
        'pu063': 125, 'pu064': 127, 'pu065': 129, 'pu066': 131, 'pu068': 135, 'pu070': 139}
STAGE = {'pu056a': '1', 'pu056b': '2', 'pu057a': '2', 'pu057b': '3'}   # chiffre romain imprime sur le scan


def stat(v):
    v = str(v).replace('\U0001F464', '*')
    if v == '★': return '0**'
    return v.replace('★+1', '1**').replace('★', '**')


cartes = []
for x in defs.JIGSAW_CARDS:
    d = {k: stat(v) for k, v in x['desc'].items()}
    if x['card_id'] in STAGE: d['Stage'] = STAGE[x['card_id']]
    e = {'card_id': x['card_id'], 'type': x['type'], 'name': x['name'], 'subtitle': x['subtitle'], 'desc': d,
         'traits': x['traits'], 'set_name': x['set_name'], 'text': x['text'], 'custom': 'MC×DC 2026'}
    cartes.append(e)

p = os.path.join(JEU, 'data/cards.json')
cj = json.load(open(p, encoding='utf-8'))
cj.pop(PACK, None); somme = cj.pop('checksum', None); cj[PACK] = cartes
if somme: cj['checksum'] = somme
with open(p, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(cj, f, ensure_ascii=False, indent=1)

for cid, n in PAGE.items():
    im = Image.open(os.path.join(SCANS, 'p%d.jpg' % n)).convert('RGB')
    if cid == 'pu065': im = im.rotate(-90, expand=True)     # manigance annexe : scan couche, on remet a plat
    im.save(os.path.join(JEU, 'assets/pics', cid + '.jpg'), quality=92)

def ecrire(chemin, obj):
    with open(os.path.join(JEU, chemin), 'w', encoding='utf-8', newline='\n') as f:
        json.dump(obj, f, ensure_ascii=False, indent=4); f.write('\n')

ecrire('data/encounter_sets/jigsaw.json', {'version': '0.5.8', 'name': 'Jigsaw', 'encounters': defs.JIGSAW_ENCOUNTERS})

MANIGANCES = ['art_museum_heist', 'the_getaway', 'protection_racket', 'the_raft_breakout', 'stop_the_presses']
noms = []
for m in MANIGANCES:
    modele = json.load(open(os.path.join(JEU, 'data/scenarios/%s_hammerhead.json' % m), encoding='utf-8'))
    for expert in (False, True):
        s = copy.deepcopy(modele)
        s['name'] = modele['name'].replace('(Hammerhead)', '(Jigsaw)')
        s['villain'] = ['pu056b', 'pu057b'] if expert else ['pu056a', 'pu057a']
        s['expert'] = expert
        s['encounter_sets'] = ['jigsaw' if e == 'hammerhead' else e for e in s['encounter_sets']]
        if expert and 'expert' not in s['encounter_sets']:
            s['encounter_sets'].append('expert')  # comme les scenarios Hammerhead expert
        nom = '%s_jigsaw%s' % (m, '_expert' if expert else '')
        ecrire('data/scenarios/%s.json' % nom, s)
        if not expert: noms.append('%s_jigsaw' % m)

p = os.path.join(JEU, 'data/sets_info.json')
si = json.load(open(p, encoding='utf-8'))
cle = '208. Custom (Punisher MC×DC 2026 « La ville ne dort jamais »)'
somme = si.pop('checksum', None); si.pop(cle, None)
si[cle] = {'name': PACK, 'scenarios': noms, 'heroes': [], 'encounters': ['jigsaw'], 'max_id': 'pu070'}
if somme: si['checksum'] = somme
with open(p, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(si, f, ensure_ascii=False, indent=1)
print('ok', len(cartes), 'cartes,', len(noms) * 2, 'scenarios')
