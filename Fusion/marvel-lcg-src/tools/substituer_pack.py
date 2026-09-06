"""Preuve par substitution d'un pack entier, en une commande.

L'etape 7 de PROCESSUS-CARTE.md exige, pour CHAQUE capacite, la preuve que le
cas de test tombe au ROUGE quand le module disparait. Fait a la main c'est un
aller-retour par carte ; ici : pour chaque module du pack, on le remplace par
un stub vide (`GetAbilities -> []`), on relance les cas du harnais filtres
sur son card_id, on note combien tombent, puis on restaure.

Lecture du rapport :
- « rouges N/N »          : la carte est PROUVEE ;
- « rouges N/M » (N<M)    : un cas reste vert sans le module. Normal pour un
  CONTRE-CAS qui verifie une ABSENCE d'effet (vp014/vp015, ho017) : a assumer
  dans le journal de portage. Anormal pour un cas nominal : le cas ne teste
  pas ce qu'il croit ;
- « AUCUN CAS »           : la carte n'a pas de cas sujet — la gate n'est pas
  tenue, ecrire le cas d'abord.

Usage
-----
    python3.10 tools/substituer_pack.py <game_dir> <port_base> <prefixe>
    # ex.:  ... .game-src 31000 ho0

⚠ JAMAIS en parallele d'un autre harnais (test_capacites, autoplay,
verifier_tous_les_decks) : chaque processus fils reecrit
`<game_dir>/launch.json` (voir l'annotation des deux autres outils).
⚠ Le stub est pose sur le FICHIER SOURCE puis restaure : ne pas interrompre
brutalement ; en cas de doute, `git status` doit rester propre a la fin.

⚠⚠ ET `git status` NE SUFFIT PAS POUR UN PACK NEUF. Un pack pas encore commite
est UNTRACKED : git ne montre alors aucune modification, et un stub laisse par
une execution interrompue passe INAPERCU. C'est arrive le 06/09/2026 sur
`sunfire` — la premiere execution, lancee au premier plan, a ete coupee par une
limite de temps de l'outil appelant et a laisse `sf014.py` reduit a
`GetAbilities -> []`. Les executions suivantes de `test_capacites` ont alors
mesure un module VIDE : un seul cas rouge, qui ressemblait a une regression, et
trois corrections ecrites pour rien avant que le fichier ne soit relu.

PROCEDURE SURE, a appliquer pour un pack non commite :

    S=/tmp/sauvegarde_pack && rm -rf $S && mkdir -p $S
    cp -r src/cards/pack/<pack> $S/
    md5sum src/cards/pack/<pack>/*/*.py | md5sum      # empreinte AVANT
    python3.10 tools/substituer_pack.py <game_dir> <port> <prefixe>
    md5sum src/cards/pack/<pack>/*/*.py | md5sum      # doit etre IDENTIQUE

Un ecart d'empreinte, ou un fichier de moins de 10 lignes, veut dire qu'un stub
est reste : restaurer depuis $S avant toute autre mesure.

Origine : le script jetable substitutions.sh du portage harry_osborn
(31/08/2026), promu ici en outil du projet.
"""
import glob
import json
import os
import shutil
import subprocess
import sys

STUB = ('from . import *\n\n'
        'def GetAbilities() -> Sequence["Ability"]:\n'
        '    return []\n')

PAS_DE_PORT = 60  # ecart entre deux cartes : chaque cas fils ouvre port+rang


def purger_pycache(racine: str) -> None:
    for chemin in glob.glob(os.path.join(racine, '**', '__pycache__'),
                            recursive=True):
        shutil.rmtree(chemin, ignore_errors=True)


def main() -> None:
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    game_dir = os.path.abspath(os.path.expanduser(sys.argv[1]))
    port = int(sys.argv[2])
    prefixe = sys.argv[3]

    ici = os.path.dirname(os.path.abspath(__file__))
    racine = os.path.dirname(ici)
    harnais = os.path.join(ici, 'test_capacites.py')

    fichiers = sorted(
        f for f in glob.glob(os.path.join(
            racine, 'src', 'cards', 'pack', '**', f'{prefixe}*.py'),
            recursive=True)
        if '__pycache__' not in f and not f.endswith('__init__.py'))
    if not fichiers:
        sys.exit(f"aucun module {prefixe}*.py sous src/cards/pack/")

    bilan = []
    for f in fichiers:
        card_id = os.path.basename(f)[:-3]
        pack_dir = os.path.dirname(os.path.dirname(f))
        sauvegarde = f + '.vrai'
        shutil.copy2(f, sauvegarde)
        try:
            open(f, 'w').write(STUB)
            purger_pycache(pack_dir)
            rapport = f'/tmp/subst_{card_id}.json'
            subprocess.run(
                [sys.executable, harnais, game_dir, str(port),
                 rapport, card_id + ' '],
                capture_output=True, timeout=3600)
            try:
                r = json.load(open(rapport))
                rouges = sum(1 for c in r['cas'] if not c['ok'])
                total = r['total']
            except Exception:
                rouges, total = -1, -1
        finally:
            shutil.move(sauvegarde, f)
            purger_pycache(pack_dir)
        port += PAS_DE_PORT

        if total == 0:
            verdict = 'AUCUN CAS — gate non tenue'
        elif rouges < 0:
            verdict = 'rapport illisible'
        elif rouges == total:
            verdict = f'rouges {rouges}/{total}'
        else:
            verdict = f'rouges {rouges}/{total} ⚠ un cas reste vert sans module'
        bilan.append((card_id, total, rouges, verdict))
        print(f'SUBST {card_id} : {verdict}', flush=True)

    prouvees = sum(1 for _, t, r, _ in bilan if t > 0 and r > 0)
    print(f'\nBILAN : {prouvees}/{len(bilan)} cartes avec au moins un cas '
          f'tombe au rouge sans leur module')
    sys.exit(0 if prouvees == len(bilan) else 1)


if __name__ == '__main__':
    main()
