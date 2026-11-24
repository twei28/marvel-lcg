from . import *
# Shi'ar Infantry (x2). Sbire SHI'AR SOLDIER, 2 PV, SCH 1, ATQ 2, boost [star] seul.
#
# When Revealed: Search the encounter deck and discard pile for another copy of Shi'ar Infantry and put it into play (it is not
#   revealed).
# [star] Boost: Put this card into play (it is not revealed).
#
# Cartes de reference : 15027 Chaos Manipulation (`Search.EncounterCard(.., name=..)` + `face.PutIntoPlay(player, effect)`),
# 16137 (`WhenCardBecomeBoost("This", ..)`).
def GetAbilities() -> Sequence['Ability']:
    def une_autre_copie(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)
        joueur = message.GetToPlayer()
        face = Search.EncounterCard(effect, include_discard_pile=True, name=INFANTERIE, card_type=Minion)
        if face:
            face.PutIntoPlay(joueur, effect)
    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Minion)
        joueur = message.GetToPlayer()
        this.PutIntoPlay(joueur, effect)
    return [
        AbilityFactory.WhenThisRevealed(None, une_autre_copie),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
