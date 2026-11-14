from . import *

# Mutant Hunting Season (1A) — COMPLOT PRINCIPAL, stade 1A.
# Contents: Lady Deathstrike (I) and (II) ((II) and (III) for expert mode). Lady Deathstrike, Reavers and Standard encounter
#   sets. One modular set (Military Grade or Reaver Resources).
# Setup: Attach a copy of Bleeding Out to each player, then set each remaining copy aside. Place 3 bleed counters on each copy
#   of Bleeding Out.
#
# Cartes de reference :
#  - « Setup » d'une face 1A : `WhenCardSetup("This", op)` (`gs117a`, officiel `50087a` Batroc) ;
#    cartes mises de cote : `Worlds.GetSetAsideAreaCards(effect, CardFinder(...))` ; mise en jeu `face.PutIntoPlay(joueur, effect)`.
#  - « Contents » : composition du scenario, portee par `data/scenarios/lady_deathstrike*.json` (standard / expert), pas par le code.
#
# ⚠ Mots-pieges :
#  - « a copy to EACH PLAYER » : un exemplaire par joueur (1 a 4), les autres RESTENT de cote (le scenario en liste 4) ;
#  - « 3 bleed counters on EACH COPY » : chaque copie EN JEU recoit 3 compteurs ; les copies de cote n'existent pas encore.


def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        Unused(message)

        copies = list(Worlds.GetSetAsideAreaCards(effect, CardFinder(card_ids=[ID_SAIGNEMENT])))
        for joueur in Worlds.GetPlayers(effect):
            if not copies:
                break
            copies.pop(0).PutIntoPlay(joueur, effect)
        for saignement in TousLesSaignements(effect):
            Faces.PlaceCountersOn([saignement], 3, 'bleed', effect)

    return [
        AbilityFactory.WhenCardSetup(
            "This",
            mise_en_place,
        ),
    ]
