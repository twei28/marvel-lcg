from . import *

# Covert Intelligence Operation (POTENTIAL ALLY, Sage). Victory 1.
# Each minion gains incite 1.
# When Defeated : Sage.
#
# Carte de reference : `AbilityFactory.ThisGainIncite` (enhance_self.py) pour l'« incite » de la carte ; ici un EFFET CONTINU sur tous les
# sbires : `GiveKeywordToInPlayWhenApplyThis(CardFinder(card_type=Minion), incite=1)` (environment.py:66 ; fiche mots-cles/incite.md).
def GetAbilities() -> Sequence['Ability']:
    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(card_type=Minion),
            incite=1,
        ),
        AbilitePotentialAlly("Sage"),
    ]
