"""Balayage des seuils du pilote : cherche le reglage qui gagne le plus.

Regler un bot a la main, seuil par seuil, deplace le probleme d'un mode
d'echec a l'autre sans qu'on sache jamais si on progresse. La machine joue une
partie en 3 secondes : autant lui faire explorer l'espace des seuils.

Chaque combinaison est jouee sur les MEMES graines, sinon la comparaison ne
vaut rien. Le classement se fait sur le taux de victoire, puis sur les PV
restants du vilain, qui departagent les reglages a zero victoire en disant
lequel s'approche le plus du but.

Usage
-----
    python3.10 tools/calibrer.py .game-src --deck spider_man --vilain rhino \\
        --graines 10 --paralleles 4
"""
import argparse
import itertools
import json
import os
import subprocess
import sys
import time

AUTOPLAY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "autoplay.py")

# L'espace explore. Volontairement large : le but est de savoir si un reglage
# gagne, pas de confirmer une intuition.
GRILLE = {
    "poids_survie": [8, 14, 20],
    "poids_progression": [4, 8, 12],
    "poids_activation": [2, 5, 9],
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("game_dir")
    ap.add_argument("--deck", default="spider_man")
    ap.add_argument("--vilain", default="rhino")
    ap.add_argument("--difficulte", default="normal")
    ap.add_argument("--graines", type=int, default=10)
    ap.add_argument("--paralleles", type=int, default=4)
    ap.add_argument("--rapport", default="/tmp/calibrage.json")
    args = ap.parse_args()

    noms = sorted(GRILLE)
    combos = [dict(zip(noms, valeurs))
              for valeurs in itertools.product(*(GRILLE[n] for n in noms))]
    print(f"{len(combos)} reglages x {args.graines} graines = "
          f"{len(combos) * args.graines} parties", flush=True)

    resultats = []
    depart = time.time()
    for i, combo in enumerate(combos, 1):
        rapport = f"/tmp/calibrage_{i}.json"
        subprocess.run(
            [sys.executable, AUTOPLAY, args.game_dir,
             "--deck", args.deck, "--vilains", args.vilain,
             "--difficultes", args.difficulte, "--profils", "equilibre",
             "--parties", str(args.graines), "--paralleles", str(args.paralleles),
             "--minuteur", "120", "--rapport", rapport,
             "--reglages", json.dumps(combo)],
            capture_output=True)
        if not os.path.exists(rapport):
            continue
        donnees = json.load(open(rapport))
        parties = donnees["parties"]
        victoires = sum(1 for p in parties if p.get("gagne") is True)
        joues = sum(1 for p in parties if p.get("gagne") is not None)
        restes = [p.get("vilain_pv") for p in parties
                  if p.get("vilain_pv") is not None]
        rounds = [p.get("rounds", 0) for p in parties]
        resultats.append({
            "reglages": combo, "victoires": victoires, "joues": joues,
            "pv_vilain_moyen": round(sum(restes) / len(restes), 1) if restes else None,
            "pv_vilain_mini": min(restes) if restes else None,
            "rounds_moyen": round(sum(rounds) / len(rounds), 1) if rounds else None,
        })
        r = resultats[-1]
        print(f"[{i:>3}/{len(combos)}] {json.dumps(combo)} -> "
              f"{victoires}/{joues} V, vilain reste {r['pv_vilain_moyen']}, "
              f"{r['rounds_moyen']} rounds  ({round(time.time() - depart)}s)",
              flush=True)

    resultats.sort(key=lambda r: (-r["victoires"], r["pv_vilain_moyen"] or 99))
    print("\n=== MEILLEURS REGLAGES ===")
    for r in resultats[:8]:
        print(f"  {r['victoires']}/{r['joues']} V  vilain {r['pv_vilain_moyen']:>5} "
              f"(mini {r['pv_vilain_mini']})  {r['rounds_moyen']:>5} rounds   "
              f"{json.dumps(r['reglages'])}")
    json.dump(resultats, open(args.rapport, "w"), indent=1, ensure_ascii=False)
    print(f"\nRapport : {args.rapport}")


if __name__ == "__main__":
    main()
