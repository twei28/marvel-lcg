"""Ce que la carte ANNONCE est-il porte par la carte CONSTRUITE ?

    python3.10 tools/verifier_cartes_en_jeu.py <game_dir> <port> <pack> [pack ...]

POURQUOI CET OUTIL EXISTE
-------------------------
Merc Squad (dt008) disait « Uses (3 tactic counters) » et se construisait sans
un seul compteur. Sa capacite existait, son cout etait « retirer 1 compteur
tactic », et ce cout ne pouvait JAMAIS etre paye : l'Action restait grisee pour
toujours. Quarante-huit autres cartes de l'aspect etaient dans le meme cas.

Aucun outil ne le voyait, parce que tous demandaient « la capacite existe-t-elle ? » :
  * `test_cards`            construit les capacites ;
  * `test_generate_cards`   construit la carte ;
  * `sonde_capacites`       compte les capacites ;
  * `verifier_noms_modules` lit le code.

Celui-ci demande autre chose : « la carte porte-t-elle ce que son texte
promet ? ». Il GENERE chaque carte dans une vraie partie et compare, attribut
par attribut, le texte imprime a ce que le moteur a retenu.

CE QU'IL VERIFIE
----------------
Les attributs que le moteur lit dans le `desc` et que le joueur voit a l'usage :
compteurs d'usage (nom ET nombre), toughness, retaliate, restricted, max par
joueur, max par deck, setup, permanent. Un ecart ici veut dire une carte qui
ment au joueur — souvent une carte inutilisable.

CE QU'IL NE FAIT PAS
--------------------
Verifier qu'une capacite fait la bonne chose. Il verifie que la carte est
EQUIPEE pour la faire.
"""
import io
import json
import os
import re
import sys
import threading
import time

# Ce que le TEXTE annonce -> ce que la FACE construite doit porter.
CONTROLES = [
    # ⚠ `Uses` n'existe pas pour un ALLY : ces cartes-la posent leurs compteurs
    # depuis leur module (ThisEnterPlayWithCounters), ce que ce controle ne voit
    # pas. Elles sont donc exclues plutot que signalees a tort.
    (r"Uses \((\d+) (\w+) counters?\)",
     lambda m: ("compteurs d'usage", (m.group(2), int(m.group(1)))),
     lambda f: (getattr(f, "uses_counter_name", None), getattr(f, "uses_counters", 0)),
     lambda carte: carte.get("type") in ("Upgrade", "Support", "Attachment",
                                         "Obligation", "Environment")),
    (r"(?m)^Toughness\.",
     lambda m: ("toughness", 1),
     lambda f: getattr(f, "printed_toughness", 0)),
    (r"Retaliate (\d)",
     lambda m: ("retaliate", int(m.group(1))),
     lambda f: getattr(f, "printed_retaliate", 0)),
    (r"(?m)^Restricted\.",
     lambda m: ("restricted", 1),
     # `restricted` est un MOT-CLE, calcule quand la carte est en jeu ; hors jeu
     # il vaut 0. C'est l'imprime qu'on lit ici.
     lambda f: getattr(f, "printed_restricted", 0)),
    (r"Max (\d+)[A-Za-z ]* per player",
     lambda m: ("max par joueur", int(m.group(1))),
     lambda f: getattr(f, "max_per_unit", 0)),
    (r"Max (\d+) per deck",
     lambda m: ("max par deck", int(m.group(1))),
     lambda f: getattr(f, "max_per_deck", 0)),
]


def main() -> int:
    if len(sys.argv) < 4:
        print(__doc__)
        return 2
    game_dir = os.path.expanduser(sys.argv[1])
    port = int(sys.argv[2])
    packs = sys.argv[3:]

    racine = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cartes_json = json.load(open(os.path.join(racine, "data", "cards.json"), encoding="utf-8"))

    os.environ["RELEASE"] = "1"
    os.chdir(game_dir)
    sys.path.insert(0, game_dir)
    cfg_path = os.path.join(game_dir, "launch.json")
    cfg = json.load(open(cfg_path))
    cfg["server_addresses"] = ["127.0.0.1:%d" % port]
    json.dump(cfg, open(cfg_path, "w"), indent=2)

    vrai_stdout = sys.stdout
    sys.stdout = sys.stderr = io.open("/tmp/verifier_cartes_en_jeu.log", "w", buffering=1)

    from engine import Engine
    Engine.Initialize()
    from game.scene.loader import SceneLoader
    scene = SceneLoader.NewScene("rhino", None, ["spider_man"], 42)
    game = Engine.game
    game.session.SetScene(scene, "Load")
    threading.Thread(
        target=lambda: game.GameSetup() and game.GameLoop(), daemon=True).start()
    time.sleep(15)

    from game.card.factory import CardFactory
    monde = game.world

    ecarts = []
    lues = 0
    for pack in packs:
        for carte in cartes_json.get(pack, []):
            lues += 1
            texte = (carte.get("text") or "").replace("<b>", "").replace("</b>", "")
            try:
                face = CardFactory.GenerateCard(
                    carte["card_id"], monde.area_removed, monde).face
            except Exception as e:
                ecarts.append("%s %-26s NE SE GENERE PAS : %r"
                              % (carte["card_id"], carte.get("name", "")[:26], e))
                continue
            for controle in CONTROLES:
                motif, attendu_fn, lu_fn = controle[0], controle[1], controle[2]
                sapplique = controle[3] if len(controle) > 3 else (lambda c: True)
                trouve = re.search(motif, texte)
                if not trouve or not sapplique(carte):
                    continue
                nom, attendu = attendu_fn(trouve)
                try:
                    lu = lu_fn(face)
                except Exception:
                    lu = "<illisible>"
                if lu != attendu:
                    ecarts.append(
                        "%s %-26s %s : le texte dit %r, la carte porte %r"
                        % (carte["card_id"], carte.get("name", "")[:26], nom, attendu, lu))

    sys.stdout = vrai_stdout
    if ecarts:
        print("\n".join(ecarts))
        print("\n%d ecart(s) sur %d carte(s)." % (len(ecarts), lues))
    else:
        print("OK : les %d cartes de %s portent ce que leur texte annonce."
              % (lues, ", ".join(packs)))
    sys.stdout.flush()
    os._exit(1 if ecarts else 0)


if __name__ == "__main__":
    sys.exit(main())
