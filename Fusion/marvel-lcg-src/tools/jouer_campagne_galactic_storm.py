"""Joue les 5 scenarios de Galactic Storm A LA SUITE, avec le vrai pilote d'autoplay (pas le
pilote scripte de test_campagnes.py), le carnet de campagne circulant reellement d'une partie
a l'autre via `campaign_log_last.json` (meme mecanisme que l'ecran de campagne reel).

Demande par l'utilisateur (revue multichoix du 21/10/2026, point 6 : « Autoplay enchaine
maintenant ») : preuve qu'un joueur HUMAIN pourrait jouer les 5 parties de la campagne d'affilee
sans que rien ne bloque, au-dela des epreuves `epreuves_campagnes.py` (qui forcent la victoire/
defaite par script et ne jouent pas vraiment).

Usage
-----
    python3.10 tools/jouer_campagne_galactic_storm.py <game_dir> [--deck spider_man]
                                                       [--difficulte normal] [--graine 100]

⚠ Un seul heros d'un bout a l'autre (simplification assumee : la rotation a 3 identites est a
l'appreciation du joueur, honor system, voir MODE-CAMPAGNE-GABARIT.md). `--deck` accepte aussi
plusieurs noms separes par `+` (comme `autoplay.py --deck a+b`, partie a 2 joueurs) ; la boucle
reste alors inchangee, le pilote joue les deux sieges.
"""
import argparse
import json
import os
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
AUTOPLAY = os.path.join(ICI, "autoplay.py")

SCENARIOS = [
    "gs_kree_sentry",
    "gs_majestrix_verdict",
    "gs_hala_ultimatum",
    "gs_earth_under_siege",
    "gs_supreme_intelligence",
]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("game_dir")
    ap.add_argument("--deck", default="spider_man")
    ap.add_argument("--difficulte", default="normal")
    ap.add_argument("--profil", default="equilibre")
    ap.add_argument("--graine", type=int, default=100)
    ap.add_argument("--port", type=int, default=29000)
    ap.add_argument("--minuteur", type=int, default=900)
    args = ap.parse_args()

    game_dir = os.path.abspath(args.game_dir)
    carnet_fichier = os.path.join(game_dir, "campaign_log_last.json")

    carnet: dict = {}
    port = args.port
    etapes = []
    for scenario in SCENARIOS:
        if os.path.exists(carnet_fichier):
            os.remove(carnet_fichier)

        sortie = f"/tmp/campagne_gs_{scenario}.json"
        if os.path.exists(sortie):
            os.remove(sortie)
        lot = {"deck": args.deck, "vilain": scenario, "difficulte": args.difficulte,
               "profil": args.profil, "graine": args.graine, "port": port,
               "sortie": sortie}
        env = dict(os.environ, AUTOPLAY_LOT=json.dumps(lot),
                   AUTOPLAY_REGLES="mode_campaign",
                   AUTOPLAY_CARNET=json.dumps(carnet))
        print(f"--- {scenario} --- carnet entrant : {carnet}", flush=True)
        proc = subprocess.run(
            [sys.executable, AUTOPLAY, game_dir, "--trace", "0"],
            env=env, timeout=args.minuteur)
        port += 1

        resultat = (json.load(open(sortie)) if os.path.exists(sortie) else
                    {"verdict": "minuteur ou plantage", "gagne": None,
                     "message": f"aucun fichier de resultat (code retour {proc.returncode})"})

        carnet_sortant = {}
        if os.path.exists(carnet_fichier):
            brut = json.load(open(carnet_fichier))
            carnet_sortant = {str(k): str(v) for k, v in (brut.get("suggestions") or {}).items()}
            carnet.update(carnet_sortant)

        etapes.append({"scenario": scenario, "gagne": resultat.get("gagne"),
                       "verdict": resultat.get("verdict"), "rounds": resultat.get("rounds"),
                       "raison": resultat.get("raison"), "carnet_sortant": carnet_sortant})
        print(f"    -> gagne={resultat.get('gagne')!r} verdict={resultat.get('verdict')!r} "
              f"rounds={resultat.get('rounds')} carnet sortant : {carnet_sortant}", flush=True)

    print("\n=== BILAN CAMPAGNE ===")
    for e in etapes:
        statut = "VICTOIRE" if e["gagne"] is True else (
            "DEFAITE" if e["gagne"] is False else f"INCIDENT ({e['verdict']})")
        print(f"{e['scenario']:<26} {statut:<20} {e['rounds']} round(s)"
              + (f"  [{e['raison']}]" if e.get("raison") else ""))
    print(f"\nCarnet final : {carnet}")


if __name__ == "__main__":
    main()
