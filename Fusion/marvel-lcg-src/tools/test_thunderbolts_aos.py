"""Les Thunderbolts survivants reviennent au scenario 5 d'Agents of S.H.I.E.L.D.

Livret p.19, encart SETUP : « If you recorded any "Surviving Thunderbolts" in
the campaign log, shuffle those minions AND THEIR ENCOUNTER SETS, except for
Jolt's, into the encounter deck. »

Jusqu'ici la cle `Surviving Thunderbolts` etait ECRITE au scenario 4 et RELUE
nulle part : rien ne revenait, ni les sbires ni leurs sets.

Le « except for Jolt's » n'est pas une exception arbitraire : Jolt appartient au
set du scenario 4 lui-meme (`data/scenarios/thunderbolts.json`), et aucun
fichier de `data/encounter_sets/` ne la contient. Il n'y a donc rien a rapporter
avec elle — on ne remet que la carte. C'est ce que verifie le cas central :
Moonstone ramene son set, Jolt vient seule.

Usage : python3.10 tools/test_thunderbolts_aos.py [racine] [port]
"""
import json
import os
import subprocess
import sys
import tempfile

RACINE = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.expanduser(
    "~/marvel-work/fusion/marvel-lcg-src")
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 4850
SONDE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sonde_campagne.py")

TAUPE = "50185;50188;50191"
# Les sept sbires, et les cartes qui n'arrivent QUE par leur set modulaire.
SBIRES = {'50133': 'Jolt', '50139': 'Moonstone', '50143': 'Songbird',
          '50148': 'Black Widow', '50152': 'Radioactive Man',
          '50156': 'MACH-IV', '50161': 'Batroc'}
ACCOMPAGNEMENT = {'50140': 'gravitational_pull', '50141': 'gravitational_pull',
                  '50142': 'gravitational_pull', '50157': 'supersonic',
                  '50158': 'supersonic', '50159': 'supersonic', '50160': 'supersonic',
                  '50144': 'hard_sound', '50145': 'hard_sound',
                  '50146': 'hard_sound', '50147': 'hard_sound'}

resultats = []
port = PORT


def verifier(nom, ok, detail=""):
    resultats.append((nom, bool(ok), detail))


def sonder(carnet, campagne=True):
    global port
    port += 1
    rapport = os.path.join(tempfile.gettempdir(), f"tb_aos_{os.getpid()}_{port}.json")
    env = dict(os.environ, RAPPORT=rapport, CAMPAIGN_LOG=json.dumps(carnet),
               RULES=json.dumps(["mode_campaign"] if campagne else []))
    env.pop("FIN_DE_PARTIE", None)
    env.pop("PUZZLE", None)
    env.pop("CHOIX", None)
    subprocess.run([sys.executable, SONDE, RACINE, "baron_zemo", "maria_hill", str(port)],
                   env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    with open(rapport, encoding="utf-8") as f:
        sortie = json.load(f)
    os.remove(rapport)
    monde = sortie.get("monde") or {}
    deck = [c.get("card_id") for c in (monde.get("encounter_deck") or [])]
    return (sortie.get("erreurs") or [],
            sorted({SBIRES[c] for c in deck if c in SBIRES}),
            sorted({ACCOMPAGNEMENT[c] for c in deck if c in ACCOMPAGNEMENT}),
            len(deck))


# 1. Moonstone et Jolt survivent : la premiere ramene son set, la seconde non.
erreurs, sbires, sets, taille = sonder({"A.I.M. Envelope": TAUPE,
                                        "Surviving Thunderbolts": "Moonstone;Jolt"})
verifier("la mise en place tourne sans erreur", not erreurs, erreurs)
verifier("les deux survivants sont dans le deck de rencontre",
         sbires == ["Jolt", "Moonstone"], sbires)
verifier("le set de Moonstone l'accompagne",
         sets == ["gravitational_pull"], sets)
verifier("Jolt vient SEULE : son set est celui du scenario 4, on ne le rapporte pas",
         "supersonic" not in sets and "hard_sound" not in sets, sets)

# 2. Temoin : sans la cle, rien ne revient. C'est l'etat d'avant le cablage.
erreurs, sbires, sets, taille_nue = sonder({"A.I.M. Envelope": TAUPE})
verifier("carnet vide : la mise en place tourne sans erreur", not erreurs, erreurs)
verifier("carnet vide : aucun Thunderbolt", sbires == [] and sets == [], (sbires, sets))
verifier("le deck de rencontre grossit bien du set entier plus Jolt",
         taille - taille_nue == 7, (taille_nue, taille))

# 3. Deux sets d'un coup, et un nom inconnu ignore.
erreurs, sbires, sets, _ = sonder({"A.I.M. Envelope": TAUPE,
                                   "Surviving Thunderbolts": "MACH-IV;Songbird;Personne"})
verifier("deux survivants a set : les deux sets reviennent",
         sets == ["hard_sound", "supersonic"], sets)
verifier("un nom inconnu est ignore sans casser la mise en place",
         not erreurs and sbires == ["MACH-IV", "Songbird"], (erreurs, sbires))

# 4. Hors campagne, la cle ne doit rien declencher : le scenario se joue seul.
erreurs, sbires, sets, _ = sonder({"Surviving Thunderbolts": "Moonstone;Jolt"}, campagne=False)
verifier("hors campagne : la mise en place tourne sans erreur", not erreurs, erreurs)
verifier("hors campagne : le carnet n'a aucun effet", sbires == [] and sets == [], (sbires, sets))

echecs = [r for r in resultats if not r[1]]
for nom, ok, detail in resultats:
    print(("  OK   " if ok else "  ECHEC") + f" {nom}" + (f"  ({detail})" if detail and not ok else ""))
print(f"\n{len(resultats) - len(echecs)}/{len(resultats)} verifications passees")
sys.exit(1 if echecs else 0)
