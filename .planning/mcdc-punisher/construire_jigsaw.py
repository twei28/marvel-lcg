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

ROT_HORAIRE = ('pu065', 'pu114', 'pu131', 'pu113', 'pu119', 'pu088a', 'pu089a', 'pu099')   # scan couche, texte montant
ROT_ANTIHORAIRE = ('pu088b', 'pu089b',)                                                   # scan couche, texte descendant
PAGE = {'pu071a': 141, 'pu071b': 142, 'pu072a': 143, 'pu072b': 144, 'pu073': 145, 'pu074': 147, 'pu075': 149,
        'pu076': 151, 'pu077': 153, 'pu078': 155, 'pu079': 157, 'pu080': 159, 'pu082': 163, 'pu084': 167,
        'pu086a': 171, 'pu086b': 172, 'pu087a': 173, 'pu087b': 174, 'pu088a': 175, 'pu088b': 176, 'pu089a': 177, 'pu089b': 178,
        'pu090a': 179, 'pu090b': 180, 'pu091a': 181, 'pu091b': 182, 'pu092': 183, 'pu093': 185, 'pu094': 187, 'pu095': 189, 'pu096': 191,
        'pu097': 193, 'pu098': 195, 'pu099': 197, 'pu100': 199, 'pu102': 203, 'pu104': 207, 'pu105': 209,
        'pu106a': 211, 'pu106b': 212, 'pu107': 213, 'pu108': 215, 'pu109': 217, 'pu110': 219, 'pu111': 221, 'pu113': 225,
        'pu119': 237, 'pu120': 239, 'pu121': 241, 'pu123': 245,
        'pu114': 227, 'pu115': 229, 'pu116': 231, 'pu117': 233, 'pu118': 235, 'pu125': 249, 'pu126': 251, 'pu127': 253,
        'pu128': 255, 'pu129': 257, 'pu130': 259, 'pu131': 261, 'pu139': 277,
        'pu048a': 95, 'pu048b': 96, 'pu049a': 97, 'pu049b': 98, 'pu050a': 99, 'pu050b': 100, 'pu051a': 101, 'pu051b': 102, 'pu052a': 103, 'pu052b': 104, 'pu053a': 105, 'pu053b': 106, 'pu054a': 107, 'pu054b': 108, 'pu055a': 109, 'pu055b': 110,
        'pu005': 9, 'pu006': 11, 'pu030': 59, 'pu031': 61, 'pu032': 63, 'pu033': 65, 'pu034': 67, 'pu035': 69, 'pu036': 71, 'pu037': 73, 'pu038': 75,
        'pu056a': 111, 'pu056b': 112, 'pu057a': 113, 'pu057b': 114, 'pu058': 115, 'pu059': 117, 'pu060': 119,
        'pu063': 125, 'pu064': 127, 'pu065': 129, 'pu066': 131, 'pu068': 135, 'pu070': 139}
STAGE = {'pu056a': '1', 'pu056b': '2', 'pu057a': '2', 'pu057b': '3',
         'pu071a': '1', 'pu071b': '2', 'pu072a': '2', 'pu072b': '3'}   # chiffre romain imprime sur le scan


def stat(v):
    v = str(v).replace('\U0001F464', '*')
    if v == '★': return '0**'
    return v.replace('★+1', '1**').replace('2+★', '2**').replace('★+2', '2**').replace('★', '**')


cartes = []
CORRECTIONS = {'pu131': {'Amplify': '2'}, 'pu113': {'Hazard': '1'}}   # deux icones Amplify imprimees (scan p261), absentes des defs
for x in defs.JIGSAW_CARDS + defs.HOBGOBLIN_CARDS + defs.ARMORY_CARDS + defs.SYNDICATE_CARDS + defs.CAPO_OF_THE_PAST_CARDS + defs.HITLIST_CARDS + defs.SWAT_CARDS + defs.PUNISHMENT_CARDS + defs.BIGAPPLE_CARDS + defs.LOCATION_CARDS + defs.CAPO_CARDS:
    d = {k: stat(v) for k, v in x['desc'].items()}
    if x['card_id'] in STAGE: d['Stage'] = STAGE[x['card_id']]
    d.update(CORRECTIONS.get(x['card_id'], {}))
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
    im = Image.open(os.path.join(SCANS, 'p%03d.jpg' % n)).convert('RGB')
    if cid in ROT_HORAIRE: im = im.rotate(-90, expand=True)
    elif cid in ROT_ANTIHORAIRE: im = im.rotate(90, expand=True)     # manigance annexe : scan couche, on remet a plat
    im.save(os.path.join(JEU, 'assets/pics', cid + '.jpg'), quality=92)

def ecrire(chemin, obj):
    with open(os.path.join(JEU, chemin), 'w', encoding='utf-8', newline='\n') as f:
        json.dump(obj, f, ensure_ascii=False, indent=4); f.write('\n')

ecrire('data/encounter_sets/jigsaw.json', {'version': '0.5.8', 'name': 'Jigsaw', 'encounters': defs.JIGSAW_ENCOUNTERS})
ecrire('data/encounter_sets/punishers_armory.json', {'version': '0.5.8', 'name': "Punisher's Armory", 'encounters': defs.ARMORY_ENCOUNTERS})
ecrire('data/encounter_sets/the_syndicate.json', {'version': '0.5.8', 'name': 'The Syndicate', 'encounters': defs.SYNDICATE_ENCOUNTERS})
ecrire('data/encounter_sets/capo_of_the_past.json', {'version': '0.5.8', 'name': 'Capo of the Past', 'encounters': defs.CAPO_OF_THE_PAST_ENCOUNTERS})
ecrire('data/encounter_sets/punishers_hit_list.json', {'version': '0.5.8', 'name': "Punisher's Hit List", 'encounters': defs.HITLIST_ENCOUNTERS})
ecrire('data/encounter_sets/swat_team.json', {'version': '0.5.8', 'name': 'SWAT Team', 'encounters': defs.SWAT_ENCOUNTERS})
ecrire('data/encounter_sets/punishment.json', {'version': '0.5.8', 'name': 'Punishment', 'encounters': defs.PUNISHMENT_ENCOUNTERS})
ecrire('data/encounter_sets/the_big_apple.json', {'version': '0.5.8', 'name': 'The Big Apple', 'encounters': defs.BIGAPPLE_ENCOUNTERS})
ecrire('data/encounter_sets/locations_the_big_apple.json', {'version': '0.5.8', 'name': 'Locations - The Big Apple', 'encounters': defs.LOCATIONS_SET_ASIDE})
ecrire('data/encounter_sets/capos.json', {'version': '0.5.8', 'name': 'CAPOS', 'encounters': defs.CAPO_SET_ASIDE})
ecrire('data/encounter_sets/hobgoblin.json', {'version': '0.5.8', 'name': 'Hobgoblin', 'encounters': defs.HOBGOBLIN_ENCOUNTERS})

MANIGANCES = ['art_museum_heist', 'the_getaway', 'protection_racket', 'the_raft_breakout', 'stop_the_presses']
# (suffixe, nom affiche, set de rencontre, [vilains standard], [vilains expert])
VILAINS = [('jigsaw', 'Jigsaw', 'jigsaw', ['pu056a', 'pu057a'], ['pu056b', 'pu057b']),
           ('hobgoblin', 'Hobgoblin', 'hobgoblin', ['pu071a', 'pu072a'], ['pu071b', 'pu072b'])]
noms = []
for suffixe, affiche, jeu_rencontre, standard, expert_v in VILAINS:
    for m in MANIGANCES:
        modele = json.load(open(os.path.join(JEU, 'data/scenarios/%s_hammerhead.json' % m), encoding='utf-8'))
        for expert in (False, True):
            s = copy.deepcopy(modele)
            s['name'] = modele['name'].replace('(Hammerhead)', '(%s)' % affiche)
            s['villain'] = expert_v if expert else standard
            s['expert'] = expert
            s['encounter_sets'] = [jeu_rencontre if e == 'hammerhead' else e for e in s['encounter_sets']]
            if expert and 'expert' not in s['encounter_sets']:
                s['encounter_sets'].append('expert')  # comme les scenarios Hammerhead expert
            nom = '%s_%s%s' % (m, suffixe, '_expert' if expert else '')
            ecrire('data/scenarios/%s.json' % nom, s)
            if not expert: noms.append('%s_%s' % (m, suffixe))

# --- Scenario 3 « One Last Kill » : Punisher + un vilain SOUS-FIFRE (Jigsaw ou Hobgoblin), standard et expert.
for suffixe, fif_std, fif_exp, ens in (('jigsaw', 'pu056a', 'pu056b', 'jigsaw'), ('hobgoblin', 'pu071a', 'pu071b', 'hobgoblin')):
    for expert in (False, True):
        s = {'version': '0.5.8', 'name': 'One Last Kill (%s)' % suffixe.capitalize(),
             'villain': ['pu086b', 'pu087b'] if expert else ['pu086a', 'pu087a'], 'expert': expert,
             'schemes': ['pu088a,pu088b', 'pu089a,pu089b'],
             'set_aside': list(defs.PUNISHMENT_SET_ASIDE) + [fif_exp if expert else fif_std],
             'encounters': [], 'encounter_sets': ['punishment', ens, 'standard'] + (['expert'] if expert else []),
             'modular_sets': ['punishers_armory']}
        ecrire('data/scenarios/one_last_kill_%s%s.json' % (suffixe, '_expert' if expert else ''), s)
        if not expert: noms.append('one_last_kill_%s' % suffixe)

p = os.path.join(JEU, 'data/sets_info.json')
si = json.load(open(p, encoding='utf-8'))
cle = '208. Custom (Punisher MC×DC 2026 « La ville ne dort jamais »)'
somme = si.pop('checksum', None); si.pop(cle, None)
si[cle] = {'name': PACK, 'scenarios': noms, 'heroes': [], 'encounters': ['jigsaw', 'hobgoblin', 'punishers_armory', 'the_syndicate', 'capo_of_the_past', 'punishers_hit_list', 'swat_team', 'punishment', 'the_big_apple', 'locations_the_big_apple', 'capos'], 'max_id': 'pu139'}
if somme: si['checksum'] = somme
with open(p, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(si, f, ensure_ascii=False, indent=1)
print('ok', len(cartes), 'cartes,', len(noms) * 2, 'scenarios')
