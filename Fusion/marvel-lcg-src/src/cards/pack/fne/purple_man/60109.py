from . import *

# Sway the Masses
# When Revealed: Choose an INFLUENCED minion from the encounter discard pile
#   and reveal it. Otherwise, this card gains surge.
# Search.SearchForCard limite a la DEFAUSSE de rencontre (01095 fouille deck
# + defausse ; ici seulement la defausse).

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        face = Search.SearchForCard(
            effect, joueur,
            include_encounter_discard_pile=True,
            trait="INFLUENCED", card_type=Minion,
        )
        if face:
            face.Reveal(joueur, effect)
        else:
            ThisCardGainSurge(effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
