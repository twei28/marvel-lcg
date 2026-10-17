from . import *

# * Uno — ALLIE unique ✦ NINJA. SAMURAI. TURTLE., classe Bushido (Inkwire, TMNT Shinobi). Cout 3, [mental]. ATQ 1*, CTR 1*, PV 3.
# [star] Response: After Uno uses a basic power, place 1 samurai counter on an OATH upgrade you control.
# « You lack discipline. »
#
# Mots-cles (fiches lues AVANT le code) : samurai counter / OATH (samurai-counter.md). Le [star] devant la Reponse et a cote de l'ATQ
# et du CTR est l'icone de rappel (fiche special.md) : aucune ligne de code pour elle, seule la Reponse compte (modele
# `tmnt_aspect_leadership/ul036` Turtle Titan, meme impression).
#
# Cartes de reference :
#  - « After <allie> uses a basic power » : `trors/spider_woman/04032` Captain Marvel (`AfterUnitUseBasicPower(Response, "This", op)` ;
#    sans `powers`, un allie compte ATK et THW) ;
#  - « place 1 samurai counter on an OATH upgrade you control » : `PlacerUnCompteurSamurai` (helper du pack).
#
# TEXTE CONTRE CODE
#  ⚠ « After UNO uses a basic power » : les pouvoirs de base d'Uno (son ATQ ET son CTR), pas ceux du heros ni d'un autre allie ;
#    la recuperation / la manigance ne sont pas des pouvoirs d'un allie.
#  ⚠ « place 1 samurai counter ON AN OATH upgrade YOU control » : UN compteur, sur une amelioration OATH sous son controle, au choix
#    du joueur ; sans OATH la Reponse ne fait rien.
#  ⚠ ATQ 1* / CTR 1* : 1 icone de degats consecutifs chacun (le [star] est l'icone de rappel) ; PV 3 ; cout 3 ; unique (« * »).


def GetAbilities() -> Sequence['Ability']:

    def uno(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this, message)
        PlacerUnCompteurSamurai(effect, effect.GetInitiator())

    return [
        AbilityFactory.AfterUnitUseBasicPower(
            AbilityType.Response,
            "This",
            uno,
        ),
    ]
