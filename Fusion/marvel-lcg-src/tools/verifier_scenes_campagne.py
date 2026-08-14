"""Les scenarios d'une campagne se CREENT-ils, et son carnet pointe-t-il des
cartes qui existent ?

CE QUE LES AUTRES OUTILS NE DISENT PAS
`test_cards` construit les capacites d'une carte, `autoplay` joue une partie,
`verifier_campagnes` compare les cles du carnet aux litteraux du `campaign.py`.
Aucun ne verifie qu'une SCENE se cree — c'est pourtant la premiere chose que
fait le moteur quand un joueur choisit un scenario dans le navigateur. Un
`encounter_sets` mal nomme, un `set_aside` qui pointe une carte absente, un
complot dont la face B manque : rien de tout cela ne leve d'erreur ailleurs, et
le joueur voit un ecran vide.

Il verifie en plus que chaque option d'arbre de talents citee par le carnet
existe dans `cards.json` : une option fantome ne leve rien non plus, elle ne
s'affiche simplement jamais.

    python3.10 tools/verifier_scenes_campagne.py <game_dir absolu>

Sortie : une ligne par scene, le compte des options du carnet, et un code de
retour non nul s'il reste un echec.
"""
import sys, os, json

GAME_DIR = os.path.expanduser(sys.argv[1])
os.chdir(GAME_DIR); sys.path.insert(0, GAME_DIR)
sortie = open("/tmp/verif_serveur_wd.log", "w", buffering=1)
vrai_stdout = sys.stdout
sys.stdout = sortie
sys.stderr = sortie

from engine import Engine
ok = Engine.Initialize()

from game.scene.loader import SceneLoader

SCENARIOS = ["wd_shocker", "wd_electro", "wd_the_lizard", "wd_vulture",
             "wd_kingpin", "wd_vulture_underling"]
resultats = []
for nom in SCENARIOS:
    for suffixe in ("", "_expert"):
        cle = nom + suffixe
        try:
            scene = SceneLoader.NewScene(cle, None, ["spider_man"], 42)
            resultats.append((cle, type(scene).__name__ if scene else "None"))
        except Exception as exc:
            resultats.append((cle, "ECHEC %s: %s" % (type(exc).__name__, exc)))

carnet = json.load(open("data/campagnes/web_of_deceit.json", encoding="utf-8"))
cartes = json.load(open("data/cards.json", encoding="utf-8"))
ids = {c["card_id"] for c in cartes["web_of_deceit"]}
manquantes = []
for sc in carnet["scenarios"]:
    for entree in sc["victoire"]:
        for option in entree.get("options", []):
            if option not in ids:
                manquantes.append((entree["cle"], option))

sys.stdout = vrai_stdout
print("INIT:", ok)
for cle, etat in resultats:
    print("  %-32s %s" % (cle, etat))
print("carnet : %d scenarios, %d options d'arbre, %d introuvables"
      % (len(carnet["scenarios"]),
         sum(len(e.get("options", [])) for s in carnet["scenarios"] for e in s["victoire"]),
         len(manquantes)))
for cle, opt in manquantes:
    print("  MANQUANTE", cle, opt)
echecs = [x for x in resultats if x[1].startswith("ECHEC") or x[1] == "None"]
print()
print("OK : les %d scenarios se creent et le carnet ne pointe que des cartes qui existent."
      % len(resultats) if not echecs and not manquantes
      else "ECHECS : %d" % (len(echecs) + len(manquantes)))
sortie.close()
# ⚠ `os._exit` ne vide PAS les tampons : sans ce flush, l'outil sort en silence
# et son rapport se perd. Le moteur garde des fils vivants apres `Initialize`,
# d'ou la sortie franche plutot qu'un `SystemExit` qui ne rendrait jamais la main.
vrai_stdout.flush()
os._exit(1 if (echecs or manquantes) else 0)
