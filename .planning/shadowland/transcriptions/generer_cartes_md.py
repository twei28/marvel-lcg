"""Regenere docs/packs/shadowland/cartes.md depuis toutes-relues.json (transcription relue par un second regard, 22/10/2026)."""
import json, re, collections, os
ICI = os.path.dirname(os.path.abspath(__file__))
SORTIE = os.path.abspath(os.path.join(ICI, "..", "..", "..", "docs", "packs", "shadowland", "cartes.md"))
allc = json.load(open(os.path.join(ICI, "toutes-relues.json")))

def sl(i):
    m = re.match(r'65(\d{3})([AB]?)', i)
    return 'sl' + m.group(1) + m.group(2).lower()

by = collections.defaultdict(dict)
for c in allc:
    m = re.match(r'(\d+)\s*/\s*(\d+)', c['numero_dans_set'])
    by[c['set']][re.match(r'65\d{3}', c['id_scan']).group(0)] = (int(m.group(1)), int(m.group(2)))
qty = {}
for s, d in by.items():
    items = sorted(d.items(), key=lambda kv: kv[1][0])
    mx = items[0][1][1]
    for i, (k, (n, _)) in enumerate(items):
        nxt = items[i + 1][1][0] if i + 1 < len(items) else mx + 1
        qty[k] = nxt - n
order = ['SHADOWS IN THE NIGHT', 'DARK PROTÉGÉ', 'NINJA SWARM', 'SHADOW LABYRINTH', 'DEADLY CONTRAPTIONS', 'HEART OF SHADOW', 'BLACK FLOWER']
L = []
L.append("# Shadowland (MC65) : inventaire des cartes\n")
L.append("Transcription du 22/10/2026 depuis les 93 scans de play.marvelsimulator.com (`.planning/shadowland/scans-marvelsimulator/`), **relue par un second regard independant** (5 relectures, une par lot, `verif1-5.json`) : 23 corrections appliquees (menaces cible/depart, icones, lignes de traits retirees du texte). **Aucun texte n'est encore valide contre le livret ni contre MarvelCDB.** Fichier genere par `.planning/shadowland/transcriptions/generer_cartes_md.py` depuis `toutes-relues.json` ; la transcription brute est `toutes.json`.\n")
L.append("Identifiants du jeu : `65NNN[A|B]` officiel -> `slNNN[a|b]` (prefixe `sl`, voir `PLAN.md`).\n")
L.append("## Verifie\n")
L.append("- **93 images, 78 numeros, 90 exemplaires** : la somme des totaux imprimes par set (13+16+9+11+11+17+13) fait 90, comme l'annonce du produit ; les « trous » dans la numerotation « n/m » d'un set sont les exemplaires multiples d'une meme carte (quantite = ecart avec le numero suivant). La quantite est DEDUITE, pas lue.")
L.append("- L'icone rouge en forme de **Y** est l'icone **Boost** (compare a Sandman 01102 Boost 2, Breakin' & Takin' 01107 Boost 2, Armored Guard 01120 Boost 1) ; l'etoile rouge isolee est l'icone de boost « ★ » (effet ecrit dans le texte).")
L.append("- **Complot principal, face B** : le rond en haut a gauche est la menace **cible** (TargetThreat), le nombre en bas a droite est la menace de **depart** (StartingThreat), `+1` au-dessus est l'escalade (compare a 01097b The Break-In!).")
L.append("- **Icones de manigance**, comparees au zoom a 01107 Hazard, 01108 Crisis, 01109 Acceleration, 16054/16069 Amplify : Crisis sl007, sl009, sl025, sl042, sl048, sl075 ; Hazard sl024, sl070 ; Acceleration sl043, sl076 (x2) ; Amplify aucune ; sl008 n'imprime aucune icone (le texte en accorde selon la position du vilain).")
L.append("- **Ressources dans le texte** : poing = physique [physical], eclair = energie [energy], reseau de noeuds = mentale [mental] (comme sur Genius 01089).")
L.append("- La **ligne de traits** (« TRAP! », « CONDITION. », « HAND. POSSESSED. »...) est dans `Traits`, pas dans le texte.\n")
L.append("## Recapitulatif par set\n")
L.append("| Set | Numeros | Faces | Exemplaires |\n|---|---|---|---|")
for s in order:
    ids = [c for c in allc if c['set'] == s]
    nums = sorted({re.match(r'65\d{3}', c['id_scan']).group(0) for c in ids})
    L.append(f"| {s} | {nums[0]}-{nums[-1]} ({len(nums)}) | {len(ids)} | {sum(qty[n] for n in nums)} |")
L.append("\n## Cartes\n")
for s in order:
    L.append(f"### {s}\n")
    for c in [x for x in allc if x['set'] == s]:
        k = re.match(r'65\d{3}', c['id_scan']).group(0)
        L.append(f"#### {sl(c['id_scan'])} ({c['id_scan']}) : {c['titre']}{' ★unique' if c['unique'] else ''} — {c['type']}{' ' + c['face'] if c['face'] else ''}, {c['numero_dans_set']}, x{qty[k]}")
        if c['traits']: L.append("- Traits : " + ", ".join(c['traits']))
        if c['stats']: L.append("- Valeurs : " + ", ".join(f"{a}={b}" for a, b in c['stats'].items()))
        if c['icones']: L.append("- Icones : " + " ; ".join(i if isinstance(i, str) else json.dumps(i, ensure_ascii=False) for i in c['icones']))
        L.append("- Texte :")
        for ln in (c['texte'] or '').split('\n'): L.append("  > " + ln)
        if c['citation']: L.append(f"- Citation : {c['citation']}")
        if c['pied']: L.append(f"- Pied : {c['pied']}")
        L.append("")
open(SORTIE, 'w').write("\n".join(L))
print(SORTIE, len(L))
