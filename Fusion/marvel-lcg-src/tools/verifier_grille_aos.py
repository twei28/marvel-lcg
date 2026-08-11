"""La grille des 27 combinaisons d'Agents of S.H.I.E.L.D. existe EN DOUBLE.

Elle est relevee sur le carnet imprime (`mc50_agents_of_shield_campaign_log.pdf`,
bloc « Evidence Combinations ») et recopiee a deux endroits qui ne se parlent
pas :

* `src/cards/pack/aos/baron_zemo/__init__.py`, dans `MembreDeLaCombinaison` :
  c'est elle qui designe la taupe et l'accuse pendant la partie ;
* `data/campagnes/aos.json`, bloc `enquete` : c'est elle que l'ecran raye.

Les deux ont ete relevees INDEPENDAMMENT et concordent. Mais rien ne les
comparait : modifier l'une sans l'autre les ferait diverger en silence, et le
joueur verrait une grille qui n'accuse pas le meme membre que le jeu. C'est
exactement le genre de defaut qu'on ne decouvre qu'en jouant cinq scenarios.

Cet outil ne demarre pas le moteur : il lit le module Python en AST, comme
`verifier_campagnes.py`, et le JSON tel quel.

    ~/marvel-work/python/bin/python3.10 tools/verifier_grille_aos.py

Sortie : une ligne par membre, et le detail des combinaisons qui divergent.
Code de retour non nul s'il en reste une.
"""
import ast
import json
import os
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODULE = os.path.join(RACINE, "src", "cards", "pack", "aos", "baron_zemo", "__init__.py")
DEFINITION = os.path.join(RACINE, "data", "campagnes", "aos.json")
FONCTION = "MembreDeLaCombinaison"

# Le nom de la liste Python <-> la cle du membre dans aos.json.
MEMBRES = {
    "ChiefMedicalOfficer": "Chief Medical Officer",
    "ChiefSurveillanceOfficer": "Chief Surveillance Officer",
    "ChiefTacticalOfficer": "Chief Tactical Officer",
}


def table_du_moteur():
    """Les trois listes de `MembreDeLaCombinaison`, identifiants resolus.

    La fonction declare d'abord ses neuf constantes (ORANGE1 = "50185"...) puis
    les trois tables qui s'en servent. On resout donc les noms dans l'ordre ou
    ils apparaissent, sans executer quoi que ce soit.
    """
    arbre = ast.parse(open(MODULE, encoding="utf-8").read())
    fonction = None
    for noeud in ast.walk(arbre):
        if isinstance(noeud, ast.FunctionDef) and noeud.name == FONCTION:
            fonction = noeud
            break
    if fonction is None:
        raise SystemExit(f"{FONCTION} est introuvable dans {MODULE}")

    constantes = {}
    tables = {}
    for noeud in fonction.body:
        if not isinstance(noeud, ast.Assign) or len(noeud.targets) != 1:
            continue
        cible = noeud.targets[0]
        if not isinstance(cible, ast.Name):
            continue
        valeur = noeud.value
        if isinstance(valeur, ast.Constant) and isinstance(valeur.value, str):
            constantes[cible.id] = valeur.value
        elif isinstance(valeur, ast.List) and cible.id in MEMBRES:
            lignes = []
            for ligne in valeur.elts:
                if not isinstance(ligne, ast.List):
                    raise SystemExit(f"{cible.id} : une ligne n'est pas une liste")
                lignes.append([constantes[x.id] for x in ligne.elts
                               if isinstance(x, ast.Name)])
            tables[cible.id] = lignes
    return tables


def table_de_l_ecran():
    definition = json.load(open(DEFINITION, encoding="utf-8"))
    enquete = definition.get("enquete") or {}
    return {m["cle"]: [c.split(";") for c in m["combinaisons"]]
            for m in (enquete.get("membres") or [])}


resultats = []


def verifier(nom, ok, detail=""):
    resultats.append((nom, bool(ok), detail))


moteur = table_du_moteur()
ecran = table_de_l_ecran()

verifier("les trois membres sont declares des deux cotes",
         len(moteur) == 3 and len(ecran) == 3, (sorted(moteur), sorted(ecran)))

toutes_moteur = []
for nom_py, cle in MEMBRES.items():
    du_moteur = [tuple(sorted(c)) for c in moteur.get(nom_py, [])]
    de_l_ecran = [tuple(sorted(c)) for c in ecran.get(cle, [])]
    toutes_moteur += du_moteur
    # L'ordre des lignes n'a aucun sens de jeu : le moteur compare une
    # combinaison TRIEE a ses lignes, l'ecran les affiche dans l'ordre du
    # carnet. On compare donc des ensembles.
    manquantes = sorted(set(du_moteur) - set(de_l_ecran))
    en_trop = sorted(set(de_l_ecran) - set(du_moteur))
    verifier(f"{cle} : neuf combinaisons de chaque cote",
             len(du_moteur) == 9 and len(de_l_ecran) == 9,
             (len(du_moteur), len(de_l_ecran)))
    verifier(f"{cle} : les deux tables disent la meme chose",
             not manquantes and not en_trop,
             {"absentes de l'ecran": manquantes, "absentes du moteur": en_trop})

# Le controle qui a servi a la transcription initiale, et qui reste vrai : les
# 27 combinaisons possibles doivent apparaitre chacune exactement une fois.
series = [("50185", "50186", "50187"), ("50188", "50189", "50190"),
          ("50191", "50192", "50193")]
attendues = {tuple(sorted((a, b, c))) for a in series[0] for b in series[1] for c in series[2]}
verifier("les 27 combinaisons possibles sont couvertes, chacune une fois",
         sorted(toutes_moteur) == sorted(attendues),
         {"manquantes": sorted(attendues - set(toutes_moteur)),
          "en double": sorted(x for x in set(toutes_moteur) if toutes_moteur.count(x) > 1)})

echecs = [r for r in resultats if not r[1]]
for nom, ok, detail in resultats:
    print(("  OK   " if ok else "  ECHEC") + f" {nom}" + (f"  ({detail})" if detail and not ok else ""))
print(f"\n{len(resultats) - len(echecs)}/{len(resultats)} verifications passees")
sys.exit(1 if echecs else 0)
