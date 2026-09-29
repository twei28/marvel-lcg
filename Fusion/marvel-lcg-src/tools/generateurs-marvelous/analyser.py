"""Lecture d'un rapport de la batterie « Marvelous » : apparie temoin et Stan
Lee carte par carte, classe, et regroupe les ecarts par famille.

    python3 tools/generateurs-marvelous/analyser.py /tmp/marvelous.json [--json sortie.json]

Classes :
  VERT           temoin vert, Stan Lee vert (empreintes comparees a part) ;
  ECART          temoin vert, Stan Lee rouge : c'est la cible de la batterie ;
  NON CONCLUANT  temoin rouge : le cas n'est pas montable tel quel (cible
                 absente, cout special...), Stan Lee n'est pas juge ;
  INCOMPLET      un des deux cas manque (processus mort, filtre).
Les familles d'ecarts sont tirees du message du cas Stan Lee (INJOUABLE,
traceback, pas en jeu, encore en main...).
"""
import json
import re
import sys
from collections import Counter, defaultdict


def charger(chemin):
    return json.load(open(chemin, encoding="utf-8"))


def carte_de(nom):
    m = re.match(r"\[marvelous\] (\S+) ", nom)
    return m.group(1) if m else None


def famille(message):
    m = message or ""
    if "INJOUABLE" in m:
        return "injouable (CanPlayBy)"
    if "n'est pas en main" in m:
        return "carte jamais arrivee en main"
    if "la partie a plante" in m or "Traceback" in m or "Error" in m and "echec de la mise en place" in m:
        return "plantage / exception"
    if "n'est pas en jeu" in m:
        return "jouee mais pas en jeu"
    if "encore en main" in m:
        return "evenement reste en main"
    if "processus mort" in m:
        return "processus mort"
    if "jamais ete atteint" in m:
        return "tour du joueur jamais atteint"
    return "autre"


def empreinte_de(message):
    m = re.search(r"empreinte=(\{.*\})\s*$", message or "")
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except ValueError:
        return None


def analyser(rapport):
    paires = defaultdict(dict)
    for r in rapport.get("cas", []):
        cid = carte_de(r.get("nom", ""))
        if not cid:
            continue
        role = "stan" if r["nom"].endswith("Stan Lee") else "temoin"
        paires[cid][role] = r
    classes = {"VERT": [], "ECART": [], "NON CONCLUANT": [], "INCOMPLET": []}
    effets = []
    for cid, p in sorted(paires.items()):
        t, s = p.get("temoin"), p.get("stan")
        if t is None or s is None:
            classes["INCOMPLET"].append((cid, p))
            continue
        if not t["ok"]:
            classes["NON CONCLUANT"].append((cid, p))
        elif not s["ok"]:
            classes["ECART"].append((cid, p))
        else:
            classes["VERT"].append((cid, p))
            et, es = empreinte_de(t["message"]), empreinte_de(s["message"])
            if et and es:
                # `main` et `defausse` different d'une carte par construction
                # (taille de main 5 chez Stan Lee, 6 chez la plupart) : seul
                # le nombre de cartes du joueur EN JEU vaut comparaison.
                diff = {k: (et.get(k), es.get(k)) for k in ("jeu",)
                        if et.get(k) != es.get(k)}
                if diff:
                    effets.append((cid, diff))
    return classes, effets


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    sortie = None
    if "--json" in sys.argv:
        sortie = sys.argv[sys.argv.index("--json") + 1]
    rapport = charger(args[0])
    classes, effets = analyser(rapport)
    total = sum(len(v) for v in classes.values())
    print(f"{total} cartes appariees : " + ", ".join(f"{k} {len(v)}" for k, v in classes.items()))
    familles = Counter(famille(p["stan"]["message"]) for _, p in classes["ECART"])
    if familles:
        print("\nFamilles d'ecarts (Stan Lee rouge, temoin vert) :")
        for f, n in familles.most_common():
            print(f"  {n:4d}  {f}")
    par_set = Counter(p["stan"]["nom"].split(" — ")[0] for _, p in classes["ECART"])
    print("\nEcarts, le detail :")
    for cid, p in classes["ECART"]:
        print(f"  {cid:8s} {p['stan']['nom'][12:60]:50s} | {p['stan']['message'][:140]}")
    if effets:
        print(f"\nVerts avec une empreinte differente (a lire, pas forcement un ecart) : {len(effets)}")
        for cid, diff in effets[:40]:
            print(f"  {cid:8s} {diff}")
    nc = Counter(famille(p["temoin"]["message"]) for _, p in classes["NON CONCLUANT"])
    if nc:
        print("\nNon concluants (temoin rouge), par famille :")
        for f, n in nc.most_common():
            print(f"  {n:4d}  {f}")
    if sortie:
        json.dump({k: [{"carte": cid, "temoin": p.get("temoin"), "stan": p.get("stan")} for cid, p in v]
                   for k, v in classes.items()} | {"empreintes_differentes": effets},
                  open(sortie, "w"), indent=1, ensure_ascii=False)
        print(f"\nDetail ecrit dans {sortie}")


if __name__ == "__main__":
    main()
