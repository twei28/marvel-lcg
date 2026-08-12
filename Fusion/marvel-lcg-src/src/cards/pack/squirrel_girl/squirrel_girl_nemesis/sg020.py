from . import *

# Discord in the Branches
# While this scheme is in play, the printed abilities of SQUIRREL allies are
#   treated as blank.
# Forced Response: After a SQUIRREL ally enters play, place 1 threat here.
#   Limit once per round.
#
# Le blanchiment n'est PAS porte par cette carte : le moteur ne sait rendre
# blanche qu'une face designee, pas une famille avec exception. Chaque capacite
# d'ecureuil teste elle-meme la presence de cette manigance (PasDeDiscorde dans
# le module du pack). Ecart documente §9 : si un septieme ecureuil est ajoute,
# il doit reprendre la condition.

def GetAbilities() -> Sequence['Ability']:

    def monter_la_menace(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        this.PlaceThreatOnSchemes([this], 1, effect)

    return [
        (AbilityFactory.AfterCardEnterPlay(
            AbilityType.ForcedResponse,
            CardFinder(card_type=Ally, traits=['SQUIRREL']),
            monter_la_menace,
        )
            .LimitOncePerRound()),
    ]
