from . import *

# * Stegron

def GetAbilities() -> Sequence['Ability']:

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        # « [star] Boost: Give the villain a tough status card. Put this minion
        # into play engaged with you. »
        this = effect.this.CastTo(Minion)
        villain = Worlds.FindVillain(effect)
        if villain:
            Faces.GiveStatus([villain], "Tough", effect)
        this.PutIntoPlay(message.GetToPlayer(), effect)

    return [
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            boost
        ),
    ]
