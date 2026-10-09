from . import *

# hs027 A Thousand Bites
# When Revealed: For each RAT minion engaged with you, choose to either place 1 threat on
# that minion, or take 1 indirect damage. Resolve the "Special" effect on Even More Rats.
# If there is one or no RAT minions engaged with you, this card gains surge.

def GetAbilities() -> Sequence['Ability']:

    def morsures(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        if joueur is None:
            return
        nombre = len(RatsEngages(joueur))
        MenaceEtIndirectPourChaqueRat(effect, joueur)
        ResoudreSpecialEvenMoreRats(effect)
        if nombre <= 1:
            ThisCardGainSurge(effect)

    return [
        AbilityFactory.WhenThisRevealed(None, morsures),
    ]
