"""Le moteur accepte-t-il un cinquieme, puis un SIXIEME aspect ?

⚠ 09/09/2026 : ce fichier ne garde son nom que pour ne pas casser les
references des vieux rapports. Il verrouille desormais DEUX aspects fan-made,
`Determination` (dt) et `Venomized` (vz).

Les quatre aspects officiels (plus 'Pool, celui de Deadpool) vivent dans deux
Literal de game/card/face/base/card_player.py, dont CARD_CLASS_LIST et
ASPECT_CLASS_LIST sont DERIVEES (Types.LiteralToList). Un card_class inconnu
tombe sur `assert IsCardClass(card_class)`.

Ce test verrouille les deux sens : Determination est accepte, et une classe
inventee reste refusee. Le second cas compte autant que le premier : un
verificateur qui accepte tout ne verifie rien.

Usage: RELEASE=1 python3.10 tools/test_aspect_determination.py <game_dir> <port>
"""
import json
import os
import sys

# Le moteur doit etre AMORCE : importer game.element.utility tout seul tombe
# sur un import circulaire (game.object <- game.player <- game.deck). Meme
# amorcage que tools/test_cards.py, dont on reprend la signature.
GAME_DIR = os.path.expanduser(sys.argv[1] if len(sys.argv) > 1 else "./.game")
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 2410

os.chdir(GAME_DIR)
sys.path.insert(0, GAME_DIR)
os.environ.setdefault("RELEASE", "1")
cfg_path = os.path.join(GAME_DIR, "launch.json")
cfg = json.load(open(cfg_path))
cfg["server_addresses"] = ["127.0.0.1:%d" % PORT]
cfg["check_for_new_version_on_startup"] = False
json.dump(cfg, open(cfg_path, "w"), indent=2)

_vrai_stdout = sys.stdout
sys.stdout = open("/tmp/aspect_stdout.log", "w", buffering=1)
sys.stderr = sys.stdout
from engine import Engine
Engine.Initialize()
sys.stdout = _vrai_stdout

from game.element.utility import IsAspectClass, IsCardClass


def cas(nom, obtenu, attendu):
    if obtenu == attendu:
        print("  ok    %s" % nom)
        return 0
    print("  ECHEC %s : attendu %r, obtenu %r" % (nom, attendu, obtenu))
    return 1


def main():
    echecs = 0
    # Les quatre officiels, et 'Pool : rien ne doit bouger pour eux.
    for aspect in ("Aggression", "Justice", "Leadership", "Protection", "'Pool"):
        echecs += cas("%s reste un aspect" % aspect, IsAspectClass(aspect), True)
        echecs += cas("%s reste une classe" % aspect, IsCardClass(aspect), True)

    # Le cinquieme.
    echecs += cas("Determination est un aspect", IsAspectClass("Determination"), True)
    echecs += cas("Determination est une classe", IsCardClass("Determination"), True)

    # Le sixieme.
    echecs += cas("Venomized est un aspect", IsAspectClass("Venomized"), True)
    echecs += cas("Venomized est une classe", IsCardClass("Venomized"), True)

    # Les classes non-aspect gardent leur nature.
    echecs += cas("Basic n'est pas un aspect", IsAspectClass("Basic"), False)
    echecs += cas("Basic reste une classe", IsCardClass("Basic"), True)
    echecs += cas("Aspect reste une classe", IsCardClass("Aspect"), True)

    # Et l'inconnu reste inconnu.
    echecs += cas("Sarcasme n'est pas une classe", IsCardClass("Sarcasme"), False)
    echecs += cas("Sarcasme n'est pas un aspect", IsAspectClass("Sarcasme"), False)

    # La couleur : sans elle, le generateur d'images n'a rien a peindre.
    from engine.lib.image_creator import ImageCreatorHelper
    couleurs = getattr(ImageCreatorHelper, "aspect_dict", None)
    if couleurs is None:
        from engine.lib import image_creator
        couleurs = None
        for objet in vars(image_creator).values():
            d = getattr(objet, "aspect_dict", None)
            if isinstance(d, dict):
                couleurs = d
                break
    echecs += cas("Determination a une couleur", "Determination" in (couleurs or {}), True)
    echecs += cas("Venomized a une couleur", "Venomized" in (couleurs or {}), True)

    # Le compteur maison de l'aspect Venomized.
    from game.card.face.card_face import CardFace
    from core import Types
    compteurs = Types.LiteralToList(CardFace.COUNTER)
    echecs += cas("le compteur klyntar existe", "klyntar" in compteurs, True)
    echecs += cas("un compteur invente n'existe pas", "sarcasme" in compteurs, False)

    # -----------------------------------------------------------------------
    # LA REGLE DE DECK-BUILDING DU SET « VENOMIZED WEAKNESS »
    #
    # Insert du pack : le nombre de cartes Weakness imposees depend du COUT
    # CUMULE des cartes Venomized du deck (1-20 -> 1 ; 21-40 -> 2). La regle
    # vit dans `PlayerSetup.CartesImposeesParLesAspects` ; ces cas la mesurent
    # sur des decks fabriques pour tomber PILE aux bornes.
    #
    # ⚠ Le tirage etant seme, on ne peut pas predire QUELLES faiblesses
    # sortent : on mesure donc le NOMBRE, et l'appartenance au bon set.
    from game.player.element.player_setup import PlayerSetup
    from cards.database import CardsDB
    from engine.lib.random import Random

    monde = None  # la regle ne lit pas le monde, seulement le catalogue
    faiblesses = sorted(cid for cid, paper in CardsDB.papers.items()
                        if paper.set_name == "Venomized Weakness")
    echecs += cas("le set Venomized Weakness compte 2 cartes", len(faiblesses), 2)

    def combien(card_ids):
        Random.SetSeed(12345)
        return PlayerSetup.CartesImposeesParLesAspects(card_ids, monde)

    # Un deck SANS carte Venomized n'impose rien. C'est le cas de tous les
    # decks officiels : sans ce temoin, une regle qui ajouterait toujours des
    # faiblesses passerait pour juste.
    echecs += cas("aucun Venomized -> aucune faiblesse",
                  combien(["01001a", "01088", "01090"]), [])

    # vz035 coute 0 : present dans le deck, il ne declenche RIEN a lui seul.
    # La regle parle d'un cout CUMULE, pas d'une presence.
    echecs += cas("cout cumule 0 -> aucune faiblesse", combien(["vz035"]), [])

    # Bornes de la premiere tranche : 1 et 20.
    echecs += cas("cout 1 -> 1 faiblesse", len(combien(["vz024"])), 1)
    echecs += cas("cout 20 -> 1 faiblesse", len(combien(["vz011"] * 6 + ["vz024"] * 2)), 1)

    # Premiere valeur de la seconde tranche : 21.
    echecs += cas("cout 21 -> 2 faiblesses", len(combien(["vz011"] * 7)), 2)
    echecs += cas("cout 40 -> 2 faiblesses",
                  len(combien(["vz011"] * 13 + ["vz024"])), 2)

    # ⚠ AU-DELA DE 40 le tableau de l'auteur s'arrete : on garde la derniere
    # tranche plutot que d'inventer une troisieme. Ce cas FIGE ce choix, pour
    # qu'un changement d'avis soit un geste conscient.
    echecs += cas("cout 45, au-dela du tableau -> 2 faiblesses (derniere tranche)",
                  len(combien(["vz011"] * 15)), 2)

    # Et ce qui est tire appartient bien au set impose.
    tirees = combien(["vz011"] * 7)
    echecs += cas("les faiblesses tirees viennent du set Venomized Weakness",
                  all(c in faiblesses for c in tirees), True)

    # ⚠ TIRAGE SEME : deux appels a la meme graine rendent la meme chose. Sans
    # cela, un rejeu ou une partie multijoueur divergerait.
    Random.SetSeed(999)
    premier = PlayerSetup.CartesImposeesParLesAspects(["vz011"] * 7, monde)
    Random.SetSeed(999)
    second = PlayerSetup.CartesImposeesParLesAspects(["vz011"] * 7, monde)
    echecs += cas("meme graine -> meme tirage", premier, second)

    print("ECHECS : %d" % echecs)
    return 1 if echecs else 0


if __name__ == "__main__":
    code = main()
    # Sortie BRUTALE, comme test_cards.py : Engine.Initialize() laisse des
    # threads non-daemon derriere lui, et un sys.exit() ordinaire attendrait
    # indefiniment qu'ils s'arretent.
    sys.stdout.flush()
    os._exit(code)
