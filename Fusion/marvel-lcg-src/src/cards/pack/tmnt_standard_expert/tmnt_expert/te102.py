from . import *

# Haunted by the Past (TMNT Expert 2/3) — TRAITRISE. 2 icones de boost.
# When Revealed: Search the encounter deck, discard pile, and set-aside area for
#   your nemesis minion and put it into play engaged with you. (Shuffle.) If your
#   nemesis minion did not enter play this way, exhaust your identity and this
#   card gains surge.
#
# Cartes de reference : `hood 24031` Seek and Destroy (la recherche + `PutIntoPlay`),
# `core expert 01191` Exhaustion (`Faces.ExhaustAll([identity])`), `ThisCardGainSurge`.
#
# Mots-pieges : « put it into play engaged with YOU » ; « did not enter play THIS
# WAY » ; les DEUX consequences (epuiser ET surge) quand il n'entre pas.


def GetAbilities() -> Sequence['Ability']:

    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        sbire = Search.EncounterCard(
            effect, joueur,
            include_discard_pile=True,
            include_set_aside=True,
            card_type=Minion,
            is_nemesis=joueur,
        )
        if sbire and sbire.PutIntoPlay(joueur, effect):
            return
        Faces.ExhaustAll([joueur.GetIdentity()], effect)
        ThisCardGainSurge(effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revelee),
    ]
