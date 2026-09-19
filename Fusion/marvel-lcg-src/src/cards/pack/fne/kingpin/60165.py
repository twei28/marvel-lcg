from . import *

# * James Wesley (PERSONA) — +1 SCH (desc SCH+), boost [star] seule.
# When Revealed: Attach to Kingpin and give him a facedown boost card.
# Hero Action: Discard a THWART event from your hand -> discard James Wesley.
#   Kingpin schemes.
# [star] Boost: Attach this card to Kingpin.
# Voir CapacitesDUnePersona. « give him a facedown boost card » hors activation :
# GiveFacedownBoostCardsInternal(1, effect, None) (la carte attend sa prochaine
# activation dans sa pile de boost, comme 56091 / 60094).

def GetAbilities() -> Sequence['Ability']:

    def carte_boost(effect: 'Effect', joueur: 'Player', kingpin: 'Villain') -> None:
        kingpin.CastTo(CanBoost).GiveFacedownBoostCardsInternal(1, effect, None)

    def manigance(effect: 'Effect', joueur: 'Player', kingpin: 'Villain') -> None:
        kingpin.DoSchemes(joueur, effect)

    return [
        *CapacitesDUnePersona("THWART", "Discard a Thwart event: discard James Wesley, Kingpin schemes",
                              carte_boost, manigance),
    ]
