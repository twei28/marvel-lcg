from . import *

# Baxter's Laboratory (1A) — MANIGANCE PRINCIPALE, face A (Baxter's Lab 4/22).
# Content: Baxter Stockman (I) and Baxter Stockman (II). (Baxter Stockman (II) and Baxter (III) for
#   expert mode.) Baxter's Lab, Cyber Swarm, and Standard sets. Two modular encounter sets
#   (High Speed and Security Protocol).
# Setup: Put a Plague of M.O.U.S.E.R.S. minion into play engaged with each player.
#
# Cartes de reference : `hs004a` Rats and More Rats (`Find.FindAndPutIntoPlay` pour chaque
# joueur, avec `check_face_fn` pour ne pas reprendre un sbire deja en jeu) ; `sp001a` pour la forme
# `WhenCardSetup("This", ...)`. Le « Content » est du texte de regle : il vit dans
# `data/scenarios/baxter_stockman*.json`, pas dans le code.
#
# Mots-pieges : « A Plague of M.O.U.S.E.R.S. minion … engaged with EACH player » (un par joueur, pas
# un seul pour le premier) ; il y en a QUATRE exemplaires dans le deck (jusqu'a 4 joueurs) ; le passage
# en 1B est fait par le moteur apres la mise en place.


def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        def un_sbire(joueur: 'Player') -> None:
            Find.FindAndPutIntoPlay(
                effect,
                joueur,
                finder=CardFinder(card_ids=[ID_PLAGUE], card_type=Minion,
                                  check_face_fn=lambda f: not f.IsInPlay()),
            )
        Players.ForEachPlayer(effect, un_sbire)

    return [AbilityFactory.WhenCardSetup("This", mise_en_place)]
