"""Pour chaque module donne : pose un stub, rejoue SES cas, dit lesquels
restent VERTS sans le module, puis restaure. C'est la lecture detaillee que
`substituer_pack.py` ne donne pas (il ne compte que les rouges).

    python3.10 qui_reste_vert.py <game_dir> <port_base> <card_id> [<card_id>...]
"""
import glob
import json
import os
import shutil
import subprocess
import sys

RACINE = '/mnt/c/Users/arnau/Desktop/Marvel LCG/Fusion/marvel-lcg-src'
STUB = ('from . import *\n\n'
        'def GetAbilities() -> Sequence["Ability"]:\n'
        '    return []\n')

game_dir, port_base, modules = sys.argv[1], int(sys.argv[2]), sys.argv[3:]
os.chdir(RACINE)

for i, card_id in enumerate(modules):
    chemins = glob.glob(f'src/cards/pack/fne/**/{card_id}.py', recursive=True)
    if not chemins:
        print(f'{card_id} : module introuvable')
        continue
    chemin = chemins[0]
    sauvegarde = f'/tmp/sauvegarde_{card_id}.py'
    shutil.copy(chemin, sauvegarde)
    prefixe = f'qrv{i}'
    for vieux in glob.glob(f'/tmp/capacites_{prefixe}*.json'):
        os.remove(vieux)
    try:
        open(chemin, 'w', encoding='utf-8').write(STUB)
        subprocess.run(
            ['/home/arnau/marvel-work/python/bin/python3.10', 'tools/test_capacites.py',
             game_dir, str(port_base + i * 50), f'/tmp/rapport-{prefixe}.json', card_id],
            env=dict(os.environ, RELEASE='1', PARALLELES='4', CAS_PREFIX=prefixe),
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=2400)
    finally:
        shutil.copy(sauvegarde, chemin)
    verts = []
    for f in glob.glob(f'/tmp/capacites_{prefixe}*.json'):
        d = json.load(open(f, encoding='utf-8'))
        if d['ok']:
            verts.append(d['nom'])
    print(f'--- {card_id} : {len(verts)} cas VERT(S) sans le module')
    for nom in sorted(verts):
        print(f'    {nom}')
    sys.stdout.flush()
