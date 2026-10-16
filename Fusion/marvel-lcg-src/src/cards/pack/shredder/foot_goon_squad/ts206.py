from . import *

# Send Out the Goons — COMPLOT ANNEXE (Foot Goon Squad). Menace 1[per_hero], icone
# CRISE, 3 icones de boost.
# When Revealed: Discard cards from the top of the encounter deck until a BRUTE
#   minion is discarded. Reveal that minion.
#
# Cartes de reference : `hood 24018` Brothers Grimm (`Worlds.DiscardEncounterCardsUntil(
# effect, card_type=..., trait=...)` puis `face.Reveal(player, effect)`).
#
# Mots-pieges : « discard until a BRUTE MINION IS DISCARDED » (type sbire ET trait) ;
# « reveal THAT minion » ; sans BRUTE dans le deck, tout le deck est defausse
# (borne : le moteur melange la defausse une fois, `DiscardUntil`).


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        face = Worlds.DiscardEncounterCardsUntil(effect, card_type=Minion, trait="BRUTE")
        if face:
            face.Reveal(joueur, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
